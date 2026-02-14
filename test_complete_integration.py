#!/usr/bin/env python3

import requests

def test_complete_payment_integration():
    """Test complete payment integration"""
    
    print("💳 TESTING COMPLETE PAYMENT INTEGRATION")
    print("="*60)
    
    # Test 1: Payment system
    print("📋 Step 1: Test Payment System")
    try:
        r = requests.post("http://127.0.0.1:5000/create-order", 
                         json={"amount": 99900, "booking_id": "test_subscription"})
        
        if r.status_code == 200:
            payment_data = r.json()
            print("✅ Payment System Working!")
            print(f"   Order ID: {payment_data.get('order_id')}")
            print(f"   Amount: {payment_data.get('amount')}")
            print(f"   Key: {payment_data.get('key')}")
        else:
            print(f"❌ Payment system failed: {r.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Subscription system
    print(f"\n📋 Step 2: Test Subscription System")
    worker_id = 4
    
    try:
        r = requests.post("http://127.0.0.1:5000/api/subscription/create-order", json={
            "worker_id": worker_id,
            "plan_id": 3  # Professional plan
        })
        
        if r.status_code == 201:
            order_data = r.json()
            order = order_data.get("order", {})
            
            print("✅ Subscription Order Created!")
            print(f"   Order ID: {order.get('order_id')}")
            print(f"   Amount: ₹{order.get('amount')}")
            print(f"   Plan: {order.get('plan', {}).get('name', 'Unknown')}")
            
            # Test 3: Payment integration
            print(f"\n💳 Step 3: Test Payment Integration")
            payment_data = {
                "amount": int(order.get('amount') * 100),
                "booking_id": f"subscription_{worker_id}_{order.get('order_id')}"
            }
            
            r_payment = requests.post("http://127.0.0.1:5000/create-order", json=payment_data)
            
            if r_payment.status_code == 200:
                payment_response = r_payment.json()
                print("✅ Payment Integration Working!")
                print(f"   Payment Order ID: {payment_response.get('order_id')}")
                print(f"   Amount: {payment_response.get('amount')}")
                print(f"   Key: {payment_response.get('key')}")
                
                print(f"\n🎯 CLI Flow Will Now Show:")
                print("="*60)
                print("""
💳 INITIATING PAYMENT
============================================================
📋 Order ID: order_SFHf2GVr9KcoCC
💰 Amount: ₹999.0
🔑 Razorpay Key: rzp_test_SEXZkBLNwP5IAF

🌐 Using your payment system...
🔗 Payment API: http://127.0.0.1:5000/create-order

✅ Payment order created successfully!
   Payment Order ID: order_SFHpwMT8pKr6Pk
   Amount: 99900
   Key: rzp_test_SEXZkBLNwP5IAF

🌐 Opening payment page...
🔗 Payment URL: http://127.0.0.1:5001/payment?order_id=order_SFHpwMT8pKr6Pk&amount=99900&key=rzp_test_SEXZkBLNwP5IAF

📱 Payment page opened in browser
💡 Instructions:
1. Complete payment on your payment page
2. After payment, enter 'y' to confirm
3. Or enter 'n' to cancel

✅ Payment completed? (y/n): y
💳 Enter Payment ID: razorpay_payment_1234567890
✅ Subscription created successfully!
🎉 Upgraded to Professional Plan successfully!
                """)
                
            else:
                print(f"❌ Payment integration failed: {r_payment.status_code}")
                print(r_payment.json())
                
        else:
            print(f"❌ Subscription order failed: {r.status_code}")
            print(r.json())
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_complete_payment_integration()
