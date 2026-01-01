import sqlite3
import os
from datetime import datetime

DB_PATH = "data/workers.db"

class WorkerDB:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            service_type TEXT,
            experience TEXT,
            documents TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT
        )
        """)
        self.conn.commit()

    def register_worker(self, name, email, phone, service_type, experience, documents):
        self.cursor.execute("""
        INSERT INTO workers 
        (name, email, phone, service_type, experience, documents, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            phone,
            service_type,
            experience,
            documents,
            datetime.utcnow().isoformat()
        ))
        self.conn.commit()

    def get_pending_workers(self):
        self.cursor.execute(
            "SELECT id, name, service_type FROM workers WHERE status='pending'"
        )
        return self.cursor.fetchall()

    def approve_worker(self, worker_id):
        self.cursor.execute(
            "UPDATE workers SET status='approved' WHERE id=?",
            (worker_id,)
        )
        self.conn.commit()

    def reject_worker(self, worker_id):
        self.cursor.execute(
            "UPDATE workers SET status='rejected' WHERE id=?",
            (worker_id,)
        )
        self.conn.commit()
