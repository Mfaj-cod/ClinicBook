from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, g, send_from_directory, abort
import os, sqlite3, functools, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from sqlite3 import IntegrityError
import re

from src.init_db import setup
from src.seed import seed
from src.logg import logger
from gem import gemini_chat


BASE = os.path.dirname(__file__)
DB = os.path.join(BASE, 'data', 'clinicBook.db')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['DATABASE'] = DB
    logger.info("\nApp and DB connected.")

    # Database connection
    def get_db():
        if 'db' not in g:
            g.db = sqlite3.connect(app.config['DATABASE'])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(exc):
        db = g.pop('db', None)
        if db:
            db.close()

    #defining login required function
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "pateint_id" or "doctor_id" not in session:
                flash("Please log in first.", "warning")
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        
        return decorated_function
    

    # Helper function: update average rating
    def update_avg_rating(db, doctor_id=None, clinic_id=None):
        if doctor_id:
            avg = db.execute("SELECT AVG(rating) FROM reviews WHERE doctor_id=?", (doctor_id,)).fetchone()[0]
            db.execute("UPDATE doctors SET average_rating=? WHERE id=?", (avg or 0, doctor_id))
        if clinic_id:
            avg = db.execute("SELECT AVG(rating) FROM reviews WHERE clinic_id=?", (clinic_id,)).fetchone()[0]
            db.execute("UPDATE clinics SET average_rating=? WHERE id=?", (avg or 0, clinic_id))
        db.commit()

    # Injecting current user for templates
    @app.context_processor
    def inject_user():
        user = None
        if 'patient_id' in session and session.get('patient_id') != 0:
            db = get_db()
            user = db.execute(
                'SELECT id, name, email, phone, age, gender FROM patients WHERE id=?',
                (session['patient_id'],)
            ).fetchone()
        return dict(current_user=user)

    # home: show clinics with ratings
    @app.route('/')
    def index():
        db = get_db()
        clinics = db.execute(
            'SELECT id, name, city, address, phone, average_rating FROM clinics ORDER BY name LIMIT 6'
        ).fetchall()

        # added: features list to send to template
        features = [
            {'icon': 'bi-calendar-check', 'title': 'Instant Booking', 'desc': 'Book in seconds with instant confirmation', 'color': 'primary'},
            {'icon': 'bi-geo-alt', 'title': 'Nearby Clinics', 'desc': 'Find trusted clinics in your city', 'color': 'danger'},
            {'icon': 'bi-people', 'title': 'Patient Friendly', 'desc': 'Easy for all ages, no tech skills needed', 'color': 'success'},
            {'icon': 'bi-shield-lock', 'title': '100% Secure', 'desc': 'Your data is always safe and private', 'color': 'info'},
            {'icon': 'bi-clock', 'title': '24/7 Availability', 'desc': 'Book anytime, anywhere', 'color': 'warning'},
            {'icon': 'bi-star', 'title': 'Top Rated', 'desc': 'Verified doctors with patient reviews', 'color': 'purple'}
        ]

        return render_template('home.html', clinics=clinics, features=features)

    @app.route('/doctors', methods=['GET'])
    def doctors():
        q = request.args.get('q', '').strip()
        city = request.args.get('city', '').strip()
        specialization = request.args.get('specialization', '').strip()

        db = get_db()
        base = '''
            SELECT d.*, c.name as clinic_name, c.city as clinic_city, c.address as address
            FROM doctors d
            LEFT JOIN clinics c ON d.clinic_id = c.id
            WHERE 1=1
        '''
        params = []

        if q:
            base += ' AND (d.name LIKE ? OR d.specialization LIKE ? OR c.name LIKE ?)'
            params += [f'%{q}%'] * 3
        if city:
            base += ' AND c.city LIKE ?'
            params.append(f'%{city}%')
        if specialization:
            base += ' AND d.specialization LIKE ?'
            params.append(f'%{specialization}%')

        rows = db.execute(base + ' ORDER BY d.name', params).fetchall()
        return render_template(
            'doctors.html',
            doctors=rows,
            q=q,
            city=city,
            specialization=specialization
        )


    # Doctor details and available slots
    @login_required
    @app.route('/doctor/<int:doc_id>')
    def doctor_detail(doc_id):
        db = get_db()
        doc = db.execute(
            '''SELECT d.*, c.name as clinic_name, c.city as clinic_city, c.address
               FROM doctors d
               LEFT JOIN clinics c ON d.clinic_id = c.id
               WHERE d.id = ?''',
            (doc_id,)
        ).fetchone()
        if not doc:
            abort(404)
        today = datetime.date.today().isoformat()
        slots = db.execute(
            'SELECT * FROM slots WHERE doctor_id=? AND date>=? ORDER BY date,time',
            (doc_id, today)
        ).fetchall()

        reviews = db.execute(
            '''SELECT r.rating, r.comment, p.name as patient_name, r.created_at
               FROM reviews r 
               JOIN patients p ON r.patient_id = p.id
               WHERE r.doctor_id=? ORDER BY r.created_at DESC''',
            (doc_id,)
        ).fetchall()

        return render_template('book.html', doc=doc, slots=slots, reviews=reviews)



    # Submit review
    @login_required
    @app.route('/review', methods=['POST'])
    def review():
        if "patient_id" not in session:
            flash("Please login to leave a review.", "warning")
            return redirect(url_for("login"))

        db = get_db()
        patient_id = session["patient_id"]
        doctor_id = request.form.get("doctor_id")
        clinic_id = request.form.get("clinic_id")
        rating = int(request.form.get("rating"))
        comment = request.form.get("comment", "")

        db.execute(
            "INSERT INTO reviews (patient_id, doctor_id, clinic_id, rating, comment) VALUES (?, ?, ?, ?, ?)",
            (patient_id, doctor_id if doctor_id else None, clinic_id if clinic_id else None, rating, comment)
        )
        update_avg_rating(db, doctor_id=doctor_id, clinic_id=clinic_id)

        flash("Thank you for your review!", "success")
        logger.info(f"New review submitted.")
        return redirect(request.referrer or url_for("index"))



    # Book appointment
    @login_required
    @app.route('/book/<int:slot_id>', methods=['GET', 'POST'])
    def book(slot_id):
        if 'patient_id' not in session:
            flash('Please login as a patient to book', 'warning')
            return redirect(url_for('login', next=request.path))

        db = get_db()
        slot = db.execute(
            '''SELECT s.*, d.name as doctor_name, d.fees, c.name as clinic_name
            FROM slots s
            JOIN doctors d ON s.doctor_id = d.id
            JOIN clinics c ON d.clinic_id = c.id
            WHERE s.id = ?''',
            (slot_id,)
        ).fetchone()

        if not slot:
            abort(404)

        if request.method == 'POST':
            if slot['booked_count'] >= slot['capacity']:
                flash('Slot full', 'danger')
                return redirect(url_for('doctor_detail', doc_id=slot['doctor_id']))

            # Incrementing booked count
            db.execute(
                'UPDATE slots SET booked_count = booked_count + 1 WHERE id = ?',
                (slot_id,)
            )

            # Inserting appointment
            db.execute(
                '''INSERT INTO appointments (doctor_id, patient_id, slot_id, date, status)
                VALUES (?, ?, ?, ?, ?)''',
                (slot['doctor_id'], session['patient_id'], slot_id, slot['date'], 'booked')
            )

            db.commit()
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('dashboard'))

        # GET → show booking page
        logger.info(f"New appointment booked.")
        return render_template('book.html', slot=slot)




    # Patient dashboard
    @app.route('/dashboard')
    def dashboard():
        if 'patient_id' not in session:
            flash("Please login as a patient first.", "danger")
            return redirect(url_for('login'))

        db = get_db()
        appts = db.execute(
            '''SELECT a.*, d.name as doctor_name, d.specialization, s.date, s.time
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            JOIN slots s ON a.slot_id = s.id
            WHERE a.patient_id = ?
            ORDER BY s.date DESC''',
            (session['patient_id'],)
        ).fetchall()

        return render_template('dashboard_patient.html', appts=appts)



    # Doctor dashboard
    @app.route('/doctors_dashboard')
    def doctors_dashboard():
        if 'doctor_id' not in session:
            flash("Please login as a doctor first.", "danger")
            return redirect(url_for('doctor_login'))

        db = get_db()
        doctor_id = session['doctor_id']

        # Doctor info (with clinic details if available)
        doctor = db.execute(
            '''SELECT d.*, c.name as clinic_name, c.city as clinic_city, c.address
            FROM doctors d
            LEFT JOIN clinics c ON d.clinic_id = c.id
            WHERE d.id=?''',
            (doctor_id,)
        ).fetchone()

        # Appointments for this doctor
        appointments = db.execute(
            '''SELECT a.id, a.date, a.status,
                    p.name as patient_name, p.phone as patient_phone
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            WHERE a.doctor_id=?
            ORDER BY a.date DESC''',
            (doctor_id,)
        ).fetchall()

        # Reviews for this doctor
        reviews = db.execute(
            '''SELECT r.rating, r.comment, p.name as patient_name, r.created_at
            FROM reviews r
            JOIN patients p ON r.patient_id = p.id
            WHERE r.doctor_id=?
            ORDER BY r.created_at DESC''',
            (doctor_id,)
        ).fetchall()

        # Calculate average rating
        avg_rating = db.execute(
            "SELECT AVG(rating) as avg FROM reviews WHERE doctor_id=?",
            (doctor_id,)
        ).fetchone()
        if avg_rating and avg_rating['avg']:
            doctor = dict(doctor)
            doctor['average_rating'] = round(avg_rating['avg'], 1)

        return render_template(
            'dashboard_doctor.html',
            doctor=doctor,
            appointments=appointments,
            reviews=reviews
        )


    # Patients list for doctor
    @app.route("/patients")
    def patients():
        if 'patient_id' not in session:
            return redirect(url_for('login'))
        db = get_db()
        if 'doctor_id' in session:
            patients = db.execute(
                """SELECT DISTINCT p.id, p.name, p.email
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                WHERE a.doctor_id = ?""",
                (session.get("doctor_id"),)
            ).fetchall()
            return render_template("patients.html", patients=patients)
        return redirect(url_for("dashboard"))



    @app.route("/all_doctors")
    def all_doctors():
        db = get_db()
        doctors = db.execute("SELECT * FROM doctors").fetchall()
        return render_template("doctors.html", doctors=doctors)


    # User profile
    @app.route("/profile")
    def profile():
        db = get_db()

        # If doctor is logged in
        if "doctor_id" in session:
            doctor = db.execute("SELECT * FROM doctors WHERE id = ?", (session["doctor_id"],)).fetchone()
            return render_template("profile.html", doctor=doctor)

        # If patient is logged in
        elif "patient_id" in session:
            patient = db.execute("SELECT * FROM patients WHERE id = ?", (session["patient_id"],)).fetchone()
            my_reviews = db.execute(
                """SELECT r.rating, r.comment, r.created_at,
                        d.name as doctor_name, c.name as clinic_name
                FROM reviews r
                LEFT JOIN doctors d ON r.doctor_id = d.id
                LEFT JOIN clinics c ON r.clinic_id = c.id
                WHERE r.patient_id=?
                ORDER BY r.created_at DESC""",
                (session["patient_id"],)
            ).fetchall()
            return render_template("profile.html", patient=patient, my_reviews=my_reviews)

        # If neither logged in
        else:
            flash("Please log in first.", "danger")
            return redirect(url_for("login"))




    # Patient registration
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            name = request.form["name"]
            email = request.form["email"]
            age = request.form["age"]
            gender = request.form["gender"]
            phone = request.form["phone"]
            password = generate_password_hash(request.form["password"])

            db = get_db()
            try:
                db.execute(
                    "INSERT INTO patients (name, email, age, gender, phone, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, email, age, gender, phone, password),
                )
                db.commit()
                flash("Registration successful. Please login.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("Email already registered.", "danger")

        logger.info(f"New user registered.")
        return render_template("register.html")



    # Doctor registration
    @app.route('/register_doctor', methods=['GET', 'POST'])
    def register_doctor():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = generate_password_hash(request.form.get('password', '').strip())
            phone = request.form.get('phone', '').strip()
            clinic = request.form.get('clinic', '').strip()
            city = request.form.get('city', '').strip()
            address = request.form.get('address', '').strip()
            fees = int(request.form.get('fees') or 0)
            specialization = request.form.get('specialization', '').strip()

            if password == '' or email == '' or name == '' or fees < 0:
                flash('Please enter valid details.', 'danger')
                return redirect(url_for('register_doctor'))
            
            # Re-read raw password for strength checks (the hashed password is already in `password`)
            raw_password = request.form.get('password', '').strip()

            # Basic email format check
            email_re = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
            if not email_re.match(email) or len(email) > 254:
                flash('Please provide a valid email address.', 'danger')
                return redirect(url_for('register_doctor'))

            # Ensure domain part looks sane
            domain = email.split('@')[-1]
            if '.' not in domain or any(len(part) == 0 for part in domain.split('.')):
                flash('Email domain seems invalid.', 'danger')
                return redirect(url_for('register_doctor'))

            # Password strength checks
            pw_errors = []
            if len(raw_password) < 8:
                pw_errors.append('at least 8 characters')
            if not re.search(r'[A-Z]', raw_password):
                pw_errors.append('an uppercase letter')
            if not re.search(r'[a-z]', raw_password):
                pw_errors.append('a lowercase letter')
            if not re.search(r'\d', raw_password):
                pw_errors.append('a digit')
            if not re.search(r'[^A-Za-z0-9]', raw_password):
                pw_errors.append('a special character')

            if pw_errors:
                flash('Password must contain ' + ', '.join(pw_errors) + '.', 'danger')
                return redirect(url_for('register_doctor'))
            

            db = get_db()
            cur = db.execute(
                'SELECT id FROM clinics WHERE name=? AND city=?', 
                (clinic, city)
            ).fetchone()

            if cur:
                clinic_id = cur['id']
            else:
                r = db.execute(
                    'INSERT INTO clinics (name, city, address, phone) VALUES (?, ?, ?, ?)',
                    (clinic, city, address, phone)
                )
                clinic_id = r.lastrowid

            try:
                db.execute(
                    '''INSERT INTO doctors
                    (clinic_id, name, specialization, fees, email, password_hash, phone, about)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (clinic_id, name, specialization, fees, email, password, phone, '')
                )
                db.commit()
                flash('Doctor registered successfully ✅ Please login.', 'success')
                return redirect(url_for('doctor_login'))
            except IntegrityError:
                flash('❌ This email is already registered. Please use a different email.', 'danger')
                return redirect(url_for('register_doctor'))
        logger.info(f"New doctor registered: {name}")
        return render_template('register_doctor.html')




    # Login for patient or doctor
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            db = get_db()
            doctor = db.execute("SELECT * FROM doctors WHERE email = ?", (email,)).fetchone()
            if doctor and check_password_hash(doctor["password_hash"], password):
                session["doctor_id"] = doctor["id"]
                flash("Welcome Doctor!", "success")
                return redirect(url_for("doctors_dashboard"))

            patient = db.execute("SELECT * FROM patients WHERE email = ?", (email,)).fetchone()
            if patient and check_password_hash(patient["password_hash"], password):
                session["patient_id"] = patient["id"]
                flash("Welcome Patient!", "success")
                return redirect(url_for("dashboard"))

            flash("Invalid email or password", "danger")

        return render_template("login.html")

    
    @app.route('/clinic/<int:clinic_id>')
    def clinic_detail(clinic_id):
        db = get_db()
        clinic = db.execute(
            "SELECT * FROM clinics WHERE id=?", (clinic_id,)
        ).fetchone()
        if not clinic:
            abort(404)
        reviews = db.execute(
            '''SELECT r.rating, r.comment, p.name as patient_name, r.created_at
            FROM reviews r
            JOIN patients p ON r.patient_id = p.id
            WHERE r.clinic_id=? ORDER BY r.created_at DESC''',
            (clinic_id,)
        ).fetchall()
        return render_template("clinic_detail.html", clinic=clinic, reviews=reviews)


    # Cancel appointment (doctor or patient can cancel)
    @app.route('/cancel_appointment/<int:appointment_id>', methods=['GET', 'POST'])
    def cancel_appointment(appointment_id):
        db = get_db()

        if 'patient_id' not in session and 'doctor_id' not in session:
            flash('You must be logged in to cancel appointments.', 'warning')
            return redirect(url_for('login'))

        appt = db.execute('SELECT * FROM appointments WHERE id=?', (appointment_id,)).fetchone()
        if not appt:
            flash('Appointment not found.', 'danger')
            if 'patient_id' in session:
                return redirect(url_for('dashboard'))
            return redirect(url_for('doctors_dashboard'))

        allowed = False
        if 'patient_id' in session and appt['patient_id'] == session['patient_id']:
            allowed = True
        if 'doctor_id' in session and appt['doctor_id'] == session['doctor_id']:
            allowed = True

        if not allowed:
            flash('You are not authorized to cancel this appointment.', 'danger')
            if 'patient_id' in session:
                return redirect(url_for('dashboard'))
            return redirect(url_for('doctors_dashboard'))

        # ✅ Instead of DELETE, just mark as cancelled
        db.execute('UPDATE appointments SET status=? WHERE id=?', ('cancelled', appointment_id))
        db.commit()

        logger.info(f"An appointment cancelled. Unfortunately")
        flash('Appointment cancelled.', 'success')
        if 'patient_id' in session:
            return redirect(url_for('dashboard'))
        return redirect(url_for('doctors_dashboard'))


    # Mark appointment as completed (doctor only)
    @app.route('/complete_appointment/<int:appointment_id>', methods=['POST'])
    def complete_appointment(appointment_id):
        db = get_db()

        if 'doctor_id' not in session:
            flash('Only doctors can complete appointments.', 'warning')
            return redirect(url_for('login'))

        appt = db.execute('SELECT * FROM appointments WHERE id=?', (appointment_id,)).fetchone()
        if not appt:
            flash('Appointment not found.', 'danger')
            return redirect(url_for('doctors_dashboard'))

        if appt['doctor_id'] != session['doctor_id']:
            flash('You are not authorized to complete this appointment.', 'danger')
            return redirect(url_for('doctors_dashboard'))

        # ✅ Update status to completed
        db.execute('UPDATE appointments SET status=? WHERE id=?', ('completed', appointment_id))
        db.commit()

        logger.info(f"An appointment attended by the patient.")
        flash('Appointment marked as completed.', 'success')
        return redirect(url_for('doctors_dashboard'))




    # Doctor view & manage slots
    @app.route("/doctor/slots")
    def doctor_slots():
        if "doctor_id" not in session:
            flash("Please login as a doctor first.", "danger")
            return redirect(url_for("doctor_login"))

        db = get_db()
        slots = db.execute(
            "SELECT * FROM slots WHERE doctor_id=? ORDER BY date, time",
            (session["doctor_id"],)
        ).fetchall()

        return render_template("doctor_slots.html", slots=slots)


    # Add new slot
    @app.route("/doctor/slots/add", methods=["POST"])
    def add_slot():
        if "doctor_id" not in session:
            return redirect(url_for("doctor_login"))

        date = request.form["date"]
        time = request.form["time"]
        capacity = request.form.get("capacity", 5)

        db = get_db()
        db.execute(
            "INSERT INTO slots (doctor_id, date, time, capacity, booked_count) VALUES (?, ?, ?, ?, 0)",
            (session["doctor_id"], date, time, capacity)
        )
        db.commit()
        flash("New slot added!", "success")
        logger.info(f"Added new slots: ", 'doctor_id')
        return redirect(url_for("doctor_slots"))


    # Delete slot
    @app.route("/doctor/slots/delete/<int:slot_id>")
    def delete_slot(slot_id):
        if "doctor_id" not in session:
            return redirect(url_for("doctor_login"))

        db = get_db()
        db.execute("DELETE FROM slots WHERE id=? AND doctor_id=?", (slot_id, session["doctor_id"]))
        db.commit()
        flash("Slot deleted.", "info")
        return redirect(url_for("doctor_slots"))
    

        
    @app.route("/chat_with_gemini", methods=["POST"])
    def chat_with_gemini_route():
        return gemini_chat(request)


    # Logout
    @app.route('/logout')
    def logout():
        session.clear()
        flash('Logged out', 'info')
        logger.info(f"User logged out.")
        return redirect(url_for('index'))

    return app
    


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        setup()
        seed()

    app.run(debug=True)
    logger.info(f"App running..................")