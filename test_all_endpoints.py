#!/usr/bin/env python3

import requests
import time

def test_server_endpoints():
    """Test all server endpoints to identify issues"""
    
    print("🔍 TESTING SERVER ENDPOINTS")
    print("="*60)
    
    endpoints = [
        ("GET", "/api/subscription/plans", "Subscription Plans"),
        ("GET", "/api/subscription/current?worker_id=4", "Current Subscription"),
        ("POST", "/create-order", "Payment System"),
        ("GET", "/", "Root Endpoint"),
        ("GET", "/health", "Health Check")
    ]
    
    for method, endpoint, name in endpoints:
        try:
            print(f"\n📋 Testing {name}: {method} {endpoint}")
            
            if method == "GET":
                r = requests.get(f"http://127.0.0.1:5000{endpoint}")
            else:
                r = requests.post(f"http://127.0.0.1:5000{endpoint}", 
                               json={"amount": 99900, "booking_id": "test"})
            
            print(f"   Status: {r.status_code}")
            if r.status_code == 200:
                print(f"   ✅ Working")
            elif r.status_code == 404:
                print(f"   ❌ Not Found - Endpoint not registered")
            elif r.status_code == 500:
                print(f"   ❌ Server Error - Check logs")
            else:
                print(f"   ⚠️ Unexpected status")
                
        except requests.exceptions.ConnectionError as e:
            print(f"   ❌ Connection Error: {e}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎯 Diagnosis:")
    print("="*60)
    print("If payment endpoint fails but subscription works:")
    print("1. ✅ Server is running")
    print("2. ✅ Subscription blueprint registered") 
    print("3. ❌ Payment blueprint may have issues")
    print("4. 🔧 Check payment blueprint registration")

if __name__ == "__main__":
    test_server_endpoints()
