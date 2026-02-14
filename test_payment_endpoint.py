#!/usr/bin/env python3

import requests

def test_payment_endpoint():
    """Test if payment endpoint exists"""
    
    try:
        # Test the payment endpoint
        r = requests.post("http://127.0.0.1:5000/payment/create-order", 
                         json={"amount": 99900, "booking_id": "test"})
        
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.text}")
        
        if r.status_code == 200:
            print("✅ Payment endpoint working!")
        else:
            print(f"❌ Payment endpoint error: {r.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_payment_endpoint()
