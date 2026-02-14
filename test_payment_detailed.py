#!/usr/bin/env python3

import requests
import json

def test_payment_detailed():
    """Test payment endpoint with detailed debugging"""
    
    print("💳 DETAILED PAYMENT ENDPOINT TEST")
    print("="*60)
    
    # Test 1: Basic payment order
    print("📋 Test 1: Basic Payment Order")
    try:
        payment_data = {
            "amount": 99900,
            "booking_id": "test_subscription_123"
        }
        
        r = requests.post("http://127.0.0.1:5000/create-order", 
                         json=payment_data,
                         timeout=10)
        
        print(f"   Status Code: {r.status_code}")
        print(f"   Response Headers: {dict(r.headers)}")
        
        if r.status_code == 200:
            response_data = r.json()
            print("   ✅ Payment Order Created Successfully!")
            print(f"   Order ID: {response_data.get('order_id')}")
            print(f"   Amount: {response_data.get('amount')}")
            print(f"   Key: {response_data.get('key')}")
        else:
            print(f"   ❌ Error Response: {r.text}")
            
    except requests.exceptions.Timeout:
        print("   ❌ Request Timeout - Server may be slow")
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ Connection Error: {e}")
    except Exception as e:
        print(f"   ❌ Unexpected Error: {e}")
    
    # Test 2: Check if payment data is saved
    print(f"\n📋 Test 2: Check Payment Database")
    try:
        # This would require access to the database
        print("   📝 Payment should be saved to database.db")
        print("   🔍 Check payment table for records")
    except Exception as e:
        print(f"   ❌ Database check failed: {e}")
    
    # Test 3: Multiple rapid requests
    print(f"\n📋 Test 3: Multiple Rapid Requests")
    for i in range(3):
        try:
            r = requests.post("http://127.0.0.1:5000/create-order", 
                             json={"amount": 99900, "booking_id": f"test_{i}"},
                             timeout=5)
            print(f"   Request {i+1}: Status {r.status_code}")
        except Exception as e:
            print(f"   Request {i+1}: Error {e}")
    
    print(f"\n🎯 Analysis:")
    print("="*60)
    print("If intermittent failures occur:")
    print("1. ✅ Endpoint exists and responds")
    print("2. ❌ Connection stability issues")
    print("3. 🔧 May need connection pooling")
    print("4. 🔄 Retry logic recommended")

if __name__ == "__main__":
    test_payment_detailed()
