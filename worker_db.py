"""
Worker/Doctor database for healthcare professionals.
"""
import sqlite3
import bcrypt
from config import WORKER_DB, DATA_DIR
import os

os.makedirs(DATA_DIR, exist_ok=True)


class WorkerDB:
    def __init__(self):
        self.conn = sqlite3.connect(WORKER_DB, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def get_conn(self):
        return sqlite3.connect(WORKER_DB)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                service TEXT DEFAULT 'healthcare',
                specialization TEXT,
                experience INTEGER DEFAULT 0,
                clinic_location TEXT,
                rating REAL DEFAULT 0,
                photo_url TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                license_number TEXT,
                password TEXT,
                consultation_fee INTEGER DEFAULT 400
            )
        """)
        
        # Check and add missing columns (migration)
        cursor.execute("PRAGMA table_info(workers)")
        existing_columns = {row[1] for row in cursor.fetchall()}
        
        required_columns = {
            'id', 'full_name', 'email', 'phone', 'service', 'specialization',
            'experience', 'clinic_location', 'rating', 'photo_url', 'status',
            'created_at', 'license_number', 'password', 'consultation_fee'
        }
        
        missing_columns = required_columns - existing_columns
        
        for column in missing_columns:
            if column == 'consultation_fee':
                print(f"🔄 Adding missing column: {column}")
                cursor.execute("ALTER TABLE workers ADD COLUMN consultation_fee INTEGER DEFAULT 400")
        
        self.conn.commit()

    def _row_to_dict(self, row):
        if row is None:
            return None
        d = dict(row) if hasattr(row, "keys") else row
        if isinstance(d, dict):
            d["name"] = d.get("full_name") or d.get("name", "")
        return d

    def register_worker(self, full_name, email, phone, service, specialization, experience, clinic_location="", license_number=None, password=None, consultation_fee=400):
        cursor = self.conn.cursor()
        hashed_pw = None
        if password:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            
        try:
            cursor.execute("""
                INSERT INTO workers (full_name, email, phone, service, specialization, experience, clinic_location, license_number, password, consultation_fee)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (full_name, email, phone, service, specialization, int(experience or 0), clinic_location or "", license_number, hashed_pw, int(consultation_fee)))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def verify_worker_login(self, email):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, status, service, specialization FROM workers WHERE email = ?",
            (email,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return (row["id"], row["status"], row["service"], row["specialization"] or "")

    def get_all_specializations(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT specialization FROM workers WHERE specialization IS NOT NULL AND specialization != ''")
        return [r["specialization"] for r in cursor.fetchall()]

    def get_all_workers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM workers WHERE status = 'approved'")
        return [self._row_to_dict(r) for r in cursor.fetchall()]

    def get_workers_by_specialization(self, specialization):
        cursor = self.conn.cursor()
        spec = (specialization or "").lower().strip()
        cursor.execute(
            "SELECT * FROM workers WHERE status = 'approved' AND LOWER(TRIM(specialization)) = ?",
            (spec,)
        )
        return [self._row_to_dict(r) for r in cursor.fetchall()]

    def search_workers(self, q):
        if not q or not str(q).strip():
            return self.get_all_workers()
        cursor = self.conn.cursor()
        pattern = f"%{q.strip()}%"
        cursor.execute("""
            SELECT * FROM workers WHERE status = 'approved'
            AND (full_name LIKE ? OR specialization LIKE ? OR clinic_location LIKE ?)
        """, (pattern, pattern, pattern))
        return [self._row_to_dict(r) for r in cursor.fetchall()]

    def get_pending_workers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM workers WHERE status = 'pending'")
        return [self._row_to_dict(r) for r in cursor.fetchall()]

    def get_worker_by_id(self, worker_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM workers WHERE id = ?", (worker_id,))
        row = cursor.fetchone()
        return self._row_to_dict(row)

    def approve_worker(self, worker_id):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE workers SET status = 'approved' WHERE id = ?", (worker_id,))
        self.conn.commit()

    def reject_worker(self, worker_id):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE workers SET status = 'rejected' WHERE id = ?", (worker_id,))
        self.conn.commit()
    
    def get_worker_consultation_fee(self, worker_id):
        """Get consultation fee for a worker"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT consultation_fee FROM workers WHERE id = ?", (worker_id,))
        result = cursor.fetchone()
        return result[0] if result else 400  # Default fee
    
    def update_consultation_fee(self, worker_id, consultation_fee):
        """Update consultation fee for a worker"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE workers 
            SET consultation_fee = ? 
            WHERE id = ?
        """, (int(consultation_fee), worker_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_worker_profile(self, worker_id):
        """Get complete worker profile including consultation fee"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT full_name, email, phone, specialization, experience, 
                   clinic_location, consultation_fee, rating, status
            FROM workers 
            WHERE id = ?
        """, (worker_id,))
        result = cursor.fetchone()
        
        if result:
            return {
                "doctor_name": result[0],
                "email": result[1],
                "phone": result[2],
                "specialization": result[3],
                "experience": result[4],
                "clinic_location": result[5],
                "consultation_fee": result[6],
                "rating": result[7],
                "status": result[8]
            }
        return None
    
    def get_worker_by_email(self, email):
        """Get worker ID by email"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM workers WHERE email = ?", (email,))
        result = cursor.fetchone()
        return result[0] if result else None
