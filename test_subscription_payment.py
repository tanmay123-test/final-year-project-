#!/usr/bin/env python3

import requests

API = "http://127.0.0.1:5000"

def test_subscription_payment_integration():
    """Test subscription payment integration with Razorpay"""
    
    print("💳 TESTING SUBSCRIPTION PAYMENT INTEGRATION")
    print("="*60)
    
    worker_id = 4
    
    # Step 1: Create subscription order
    print("📋 Step 1: Create Subscription Order")
    try:
        r = requests.post(f"{API}/api/subscription/create-order", json={
            "worker_id": worker_id,
            "plan_id": 3  # Professional plan
        })
        
        if r.status_code == 201:
            order_data = r.json()
            order = order_data.get("order", {})
            
            print("✅ Order Created Successfully!")
            print(f"   Order ID: {order.get('order_id')}")
            print(f"   Amount: ₹{order.get('amount')}")
            print(f"   Currency: {order.get('currency')}")
            print(f"   Razorpay Key: {order.get('key')}")
            print(f"   Plan: {order.get('plan', {}).get('name', 'Unknown')}")
            
            # Show payment URL
            payment_url = f"https://razorpay.com/payment/{order.get('order_id')}"
            print(f"\n🌐 Payment Gateway URL:")
            print(f"   {payment_url}")
            
            print(f"\n💡 Payment Integration Details:")
            print(f"   🔑 Razorpay Key: {order.get('key')}")
            print(f"   📋 Order ID: {order.get('order_id')}")
            print(f"   💰 Amount: {int(order.get('amount', 0) * 100)} paise")
            print(f"   📝 Receipt: subscription_{worker_id}_3_{int(__import__('datetime').datetime.now().timestamp())}")
            
            # Step 2: Show payment confirmation flow
            print(f"\n🔒 Payment Confirmation Flow:")
            print(f"   1. User visits: {payment_url}")
            print(f"   2. User pays ₹{order.get('amount')} via Razorpay")
            print(f"   3. Razorpay returns payment_id")
            print(f"   4. Backend confirms payment via API")
            print(f"   5. Subscription activated immediately")
            
            # Step 3: Simulate payment confirmation
            print(f"\n🧪 Simulating Payment Confirmation...")
            payment_id = f"razorpay_payment_{__import__('random').randint(1000000000, 9999999999)}"
            
            r_confirm = requests.post(f"{API}/api/subscription/confirm", json={
                "worker_id": worker_id,
                "order_id": order.get('order_id'),
                "payment_id": payment_id
            })
            
            if r_confirm.status_code == 200:
                confirm_data = r_confirm.json()
                print("✅ Payment Confirmed!")
                print(f"   Message: {confirm_data.get('message')}")
                print(f"   Payment ID: {payment_id}")
                
                # Check updated subscription
                r_current = requests.get(f"{API}/api/subscription/current?worker_id={worker_id}")
                if r_current.status_code == 200:
                    current_data = r_current.json()
                    subscription = current_data.get("subscription")
                    if subscription:
                        print(f"\n📊 Updated Subscription:")
                        print(f"   Plan: {subscription.get('plan_name')}")
                        print(f"   Daily Limit: {subscription.get('daily_limit')}")
                        print(f"   Status: {subscription.get('status')}")
            else:
                print("❌ Payment confirmation failed")
                print(r_confirm.json())
                
        else:
            print(f"❌ Order creation failed: {r.status_code}")
            print(r.json())
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n🎯 CLI Payment Flow:")
    print("="*60)
    print("""
When you run CLI now:

1. Select subscription plan
2. Confirm subscription (y/n): y
3. 💳 INITIATING PAYMENT
   📋 Order ID: order_SFGaCd6ox6jvoU
   💰 Amount: ₹999.0
   🔑 Razorpay Key: rzp_test_1234567890
   
4. 🌐 Opening payment gateway...
   🔗 Payment URL: https://razorpay.com/payment/order_SFGaCd6ox6jvoU
   📱 Payment page opened in browser
   
5. 💡 Instructions:
   1. Complete payment in browser
   2. After payment, enter 'y' to confirm
   3. Or enter 'n' to cancel
   
6. ✅ Payment completed? (y/n): y
   💳 Enter Payment ID: razorpay_payment_1234567890
   ✅ Subscription created successfully!
   🎉 Upgraded to Professional Plan successfully!
""")

if __name__ == "__main__":
    test_subscription_payment_integration()
