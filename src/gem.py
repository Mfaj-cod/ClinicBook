import os
import sqlite3
import re
import json
from flask import current_app, jsonify, session
from dotenv import load_dotenv
from google.generativeai.protos import Part, FunctionResponse
from datetime import datetime
from src.logg import logger
from src.prompt import sys_prompt

try:
    import google.generativeai as genai
except ImportError:
    genai = None

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME")


def load_tools_config():
    # Loads tool definitions from the JSON file.
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_path, "tools_config.json")
        
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load tools config: {e}")
        return []


gemini_model = None

if GEMINI_API_KEY and genai:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Loading tools from file
        tool_functions = load_tools_config()
        
        gemini_model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_NAME,
            # wrapping the loaded list in the structure Gemini expects
            tools=[{
                "function_declarations": tool_functions
            }]
        )
        logger.info("[Gemini] Model loaded with tools from JSON.")
    except Exception as exc:
        logger.exception("[Gemini] Failed to configure model: %s", exc)
else:
    logger.warning("Gemini not configured. API key or package missing.")


# DB Helpers
def get_db_connection():
    db_path = current_app.config["DATABASE"]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def run_query(query, args=()):
    # Runs SQL SELECT statements and returns rows as dicts.
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        rows = cur.execute(query, args).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.error(f"SQL Error: {e}")
        return []

def write_query(query, args=()):
    # Runs SQL INSERT/UPDATE/DELETE statements and COMMITS changes.
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, args)
        if cur.rowcount == 0:
            msg = "No records were updated. Check if the ID is correct."
        else:
            msg = "Success"
        conn.commit()
        conn.close()
        return msg
    except Exception as e:
        logger.error(f"SQL Write Error: {e}")
        return f"Database error: {e}"

def save_chat_log(user_id, user_type, role, message):
    # Saves a message to the chat_history table.
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO chat_history (user_id, user_type, role, message) VALUES (?, ?, ?, ?)",
        (user_id, user_type, role, message)
    )
    conn.commit()
    conn.close()


def get_chat_history_for_gemini(user_id, user_type, limit=10):
    # Fetches last N messages and formats them for Gemini history.
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT role, message FROM chat_history WHERE user_id=? AND user_type=? ORDER BY id DESC LIMIT ?",
        (user_id, user_type, limit)
    ).fetchall()
    conn.close()

    # Flip to chronological order (oldest -> newest)
    rows = rows[::-1] 

    history = []
    for r in rows:
        history.append({
            "role": r["role"],
            "parts": [r["message"]]
        })
    return history


# Tool Functions

def search_doctor_by_specialization(specialization: str):
    return run_query(
        "SELECT name, specialization, fees, phone, email FROM doctors WHERE specialization LIKE ?",
        (f"%{specialization}%",)
    )

def search_doctor_by_name(name: str):
    return run_query(
        "SELECT name, specialization, fees, phone, email FROM doctors WHERE name LIKE ?",
        (f"%{name}%",)
    )

def search_clinic_by_city(city: str):
    return run_query(
        "SELECT name, address, phone, average_rating FROM clinics WHERE city LIKE ?",
        (f"%{city}%",)
    )

def search_appointments_by_patient():
    user_id = session.get('patient_id')
    
    if not user_id:
        return "Error: You must be logged in as a patient to view appointments."

    # Fetch the email from the database using the ID
    conn = get_db_connection()
    user_row = conn.execute("SELECT email FROM patients WHERE id = ?", (user_id,)).fetchone()
    conn.close()

    if not user_row:
        return "Error: patient profile not found."
    
    email = user_row['email']

    # Run the query using the retrieved email
    # NOTE: We include 'id' in the SELECT so the user can see it to cancel later
    return run_query(
        """
        SELECT a.id, a.status, s.date, s.time, d.name AS doctor
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN slots s ON a.slot_id = s.id
        JOIN doctors d ON a.doctor_id = d.id
        WHERE p.email LIKE ? AND status LIKE 'booked'
        ORDER BY s.date DESC
        """,
        (f"%{email}%",)
    )

def get_doctor_schedule():
    # Retrieves appointments for the logged-in DOCTOR.
    doctor_id = session.get('doctor_id')
    
    if not doctor_id:
        return "Error: You must be logged in as a doctor to view your schedule."

    # Query appointments linked to this doctor_id
    # We join with 'patients' to show the doctor WHO is visiting
    return run_query(
        """
        SELECT a.id, p.name AS patient_name, s.date, s.time, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN slots s ON a.slot_id = s.id
        WHERE a.doctor_id = ? AND a.status LIKE 'booked'
        ORDER BY s.date DESC, s.time ASC
        """,
        (doctor_id,)
    )

def cancel_appointment_by_patient(appointment_id):
    user_id = session.get('patient_id')
    
    if not user_id:
        return "Error: You must be logged in as a patient to cancel appointments."

    # Use write_query to ensure COMMIT happens.
    # We verify 'patient_id' in the WHERE clause for security (prevent deleting others' data)
    return write_query(
        """
        UPDATE appointments
        SET status = 'cancelled'
        WHERE id = ? AND patient_id = ?
        """,
        (appointment_id, user_id)
    )

def complete_appointment_by_doctor(appointment_id):
    user_id = session.get('doctor_id')
    
    if not user_id:
        return "Error: You must be logged in as a doctor to complete appointments."

    # Use write_query to ensure COMMIT happens.
    # We verify 'complete_id' in the WHERE clause for security (prevent deleting others' data)
    return write_query(
        """
        UPDATE appointments
        SET status = 'completed'
        WHERE id = ? AND doctor_id = ?
        """,
        (appointment_id, user_id)
    )

def generate_slots_by_doctor(date, time, n_slots):
    user_id = session.get('doctor_id')

    if not user_id:
        return "Error: You must be logged in as a doctor to generate slots."

    return write_query(
        """
        INSERT INTO slots (doctor_id, date, time, capacity)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, date, time, n_slots)
    )


# TEXT PROCESSING HELPERS

def get_response_text(resp):
    """Safely extracts the raw text from the Gemini response object."""
    try:
        if hasattr(resp, 'text'):
            return resp.text
        else:
            result = resp._result
            parts = result.candidates[0].content.parts
            return "\n".join([p.text for p in parts if hasattr(p, "text")])
    except Exception as e:
        logger.error(f"Text extraction failed: {e}")
        return ""

def clean_text_for_display(text):
    """
    Removes [ID: 123] tags and cleans Markdown for the frontend.
    This hides the technical IDs from the user while keeping them in the DB history.
    """
    if not text:
        return "I couldn't generate a response."

    # 1. Remove the "Invisible Ink" IDs (e.g., [ID: 5])
    # This regex finds [ID: number] and replaces it with an empty string
    text = re.sub(r'\s*\[ID: \d+\]', '', text)

    # 2. Remove bolding markers (**)
    text = text.replace("**", "")
    
    # 3. Convert list bullets (*) to a clean newline + unicode bullet
    text = text.replace("* ", "\n• ")
    
    # 4. Remove generic header Markdown (#)
    text = text.replace("##", "").replace("###", "")
    
    return text.strip()


# main function

def gemini_chat(request):
    """Handles a chat request with memory and tools."""
    if gemini_model is None:
        return jsonify({"error": "Gemini model unavailable"}), 500

    user_msg = request.json.get("message", "").strip()
    if not user_msg:
        return jsonify({"reply": "Say something…"}), 200

    # 1. Identify User
    if 'patient_id' in session:
        user_id = session['patient_id']
        user_type = 'patient'
    elif 'doctor_id' in session:
        user_id = session['doctor_id']
        user_type = 'doctor'
    else:
        user_id = 0
        user_type = 'guest'

    try:
        # 2. Load History
        db_history = []
        if user_id != 0:
            db_history = get_chat_history_for_gemini(user_id, user_type, limit=10)

        chat = gemini_model.start_chat(history=db_history)

        today_str = datetime.now().strftime("%A, %d-%m-%Y")

        context_header = f"CURRENT USER ROLE: {user_type.upper()}"
        if user_id != 0:
            context_header += f" (ID: {user_id})"
        
        context_header += f"\nCURRENT SYSTEM DATE: {today_str}" 
        
        full_prompt = f"{sys_prompt}\n\n{context_header}\nUser Query: {user_msg}"
        
        response = chat.send_message(
            full_prompt,
            generation_config={"candidate_count": 1, "temperature": 0.5}
        )

        # 4. Tool Loop (Handle Function Calls)
        # We loop as long as the model wants to call a function.
        while True:
            # Check if the response contains a function call
            function_call = None
            try:
                # Iterate through all parts to find a function call
                for part in response.candidates[0].content.parts:
                    if part.function_call and part.function_call.name:
                        function_call = part.function_call
                        break
            except (AttributeError, IndexError):
                pass

            # If no function call found, we are done. Break the loop to show text.
            if not function_call:
                break

            # Execute the tool
            fname = function_call.name
            args = dict(function_call.args)
            logger.info(f"Gemini Tool request --> {fname}({args})")

            result = "Error: Tool function not found."
            if fname in globals():
                try:
                    result = globals()[fname](**args)
                except Exception as e:
                    result = f"Tool Execution Error: {e}"

            # Send tool result back to Gemini
            logger.info(f"Tool Result: {result}")
            response = chat.send_message(
                Part(
                    function_response=FunctionResponse(
                        name=fname,
                        response={'result': str(result)} 
                    )
                )
            )

        # 5. Extract Final Text (Robust Method)
        final_text = ""
        try:
            if response.candidates:
                # Join all text parts (sometimes the model splits thoughts and answers)
                parts = response.candidates[0].content.parts
                final_text = "\n".join([p.text for p in parts if p.text])
        except Exception as e:
            logger.error(f"Text Extraction Error: {e}")
            final_text = ""

        # Fallback if the model returns nothing (rare, but handles the 'Action Completed' case)
        if not final_text.strip():
            final_text = "I have processed your request. Is there anything else you need?"

        # 6. Clean & Save
        display_reply = clean_text_for_display(final_text)

        if user_id != 0:
            save_chat_log(user_id, user_type, "user", user_msg)
            # Save the RAW text (with [ID: 123]) to history so memory works
            save_chat_log(user_id, user_type, "model", final_text)

        return jsonify({"reply": display_reply})

    except Exception as exc:
        logger.exception("Chat failure: %s", exc)
        return jsonify({"error": "Chat failed"}), 500