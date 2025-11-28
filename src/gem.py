import os
import sqlite3
from flask import current_app, jsonify, session
from dotenv import load_dotenv
from google.generativeai.protos import Part, FunctionResponse

from src.logg import logger
from src.prompt import sys_prompt

try:
    import google.generativeai as genai
except ImportError:
    genai = None

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME")

gemini_model = None

if GEMINI_API_KEY and genai:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_NAME,
            tools=[{
                "function_declarations": [
                    {
                        "name": "search_doctor_by_specialization",
                        "description": "Finds doctors by specialization. IMPORTANT: Convert input to the SINGULAR PRACTITIONER TITLE (e.g., 'Cardiologist' instead of 'Cardiology', 'Urologist' instead of 'Urologists').",
                        "parameters": {
                            "type": "object",
                            "properties": {"specialization": {"type": "string"}},
                            "required": ["specialization"]
                        }
                    },
                    {
                        "name": "search_doctor_by_name",
                        "description": "Returns doctor details whose name matches the given input.",
                        "parameters": {
                            "type": "object",
                            "properties": {"name": {"type": "string"}},
                            "required": ["name"]
                        }
                    },
                    {
                        "name": "search_clinic_by_city",
                        "description": "Finds clinics in a given city.",
                        "parameters": {
                            "type": "object",
                            "properties": {"city": {"type": "string"}},
                            "required": ["city"]
                        }
                    },
                    {
                        "name": "search_appointments_by_patient",
                        "description": "Returns upcoming appointments for a patient by email. NECESSARY: fetch email using user_id in the chat history",
                        "parameters": {
                            "type": "object",
                            "properties": {"email": {"type": "string"}},
                            "required": ["email"]
                        }
                    }
                ]
            }]
        )
        logger.info("[Gemini] Model loaded with tools.")
    except Exception as exc:
        logger.exception("[Gemini] Failed to configure model: %s", exc)
else:
    logger.warning("Gemini not configured. API key or package missing.")


# --- DB HELPERS ---

def get_db_connection():
    db_path = current_app.config["DATABASE"]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def run_query(query, args=()):
    """Runs SQL (SELECT) and returns rows as dicts."""
    conn = get_db_connection()
    cur = conn.cursor()
    rows = cur.execute(query, args).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_chat_log(user_id, user_type, role, message):
    """Saves a message to the chat_history table."""
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO chat_history (user_id, user_type, role, message) VALUES (?, ?, ?, ?)",
        (user_id, user_type, role, message)
    )
    conn.commit()
    conn.close()


def get_chat_history_for_gemini(user_id, user_type, limit=10):
    """Fetches last N messages and formats them for Gemini history."""
    conn = get_db_connection()
    # Fetch in reverse order (newest first) to apply limit, then flip back
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


# --- TOOL FUNCTIONS ---

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

def search_appointments_by_patient(email: str):
    return run_query(
        """
        SELECT a.id, a.status, s.date, s.time, d.name AS doctor
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN slots s ON a.slot_id = s.id
        JOIN doctors d ON a.doctor_id = d.id
        WHERE p.email LIKE ?
        ORDER BY s.date DESC
        """,
        (f"%{email}%",)
    )


def extract_text(resp):
    """Extracts Gemini text from the final result object or returns string as-is."""
    if isinstance(resp, str):
        return resp
    try:
        # Check if the object has a direct 'text' property (simple response)
        if hasattr(resp, 'text'):
            return resp.text
            
        result = resp._result
        parts = result.candidates[0].content.parts
        texts = [p.text for p in parts if hasattr(p, "text")]
        return "\n".join(texts).strip() if texts else ""
    except Exception as e:
        logger.error(f"extract_text failed: {e}")
        return "I couldn't generate a response."



# --- MAIN CHAT HANDLER ---

def gemini_chat(request):
    """Handles a chat request with memory and tools."""
    if gemini_model is None:
        return jsonify({"error": "Gemini model unavailable"}), 500

    user_msg = request.json.get("message", "").strip()
    if not user_msg:
        return jsonify({"reply": "Say something…"}), 200

    # 1. IDENTIFY USER
    if 'patient_id' in session:
        user_id = session['patient_id']
        user_type = 'patient'
    elif 'doctor_id' in session:
        user_id = session['doctor_id']
        user_type = 'doctor'
    else:
        # Anonymous user (no memory persistence)
        user_id = 0
        user_type = 'guest'

    try:
        # 2. LOAD HISTORY FROM DB
        db_history = []
        if user_id != 0:
            db_history = get_chat_history_for_gemini(user_id, user_type, limit=10)

        # 3. START CHAT WITH HISTORY
        chat = gemini_model.start_chat(history=db_history)
        
        # 4. SEND MESSAGE (with system prompt instruction on first turn if needed, 
        #    but usually sys_prompt is better sent as the first history item or prepended.
        #    Here we prepend it to the current message to enforce instructions.)
        full_prompt = sys_prompt + "\nUser Query: " + user_msg
        
        response = chat.send_message(
            full_prompt,
            generation_config={"candidate_count": 1, "temperature": 0.5}
        )

        # 5. CHECK FOR TOOLS
        try:
            part = response.candidates[0].content.parts[0]
            function_call = part.function_call
        except (AttributeError, IndexError):
            function_call = None

        if function_call and function_call.name:
            fname = function_call.name
            args = dict(function_call.args)
            logger.info(f"Gemini Tool request --> {fname}({args})")

            if fname in globals():
                result = globals()[fname](**args)
            else:
                result = "Error: Tool function not found."

            # Send tool result back to chat
            response = chat.send_message(
                Part(
                    function_response=FunctionResponse(
                        name=fname,
                        response={'result': result}
                    )
                )
            )

        # 6. EXTRACT FINAL TEXT
        final_reply = extract_text(response)

        # 7. SAVE TO DB (Only if user is logged in)
        if user_id != 0:
            save_chat_log(user_id, user_type, "user", user_msg)
            save_chat_log(user_id, user_type, "model", final_reply)

        return jsonify({"reply": final_reply})

    except Exception as exc:
        logger.exception("Chat failure: %s", exc)
        return jsonify({"error": "Chat failed"}), 500