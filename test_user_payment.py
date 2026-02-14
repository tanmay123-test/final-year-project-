#!/usr/bin/env python3

import requests
import json

API = "http://127.0.0.1:5000"

def test_user_payment_flow():
    """Test the complete user payment flow"""
    
    print("🧪 TESTING USER PAYMENT FLOW")
    print("="*60)
    
    # Step 1: Login as user
    print("🔐 Step 1: User Login")
    login_response = requests.post(f"{API}/login", json={
        "username": "Sarthy",
        "password": "890"
    })
    
    if login_response.status_code == 200:
        token = login_response.json().get("token")
        print("✅ User login successful")
        
        # Step 2: Get appointment details
        print("\n📋 Step 2: Get Appointment Details")
        appointment_id = 13  # The appointment you just booked
        
        apt_response = requests.get(
            f"{API}/appointment/{appointment_id}?sender_role=user",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if apt_response.status_code == 200:
            apt = apt_response.json()
            print(f"✅ Appointment {appointment_id} found")
            print(f"📊 Status: {apt['status']}")
            print(f"💰 Payment Status: {apt.get('payment_status', 'N/A')}")
            
            # Step 3: Create payment order
            if apt.get('payment_status') in ['pending', 'payment_pending']:
                print("\n💳 Step 3: Create Payment Order")
                
                payment_response = requests.post(
                    f"{API}/api/payment/create-order",
                    json={"appointment_id": appointment_id},
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if payment_response.status_code == 200:
                    payment_data = payment_response.json()
                    print("✅ Payment order created!")
                    print(f"📋 Order ID: {payment_data['order_id']}")
                    print(f"💰 Amount: ₹{payment_data['amount']}")
                    
                    if payment_data.get('pricing_breakdown'):
                        breakdown = payment_data['pricing_breakdown']
                        print(f"\n📊 PRICE BREAKDOWN:")
                        print(f"   Doctor Fee: ₹{breakdown['doctor_fee']}")
                        print(f"   Platform Fee (20%): ₹{breakdown['platform_fee']}")
                        print(f"   Total Amount: ₹{breakdown['total_amount']}")
                    
                    print(f"\n🌐 Payment ready for Razorpay integration")
                    print(f"🔗 Test Payment URL: http://localhost:5000/test-payment")
                    
                    # Step 4: Simulate payment confirmation
                    print("\n✅ Step 4: Simulate Payment Confirmation")
                    
                    confirm_response = requests.post(
                        f"{API}/api/payment/confirm",
                        json={
                            "appointment_id": appointment_id,
                            "razorpay_payment_id": f"test_payment_{appointment_id}"
                        },
                        headers={"Authorization": f"Bearer {token}"}
                    )
                    
                    if confirm_response.status_code == 200:
                        confirm_data = confirm_response.json()
                        print("✅ Payment confirmed!")
                        print(f"📅 Appointment Status: {confirm_data.get('appointment_status')}")
                        
                        if confirm_data.get('video_details'):
                            video = confirm_data['video_details']
                            print(f"\n🎥 Video Consultation Details:")
                            print(f"   Patient URL: {video['patient_url']}")
                            print(f"   OTP: {video['otp']}")
                    else:
                        print("❌ Payment confirmation failed")
                else:
                    print("❌ Failed to create payment order")
                    print("Error:", payment_response.json().get("error", "Unknown"))
            else:
                print("ℹ️ No payment required for this appointment")
        else:
            print("❌ Failed to get appointment details")
    else:
        print("❌ User login failed")

if __name__ == "__main__":
    test_user_payment_flow()
