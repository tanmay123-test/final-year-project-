#!/usr/bin/env python3

import requests
import json

API = "http://127.0.0.1:5000"

def test_appointment_acceptance_with_subscription():
    """Test appointment acceptance with subscription validation"""
    
    print("🧪 TESTING APPOINTMENT ACCEPTANCE WITH SUBSCRIPTION")
    print("="*60)
    
    # Step 1: Worker login
    print("🔐 Step 1: Worker Login")
    try:
        r = requests.post(f"{API}/worker/login", json={
            "email": "co2023.niharika.rothe@ves.ac.in"
        })
        
        if r.status_code == 200:
            worker_data = r.json()
            worker_id = worker_data.get("worker_id")
            print(f"✅ Worker login successful - ID: {worker_id}")
        else:
            print("❌ Worker login failed")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Step 2: Try to accept an appointment
    print(f"\n📋 Step 2: Accept Appointment with Subscription Check")
    
    # Get a pending appointment (you may need to adjust this)
    appointment_id = 7  # Use the appointment from your previous test
    
    try:
        r = requests.post(f"{API}/worker/respond", json={
            "appointment_id": appointment_id,
            "status": "accepted"
        })
        
        if r.status_code == 200:
            result = r.json()
            print("✅ Appointment accepted successfully!")
            print(f"   Payment Required: {result.get('payment_required', False)}")
            print(f"   Doctor Fee: ₹{result.get('doctor_fee', 'N/A')}")
        elif r.status_code == 402:
            error_data = r.json()
            print("❌ Appointment acceptance blocked by subscription:")
            print(f"   Error: {error_data.get('error')}")
            print(f"   Subscription Required: {error_data.get('subscription_required', False)}")
        else:
            print(f"❌ Unexpected response: {r.status_code}")
            print(r.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 3: Check subscription status after usage
    print(f"\n📊 Step 3: Check Updated Subscription Status")
    try:
        r = requests.get(f"{API}/api/subscription/current?worker_id={worker_id}")
        if r.status_code == 200:
            subscription = r.json().get("subscription")
            if subscription:
                print("✅ Updated subscription status:")
                print(f"   Plan: {subscription['plan_name']}")
                print(f"   Today's Usage: {subscription['today_usage']}")
                print(f"   Remaining: {subscription['remaining_today']}")
        else:
            print("❌ Failed to get subscription status")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎉 Appointment acceptance test completed!")

if __name__ == "__main__":
    test_appointment_acceptance_with_subscription()
