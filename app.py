from flask import Flask, render_template, request, redirect, url_for, session, flash, g, send_from_directory, abort
import os, sqlite3, functools, datetime
from werkzeug.security import generate_password_hash, check_password_hash

BASE = os.path.dirname(__file__)
DB = os.path.join(BASE, 'instance', 'app_v2.db')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_change_me')
    app.config['DATABASE'] = DB

    # Serve manifest.json for PWA
    @app.route('/manifest.json')
    def manifest():
        return send_from_directory(os.path.join(BASE, 'static'), 'manifest.json')

    # Serve service worker JS for PWA
    @app.route('/sw.js')
    def sw():
        # Set correct mimetype for service worker
        return send_from_directory(os.path.join(BASE, 'static', 'js'), 'sw.js', mimetype='application/javascript')

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

    # Inject current user for templates
    @app.context_processor
    def inject_user():
        user = None
        if 'user_id' in session and session.get('user_id') != 0:
            db = get_db()
            user = db.execute(
                'SELECT id, name, email, role FROM users WHERE id=?',
                (session['user_id'],)
            ).fetchone()
        return dict(current_user=user)

    # Home page: show clinics
    @app.route('/')
    def index():
        db = get_db()
        clinics = db.execute('SELECT * FROM clinics ORDER BY name LIMIT 6').fetchall()
        return render_template('home.html', clinics=clinics)

    # Doctors search/listing
    @app.route('/doctors', methods=['GET'])
    def doctors():
        q = request.args.get('q', '').strip()
        city = request.args.get('city', '').strip()
        db = get_db()
        base = '''
            SELECT d.*, c.name as clinic_name, c.city as clinic_city
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
        rows = db.execute(base + ' ORDER BY d.name', params).fetchall()
        return render_template('doctors.html', doctors=rows, q=q, city=city)


    # Doctor detail and available slots
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
        return render_template('book.html', doc=doc, slots=slots)



    # Book appointment
    @app.route('/book/<int:slot_id>', methods=['GET', 'POST'])
    def book(slot_id):
        if 'user_id' not in session:
            flash('Please login to book', 'warning')
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
            patient_name = request.form.get('patient_name', '').strip()
            patient_phone = request.form.get('patient_phone', '').strip()
            symptoms = request.form.get('symptoms', '').strip()
            if slot['booked_count'] >= slot['capacity']:
                flash('Slot full', 'danger')
                return redirect(url_for('doctor_detail', doc_id=slot['doctor_id']))
            db.execute(
                '''INSERT INTO appointments
                   (user_id, doctor_id, slot_id, patient_name, patient_phone, symptoms)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (session['user_id'], slot['doctor_id'], slot_id, patient_name, patient_phone, symptoms)
            )
            db.execute('UPDATE slots SET booked_count = booked_count + 1 WHERE id = ?', (slot_id,))
            db.commit()
            flash('Appointment booked', 'success')
            return redirect(url_for('dashboard'))
        return render_template('book.html', slot=slot)



    # Dashboard for patient or doctor
    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        db = get_db()
        if session.get('role') == 'doctor':
            appts = db.execute(
                '''SELECT a.*, u.name as patient_name, s.date, s.time, d.name as doctor_name
                   FROM appointments a
                   JOIN slots s ON a.slot_id = s.id
                   JOIN users u ON a.user_id = u.id
                   JOIN doctors d ON a.doctor_id = d.id
                   WHERE d.id = ?''',
                (session.get('doctor_id'),)
            ).fetchall()
            return render_template('dashboard_doctor.html', appts=appts)
        appts = db.execute(
            '''SELECT a.*, d.name as doctor_name, s.date, s.time, d.specialization
               FROM appointments a
               JOIN doctors d ON a.doctor_id = d.id
               JOIN slots s ON a.slot_id = s.id
               WHERE a.user_id = ?
               ORDER BY s.date DESC''',
            (session['user_id'],)
        ).fetchall()
        return render_template('dashboard_patient.html', appts=appts)



    # Patient registration
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip().lower()
            phone = request.form.get('phone', '').strip()
            password = request.form.get('password', '')
            db = get_db()
            if db.execute('SELECT id FROM users WHERE email=?', (email,)).fetchone():
                flash('Email exists', 'warning')
                return redirect(url_for('login'))
            db.execute(
                '''INSERT INTO users (name, email, phone, password_hash, role)
                   VALUES (?, ?, ?, ?, ?)''',
                (name, email, phone, generate_password_hash(password), 'patient')
            )
            db.commit()
            flash('Account created, login')
            return redirect(url_for('login'))
        return render_template('register.html')



    # Doctor registration
    @app.route('/register_doctor', methods=['GET', 'POST'])
    def register_doctor():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip().lower()
            phone = request.form.get('phone', '').strip()
            clinic = request.form.get('clinic', '').strip()
            city = request.form.get('city', '').strip()
            fees = int(request.form.get('fees') or 0)
            specialization = request.form.get('specialization', '').strip()
            db = get_db()
            cur = db.execute('SELECT id FROM clinics WHERE name=? AND city=?', (clinic, city)).fetchone()
            if cur:
                clinic_id = cur['id']
            else:
                r = db.execute(
                    'INSERT INTO clinics (name, city, address, phone) VALUES (?, ?, ?, ?)',
                    (clinic, city, '', phone)
                )
                clinic_id = r.lastrowid
            db.execute(
                '''INSERT INTO doctors
                   (clinic_id, name, specialization, fees, email, phone, about)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (clinic_id, name, specialization, fees, email, phone, '')
            )
            db.commit()
            flash('Doctor registered.', 'success')
            return redirect(url_for('doctors'))
        return render_template('register_doctor.html')


    # Login for patient or doctor
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            db = get_db()
            user = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['role'] = user['role']
                session['user_name'] = user['name']
                flash('Welcome!', 'success')
                return redirect(url_for('index'))
            doc = db.execute('SELECT * FROM doctors WHERE email=?', (email,)).fetchone()
            if doc:
                session['user_id'] = 0
                session['role'] = 'doctor'
                session['doctor_id'] = doc['id']
                session['user_name'] = doc['name']
                flash('Logged in as doctor (seed login).', 'success')
                return redirect(url_for('dashboard'))
            flash('Invalid credentials', 'danger')
        return render_template('login.html')


    # Logout
    @app.route('/logout')
    def logout():
        session.clear()
        flash('Logged out', 'info')
        return redirect(url_for('index'))

    return app


if __name__ == '__main__':
    from init_db import setup as init_setup
    if not os.path.exists(DB):
        init_setup()
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)