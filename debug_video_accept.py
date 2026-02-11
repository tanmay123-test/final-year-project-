#!/usr/bin/env python3
"""
Debug script to test video consultation acceptance
"""

import requests
import json

API = "http://127.0.0.1:5000"

def test_video_acceptance():
    """Test accepting a video consultation"""
    
    # Test data - use an existing video appointment ID
    appointment_id = 9  # From the user's log
    
    print(f"🧪 Testing video consultation acceptance for appointment {appointment_id}")
    
    try:
        # Test the respond endpoint
        print(f"\n📡 Sending POST request to {API}/worker/respond")
        
        payload = {
            "appointment_id": appointment_id,
            "status": "accepted"
        }
        
        print(f"📦 Payload: {json.dumps(payload, indent=2)}")
        
        r = requests.post(f"{API}/worker/respond", json=payload)
        
        print(f"\n📊 Response Status: {r.status_code}")
        print(f"📋 Response Headers: {dict(r.headers)}")
        
        try:
            response_data = r.json()
            print(f"📄 Response Body: {json.dumps(response_data, indent=2)}")
        except:
            print(f"📄 Response Body (raw): {r.text}")
        
        if r.status_code == 200:
            print("\n✅ SUCCESS! Video consultation accepted")
        else:
            print(f"\n❌ FAILED! Status code: {r.status_code}")
            
    except Exception as e:
        print(f"❌ Network error: {e}")

def test_appointment_details():
    """Test getting appointment details"""
    
    appointment_id = 9
    
    print(f"\n🔍 Getting details for appointment {appointment_id}")
    
    try:
        r = requests.get(f"{API}/appointment/{appointment_id}")
        
        print(f"📊 Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            print(f"📄 Appointment: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Failed to get appointment: {r.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🐛 DEBUG: Video Consultation Acceptance Test")
    print("=" * 50)
    
    # Test appointment details first
    test_appointment_details()
    
    # Test acceptance
    test_video_acceptance()
