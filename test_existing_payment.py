#!/usr/bin/env python3

import requests

API = "http://127.0.0.1:5000"

def test_subscription_with_existing_payment():
    """Test subscription using your existing payment system"""
    
    print("💳 TESTING SUBSCRIPTION WITH YOUR PAYMENT SYSTEM")
    print("="*60)
    
    worker_id = 4
    
    # Step 1: Test your payment system directly
    print("📋 Step 1: Test Your Payment System")
    try:
        payment_data = {
            "amount": 99900,  # ₹999 in paise
            "booking_id": "test_subscription_123"
        }
        
        r = requests.post(f"{API}/payment/create-order", json=payment_data)
        
        if r.status_code == 200:
            payment_response = r.json()
            print("✅ Your Payment System Working!")
            print(f"   Order ID: {payment_response.get('order_id')}")
            print(f"   Amount: {payment_response.get('amount')}")
            print(f"   Key: {payment_response.get('key')}")
            
            # Show frontend URL
            frontend_url = f"http://127.0.0.1:5001/payment?order_id={payment_response.get('order_id')}&amount={payment_response.get('amount')}&key={payment_response.get('key')}"
            print(f"   Frontend URL: {frontend_url}")
            
        else:
            print(f"❌ Payment system error: {r.status_code}")
            print(r.json())
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 2: Test subscription order creation
    print(f"\n📋 Step 2: Create Subscription Order")
    try:
        r = requests.post(f"{API}/api/subscription/create-order", json={
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
            
            # Step 3: Create payment using your system
            print(f"\n💳 Step 3: Create Payment Using Your System")
            payment_data = {
                "amount": int(order.get('amount') * 100),  # Convert to paise
                "booking_id": f"subscription_{worker_id}_{order.get('order_id')}"
            }
            
            r_payment = requests.post(f"{API}/payment/create-order", json=payment_data)
            
            if r_payment.status_code == 200:
                payment_response = r_payment.json()
                print("✅ Payment Order Created!")
                print(f"   Payment Order ID: {payment_response.get('order_id')}")
                print(f"   Amount: {payment_response.get('amount')}")
                print(f"   Key: {payment_response.get('key')}")
                
                # Show the complete flow
                frontend_url = f"http://127.0.0.1:5001/payment?order_id={payment_response.get('order_id')}&amount={payment_response.get('amount')}&key={payment_response.get('key')}"
                
                print(f"\n🌐 Complete Payment Flow:")
                print(f"   1. CLI calls your payment API: {API}/payment/create-order")
                print(f"   2. Your system creates Razorpay order")
                print(f"   3. User visits your frontend: {frontend_url}")
                print(f"   4. User pays on your payment page")
                print(f"   5. Your system handles payment completion")
                print(f"   6. CLI confirms subscription activation")
                
            else:
                print(f"❌ Payment creation failed: {r_payment.status_code}")
                print(r_payment.json())
                
        else:
            print(f"❌ Subscription order failed: {r.status_code}")
            print(r.json())
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n🎯 Updated CLI Flow:")
    print("="*60)
    print("""
Now when you run CLI:

1. Select subscription plan
2. Confirm subscription (y/n): y
3. 💳 INITIATING PAYMENT
   🌐 Using your payment system...
   🔗 Payment API: http://127.0.0.1:5000/payment/create-order
   
4. ✅ Payment order created successfully!
   Payment Order ID: order_SFGaCd6ox6jvoU
   Amount: 99900
   Key: rzp_test_SEXZkBLNwP5IAF
   
5. 🌐 Opening payment page...
   🔗 Payment URL: http://127.0.0.1:5001/payment?order_id=order_SFGaCd6ox6jvoU&amount=99900&key=rzp_test_SEXZkBLNwP5IAF
   📱 Payment page opened in browser
   
6. 💡 Instructions:
   1. Complete payment on your payment page
   2. After payment, enter 'y' to confirm
   3. Or enter 'n' to cancel
   
7. ✅ Payment completed? (y/n): y
   💳 Enter Payment ID: razorpay_payment_1234567890
   ✅ Subscription created successfully!
   🎉 Upgraded to Professional Plan successfully!
""")

if __name__ == "__main__":
    test_subscription_with_existing_payment()
