import os
import sqlite3
from flask import current_app, jsonify
from dotenv import load_dotenv
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
            tools= [
            {
                "function_declarations": [
                    {
                        "name": "search_doctor_by_name",
                        "description": "Returns doctor details whose name matches the given input.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"}
                            },
                            "required": ["name"]
                        }
                    },
                    {
                        "name": "search_clinic_by_city",
                        "description": "Finds clinics in a given city.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "city": {"type": "string"}
                            },
                            "required": ["city"]
                        }
                    },
                    {
                        "name": "search_appointments_by_patient",
                        "description": "Returns upcoming appointments for a patient by email.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "email": {"type": "string"}
                            },
                            "required": ["email"]
                        }
                    }
                ]
            }
        ]
        )

        logger.info("[Gemini] Model loaded with tools.")
    except Exception as exc:
        logger.exception("[Gemini] Failed to configure model: %s", exc)
else:
    logger.warning("Gemini not configured. API key or package missing.")


# DB HELPER (NO IMPORT FROM app.py)
def run_query(query, args=()):
    """Runs SQL and returns rows as dicts."""
    db_path = current_app.config["DATABASE"]

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute(query, args).fetchall()
    conn.close()

    return [dict(r) for r in rows]


# TOOL FUNCTIONS
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
    # FIX: If resp is already a string, just return it
    if isinstance(resp, str):
        return resp
        
    try:
        # Use the internal _result which ALWAYS contains the final content
        result = resp._result        

        # In Gemini API, the actual text is inside:
        # result.candidates[0].content.parts[*].text
        parts = result.candidates[0].content.parts
        texts = [p.text for p in parts if hasattr(p, "text")]

        return "\n".join(texts).strip() if texts else ""
    except Exception as e:
        logger.error(f"extract_text failed: {e}")
        return "I couldn't generate a response."


# MAIN CHAT HANDLER (CALLED BY APP.PY)
def gemini_chat(request):
    """Handles a chat request from Flask route."""

    if gemini_model is None:
        return jsonify({"error": "Gemini model unavailable"}), 500

    user_msg = request.json.get("message", "").strip()


    if not user_msg:
        return jsonify({"reply": "Say something…"}), 200

    try:
        # STEP 1 → Ask Gemini
        response = gemini_model.generate_content(
            (sys_prompt + user_msg),
            generation_config={"candidate_count": 1, "temperature": 0.4}
        )
        logger.info(f"DEBUG: Type of response is: {type(response)}")

        # STEP 2 → Did Gemini call a tool?
        # STEP 2 → Manually check for tool calls (Compatible with older versions)
        try:
            # specific check for older library versions
            part = response.candidates[0].content.parts[0]
            function_call = part.function_call
        except (AttributeError, IndexError):
            function_call = None

        if function_call:
            fname = function_call.name
            args = dict(function_call.args)

            logger.info(f"[Gemini] Tool request → {fname}({args})")

            # Execute tool function safely
            if fname in globals():
                result = globals()[fname](**args)
            else:
                result = "Error: Tool function not found."

            # STEP 3 → Feed results back to model
            # We must construct the FunctionResponse explicitly for older versions
            from google.generativeai.protos import Part, FunctionResponse
            
            final = gemini_model.generate_content([
                response, # The chat history so far
                Part(
                    function_response=FunctionResponse(
                        name=fname,
                        response={'result': result}
                    )
                )
            ])
            
            # Note: final is an object, so we extract text from it
            final_text = extract_text(final) 
            return jsonify({"reply": final_text})
        
        # STEP 4 → Normal LLM answer
        final_text = extract_text(response.text)
        return jsonify({"reply": final_text})

    except Exception as exc:
        logger.exception("Chat failure: %s", exc)
        return jsonify({"error": "Chat failed"}), 500
