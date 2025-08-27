🏥 Clinic Appointment Booking System

    A web-based platform that connects patients with doctors without running to the clinic for appointment, allowing seamless appointment booking, management, and cancellations.

    This project is built with Flask, SQLite, and Bootstrap 5, designed to help small clinics and independent doctors digitize their practice.



✨ Features: 

👩‍⚕️ For Doctors

    Create and manage doctor profiles (specialization, fees, clinic details).

    Add available slots with date & time.

    View all booked appointments in a dashboard.

    Cancel appointments if needed.



🧑‍🤝‍🧑 For Patients

    Browse doctors by specialization and clinic.

    Book appointments in available slots.

    Manage upcoming appointments in a personal dashboard.

    Cancel appointments easily.



⚙️ General

    Secure authentication for both patients & doctors.

    Mobile-friendly interface with Bootstrap.

    Clear notifications and messages (via Flask-Flash).

    Simple SQLite backend for lightweight deployment.



🛠️ Tech Stack

    Backend: Flask (Python)

    Database: SQLite

    Frontend: HTML, CSS, Bootstrap 5, Jinja2 Templates

    Authentication: Flask-Login

    Deployment Ready: Works on Render/Heroku or any Flask-supporting server



🚀 Installation & Setup

    1. Clone the repository
    git clone https://github.com/Mfaj-cod
    cd ClinicBook

    2. Create virtual environment
    python -m venv clinic
    clinic\Scripts\activate

    3. Install dependencies
    pip install -r requirements.txt

    4. Initialize the database
    python init_db.py

    5. Add data to database
    python seed.py

    6. Run the app
    python app.py



The app will be available at:
👉 http://127.0.0.1:5000/


📂 Project Structure
    ClinicBook/
        │── app.py              # Main Flask app
        │── init_db.py          # created db
        |-- seed.py             # Database helper functions
        |-- data.py             # doctors data
        │── instance/db         # Database
        │── templates/          # Jinja2 HTML templates
        │── static/             # CSS, JS, manifest, service-wroker, icons
        │── requirements.txt    # Dependencies
        │── README.md           # Project Documentation


🔮 Future Improvements

    ✅ Add online payment integration.

    ✅ Email/SMS reminders for patients.

    ✅ Multi-clinic support.

    ✅ Admin dashboard for overall management.

🤝 Contributing
    Pull requests are welcome! For major changes, please open an issue first to discuss your idea.