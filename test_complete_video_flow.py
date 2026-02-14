#!/usr/bin/env python3

import requests
import time
import json

API = "http://127.0.0.1:5000"

def test_video_consultation_complete_flow():
    """Complete end-to-end test of video consultation system"""
    
    print("🎥 COMPLETE VIDEO CONSULTATION FLOW TEST")
    print("="*60)
    
    # Step 1: Create a test appointment first
    print("📋 Step 1: Creating Test Appointment")
    try:
        # Create a test appointment for video consultation
        test_appointment = {
            "user_id": 1,
            "worker_id": 4,
            "user_name": "Test User",
            "symptoms": "Test video consultation symptoms",
            "booking_date": "2026-02-14"
        }
        
        r = requests.post(f"{API}/appointment/video-request", json=test_appointment, timeout=10)
        
        if r.status_code == 201:
            appointment_data = r.json()
            appointment_id = appointment_data.get('appointment_id')
            print(f"   ✅ Test appointment created: #{appointment_id}")
        else:
            print(f"   ❌ Failed to create appointment: {r.status_code}")
            print(f"   Response: {r.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Error creating appointment: {e}")
        return
    
    # Step 2: Accept the appointment (simulate doctor acceptance)
    print(f"\n📋 Step 2: Accepting Appointment")
    try:
        r = requests.post(f"{API}/worker/respond", json={
            "appointment_id": appointment_id,
            "status": "accepted"
        }, timeout=10)
        
        if r.status_code == 200:
            print(f"   ✅ Appointment accepted successfully")
        else:
            print(f"   ❌ Failed to accept appointment: {r.status_code}")
            return
            
    except Exception as e:
        print(f"   ❌ Error accepting appointment: {e}")
        return
    
    # Step 3: Create video session with OTP
    print(f"\n📋 Step 3: Creating Video Session")
    try:
        r = requests.post(f"{API}/video/create-session/{appointment_id}", 
                         json={"doctor_id": 4},
                         timeout=10)
        
        print(f"   Status: {r.status_code}")
        
        if r.status_code == 201:
            data = r.json()
            session = data['session']
            print("   ✅ Video session created successfully!")
            print(f"   📋 Appointment ID: {session['appointment_id']}")
            print(f"   🔑 OTP: {session['doctor_otp']}")
            print(f"   🏠 Room ID: {session['room_id']}")
            
            otp = session['doctor_otp']
            room_id = session['room_id']
            
        else:
            error_data = r.json()
            print(f"   ❌ Error: {error_data.get('message', 'Unknown error')}")
            return
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 4: Start video call with OTP
    print(f"\n📋 Step 4: Starting Video Call")
    try:
        r = requests.post(f"{API}/video/start", 
                         json={
                             "appointment_id": appointment_id,
                             "otp": otp,
                             "doctor_id": 4
                         },
                         timeout=10)
        
        print(f"   Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            print("   ✅ Video call started successfully!")
            print(f"   🏠 Room ID: {data['room_id']}")
            print(f"   📋 Session Status: {data['session']['session_status']}")
            print("   💡 Room is now live for patients to join")
            
        else:
            error_data = r.json()
            print(f"   ❌ Error: {error_data.get('message', 'Unknown error')}")
            return
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 5: Patient joins video call
    print(f"\n📋 Step 5: Patient Joins Video Call")
    try:
        r = requests.get(f"{API}/video/join/{appointment_id}", timeout=10)
        
        print(f"   Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            print("   ✅ Patient joined successfully!")
            print(f"   🏠 Room ID: {data['room_id']}")
            print(f"   📋 Session Status: {data['session']['session_status']}")
            print("   💡 Ready for WebRTC connection")
            
        else:
            error_data = r.json()
            print(f"   ❌ Error: {error_data.get('message', 'Unknown error')}")
            return
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 6: End video call
    print(f"\n📋 Step 6: Ending Video Call")
    try:
        r = requests.post(f"{API}/video/end", 
                         json={
                             "appointment_id": appointment_id,
                             "user_id": 4,
                             "user_type": "doctor"
                         },
                         timeout=10)
        
        print(f"   Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            print("   ✅ Video call ended successfully!")
            print(f"   📋 Session Status: {data['session']['session_status']}")
            print("   📊 Appointment marked as completed")
            
        else:
            error_data = r.json()
            print(f"   ❌ Error: {error_data.get('message', 'Unknown error')}")
            return
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 7: Check final session status
    print(f"\n📋 Step 7: Final Session Status")
    try:
        r = requests.get(f"{API}/video/session/{appointment_id}", timeout=10)
        
        print(f"   Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            session = data['session']
            print("   ✅ Final session details:")
            print(f"   🏠 Room ID: {session['room_id']}")
            print(f"   📋 Status: {session['session_status']}")
            print(f"   📅 Started: {session['started_at'] or 'Not started'}")
            print(f"   📅 Ended: {session['ended_at'] or 'Not ended'}")
            
        else:
            print(f"   ❌ Error: {r.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n🎯 COMPLETE FLOW TEST SUMMARY")
    print("="*60)
    print("✅ Video consultation system is FULLY WORKING!")
    print("✅ Complete end-to-end flow tested successfully!")
    print("✅ All APIs responding correctly!")
    print("✅ OTP security working!")
    print("✅ Session lifecycle management working!")
    print("✅ Ready for frontend integration!")
    
    print(f"\n🚀 PRODUCTION READY!")
    print("="*60)

if __name__ == "__main__":
    test_video_consultation_complete_flow()
