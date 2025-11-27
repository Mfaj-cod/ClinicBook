# 🏥 Clinic Appointment Booking System

A comprehensive web-based platform that streamlines the appointment booking process between patients and healthcare providers. This system eliminates the need for physical visits to clinics for appointment scheduling, offering a seamless digital experience for both patients and doctors.

---
## ✨ Key Features

### 🤖 AI Health Assistant (Powered by Gemini)
- **Smart Doctor Search**: Find doctors using natural language (e.g., *"Find me a cardiologist"* or *"Is Dr. Arjun available?"*).
- **Intelligent Querying**: Automatically converts patient symptoms or general terms into specific medical specializations (e.g., searches for "Urologist" when asked for "urologists").
- **Context-Aware Memory**: Remembers the last 10 interactions for logged-in users, allowing for smooth, continuous conversations.
- **Database Integration**: Directly connects with the clinic database to fetch real-time doctor details, clinic locations, and appointment slots.

### 👩‍⚕️ Doctor Portal
- **Profile Management**: Create and maintain detailed doctor profiles including specialization, consultation fees, and clinic information
- **Slot Management**: Add and manage available appointment slots with specific dates and times
- **Appointment Dashboard**: View all booked appointments with patient details and appointment status
- **Appointment Control**: Cancel or modify appointments as needed

### 🧑‍🤝‍🧑 Patient Portal
- **Doctor Discovery**: Browse and search doctors by specialization and clinic location
- **Easy Booking**: Book appointments in available time slots with just a few clicks
- **Personal Dashboard**: Manage upcoming appointments and view booking history
- **Flexible Cancellation**: Cancel appointments easily through the patient dashboard

### ⚙️ System Features
- **Secure Authentication**: Robust login system for both patients and healthcare providers
- **Responsive Design**: Mobile-friendly interface built with Bootstrap 5
- **Real-time Notifications**: Flash messages and status updates for better user experience
- **Lightweight Database**: SQLite backend for easy deployment and maintenance

## 🛠️ Technology Stack

- **Backend Framework**: Flask (Python)
- **AI/LLM**: Google Gemini 1.5 Flash (via `google-generativeai`)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2 Templates
- **Authentication**: Flask-Login
- **Deployment**: Compatible with Render, Heroku, and any Flask-supporting server

---
## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- A Google Cloud API Key for Gemini

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone [https://github.com/Mfaj-cod/ClinicBook](https://github.com/Mfaj-cod/ClinicBook)
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
   ├── gem.py              # Gemini AI Chatbot logic & Tool definitions
   ├── .env                # Environment variables (API Keys)
   ├── src/
   |   |___init_db.py      # Database initialization script
   |   |___seed.py         # Database seeding with sample data
   |   |_doctors_data.py   # Sample doctors data    
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