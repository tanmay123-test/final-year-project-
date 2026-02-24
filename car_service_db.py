#!/usr/bin/env python3
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import bcrypt

class CarServiceDB:
    def __init__(self, db_path: str = "car_service/car_mechanics.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize car service database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Mechanics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mechanics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                specialization TEXT NOT NULL,
                experience INTEGER NOT NULL,
                service_center TEXT NOT NULL,
                location TEXT NOT NULL,
                rating REAL DEFAULT 0.0,
                consultation_fee INTEGER DEFAULT 400,
                status TEXT DEFAULT 'pending',
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                online_status TEXT DEFAULT 'offline'
            )
        ''')
        
        # Car services table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS car_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                estimated_duration TEXT NOT NULL,
                base_price INTEGER NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        
        # Car appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS car_appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mechanic_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                user_email TEXT NOT NULL,
                user_phone TEXT NOT NULL,
                car_model TEXT NOT NULL,
                car_issue TEXT NOT NULL,
                service_type TEXT NOT NULL,
                booking_date TEXT NOT NULL,
                time_slot TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                payment_status TEXT DEFAULT 'pending',
                payment_amount INTEGER DEFAULT 0,
                consultation_fee INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def register_mechanic(self, name: str, email: str, phone: str, specialization: str,
                         experience: int, service_center: str, location: str,
                         consultation_fee: int = 400, password: str = "mechanic123") -> int:
        """Register a new mechanic"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute('''
            INSERT INTO mechanics (name, email, phone, specialization, experience, 
                                 service_center, location, consultation_fee, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, specialization, experience, service_center, 
              location, consultation_fee, hashed_password))
        
        mechanic_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return mechanic_id
    
    def get_mechanics(self, status: str = "approved") -> List[Dict]:
        """Get all mechanics by status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, email, phone, specialization, experience, 
                   service_center, location, rating, consultation_fee, 
                   status, online_status
            FROM mechanics 
            WHERE status = ?
            ORDER BY rating DESC, experience DESC
        ''', (status,))
        
        mechanics = []
        for row in cursor.fetchall():
            mechanics.append({
                'id': row[0], 'name': row[1], 'email': row[2], 'phone': row[3],
                'specialization': row[4], 'experience': row[5], 
                'service_center': row[6], 'location': row[7], 'rating': row[8],
                'consultation_fee': row[9], 'status': row[10], 'online_status': row[11]
            })
        
        conn.close()
        return mechanics
    
    def get_mechanic_by_id(self, mechanic_id: int) -> Optional[Dict]:
        """Get mechanic by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, email, phone, specialization, experience, 
                   service_center, location, rating, consultation_fee, 
                   status, online_status
            FROM mechanics 
            WHERE id = ?
        ''', (mechanic_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0], 'name': row[1], 'email': row[2], 'phone': row[3],
                'specialization': row[4], 'experience': row[5], 
                'service_center': row[6], 'location': row[7], 'rating': row[8],
                'consultation_fee': row[9], 'status': row[10], 'online_status': row[11]
            }
        return None
    
    def update_mechanic_status(self, mechanic_id: int, status: str) -> bool:
        """Update mechanic status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE mechanics SET status = ? WHERE id = ?
        ''', (status, mechanic_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def update_online_status(self, mechanic_id: int, online_status: str) -> bool:
        """Update mechanic online status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE mechanics SET online_status = ? WHERE id = ?
        ''', (online_status, mechanic_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def get_car_services(self) -> List[Dict]:
        """Get all available car services"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, estimated_duration, base_price, category
            FROM car_services
            ORDER BY category, name
        ''')
        
        services = []
        for row in cursor.fetchall():
            services.append({
                'id': row[0], 'name': row[1], 'description': row[2],
                'estimated_duration': row[3], 'base_price': row[4], 'category': row[5]
            })
        
        conn.close()
        return services
    
    def book_appointment(self, user_id: int, mechanic_id: int, user_name: str,
                        user_email: str, user_phone: str, car_model: str,
                        car_issue: str, service_type: str, booking_date: str,
                        time_slot: str, consultation_fee: int) -> int:
        """Book a car service appointment"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get service price
        cursor.execute('''
            SELECT base_price FROM car_services WHERE name = ?
        ''', (service_type,))
        service_price = cursor.fetchone()
        base_price = service_price[0] if service_price else 400
        
        total_amount = base_price + consultation_fee
        
        cursor.execute('''
            INSERT INTO car_appointments 
            (user_id, mechanic_id, user_name, user_email, user_phone, 
             car_model, car_issue, service_type, booking_date, time_slot, 
             consultation_fee, payment_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, mechanic_id, user_name, user_email, user_phone,
              car_model, car_issue, service_type, booking_date, time_slot,
              consultation_fee, total_amount))
        
        appointment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return appointment_id
    
    def get_mechanic_appointments(self, mechanic_id: int) -> List[Dict]:
        """Get appointments for a specific mechanic"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_name, user_email, user_phone, car_model, 
                   car_issue, service_type, booking_date, time_slot, 
                   status, payment_status, payment_amount
            FROM car_appointments 
            WHERE mechanic_id = ?
            ORDER BY booking_date, time_slot
        ''', (mechanic_id,))
        
        appointments = []
        for row in cursor.fetchall():
            appointments.append({
                'id': row[0], 'user_name': row[1], 'user_email': row[2], 
                'user_phone': row[3], 'car_model': row[4], 'car_issue': row[5],
                'service_type': row[6], 'booking_date': row[7], 'time_slot': row[8],
                'status': row[9], 'payment_status': row[10], 'payment_amount': row[11]
            })
        
        conn.close()
        return appointments
    
    def update_appointment_status(self, appointment_id: int, status: str) -> bool:
        """Update appointment status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE car_appointments SET status = ? WHERE id = ?
        ''', (status, appointment_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def verify_mechanic_login(self, email: str, password: str) -> Optional[Dict]:
        """Verify mechanic login credentials"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, email, password, status FROM mechanics 
            WHERE email = ? AND status = 'approved'
        ''', (email,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row and bcrypt.checkpw(password.encode('utf-8'), row[4].encode('utf-8')):
            return {
                'id': row[0], 'name': row[1], 'email': row[2], 'status': row[3]
            }
        return None

# Initialize database instance
car_service_db = CarServiceDB()
