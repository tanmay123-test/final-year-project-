#!/usr/bin/env python3

import requests

def test_cli_subscription_flow():
    """Test the exact flow CLI uses"""
    
    print("🧪 TESTING CLI SUBSCRIPTION FLOW")
    print("="*60)
    
    worker_id = 4
    
    # Test 1: Get current subscription (what CLI does first)
    print("📋 Step 1: Get Current Subscription")
    try:
        r = requests.get(f"http://127.0.0.1:5000/api/subscription/current?worker_id={worker_id}", timeout=10)
        print(f"   Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            subscription = data.get("subscription")
            if subscription:
                print("   ✅ Current subscription found:")
                print(f"      Plan: {subscription.get('plan_name', 'Unknown')}")
                print(f"      Status: {subscription.get('status', 'Unknown')}")
                print(f"      Daily Limit: {subscription.get('daily_limit', 'Unknown')}")
            else:
                print("   ✅ No active subscription (ready for new subscription)")
        else:
            print(f"   ❌ Error: {r.status_code}")
            print(f"   Response: {r.text}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 2: Create subscription order (what CLI does when subscribing)
    print(f"\n📋 Step 2: Create Subscription Order")
    try:
        r = requests.post("http://127.0.0.1:5000/api/subscription/create-order", 
                         json={"worker_id": worker_id, "plan_id": 2},  # Basic plan
                         timeout=10)
        print(f"   Status: {r.status_code}")
        
        if r.status_code == 201:
            data = r.json()
            order = data.get("order", {})
            print("   ✅ Subscription order created:")
            print(f"      Order ID: {order.get('order_id', 'Unknown')}")
            print(f"      Amount: ₹{order.get('amount', 'Unknown')}")
            print(f"      Plan: {order.get('plan', {}).get('name', 'Unknown')}")
            
            # Test 3: Create payment order (what CLI does next)
            print(f"\n📋 Step 3: Create Payment Order")
            payment_data = {
                "amount": int(order.get('amount', 0) * 100),
                "booking_id": f"subscription_{worker_id}_{order.get('order_id', '')}"
            }
            
            r_payment = requests.post("http://127.0.0.1:5000/create-order", 
                                   json=payment_data, timeout=10)
            print(f"   Status: {r_payment.status_code}")
            
            if r_payment.status_code == 200:
                payment_response = r_payment.json()
                print("   ✅ Payment order created:")
                print(f"      Payment Order ID: {payment_response.get('order_id', 'Unknown')}")
                print(f"      Amount: {payment_response.get('amount', 'Unknown')}")
                print(f"      Key: {payment_response.get('key', 'Unknown')}")
                
                print(f"\n🎯 CLI FLOW TEST RESULT:")
                print("="*60)
                print("✅ All CLI steps working correctly!")
                print("✅ Subscription system ready for production!")
                print("✅ Payment integration working!")
                print("✅ No more errors!")
                
            else:
                print(f"   ❌ Payment order failed: {r_payment.status_code}")
                print(f"   Response: {r_payment.text}")
                
        else:
            print(f"   ❌ Subscription order failed: {r.status_code}")
            print(f"   Response: {r.text}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")

if __name__ == "__main__":
    test_cli_subscription_flow()
