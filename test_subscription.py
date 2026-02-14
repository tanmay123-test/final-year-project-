#!/usr/bin/env python3

import requests
import json
import sys

API = "http://127.0.0.1:5000"

def test_subscription_system():
    """Test the complete subscription system"""
    
    print("🧪 TESTING SUBSCRIPTION SYSTEM")
    print("="*60)
    
    # Step 1: Test getting subscription plans
    print("📋 Step 1: Get Available Plans")
    try:
        r = requests.get(f"{API}/api/subscription/plans")
        if r.status_code == 200:
            plans = r.json().get("plans", [])
            print("✅ Plans retrieved successfully:")
            for plan in plans:
                print(f"   {plan['name']}: ₹{plan['price']}/month - {plan['daily_appointment_limit']} appointments/day")
        else:
            print("❌ Failed to get plans")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Step 2: Test worker login to get worker_id
    print("\n🔐 Step 2: Worker Login")
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
    
    # Step 3: Test current subscription status
    print(f"\n📊 Step 3: Check Current Subscription (Worker {worker_id})")
    try:
        r = requests.get(f"{API}/api/subscription/current?worker_id={worker_id}")
        if r.status_code == 200:
            subscription = r.json().get("subscription")
            if subscription:
                print("✅ Active subscription found:")
                print(f"   Plan: {subscription['plan_name']}")
                print(f"   Daily Limit: {subscription['daily_limit']}")
                print(f"   Today's Usage: {subscription['today_usage']}")
                print(f"   Remaining: {subscription['remaining_today']}")
                print(f"   Is Trial: {subscription['is_trial']}")
            else:
                print("❌ No active subscription")
        else:
            print("❌ Failed to get subscription status")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 4: Test subscription eligibility
    print(f"\n🔍 Step 4: Check Subscription Eligibility")
    try:
        r = requests.get(f"{API}/api/subscription/check-eligibility/{worker_id}")
        if r.status_code == 200:
            eligibility = r.json()
            if eligibility['eligible']:
                print("✅ Worker is eligible to accept appointments")
            else:
                print(f"❌ Worker not eligible: {eligibility['error']}")
        else:
            print("❌ Failed to check eligibility")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 5: Test creating subscription order (if no active subscription)
    print(f"\n💳 Step 5: Create Subscription Order")
    try:
        # Get Basic plan (id=2)
        r = requests.post(f"{API}/api/subscription/create-order", json={
            "worker_id": worker_id,
            "plan_id": 2  # Basic plan
        })
        
        if r.status_code == 201:
            order = r.json().get("order", {})
            print("✅ Subscription order created:")
            print(f"   Order ID: {order['order_id']}")
            print(f"   Amount: ₹{order['amount']}")
            print(f"   Plan: {order['plan']['name']}")
        elif r.status_code == 400:
            error = r.json().get("error", "Unknown error")
            print(f"⚠️ Order creation failed: {error}")
        else:
            print("❌ Failed to create order")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 6: Test usage tracking
    print(f"\n📈 Step 6: Track Appointment Usage")
    try:
        r = requests.post(f"{API}/api/subscription/track-usage", json={
            "worker_id": worker_id
        })
        
        if r.status_code == 200:
            result = r.json()
            if result['success']:
                print("✅ Usage tracked successfully")
            else:
                print(f"⚠️ Usage tracking failed: {result['message']}")
        else:
            print("❌ Failed to track usage")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎉 Subscription system test completed!")

if __name__ == "__main__":
    test_subscription_system()
