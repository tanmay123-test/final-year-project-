#!/usr/bin/env python3

import requests
import json

# Test appointment acceptance
API = "http://127.0.0.1:5000"

def test_accept_appointment():
    """Test accepting an appointment with payment flow"""
    
    # Test accepting appointment ID 12 (from your CLI session)
    appointment_id = 12
    
    print(f"🧪 Testing appointment acceptance for ID: {appointment_id}")
    
    try:
        # Send acceptance request
        response = requests.post(f"{API}/worker/respond", json={
            "appointment_id": appointment_id,
            "status": "accepted"
        })
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Acceptance successful!")
            
            if data.get('payment_required'):
                print("💰 Payment flow activated")
                print(f"📋 Doctor Fee: ₹{data.get('doctor_fee')}")
            else:
                print("📅 Regular acceptance flow")
        else:
            print("❌ Acceptance failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_accept_appointment()
