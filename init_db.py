import sqlite3, os
BASE = os.path.dirname(__file__)
DB = os.path.join(BASE, 'instance', 'app_v2.db')

def setup():
    os.makedirs(os.path.join(BASE, 'instance'), exist_ok=True)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    # Enable foreign key support
    cur.execute('PRAGMA foreign_keys = ON;')
    # Create tables
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        password_hash TEXT,
        role TEXT DEFAULT 'patient'
    );
    CREATE TABLE IF NOT EXISTS clinics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        city TEXT,
        address TEXT,
        phone TEXT
    );
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinic_id INTEGER,
        name TEXT NOT NULL,
        specialization TEXT,
        fees INTEGER,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        about TEXT,
        FOREIGN KEY (clinic_id) REFERENCES clinics(id) ON DELETE SET NULL
    );
    CREATE TABLE IF NOT EXISTS slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER,
        date TEXT,
        time TEXT,
        capacity INTEGER DEFAULT 1,
        booked_count INTEGER DEFAULT 0,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        doctor_id INTEGER,
        slot_id INTEGER,
        patient_name TEXT,
        patient_phone TEXT,
        symptoms TEXT,
        status TEXT DEFAULT 'booked',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
        FOREIGN KEY (slot_id) REFERENCES slots(id) ON DELETE CASCADE
    );
    ''')
    conn.commit()
    conn.close()
    print('DB schema ready at', DB)
if __name__ == '__main__':
    setup()