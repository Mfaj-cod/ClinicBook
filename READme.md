# 🏥 Clinic Appointment Booking System

A comprehensive web-based platform that streamlines the appointment booking process between patients and healthcare providers. This system combines a robust Flask backend with an **Agentic AI Assistant** to offer a seamless, conversational experience for managing healthcare needs.

---

## ✨ Key Features

### 🤖 Agentic AI Health Assistant (Powered by Gemini)
*Unlike standard chatbots, this assistant acts as an agent with direct database access.*

- **Zero-Touch Context**: Automatically identifies the logged-in user (Patient or Doctor) via session data—no need to ask for emails or IDs.
- **Smart Appointment Management**: 
- **Fetching**: "Show my appointments" retrieves real-time data from the database.
- **Cancelling**: "Cancel the booked one" works intuitively. The system uses an **"Invisible Ink" strategy** to handle database IDs, allowing users to refer to items naturally without seeing technical ID numbers.
- **Completing**: "Complete the booked one" works intuitively. The system uses an **"Invisible Ink" strategy** to handle database IDs, allowing doctors to complete the appointments naturally without seeing technical ID numbers.
- **Intelligent Routing**: Converts symptoms (e.g., *"I have chest pain"*) into specific specialist queries (searches for *Cardiologists*) using Function Calling.
- **Clean UI Formatting**: The AI automatically cleans markdown and formats database results into readable, bulleted lists for the frontend.
- **Context-Aware Memory**: Remembers the last 10 interactions, allowing for follow-up questions like *"Where is that clinic located?"* after searching for a doctor.

### 👩‍⚕️ Doctor Portal
- **Profile Management**: Maintain professional details, specialization, and consultation fees.
- **Slot Management**: Create and manage availability slots.
- **Patient Dashboard**: View booked patients and upcoming schedule.
- **Secure Access**: Session-based security ensures doctors only manage their own slots.

### 🧑‍🤝‍🧑 Patient Portal
- **Doctor Discovery**: Search by name, specialization, or city.
- **One-Click Booking**: Streamlined booking process for available slots.
- **Personal Dashboard**: View history, check status, and cancel upcoming visits.
- **Visual Status**: Clear indicators for 'Booked' vs 'Cancelled' appointments.

### ⚙️ System Features
- **Secure Authentication**: Flask-Login implementation for session management.
- **Robust Database**: SQLite with transactional integrity (Commit/Rollback protections).
- **Responsive Design**: Mobile-friendly interface built with Bootstrap 5.
- **Real-time Updates**: changes made via Chatbot are immediately reflected in the dashboard.

---

## 🛠️ Technology Stack

- **Backend**: Flask (Python 3.x)
- **AI Engine**: Google Gemini 1.5 Flash via `google-generativeai`
- **AI Techniques**: 
  - **Function Calling** (Tool Use)
  - **Prompt Engineering** (System Instructions)
  - **Context Caching** (Chat History via DB)
- **Database**: SQLite (Native Python support)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2
- **Authentication**: Flask-Login & Bcrypt
- **Deployment**: Ready for Render / Heroku

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