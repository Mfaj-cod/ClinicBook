import sqlite3, os
from data import doctors_data

BASE = os.path.dirname(__file__)
DB = os.path.join(BASE, 'instance', 'app_v2.db')

def ensure_schema(conn):
    cur = conn.cursor()
    # Enable foreign key support
    cur.execute('PRAGMA foreign_keys = ON;')
    # Create tables if not exist (schema matches init_db.py)
    cur.executescript('''
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
    ''')
    conn.commit()
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
            cur.execute('INSERT INTO clinics (name, city, address, phone) VALUES (?, ?, ?, ?)', (d['clinic'], d['city'], d.get('address',''), d.get('phone','')))
            clinic_id = cur.lastrowid
        try:
            cur.execute('''INSERT OR IGNORE INTO doctors (clinic_id, name, specialization, fees, email, phone, about)
                           VALUES (?, ?, ?, ?, ?, ?, ?)''', (clinic_id, d['name'], d['specialization'], d['fees'], d['email'], d.get('phone',''), d.get('about','')))
        except Exception as e:
            print('Error', e)
    conn.commit()
    conn.close()
    print('Seeding complete. DB at', DB)

if __name__ == '__main__':
    seed()