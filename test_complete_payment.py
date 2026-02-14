#!/usr/bin/env python3

import requests
import json

def create_fresh_appointment():
    """Create a fresh appointment for payment testing"""
    
    print("🆕 CREATING FRESH APPOINTMENT FOR PAYMENT TESTING")
    print("="*60)
    
    API = "http://127.0.0.1:5000"
    
    # First, login to get token
    print("📋 STEP 1: GET USER TOKEN")
    login_data = {
        "username": "Sarthy",
        "password": "890"
    }
    
    try:
        r = requests.post(f"{API}/login", json=login_data, timeout=10)
        if r.status_code == 200:
            token = r.json().get("token")
            print(f"✅ User token: {token[:20]}...")
        else:
            print(f"❌ Login failed: {r.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Create new video appointment
    print(f"\n📋 STEP 2: CREATE VIDEO APPOINTMENT")
    appointment_data = {
        "user_id": "6",
        "worker_id": "4", 
        "user_name": "Sarthy",
        "symptoms": "Payment testing video consultation",
        "appointment_type": "video",
        "booking_date": "2026-02-14",
        "time_slot": "15:00"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        r = requests.post(f"{API}/appointment/video-request", 
                         json=appointment_data, headers=headers, timeout=10)
        
        print(f"📊 Status: {r.status_code}")
        print(f"📄 Response: {r.text}")
        
        if r.status_code == 201:
            data = r.json()
            print("✅ Fresh appointment created!")
            print(f"📋 Appointment ID: {data.get('appointment_id')}")
            print(f"🩺 Type: Video Consultation")
            print(f"💰 Status: pending (ready for payment)")
            
            appointment_id = data.get('appointment_id')
            
            # Test payment flow
            print(f"\n📋 STEP 3: TEST PAYMENT FLOW")
            order_data = {"appointment_id": appointment_id}
            
            r = requests.post(f"{API}/api/payment/create-order", 
                             json=order_data, timeout=10)
            
            print(f"📊 Order Status: {r.status_code}")
            
            if r.status_code == 200:
                order_data = r.json()
                print("✅ Payment order created!")
                print(f"📋 Order ID: {order_data.get('order_id')}")
                print(f"💰 Amount: ₹{order_data.get('amount')}")
                
                # Test payment confirmation
                print(f"\n📋 STEP 4: TEST PAYMENT CONFIRMATION")
                payment_data = {
                    "appointment_id": appointment_id,
                    "razorpay_payment_id": f"test_payment_{appointment_id}_{int(time.time())}"
                }
                
                r = requests.post(f"{API}/api/payment/confirm", 
                                 json=payment_data, timeout=10)
                
                print(f"📊 Confirmation Status: {r.status_code}")
                
                if r.status_code == 200:
                    confirm_data = r.json()
                    print("✅ Payment confirmed!")
                    print(f"📋 Status: {confirm_data.get('appointment_status')}")
                    
                    if confirm_data.get('video_details'):
                        video = confirm_data['video_details']
                        print(f"🎥 Video Details:")
                        print(f"   🔑 OTP: {video.get('otp')}")
                        print(f"   🏠 Room: {video.get('meeting_link')}")
                        print(f"   🔗 Doctor URL: {video.get('doctor_url')}")
                        print(f"   🔗 Patient URL: {video.get('patient_url')}")
                    
                    print(f"\n🎯 COMPLETE PAYMENT FLOW WORKING!")
                else:
                    print(f"❌ Payment confirmation failed: {r.text}")
            else:
                print(f"❌ Order creation failed: {r.text}")
        else:
            print(f"❌ Appointment creation failed: {r.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import time
    create_fresh_appointment()
