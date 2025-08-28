import sqlite3, os
from doctors_data import doctors_data
import datetime

BASE = os.path.dirname(__file__)
DB = os.path.join(BASE, 'data', 'clinicBook.db')

def ensure_schema(conn):
    cur = conn.cursor()
    # Enable foreign key support
    cur.execute('PRAGMA foreign_keys = ON;')
    # Create tables if not exist
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS clinics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        city TEXT,
        address TEXT,
        phone TEXT,
        average_rating REAL DEFAULT 0.0
    );
                      
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinic_id INTEGER,
        name TEXT NOT NULL,
        specialization TEXT,
        fees INTEGER,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT,
        phone TEXT,
        about TEXT,
        average_rating REAL DEFAULT 0.0,
        FOREIGN KEY (clinic_id) REFERENCES clinics(id) ON DELETE SET NULL
    );
                      
    CREATE TABLE IF NOT EXISTS slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        capacity INTEGER NOT NULL DEFAULT 5,
        booked_count INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
    );
                      
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone TEXT,
        age INTEGER,
        gender TEXT
    );

    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER NOT NULL,
        patient_id INTEGER NOT NULL,
        slot_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT DEFAULT 'booked',
        FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
        FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
        FOREIGN KEY (slot_id) REFERENCES slots(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER,
        clinic_id INTEGER,
        rating INTEGER CHECK(rating >= 1 AND rating <= 5),
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
        FOREIGN KEY (clinic_id) REFERENCES clinics(id) ON DELETE CASCADE,
        CHECK (
            (doctor_id IS NOT NULL AND clinic_id IS NULL) OR
            (doctor_id IS NULL AND clinic_id IS NOT NULL)
        )
    );
    ''')
    conn.commit()


def generate_slots(doctor_id, days=7):
    """Generate slots for next N days."""
    slots = []
    today = datetime.date.today()
    for i in range(days):
        date = today + datetime.timedelta(days=i)
        for time in ["10:00", "16:00"]:  # 2 slots per day
            slots.append((doctor_id, date.isoformat(), time, 5, 0))
    return slots


def seed():
    os.makedirs(os.path.join(BASE, 'instance'), exist_ok=True)
    conn = sqlite3.connect(DB)
    ensure_schema(conn)
    cur = conn.cursor()

    for d in doctors_data:
        cur.execute('SELECT id FROM clinics WHERE name=? AND city=?', (d['clinic'], d['city']))
        row = cur.fetchone()
        if row:
            clinic_id = row[0]
        else:
            cur.execute(
                'INSERT INTO clinics (name, city, address, phone) VALUES (?, ?, ?, ?)',
                (d['clinic'], d['city'], d.get('address',''), d.get('phone',''))
            )
            clinic_id = cur.lastrowid
        try:
            cur.execute('''INSERT OR IGNORE INTO doctors (clinic_id, name, specialization, fees, email, phone, about)
                           VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (clinic_id, d['name'], d['specialization'], d['fees'],
                            d['email'], d.get('phone',''), d.get('about','')))
            
            # Always fetch doctor_id
            cur.execute('SELECT id FROM doctors WHERE email=?', (d['email'],))
            doctor_id = cur.fetchone()[0]

            # Generate slots only if none exist yet
            cur.execute('SELECT COUNT(*) FROM slots WHERE doctor_id=?', (doctor_id,))
            if cur.fetchone()[0] == 0:
                slots = generate_slots(doctor_id, days=7)
                cur.executemany(
                    '''INSERT INTO slots (doctor_id, date, time, capacity, booked_count)
                    VALUES (?, ?, ?, ?, ?)''',
                    slots
                )

        except Exception as e:
            print('Error', e)

    conn.commit()
    conn.close()
    print('Seeding complete. DB at', DB)


if __name__ == '__main__':
    seed()
