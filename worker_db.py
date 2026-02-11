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
                password TEXT
            )
        """)
        self.conn.commit()

    def _row_to_dict(self, row):
        if row is None:
            return None
        d = dict(row) if hasattr(row, "keys") else row
        if isinstance(d, dict):
            d["name"] = d.get("full_name") or d.get("name", "")
        return d

    def register_worker(self, full_name, email, phone, service, specialization, experience, clinic_location="", license_number=None, password=None):
        cursor = self.conn.cursor()
        hashed_pw = None
        if password:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            
        try:
            cursor.execute("""
                INSERT INTO workers (full_name, email, phone, service, specialization, experience, clinic_location, license_number, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (full_name, email, phone, service, specialization, int(experience or 0), clinic_location or "", license_number, hashed_pw))
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
