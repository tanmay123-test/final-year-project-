#!/usr/bin/env python3

import requests

API = "http://127.0.0.1:5000"

def test_current_subscription():
    """Test current subscription directly"""
    
    print("🔍 TESTING CURRENT SUBSCRIPTION DIRECTLY")
    print("="*60)
    
    worker_id = 4
    
    # Test current subscription API
    try:
        r = requests.get(f"{API}/api/subscription/current?worker_id={worker_id}")
        if r.status_code == 200:
            data = r.json()
            subscription = data.get("subscription")
            
            if subscription:
                print("✅ Current Subscription Found:")
                print(f"   Plan ID: {subscription.get('plan_id', 'N/A')}")
                print(f"   Plan Name: {subscription.get('plan_name', 'N/A')}")
                print(f"   Daily Limit: {subscription.get('daily_limit', 'N/A')}")
                print(f"   Status: {subscription.get('status', 'N/A')}")
                print(f"   End Date: {subscription.get('end_date', 'N/A')}")
            else:
                print("❌ No active subscription")
        else:
            print(f"❌ API Error: {r.status_code}")
            print(r.text)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_current_subscription()
