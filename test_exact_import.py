#!/usr/bin/env python3

# Test the exact same import as in app.py
import sys
import os
sys.path.insert(0, os.getcwd())

from flask import Flask
app = Flask(__name__)

print("🔍 TESTING EXACT APP.PY IMPORT")
print("="*60)

try:
    from payment.payments.payment_route import payment_bp
    app.register_blueprint(payment_bp)
    print("✅ Payment blueprint registered successfully!")
    
    # Check the route
    print(f"Routes: {list(app.url_map.iter_rules())}")
    
except ImportError as e:
    print(f"❌ Could not register payment blueprint: {e}")
    print("🔄 Subscription will use demo mode")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print(f"\n🌐 Testing endpoint directly:")
try:
    with app.test_client() as client:
        response = client.post('/payment/create-order', 
                           json={"amount": 99900, "booking_id": "test"})
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.get_json()}")
except Exception as e:
    print(f"❌ Endpoint test failed: {e}")
