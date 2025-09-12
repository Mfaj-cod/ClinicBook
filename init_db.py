import sqlite3, os
BASE = os.path.dirname(__file__)
DB = os.path.join(BASE, 'data', 'clinicBook.db')

def setup():
    os.makedirs(os.path.join(BASE, 'data'), exist_ok=True)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    # Enable foreign key support
    cur.execute('PRAGMA foreign_keys = ON;')
    # Create tables
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        password_hash TEXT
    );
                      
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
        doctor_id INTEGER,
        date TEXT,
        time TEXT,
        capacity INTEGER DEFAULT 1,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        slot_id INTEGER,
        patient_name TEXT,
        patient_phone TEXT,
        symptoms TEXT,
        date TEXT NOT NULL,
        status TEXT DEFAULT 'booked',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
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
    conn.close()
    print('DB schema ready at', DB)

if __name__ == '__main__':
    setup()
