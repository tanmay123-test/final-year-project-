#!/usr/bin/env python3

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

print("🔍 DEBUGGING BLUEPRINT REGISTRATION")
print("="*60)
print(f"Current directory: {os.getcwd()}")
print(f"Python path includes current dir: {os.getcwd() in sys.path}")

print(f"\n📁 File checks:")
print(f"payment folder exists: {os.path.exists('payment')}")
print(f"payments folder exists: {os.path.exists('payment/payments')}")
print(f"payment_route.py exists: {os.path.exists('payment/payments/payment_route.py')}")

print(f"\n🧪 Import tests:")
try:
    from payment.payments.payment_route import payment_bp
    print("✅ Import successful!")
    print(f"Blueprint name: {payment_bp.name}")
    print(f"Blueprint url_prefix: {getattr(payment_bp, 'url_prefix', 'None')}")
    
    # Check if blueprint has routes
    print(f"Blueprint has defer_functions: {hasattr(payment_bp, 'defer_functions')}")
    if hasattr(payment_bp, 'defer_functions'):
        print(f"Number of functions: {len(payment_bp.defer_functions)}")
        for func in payment_bp.defer_functions:
            print(f"  - {func}")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")

print(f"\n🌐 Testing Flask app registration:")
try:
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(payment_bp)
    print("✅ Blueprint registration successful!")
    
    # Check routes
    print(f"App routes: {list(app.url_map.iter_rules())}")
    
except Exception as e:
    print(f"❌ Blueprint registration failed: {e}")
