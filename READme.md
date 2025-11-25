# 🏥 Clinic Appointment Booking System

A comprehensive web-based platform that streamlines the appointment booking process between patients and healthcare providers. This system eliminates the need for physical visits to clinics for appointment scheduling, offering a seamless digital experience for both patients and doctors.

## ✨ Key Features

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
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2 Templates
- **Authentication**: Flask-Login
- **Deployment**: Compatible with Render, Heroku, and any Flask-supporting server

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mfaj-cod/ClinicBook
   cd ClinicBook
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv clinic
   # On Windows
   clinic\Scripts\activate
   # On macOS/Linux
   source clinic/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

5. **Seed the database with sample data**
   ```bash
   python seed.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at: **http://127.0.0.1:5000/**

## 📁 Project Structure

```
ClinicBook/
├── app.py              # Main Flask application
├── src/
|     |___init_db.py    # Database initialization script
|     |___seed.py       # Database seeding with sample data
|     |_doctors_data.py # Sample doctors data    
|
├── data/
│   └── db              # SQLite database files
├── templates/          # Jinja2 HTML templates
├── static/             # Static assets (CSS, JS, icons)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 🔧 Configuration

The application uses SQLite as the default database, which is automatically created in the `data/` directory. No additional configuration is required for basic usage.

## 🎯 Use Cases

### For Healthcare Providers
- **Small Clinics**: Perfect for independent practitioners and small medical practices
- **Specialists**: Manage appointments across different specializations
- **Multi-location Practices**: Handle appointments for multiple clinic locations

### For Patients
- **Convenient Booking**: Schedule appointments from anywhere, anytime
- **Doctor Selection**: Choose from a variety of healthcare providers
- **Appointment Management**: Keep track of all medical appointments in one place

## 🔮 Roadmap

- [ ] **Payment Integration**: Online payment processing for consultations
- [ ] **Communication System**: Email and SMS reminders for appointments
- [ ] **Multi-clinic Support**: Enhanced support for multiple clinic locations
- [ ] **Admin Dashboard**: Comprehensive administrative interface
- [ ] **API Development**: RESTful API for mobile app integration
- [ ] **Analytics**: Appointment analytics and reporting features

## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Contributing Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Built with grace for better healthcare management**