#!/usr/bin/env python3

import requests

API = "http://127.0.0.1:5000"

def test_subscription_upgrade():
    """Test subscription upgrade functionality"""
    
    print("🔄 TESTING SUBSCRIPTION UPGRADE FUNCTIONALITY")
    print("="*60)
    
    worker_id = 4
    
    # Step 1: Check current subscription
    print("📊 Step 1: Current Subscription Status")
    try:
        r = requests.get(f"{API}/api/subscription/current?worker_id={worker_id}")
        if r.status_code == 200:
            data = r.json()
            subscription = data.get("subscription")
            if subscription:
                print("✅ Current Subscription:")
                print(f"   Plan: {subscription['plan_name']}")
                print(f"   Daily Limit: {subscription['daily_limit']}")
                print(f"   Today's Usage: {subscription['today_usage']}")
                print(f"   Remaining: {subscription['remaining_today']}")
                print(f"   End Date: {subscription['end_date'][:10] if subscription['end_date'] else 'N/A'}")
        else:
            print("❌ No active subscription")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 2: Try to upgrade to Basic plan
    print(f"\n💳 Step 2: Upgrade to Basic Plan")
    try:
        r = requests.post(f"{API}/api/subscription/create-order", json={
            "worker_id": worker_id,
            "plan_id": 2  # Basic plan
        })
        
        if r.status_code == 201:
            order_data = r.json()
            order = order_data.get("order", {})
            print("✅ Upgrade Order Created:")
            print(f"   Order ID: {order.get('order_id')}")
            print(f"   Amount: ₹{order.get('amount')}")
            print(f"   Plan: {order.get('plan', {}).get('name', 'Unknown')}")
            
            # Simulate payment confirmation
            payment_id = f"UPGRADE_{worker_id}_{int(time.time())}"
            
            r_confirm = requests.post(f"{API}/api/subscription/confirm", json={
                "worker_id": worker_id,
                "order_id": order.get('order_id'),
                "payment_id": payment_id
            })
            
            if r_confirm.status_code == 200:
                confirm_data = r_confirm.json()
                print("✅ Upgrade Successful!")
                print(f"   Message: {confirm_data.get('message')}")
                
                # Check updated subscription
                r_updated = requests.get(f"{API}/api/subscription/current?worker_id={worker_id}")
                if r_updated.status_code == 200:
                    updated_data = r_updated.json()
                    updated_sub = updated_data.get("subscription")
                    if updated_sub:
                        print("📊 Updated Subscription:")
                        print(f"   New Plan: {updated_sub['plan_name']}")
                        print(f"   New Daily Limit: {updated_sub['daily_limit']}")
                        print(f"   End Date: {updated_sub['end_date'][:10] if updated_sub['end_date'] else 'N/A'}")
            else:
                print("❌ Upgrade Payment Failed")
        elif r.status_code == 400:
            error_data = r.json()
            print(f"❌ Upgrade Failed: {error_data.get('error')}")
        else:
            print(f"❌ Unexpected Error: {r.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 3: Test appointment acceptance with new limits
    print(f"\n📋 Step 3: Test Appointment Acceptance with New Limits")
    try:
        r = requests.get(f"{API}/api/subscription/check-eligibility/{worker_id}")
        if r.status_code == 200:
            eligibility = r.json()
            if eligibility['eligible']:
                print("✅ Eligible for Appointments:")
                print(f"   Daily Limit: {eligibility['subscription']['daily_limit']}")
                print(f"   Can Accept: YES")
            else:
                print("❌ Not Eligible:")
                print(f"   Error: {eligibility.get('error')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎯 Expected CLI Upgrade Flow:")
    print("="*60)
    print("""
When you run CLI now with active trial:

1. Go to Subscription Menu → Option 2 (Subscribe)
2. Choose Basic Plan → Confirm: y
3. Payment order created → Payment confirmed
4. ✅ Upgraded to Basic Plan successfully!
5. New daily limit: 5 appointments/day
6. Can accept more appointments immediately!

This allows users to UPGRADE anytime without waiting for trial to expire!
""")

if __name__ == "__main__":
    import time
    test_subscription_upgrade()
