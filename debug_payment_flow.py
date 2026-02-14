#!/usr/bin/env python3

import requests
import json

def debug_payment_flow():
    """Debug the payment flow to identify the exact issue"""
    
    print("🔍 DEBUGGING PAYMENT FLOW")
    print("="*60)
    
    API = "http://127.0.0.1:5000"
    
    # Test 1: Check if main app is running
    print("📋 STEP 1: CHECK MAIN APP")
    try:
        r = requests.get(f"{API}/", timeout=5)
        print(f"✅ Main app: {r.status_code}")
    except Exception as e:
        print(f"❌ Main app error: {e}")
        return
    
    # Test 2: Test payment order creation
    print(f"\n📋 STEP 2: TEST PAYMENT ORDER CREATION")
    try:
        order_data = {"appointment_id": "19"}
        
        r = requests.post(f"{API}/api/payment/create-order", 
                         json=order_data, timeout=10)
        
        print(f"📊 Status: {r.status_code}")
        print(f"📄 Response: {r.text}")
        
        if r.status_code == 200:
            data = r.json()
            print("✅ Payment order created!")
            print(f"📋 Order ID: {data.get('order_id')}")
            print(f"💰 Amount: ₹{data.get('amount')}")
            
            # Test 3: Test payment confirmation
            print(f"\n📋 STEP 3: TEST PAYMENT CONFIRMATION")
            payment_data = {
                "appointment_id": "19",
                "razorpay_payment_id": "pay_test_123456789"
            }
            
            r_confirm = requests.post(f"{API}/api/payment/confirm", 
                                   json=payment_data, timeout=10)
            
            print(f"📊 Confirmation Status: {r_confirm.status_code}")
            print(f"📄 Confirmation Response: {r_confirm.text}")
            
            if r_confirm.status_code == 200:
                print("✅ Payment confirmation working!")
            else:
                print("❌ Payment confirmation failed")
                
        else:
            print("❌ Payment order creation failed")
            
    except Exception as e:
        print(f"❌ Payment test error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Check payment status
    print(f"\n📋 STEP 4: CHECK PAYMENT STATUS")
    try:
        r = requests.get(f"{API}/api/payment/status/19", timeout=5)
        print(f"📊 Status: {r.status_code}")
        print(f"📄 Response: {r.text}")
    except Exception as e:
        print(f"❌ Status check error: {e}")
    
    print(f"\n🎯 DEBUGGING COMPLETE")
    print("="*60)

if __name__ == "__main__":
    debug_payment_flow()
