#!/usr/bin/env python3
import sqlite3
import os
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import math

class DispatchDB:
    def __init__(self, db_path: str = "dispatch_system.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize dispatch system database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Mechanics table for dispatch
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mechanics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                service_type TEXT DEFAULT 'MECHANIC',
                specialization TEXT NOT NULL,
                rating REAL DEFAULT 0.0,
                experience_years INTEGER DEFAULT 0,
                status TEXT DEFAULT 'OFFLINE',
                latitude REAL DEFAULT 0.0,
                longitude REAL DEFAULT 0.0,
                last_location_update TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Mechanic jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mechanic_jobs (
                id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                mechanic_id INTEGER,
                issue TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                address TEXT NOT NULL,
                service_type TEXT DEFAULT 'MECHANIC',
                urgency INTEGER DEFAULT 0,  -- 0: Normal, 1: Urgent, 2: Emergency
                status TEXT DEFAULT 'SEARCHING',  -- SEARCHING, ACCEPTED, ARRIVED, IN_PROGRESS, COMPLETED, CANCELLED
                base_fee REAL DEFAULT 0.0,
                distance_fee REAL DEFAULT 0.0,
                emergency_bonus REAL DEFAULT 0.0,
                total_fee REAL DEFAULT 0.0,
                platform_commission REAL DEFAULT 0.0,
                mechanic_earnings REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                accepted_at TEXT,
                arrived_at TEXT,
                started_work_at TEXT,
                completed_at TEXT,
                cancelled_at TEXT,
                cancellation_reason TEXT
            )
        ''')
        
        # Job offers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_offers (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                mechanic_id INTEGER NOT NULL,
                eta_minutes INTEGER NOT NULL,
                status TEXT DEFAULT 'PENDING',  -- PENDING, ACCEPTED, REJECTED, EXPIRED
                offered_at TEXT DEFAULT CURRENT_TIMESTAMP,
                responded_at TEXT,
                expires_at TEXT
            )
        ''')
        
        # Mechanic live locations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mechanic_live_locations (
                mechanic_id INTEGER PRIMARY KEY,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                address TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Job tracking logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_tracking_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT NOT NULL,
                mechanic_id INTEGER NOT NULL,
                latitude REAL,
                longitude REAL,
                eta_minutes INTEGER,
                event_type TEXT NOT NULL,  -- OFFER_SENT, ACCEPTED, ARRIVED, STARTED, COMPLETED
                logged_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Worker metrics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS worker_metrics (
                mechanic_id INTEGER PRIMARY KEY,
                total_jobs INTEGER DEFAULT 0,
                completed_jobs INTEGER DEFAULT 0,
                cancelled_jobs INTEGER DEFAULT 0,
                average_rating REAL DEFAULT 0.0,
                total_earnings REAL DEFAULT 0.0,
                acceptance_rate REAL DEFAULT 0.0,
                average_response_time INTEGER DEFAULT 0,  -- in seconds
                fairness_score REAL DEFAULT 1.0,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Worker wallet
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS worker_wallet (
                mechanic_id INTEGER PRIMARY KEY,
                current_balance REAL DEFAULT 0.0,
                total_earned REAL DEFAULT 0.0,
                total_withdrawn REAL DEFAULT 0.0,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Job proofs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_proofs (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                mechanic_id INTEGER NOT NULL,
                proof_type TEXT NOT NULL,  -- PHOTO, VIDEO, RECEIPT
                file_path TEXT NOT NULL,
                description TEXT,
                uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
                verified INTEGER DEFAULT 0
            )
        ''')
        
        # OTP sessions for job verification
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS otp_sessions (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                mechanic_id INTEGER NOT NULL,
                otp_code TEXT NOT NULL,
                generated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                expires_at TEXT NOT NULL,
                verified INTEGER DEFAULT 0,
                verified_at TEXT
            )
        ''')
        
        # Commission tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commission_tracking (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                mechanic_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                platform_commission REAL NOT NULL,
                mechanic_earnings REAL NOT NULL,
                commission_rate REAL NOT NULL,
                processed_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def register_mechanic(self, name: str, phone: str, email: str, 
                          specialization: str, experience_years: int = 0,
                          latitude: float = 0.0, longitude: float = 0.0) -> int:
        """Register a mechanic for dispatch"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO mechanics (name, phone, email, specialization, 
                                 experience_years, latitude, longitude, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'OFFLINE')
        ''', (name, phone, email, specialization, experience_years, latitude, longitude))
        
        mechanic_id = cursor.lastrowid
        
        # Initialize metrics and wallet
        cursor.execute('''
            INSERT INTO worker_metrics (mechanic_id) VALUES (?)
        ''', (mechanic_id,))
        
        cursor.execute('''
            INSERT INTO worker_wallet (mechanic_id) VALUES (?)
        ''', (mechanic_id,))
        
        conn.commit()
        conn.close()
        return mechanic_id
    
    def update_mechanic_location(self, mechanic_id: int, latitude: float, 
                               longitude: float, address: str = None) -> bool:
        """Update mechanic real-time location"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE mechanics 
            SET latitude = ?, longitude = ?, last_location_update = ?, updated_at = ?
            WHERE id = ?
        ''', (latitude, longitude, datetime.now().isoformat(), datetime.now().isoformat(), mechanic_id))
        
        cursor.execute('''
            INSERT OR REPLACE INTO mechanic_live_locations 
            (mechanic_id, latitude, longitude, address, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (mechanic_id, latitude, longitude, address, datetime.now().isoformat()))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def create_job(self, user_id: int, issue: str, latitude: float, longitude: float,
                   address: str, service_type: str = 'MECHANIC', urgency: int = 0) -> str:
        """Create a new mechanic job"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        job_id = str(uuid.uuid4())
        
        # Calculate pricing
        base_fee = 200.0  # Base service fee
        emergency_bonus = urgency * 100.0  # Urgency bonus
        
        cursor.execute('''
            INSERT INTO mechanic_jobs 
            (id, user_id, issue, latitude, longitude, address, 
             service_type, urgency, base_fee, emergency_bonus)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (job_id, user_id, issue, latitude, longitude, address,
              service_type, urgency, base_fee, emergency_bonus))
        
        conn.commit()
        conn.close()
        return job_id
    
    def find_nearby_mechanics(self, latitude: float, longitude: float, 
                             radius_km: float = 10.0, specialization: str = None) -> List[Dict]:
        """Find nearby available mechanics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT id, name, phone, email, specialization, rating, 
                   experience_years, latitude, longitude, status
            FROM mechanics 
            WHERE status = 'ONLINE'
        '''
        params = []
        
        if specialization:
            query += ' AND specialization = ?'
            params.append(specialization)
        
        cursor.execute(query, params)
        mechanics = []
        
        for row in cursor.fetchall():
            # Calculate distance
            mech_lat, mech_lon = row[7], row[8]
            distance = self.calculate_distance(latitude, longitude, mech_lat, mech_lon)
            
            if distance <= radius_km:
                mechanics.append({
                    'id': row[0], 'name': row[1], 'phone': row[2], 'email': row[3],
                    'specialization': row[4], 'rating': row[5], 
                    'experience_years': row[6], 'latitude': row[7], 
                    'longitude': row[8], 'status': row[9], 'distance_km': distance
                })
        
        conn.close()
        
        # Sort by distance and rating
        mechanics.sort(key=lambda x: (x['distance_km'], -x['rating']))
        return mechanics
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates in kilometers"""
        R = 6371.0  # Earth radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def offer_job_to_mechanics(self, job_id: str, mechanics: List[Dict]) -> List[str]:
        """Offer job to multiple mechanics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        offer_ids = []
        expires_at = (datetime.now() + timedelta(minutes=5)).isoformat()
        
        for mechanic in mechanics:
            offer_id = str(uuid.uuid4())
            eta_minutes = self.calculate_eta(mechanic['latitude'], mechanic['longitude'])
            
            cursor.execute('''
                INSERT INTO job_offers 
                (id, job_id, mechanic_id, eta_minutes, expires_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (offer_id, job_id, mechanic['id'], eta_minutes, expires_at))
            
            offer_ids.append(offer_id)
        
        conn.commit()
        conn.close()
        return offer_ids
    
    def calculate_eta(self, mechanic_lat: float, mechanic_lon: float, 
                     job_lat: float = None, job_lon: float = None) -> int:
        """Calculate ETA in minutes (simplified)"""
        # For now, return a simple estimate based on average speed
        if job_lat and job_lon:
            distance = self.calculate_distance(mechanic_lat, mechanic_lon, job_lat, job_lon)
            # Assuming average speed of 30 km/h in city
            eta_minutes = int((distance / 30) * 60)
        else:
            eta_minutes = 15  # Default 15 minutes
        
        return max(5, eta_minutes)  # Minimum 5 minutes
    
    def accept_job_offer(self, offer_id: str, mechanic_id: int) -> bool:
        """Accept a job offer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get job details
            cursor.execute('''
                SELECT job_id FROM job_offers 
                WHERE id = ? AND mechanic_id = ? AND status = 'PENDING'
            ''', (offer_id, mechanic_id))
            
            result = cursor.fetchone()
            if not result:
                conn.close()
                return False
            
            job_id = result[0]
            
            # Update offer status
            cursor.execute('''
                UPDATE job_offers 
                SET status = 'ACCEPTED', responded_at = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), offer_id))
            
            # Reject other offers for this job
            cursor.execute('''
                UPDATE job_offers 
                SET status = 'REJECTED', responded_at = ?
                WHERE job_id = ? AND id != ? AND status = 'PENDING'
            ''', (datetime.now().isoformat(), job_id, offer_id))
            
            # Update job status
            cursor.execute('''
                UPDATE mechanic_jobs 
                SET mechanic_id = ?, status = 'ACCEPTED', accepted_at = ?
                WHERE id = ?
            ''', (mechanic_id, datetime.now().isoformat(), job_id))
            
            # Calculate final pricing
            self.calculate_job_pricing(job_id, mechanic_id, cursor)
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            conn.close()
            return False
    
    def calculate_job_pricing(self, job_id: str, mechanic_id: int, cursor):
        """Calculate final job pricing with commission"""
        # Get job details
        cursor.execute('''
            SELECT base_fee, distance_fee, emergency_bonus 
            FROM mechanic_jobs WHERE id = ?
        ''', (job_id,))
        
        job_details = cursor.fetchone()
        if not job_details:
            return
        
        base_fee, distance_fee, emergency_bonus = job_details
        
        # Get mechanic rating for commission calculation
        cursor.execute('''
            SELECT rating FROM mechanics WHERE id = ?
        ''', (mechanic_id,))
        
        rating_result = cursor.fetchone()
        rating = rating_result[0] if rating_result else 4.0
        
        # Commission rates based on rating
        if rating >= 4.5:
            commission_rate = 0.15  # 15% for top rated
        elif rating >= 4.0:
            commission_rate = 0.20  # 20% for good rating
        else:
            commission_rate = 0.25  # 25% for others
        
        total_amount = base_fee + distance_fee + emergency_bonus
        platform_commission = total_amount * commission_rate
        mechanic_earnings = total_amount - platform_commission
        
        # Update job with pricing
        cursor.execute('''
            UPDATE mechanic_jobs 
            SET total_fee = ?, platform_commission = ?, mechanic_earnings = ?
            WHERE id = ?
        ''', (total_amount, platform_commission, mechanic_earnings, job_id))
        
        # Track commission
        commission_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO commission_tracking 
            (id, job_id, mechanic_id, total_amount, platform_commission, 
             mechanic_earnings, commission_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (commission_id, job_id, mechanic_id, total_amount, 
              platform_commission, mechanic_earnings, commission_rate))
    
    def get_job_details(self, job_id: str) -> Optional[Dict]:
        """Get detailed job information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT j.id, j.user_id, j.mechanic_id, j.issue, j.latitude, j.longitude,
                   j.address, j.service_type, j.urgency, j.status, j.base_fee,
                   j.distance_fee, j.emergency_bonus, j.total_fee, j.platform_commission,
                   j.mechanic_earnings, j.created_at, j.accepted_at, j.arrived_at,
                   j.started_work_at, j.completed_at,
                   m.name as mechanic_name, m.phone as mechanic_phone, m.specialization
            FROM mechanic_jobs j
            LEFT JOIN mechanics m ON j.mechanic_id = m.id
            WHERE j.id = ?
        ''', (job_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0], 'user_id': row[1], 'mechanic_id': row[2],
                'issue': row[3], 'latitude': row[4], 'longitude': row[5],
                'address': row[6], 'service_type': row[7], 'urgency': row[8],
                'status': row[9], 'base_fee': row[10], 'distance_fee': row[11],
                'emergency_bonus': row[12], 'total_fee': row[13],
                'platform_commission': row[14], 'mechanic_earnings': row[15],
                'created_at': row[16], 'accepted_at': row[17], 'arrived_at': row[18],
                'started_work_at': row[19], 'completed_at': row[20],
                'mechanic_name': row[21], 'mechanic_phone': row[22],
                'mechanic_specialization': row[23]
            }
        return None
    
    def update_job_status(self, job_id: str, status: str, mechanic_id: int = None) -> bool:
        """Update job status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        if status == 'ARRIVED':
            cursor.execute('''
                UPDATE mechanic_jobs SET status = ?, arrived_at = ? WHERE id = ?
            ''', (status, timestamp, job_id))
        elif status == 'IN_PROGRESS':
            cursor.execute('''
                UPDATE mechanic_jobs SET status = ?, started_work_at = ? WHERE id = ?
            ''', (status, timestamp, job_id))
        elif status == 'COMPLETED':
            cursor.execute('''
                UPDATE mechanic_jobs SET status = ?, completed_at = ? WHERE id = ?
            ''', (status, timestamp, job_id))
            
            # Update mechanic metrics and wallet
            if mechanic_id:
                self.update_mechanic_metrics(mechanic_id, cursor)
                self.update_mechanic_wallet(mechanic_id, job_id, cursor)
        else:
            cursor.execute('''
                UPDATE mechanic_jobs SET status = ? WHERE id = ?
            ''', (status, job_id))
        
        # Log the status change
        cursor.execute('''
            INSERT INTO job_tracking_logs 
            (job_id, mechanic_id, event_type, logged_at)
            VALUES (?, ?, ?, ?)
        ''', (job_id, mechanic_id, status, timestamp))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def update_mechanic_metrics(self, mechanic_id: int, cursor):
        """Update mechanic performance metrics"""
        # Get job counts
        cursor.execute('''
            SELECT 
                COUNT(*) as total_jobs,
                SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) as completed_jobs,
                SUM(CASE WHEN status = 'CANCELLED' THEN 1 ELSE 0 END) as cancelled_jobs
            FROM mechanic_jobs WHERE mechanic_id = ?
        ''', (mechanic_id,))
        
        job_stats = cursor.fetchone()
        
        # Calculate acceptance rate
        cursor.execute('''
            SELECT 
                COUNT(*) as total_offers,
                SUM(CASE WHEN status = 'ACCEPTED' THEN 1 ELSE 0 END) as accepted_offers
            FROM job_offers WHERE mechanic_id = ?
        ''', (mechanic_id,))
        
        offer_stats = cursor.fetchone()
        
        total_offers, accepted_offers = offer_stats
        acceptance_rate = (accepted_offers / total_offers) if total_offers > 0 else 0.0
        
        # Update metrics
        cursor.execute('''
            UPDATE worker_metrics 
            SET total_jobs = ?, completed_jobs = ?, cancelled_jobs = ?,
                acceptance_rate = ?, last_updated = ?
            WHERE mechanic_id = ?
        ''', (job_stats[0], job_stats[1], job_stats[2], 
              acceptance_rate, datetime.now().isoformat(), mechanic_id))
    
    def update_mechanic_wallet(self, mechanic_id: int, job_id: str, cursor):
        """Update mechanic wallet after job completion"""
        cursor.execute('''
            SELECT mechanic_earnings FROM mechanic_jobs 
            WHERE id = ? AND mechanic_id = ? AND status = 'COMPLETED'
        ''', (job_id, mechanic_id))
        
        earnings = cursor.fetchone()
        if earnings and earnings[0] > 0:
            cursor.execute('''
                UPDATE worker_wallet 
                SET current_balance = current_balance + ?,
                    total_earned = total_earned + ?,
                    last_updated = ?
                WHERE mechanic_id = ?
            ''', (earnings[0], earnings[0], datetime.now().isoformat(), mechanic_id))
    
    def get_mechanic_jobs(self, mechanic_id: int, status: str = None) -> List[Dict]:
        """Get jobs for a specific mechanic"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT id, user_id, issue, latitude, longitude, address, 
                   service_type, urgency, status, total_fee, mechanic_earnings,
                   created_at, accepted_at, arrived_at, started_work_at, completed_at
            FROM mechanic_jobs 
            WHERE mechanic_id = ?
        '''
        params = [mechanic_id]
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        query += ' ORDER BY created_at DESC'
        
        cursor.execute(query, params)
        
        jobs = []
        for row in cursor.fetchall():
            jobs.append({
                'id': row[0], 'user_id': row[1], 'issue': row[2],
                'latitude': row[3], 'longitude': row[4], 'address': row[5],
                'service_type': row[6], 'urgency': row[7], 'status': row[8],
                'total_fee': row[9], 'mechanic_earnings': row[10],
                'created_at': row[11], 'accepted_at': row[12], 'arrived_at': row[13],
                'started_work_at': row[14], 'completed_at': row[15]
            })
        
        conn.close()
        return jobs
    
    def get_mechanic_wallet(self, mechanic_id: int) -> Optional[Dict]:
        """Get mechanic wallet information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT current_balance, total_earned, total_withdrawn, last_updated
            FROM worker_wallet WHERE mechanic_id = ?
        ''', (mechanic_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'current_balance': row[0], 'total_earned': row[1],
                'total_withdrawn': row[2], 'last_updated': row[3]
            }
        return None

# Initialize database instance
dispatch_db = DispatchDB()
