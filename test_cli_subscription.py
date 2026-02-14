#!/usr/bin/env python3

import requests

API = "http://127.0.0.1:5000"

def test_cli_subscription_flow():
    """Test the CLI subscription flow with expected output"""
    
    print("🧪 TESTING CLI SUBSCRIPTION FLOW")
    print("="*60)
    
    # Test 1: Get subscription plans
    print("📋 Step 1: Testing View Plans API")
    try:
        r = requests.get(f"{API}/api/subscription/plans")
        if r.status_code == 200:
            data = r.json()
            plans = data.get("plans", [])
            print("✅ API Response:")
            for plan in plans:
                print(f"   {plan['name']}: ₹{plan['price']}/month - {plan['daily_appointment_limit']}/day")
        else:
            print(f"❌ API Error: {r.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Get current subscription
    print(f"\n📊 Step 2: Testing Current Subscription API")
    try:
        worker_id = 4
        r = requests.get(f"{API}/api/subscription/current?worker_id={worker_id}")
        if r.status_code == 200:
            data = r.json()
            subscription = data.get("subscription")
            if subscription:
                print("✅ Current Subscription Found:")
                print(f"   Plan: {subscription['plan_name']}")
                print(f"   Daily Limit: {subscription['daily_limit']}")
                print(f"   Today's Usage: {subscription['today_usage']}")
                print(f"   Remaining: {subscription['remaining_today']}")
                print(f"   Is Trial: {subscription['is_trial']}")
            else:
                print("❌ No active subscription")
        else:
            print(f"❌ API Error: {r.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Get subscription stats
    print(f"\n📈 Step 3: Testing Stats API")
    try:
        r = requests.get(f"{API}/api/subscription/stats/{worker_id}")
        if r.status_code == 200:
            data = r.json()
            stats = data.get("stats")
            if stats:
                print("✅ Stats Found:")
                print(f"   Plan: {stats['plan_name']}")
                print(f"   End Date: {stats['end_date'][:10] if stats['end_date'] else 'N/A'}")
                print(f"   Daily Limit: {stats['daily_limit']}")
                print(f"   Today's Usage: {stats['today_usage']}")
                print(f"   Remaining: {stats['remaining_today']}")
            else:
                print("❌ No stats found")
        else:
            print(f"❌ API Error: {r.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎯 Expected CLI Output Format:")
    print("="*60)
    print("""
When you run the CLI now, you should see:

============================================================
💳 SUBSCRIPTION MANAGEMENT
============================================================

📋 Current Plan: Trial
📅 End Date: 2026-03-14
📝 Features: Basic appointment scheduling, Profile management

📊 Today's Usage: 0/3
🔄 Remaining Today: 3

------------------------------------------------------------
1. 📋 View Available Plans
2. 💳 Subscribe to Plan
3. 📊 View Usage Stats
4. ❌ Cancel Subscription
5. ⬅️ Back

Select option: 1

============================================================
📋 AVAILABLE SUBSCRIPTION PLANS
============================================================

[1] Basic Plan
💰 Price: ₹499/month
📅 Duration: 30 days
📊 Max Appointments/Day: 5
----------------------------------------
[2] Professional Plan
💰 Price: ₹999/month
📅 Duration: 30 days
📊 Max Appointments/Day: 15
----------------------------------------
[3] Enterprise Plan
💰 Price: ₹1999/month
📅 Duration: 30 days
📊 Max Appointments/Day: Unlimited
----------------------------------------
""")

if __name__ == "__main__":
    test_cli_subscription_flow()
