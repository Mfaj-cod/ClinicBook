# 🏥 ClinicBook - AI-Powered Healthcare Platform

A comprehensive web-based platform that streamlines the appointment booking process between patients and healthcare providers. ClinicBook transforms standard booking into an intelligent, conversational experience using a **Context-Aware Agentic AI**.

---

## ✨ Key Features

### 🤖 Agentic AI Health Assistant (Powered by Gemini)
*Unlike standard chatbots, this assistant acts as an intelligent agent with direct database access.*

- **Context-Aware Identity**: Automatically detects if the user is a **Doctor** or **Patient** and adjusts its behavior and available tools accordingly.
- **Temporal Intelligence**: Understands natural language dates and times (e.g., *"Generate slots for tomorrow at 4 PM"* or *"Cancel the appointment next Friday"*) by referencing the live system date.
- **Smart Data Handling ("Invisible Ink")**: Uses internal database IDs to perform precise actions (like cancellations) without exposing technical details to the user, keeping the chat clean and conversational.
- **Role-Based Workflows**:
  - **For Patients**: Finds specialists, checks availability, views history, and cancels appointments.
  - **For Doctors**: Manages schedules, views upcoming patient lists, and creates new appointment slots using simple voice-like commands.

### 👩‍⚕️ Doctor Portal
- **AI Slot Generation**: Create bulk appointment slots instantly by simply typing *"Create 10 slots for tomorrow at 5 PM"*.
- **Schedule Management**: Ask *"Who is visiting me today?"* to get a real-time list of patients.
- **Workflow Automation**: Mark appointments as "Completed" directly through the chat interface.
- **Secure Profile Control**: Manage fees, specialization, and clinic details securely.

### 🧑‍🤝‍🧑 Patient Portal
- **Natural Language Search**: Find doctors by describing symptoms (e.g., *"I have a migraine"* -> searches for *Neurologists*).
- **One-Click Booking**: Streamlined booking process for available slots.
- **Visual Dashboard**: Track appointment status (Booked, Cancelled, Completed) in real-time.

---

## 🛠️ Technology Stack

- **Backend**: Flask (Python 3.x)
- **AI Engine**: Google Gemini 1.5 Flash
- **AI Architecture**: 
  - **Function Calling**: Modular tool definitions stored in `tools_config.json`.
  - **System Prompting**: Robust rule sets for safety, formatting, and role management.
  - **Context Injection**: Dynamically injects User Role and System Date into every prompt.
- **Database**: SQLite (Native Python support)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2
- **Authentication**: Flask-Login & Bcrypt

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- A Google Cloud API Key for Gemini

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
   |   |___init_db.py      # Database initialization script
   |   |___seed.py         # Database seeding with sample data
   |   |___gem.py          # Gemini AI Chatbot logic
   |   |___doctors_data.py # Sample doctors data  
   |   |_tools_config.json # Stores tool definitions 
   |
   ├── data/
   │   └── clinicBook.db   # SQLite database files
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

- [x] AI Chatbot: Integrated Gemini for natural language queries

- [ ] Payment Integration: Online payment processing for consultations

- [ ] Communication System: Email and SMS reminders for appointments

- [ ] Multi-clinic Support: Enhanced support for multiple clinic locations

- [ ] Admin Dashboard: Comprehensive administrative interface

- [ ] API Development: RESTful API for mobile app integration

- [ ] Analytics: Appointment analytics and reporting features

**📞 Support**
For support, please open an issue in the GitHub repository or contact the development team.

---
Built with grace for better healthcare management