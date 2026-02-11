# appointment_db.py
import sqlite3
import random
import string
from availability_db import AvailabilityDB

DB_PATH = "data/expertease.db"

class AppointmentDB:

    def __init__(self):
        print("🔥 AppointmentDB LOADED")
        self.availability_db = AvailabilityDB()
        self.create_table()

    def get_conn(self):
        return sqlite3.connect(DB_PATH)

    # =========================================================
    # SAFE AUTO-MIGRATION
    # =========================================================
    def _ensure_schema(self):
        """
        Safely migrate database schema to include all required columns
        This runs on every app startup to ensure consistency
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        
        # Get current schema
        cursor.execute("PRAGMA table_info(appointments)")
        existing_columns = {row[1] for row in cursor.fetchall()}
        
        # Required columns for the system
        required_columns = {
            'id', 'user_id', 'worker_id', 'user_name', 'patient_symptoms',
            'booking_date', 'time_slot', 'appointment_type', 'status',
            'meeting_link', 'doctor_otp', 'otp_verified', 'created_at',
            'video_room', 'video_status', 'prescription_file'
        }
        
        # Add missing columns
        missing_columns = required_columns - existing_columns
        
        for column in missing_columns:
            if column == 'id':
                continue  # Primary key, should always exist
                
            print(f"🔄 Adding missing column: {column}")
            
            # Define column types
            column_definitions = {
                'user_id': 'INTEGER',
                'worker_id': 'INTEGER', 
                'user_name': 'TEXT',
                'patient_symptoms': 'TEXT',
                'booking_date': 'TEXT',
                'time_slot': 'TEXT',
                'appointment_type': 'TEXT',
                'status': 'TEXT DEFAULT "pending"',
                'meeting_link': 'TEXT',
                'doctor_otp': 'TEXT',
                'otp_verified': 'INTEGER DEFAULT 0',
                'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
                'video_room': 'TEXT',
                'video_status': 'TEXT DEFAULT "ready"',
                'prescription_file': 'TEXT'
            }
            
            try:
                alter_sql = f"ALTER TABLE appointments ADD COLUMN {column} {column_definitions.get(column, 'TEXT')}"
                cursor.execute(alter_sql)
                print(f"✅ Added column: {column}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"⚠️ Column {column} already exists")
                else:
                    print(f"❌ Error adding column {column}: {e}")
        
        conn.commit()
        conn.close()
        print("🔧 Schema migration completed")

    # =========================================================
    # CREATE TABLE (VIDEO + CLINIC SUPPORTED)
    # =========================================================
    def create_table(self):
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            worker_id INTEGER,
            user_name TEXT,
            patient_symptoms TEXT,
            booking_date TEXT,
            time_slot TEXT,
            appointment_type TEXT,
            status TEXT DEFAULT 'pending',

            meeting_link TEXT,
            doctor_otp TEXT,
            otp_verified INTEGER DEFAULT 0,
            
            -- Video consultation specific fields
            video_room TEXT,
            video_status TEXT DEFAULT 'ready',
            prescription_file TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        conn.close()
        
        # Run auto-migration after table creation
        self._ensure_schema()

    # =========================================================
    # UTIL FUNCTIONS
    # =========================================================
    def _generate_meeting_link(self):
        code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"https://expertease.app/meet/{code}"

    def _generate_otp(self):
        return str(random.randint(100000, 999999))

    # =========================================================
    # VIDEO REQUEST (USER SIDE)
    # =========================================================
    def book_video(self, user_id, worker_id, user_name, symptoms):
        from datetime import datetime, timedelta
        import random
        import string
        
        conn = self.get_conn()
        cursor = conn.cursor()

        # Set booking_date to today and time_slot to a default for video consultations
        today = datetime.now().strftime('%Y-%m-%d')
        default_time = "ASAP (Video Call)"
        
        # Generate unique video room
        room_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        video_room = f"room_{room_code}"

        cursor.execute("""
        INSERT INTO appointments
        (user_id, worker_id, user_name, patient_symptoms,
         booking_date, time_slot, appointment_type, status, video_room, video_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, worker_id, user_name, symptoms, today, default_time, 'video', 'pending', video_room, 'ready'))

        conn.commit()
        apt_id = cursor.lastrowid
        conn.close()
        
        print(f"📹 Video consultation booked with ID: {apt_id}")
        print(f"📅 Date: {today}")
        print(f"⏰ Time: {default_time}")
        print(f"🔗 Video Room: {video_room}")
        
        return apt_id

    # =========================================================
    # CLINIC BOOKING (ENHANCED)
    # =========================================================
    def book_clinic(self, user_id, worker_id, user_name, symptoms, date, time_slot):
        """
        Book clinic appointment with enhanced slot matching and logging
        Returns (success, result) where result is appointment_id or error message
        """
        print(f"📅 Attempting clinic booking for user {user_id}, worker {worker_id}")
        print(f"📅 Date: {date}, Time Slot: '{time_slot}'")
        
        # Normalize time slot
        time_slot = time_slot.strip()
        print(f"📅 Normalized time slot: '{time_slot}'")

        # Check availability with proper normalization
        slots = self.availability_db.get_availability(worker_id, date)
        if not slots:
            print(f"❌ No availability found for worker {worker_id} on {date}")
            return False, "No availability found for this date"

        print(f"📅 Available slots: {[s['time_slot'].strip() for s in slots]}")
        
        # Check if slot exists (with proper normalization)
        slot_found = False
        for slot in slots:
            available_slot = slot["time_slot"].strip()
            if available_slot == time_slot:
                slot_found = True
                break

        if not slot_found:
            print(f"❌ Slot '{time_slot}' not found in available slots")
            return False, "Selected time slot is not available"

        # Remove the availability
        try:
            self.availability_db.remove_availability(worker_id, date, time_slot)
            print(f"✅ Removed availability for slot '{time_slot}'")
        except Exception as e:
            print(f"❌ Error removing availability: {e}")
            return False, "Failed to reserve time slot"

        # Book the appointment
        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO appointments
            (user_id, worker_id, user_name, patient_symptoms,
             booking_date, time_slot, appointment_type, status)
            VALUES (?, ?, ?, ?, ?, ?, 'clinic', 'pending')
            """, (user_id, worker_id, user_name, symptoms, date, time_slot))

            conn.commit()
            apt_id = cursor.lastrowid
            print(f"✅ Clinic appointment booked successfully with ID: {apt_id}")
            
            return True, apt_id
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Database error during booking: {e}")
            return False, "Database error during booking"
        finally:
            conn.close()

    # =========================================================
    # FETCH REQUESTS FOR DOCTOR
    # =========================================================
    def get_pending_for_worker(self, worker_id):
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM appointments
        WHERE worker_id=? AND status='pending'
        ORDER BY created_at DESC
        """, (worker_id,))

        rows = cursor.fetchall()
        keys = [d[0] for d in cursor.description]
        conn.close()

        return [dict(zip(keys, r)) for r in rows]

    # =========================================================
    # GET APPOINTMENTS BY WORKER
    # =========================================================
    def get_by_worker(self, worker_id):
        """
        Get all appointments for a specific worker
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM appointments
        WHERE worker_id=?
        ORDER BY created_at DESC
        """, (worker_id,))

        rows = cursor.fetchall()
        keys = [d[0] for d in cursor.description]
        conn.close()

        return [dict(zip(keys, r)) for r in rows]

    # =========================================================
    # GET APPOINTMENT BY ID
    # =========================================================
    def get_by_id(self, appointment_id):
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM appointments WHERE id=?", (appointment_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        keys = [d[0] for d in cursor.description]
        conn.close()
        return dict(zip(keys, row))

    # =========================================================
    # ACCEPT / REJECT
    # =========================================================
    def respond(self, appointment_id, status):
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE appointments SET status=? WHERE id=?",
            (status, appointment_id)
        )

        conn.commit()
        conn.close()

    # =========================================================
    # SAVE MEETING LINK + OTP (WHEN DOCTOR ACCEPTS)
    # =========================================================
    def set_video_details(self, appointment_id):
        conn = self.get_conn()
        cursor = conn.cursor()

        # Get current video room
        cursor.execute("SELECT video_room FROM appointments WHERE id=?", (appointment_id,))
        result = cursor.fetchone()
        
        meeting_link = self._generate_meeting_link()
        otp = self._generate_otp()
        video_room = result[0] if result else f"room_{appointment_id}"

        cursor.execute("""
        UPDATE appointments
        SET meeting_link=?, doctor_otp=?, video_status='ready'
        WHERE id=?
        """, (meeting_link, otp, appointment_id))

        conn.commit()
        conn.close()

        print(f"🔧 Setting video details for appointment {appointment_id}")
        print(f"🔗 Meeting Link: {meeting_link}")
        print(f"🔐 Generated OTP: {otp}")
        print(f"🏠 Video Room: {video_room}")
        
        return meeting_link, otp, video_room

    # =========================================================
    # VERIFY OTP (DOCTOR STARTING CALL)
    # =========================================================
    def verify_otp(self, appointment_id, otp):
        """
        Verify doctor's OTP and mark consultation as started
        Returns True if OTP is correct, False otherwise
        """
        print(f"🔐 Verifying OTP for appointment {appointment_id}")
        
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT doctor_otp FROM appointments WHERE id=?", (appointment_id,))
        row = cursor.fetchone()

        if not row or row[0] != otp:
            conn.close()
            print(f"❌ OTP verification failed for appointment {appointment_id}")
            return False

        cursor.execute("""
        UPDATE appointments
        SET status='in_consultation', otp_verified=1
        WHERE id=?
        """, (appointment_id,))

        conn.commit()
        conn.close()
        
        print(f"✅ OTP verified successfully for appointment {appointment_id}")
        return True

    # =========================================================
    # START VIDEO SESSION (ENHANCED)
    # =========================================================
    def start_video_session(self, appointment_id, otp):
        """
        Start video session by verifying OTP and updating status
        Returns True if successful, False otherwise
        """
        print(f"🎥 Starting video session for appointment {appointment_id}")
        
        if self.verify_otp(appointment_id, otp):
            # Additional session setup if needed
            return True
        return False

    # =========================================================
    # DOCTOR STARTS CALL (LEGACY METHOD)
    # =========================================================
    def verify_doctor_otp(self, appointment_id, otp):
        """Legacy method - use verify_otp instead"""
        return self.verify_otp(appointment_id, otp)

    # =========================================================
    # USER JOINS CALL
    # =========================================================
    def get_meeting_link(self, appointment_id):
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT meeting_link, otp_verified
        FROM appointments
        WHERE id=?
        """, (appointment_id,))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return {
            "meeting_link": row[0],
            "otp_verified": row[1]
        }

    # =========================================================
    # EMAIL DATA FETCH
    # =========================================================
    def get_email_details(self, appointment_id):
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_id, worker_id, user_name,
                   booking_date, time_slot, appointment_type
            FROM appointments WHERE id=?
        """, (appointment_id,))

        row = cursor.fetchone()
        if not row:
            conn.close()
            return None

        user_id, worker_id, user_name, date, time_slot, appt_type = row

        from config import USER_DB, WORKER_DB

        uconn = sqlite3.connect(USER_DB)
        ucur = uconn.cursor()
        ucur.execute("SELECT email FROM users WHERE id=?", (user_id,))
        user_email = ucur.fetchone()[0]
        uconn.close()

        wconn = sqlite3.connect(WORKER_DB)
        wcur = wconn.cursor()
        wcur.execute("SELECT email FROM workers WHERE id=?", (worker_id,))
        worker_email = wcur.fetchone()[0]
        wconn.close()

        conn.close()

        return {
            "user_name": user_name,
            "date": date,
            "time_slot": time_slot,
            "appointment_type": appt_type,
            "user_email": user_email,
            "worker_email": worker_email
        }
