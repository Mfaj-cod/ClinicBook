# 🏥 ClinicBook - Multimodal AI Healthcare Platform

A comprehensive web-based platform that transforms appointment booking into an intelligent, conversational experience. **ClinicBook** features a **Context-Aware Agentic AI** capable of reading, writing, listening (Voice), and reasoning to manage healthcare needs seamlessly.

---

## ✨ Key Features

### 🤖 Agentic AI Health Assistant (Powered by Gemini)
*A Hybrid AI system combining Agentic Tool Use with Retrieval-Augmented Generation (RAG).*

- **🗣️ Voice Interface**: Built-in **Speech-to-Text** allows doctors and patients to speak commands naturally (e.g., *"Book an appointment"* or *"Generate 5 slots"*).
- **📚 Hybrid RAG System**: 
  - **Dynamic Data**: Queries the SQLite database for live schedules and doctor availability.
  - **Static Knowledge**: Instantly answers policy questions (Refunds, Insurance, Hours) from a local Knowledge Base (`clinic_policies.txt`) without unnecessary database calls.
- **🧠 Context-Aware Identity**: Automatically detects User Role (Doctor/Patient) and Current Date to handle relative queries like *"Show me tomorrow's schedule"*.
- **📧 Active Notifications**: Automatically sends email confirmations via **Flask-Mail** upon successful bookings.

![Agentic Workflow Diagram](assets\Agent.jpg)

### 👩‍⚕️ Doctor Portal
- **Voice-Powered Management**: Dictate commands like *"Create slots for next Monday at 10 AM"* to bulk-generate schedule capacity.
- **Smart Dashboard**: Ask *"Who is visiting me today?"* to get a filtered, real-time patient list.
- **Workflow Automation**: Mark appointments as "Completed" directly through chat.
- **Secure Access**: Session-based isolation ensures doctors only manage their own data.

### 🧑‍🤝‍🧑 Patient Portal
- **Symptom-to-Specialist**: AI intelligently maps symptoms (e.g., *"chest pain"*) to the correct specialist (e.g., *Cardiologist*).
- **One-Click Booking**: Streamlined booking flow with email confirmation.
- **Transparency**: Clear visibility of appointment status, fees, and clinic policies via the AI assistant.

---

## 🛠️ Technology Stack

- **Backend**: Flask (Python 3.x)
- **AI Engine**: Google Gemini 2.5 Flash
- **AI Architecture**: 
  - **Agentic Tools**: Function Calling for DB Writes/Reads.
  - **Lightweight RAG**: Context injection for policy documents.
  - **System Prompting**: Role-based behavior control.
- **Frontend**: 
  - **Framework**: Bootstrap 5 & Jinja2
  - **Voice**: Web Speech API (Native JavaScript)
- **Database**: SQLite (Transactional)
- **Services**: Flask-Mail (SMTP Notifications)

---
## 🎯 AI Capabilities Breakdown

The system uses a **Router Architecture** to decide how to handle a user query:

1. **Knowledge Query** (e.g., *"Do you accept insurance?"*)
   - **Source:** `clinic_policies.txt`
   - **Action:** RAG Response (No DB Call)

2. **Data Query** (e.g., *"Find a Urologist"*)
   - **Source:** `search_doctor_by_specialization` Tool
   - **Action:** DB Read → Returns List with `[Hidden IDs]`

3. **Action Command** (e.g., *"Book the 10 AM slot"*)
   - **Source:** `book_appointment_by_patient` Tool
   - **Action:** DB Write → Email Trigger → Confirmation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Cloud API Key (Gemini)
- Gmail Account (for sending notifications)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone [https://github.com/Mfaj-cod/ClinicBook.git](https://github.com/Mfaj-cod/ClinicBook.git)
   cd ClinicBook

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone [https://github.com/Mfaj-cod/ClinicBook.git](https://github.com/Mfaj-cod/ClinicBook.git)
   cd ClinicBook
2. **Create and activate virtual environment**
   ```bash
   python -m venv clinic
   # On Windows
   clinic\Scripts\activate
   # On macOS/Linux
   source clinic/bin/activate
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
4. **Configure Environment Variables**
   ***Create a .env file in the root directory and add your API credentials:***
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   GEMINI_MODEL_NAME=gemini_model_name_here
   SECRET_KEY=your_flask_secret_key
5. **Run the application**
   ```bash
   python app.py

---
**📁 Project Structure**

   ```bash
   ClinicBook/
   ├── app.py              # Main Flask application            
   ├── src/
   |___|__ __init__.py
   |   |___init_db.py      # Database initialization script
   |   |___seed.py         # Database seeding with sample data
   |   |___gem.py          # Gemini AI Chatbot logic
   |   |___logg.py
   |   |___doctors_data.py # Sample doctors data  
   |   |___prompt.py
   |   |_tools_config.json # Stores tool definitions 
   |
   ├── data/
   │   |___clinicBook.db   # SQLite database files
   |   |_clinic_policies.txt
   |
   ├── templates/          # Jinja2 HTML templates
   ├── static/             # Static assets (CSS, JS, icons)
   ├── requirements.txt    # Python dependencies
   └── README.md           # Project documentation
   ```
---

***Note on AI Features:*** To enable the chatbot, ensure the GEMINI_API_KEY is set in your .env file. If the key is missing, the app will run, but the chat feature will return an error or be disabled.

---
**🎯 Use Cases**
**For Healthcare Providers**
- Small Clinics: Perfect for independent practitioners and small medical practices
- Specialists: Manage appointments across different specializations
- Multi-location Practices: Handle appointments for multiple clinic locations
- AI Assistance: Get instant answers about your upcoming appointments without browsing menus

**For Patients**
- Convenient Booking: Schedule appointments from anywhere, anytime
- Doctor Selection: Choose from a variety of healthcare providers
- AI Assistance: Get instant answers about doctor availability without browsing menus

---
**🔮 Roadmap**

- [x] Multimodal: Voice Input & Text Output

- [x] RAG Integration: Knowledge Base for FAQ

- [x] Agentic Writes: Booking & Slot Generation

- [ ] Payment Integration

- [ ] Analytics: Appointment analytics and reporting features

**📞 Support**
For support, please open an issue in the GitHub repository or contact the development team.

---
Built with ❤️ for better healthcare management