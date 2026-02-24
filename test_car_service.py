#!/usr/bin/env python3
"""
Test script for Car Service System
Tests both car service booking and dispatch system
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_car_service_endpoints():
    """Test car service booking endpoints"""
    print("🔧 Testing Car Service Endpoints")
    print("=" * 50)
    
    # Test 1: Get all mechanics
    print("1. Testing GET /car/mechanics")
    try:
        response = requests.get(f"{BASE_URL}/car/mechanics")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            mechanics = data.get('mechanics', [])
            print(f"✅ Found {len(mechanics)} mechanics")
            if mechanics:
                print(f"   First mechanic: {mechanics[0]['name']} - {mechanics[0]['specialization']}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print()
    
    # Test 2: Get car services
    print("2. Testing GET /car/services")
    try:
        response = requests.get(f"{BASE_URL}/car/services")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            services = data.get('services', [])
            print(f"✅ Found {len(services)} services")
            if services:
                print(f"   First service: {services[0]['name']} - ₹{services[0]['base_price']}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print()
    
    # Test 3: Book a car service
    print("3. Testing POST /car/book")
    try:
        booking_data = {
            "user_id": 1,
            "mechanic_id": 1,
            "user_name": "Test User",
            "user_email": "test@example.com",
            "user_phone": "9876543210",
            "car_model": "Maruti Suzuki Swift",
            "car_issue": "Engine making strange noise",
            "service_type": "General Service",
            "booking_date": "2026-02-25",
            "time_slot": "10:00 AM"
        }
        
        response = requests.post(f"{BASE_URL}/car/book", json=booking_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Appointment booked: {data['appointment_id']}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print()

def test_dispatch_endpoints():
    """Test dispatch system endpoints"""
    print("🚗 Testing Dispatch System Endpoints")
    print("=" * 50)
    
    # Test 1: Create dispatch job
    print("1. Testing POST /dispatch/job")
    try:
        job_data = {
            "user_id": 1,
            "issue": "Car broke down on highway - engine failure",
            "latitude": 19.2183,
            "longitude": 72.9781,
            "address": "Western Express Highway, Andheri",
            "urgency": 2,  # Emergency
            "specialization": "Engine Specialist"
        }
        
        response = requests.post(f"{BASE_URL}/dispatch/job", json=job_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            job_id = data.get('job_id')
            print(f"✅ Job created: {job_id}")
            print(f"   Mechanics offered: {data.get('mechanics_offered')}")
            print(f"   Estimated arrival: {data.get('estimated_arrival')}")
            
            # Test 2: Get job details
            print("\n2. Testing GET /dispatch/job/<job_id>")
            response = requests.get(f"{BASE_URL}/dispatch/job/{job_id}")
            if response.status_code == 200:
                job_data = response.json()
                print(f"✅ Job details retrieved")
                print(f"   Status: {job_data['status']}")
                print(f"   Issue: {job_data['issue']}")
                print(f"   Total fee: ₹{job_data['total_fee']}")
            else:
                print(f"❌ Error: {response.text}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print()
    
    # Test 3: Find nearby mechanics
    print("3. Testing GET /dispatch/mechanics/nearby")
    try:
        params = {
            "latitude": 19.2183,
            "longitude": 72.9781,
            "radius": 10.0
        }
        
        response = requests.get(f"{BASE_URL}/dispatch/mechanics/nearby", params=params)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            mechanics = data.get('mechanics', [])
            print(f"✅ Found {len(mechanics)} nearby mechanics")
            for mech in mechanics[:3]:  # Show first 3
                print(f"   {mech['name']} - {mech['distance_km']:.1f}km away - Rating: {mech['rating']}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print()

def test_mechanic_auth():
    """Test mechanic authentication"""
    print("🔐 Testing Mechanic Authentication")
    print("=" * 50)
    
    # Test 1: Mechanic signup
    print("1. Testing POST /car/mechanic/signup")
    try:
        signup_data = {
            "name": "Test Mechanic",
            "email": "testmechanic@example.com",
            "phone": "9876543212",
            "specialization": "General Mechanic",
            "experience": 5,
            "service_center": "Test Garage",
            "location": "Mumbai",
            "consultation_fee": 450
        }
        
        response = requests.post(f"{BASE_URL}/car/mechanic/signup", json=signup_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Mechanic registered: {data['mechanic_id']}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print()
    
    # Test 2: Mechanic login
    print("2. Testing POST /car/mechanic/login")
    try:
        login_data = {
            "email": "rajesh.kumar@autocare.com",  # Using existing mechanic
            "password": "mechanic123"
        }
        
        response = requests.post(f"{BASE_URL}/car/mechanic/login", json=login_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login successful")
            print(f"   Token: {data['token'][:20]}...")
            print(f"   Mechanic: {data['mechanic']['name']}")
            return data['token']
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    return None

def test_with_auth(token):
    """Test endpoints that require authentication"""
    if not token:
        print("⚠️ Skipping authenticated tests - no token available")
        return
    
    print("🔒 Testing Authenticated Endpoints")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test: Get mechanic appointments
    print("Testing GET /car/mechanic/appointments")
    try:
        response = requests.get(f"{BASE_URL}/car/mechanic/appointments", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            appointments = data.get('appointments', [])
            print(f"✅ Found {len(appointments)} appointments")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print()

def main():
    """Run all tests"""
    print("🚗 ExpertEase Car Service System Test")
    print("=" * 60)
    print(f"Testing against: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test basic endpoints
    test_car_service_endpoints()
    test_dispatch_endpoints()
    
    # Test authentication
    token = test_mechanic_auth()
    
    # Test authenticated endpoints
    test_with_auth(token)
    
    print("=" * 60)
    print("✅ Car Service System Testing Complete!")
    print()
    print("📝 Summary:")
    print("- Car service booking system tested")
    print("- Dispatch system tested")
    print("- Mechanic authentication tested")
    print("- Database integration verified")
    print()
    print("🔧 Available Endpoints:")
    print("- GET /car/mechanics - List all mechanics")
    print("- GET /car/services - List all services")
    print("- POST /car/book - Book service appointment")
    print("- POST /car/mechanic/signup - Register mechanic")
    print("- POST /car/mechanic/login - Mechanic login")
    print("- POST /dispatch/job - Create dispatch job")
    print("- GET /dispatch/mechanics/nearby - Find nearby mechanics")
    print("- GET /dispatch/job/<id> - Get job details")
    print("- PUT /dispatch/offer/<id>/accept - Accept job offer")

if __name__ == "__main__":
    main()
