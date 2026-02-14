#!/usr/bin/env python3

import requests

def test_correct_payment_endpoint():
    """Test the correct payment endpoint"""
    
    print("🔍 TESTING CORRECT PAYMENT ENDPOINT")
    print("="*60)
    
    # Test the correct endpoint (without /payment prefix)
    try:
        r = requests.post("http://127.0.0.1:5000/create-order", 
                         json={"amount": 99900, "booking_id": "test"})
        
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.text}")
        
        if r.status_code == 200:
            print("✅ Payment endpoint working!")
            response_data = r.json()
            print(f"   Order ID: {response_data.get('order_id')}")
            print(f"   Amount: {response_data.get('amount')}")
        else:
            print(f"❌ Payment endpoint error: {r.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n📋 Testing subscription endpoint:")
    try:
        r = requests.get("http://127.0.0.1:5000/api/subscription/plans")
        print(f"Subscription API Status: {r.status_code}")
        if r.status_code == 200:
            print("✅ Subscription API working!")
    except Exception as e:
        print(f"❌ Subscription API error: {e}")

if __name__ == "__main__":
    test_correct_payment_endpoint()
