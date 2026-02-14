#!/usr/bin/env python3

import requests

API = "http://127.0.0.1:5000"

def test_user_appointments():
    """Test user appointments API"""
    
    print("🔍 TESTING USER APPOINTMENTS API")
    print("="*60)
    
    # First login as Sarthy
    print("📋 STEP 1: LOGIN AS SARTHY")
    try:
        login_data = {
            "username": "Sarthy",
            "password": "890"
        }
        
        r = requests.post(f"{API}/login", json=login_data, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            token = data.get("token")
            user_id = data.get("user_id")
            
            print(f"✅ Login successful!")
            print(f"👤 User ID: {user_id}")
            print(f"🔑 Token: {token[:20]}...")
            
        else:
            print(f"❌ Login failed: {r.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test user appointments API
    print(f"\n📋 STEP 2: GET USER APPOINTMENTS")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(f"{API}/user/appointments", headers=headers, timeout=10)
        
        print(f"📊 Status Code: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            appointments = data.get("appointments", [])
            
            print(f"✅ Found {len(appointments)} appointments:")
            
            for i, apt in enumerate(appointments, 1):
                print(f"\n🏥 Appointment #{i}:")
                print(f"   📋 ID: {apt.get('id')}")
                print(f"   👨‍⚕️ Worker ID: {apt.get('worker_id')}")
                print(f"   📅 Date: {apt.get('booking_date')}")
                print(f"   🩺 Symptoms: {apt.get('patient_symptoms')}")
                print(f"   📝 Type: {apt.get('appointment_type')}")
                print(f"   📋 Status: {apt.get('status')}")
                print(f"   💰 Payment: {apt.get('payment_status', 'N/A')}")
                
        else:
            print(f"❌ API call failed: {r.status_code}")
            print(f"Response: {r.text}")
            
    except Exception as e:
        print(f"❌ API call error: {e}")
    
    print(f"\n🎯 TEST COMPLETE")

if __name__ == "__main__":
    test_user_appointments()
