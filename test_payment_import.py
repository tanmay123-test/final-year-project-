#!/usr/bin/env python3

try:
    from payment.payments.payment_route import payment_bp
    print("✅ Import successful!")
    print(f"Blueprint: {payment_bp}")
    print(f"Name: {payment_bp.name}")
except ImportError as e:
    print(f"❌ Import failed: {e}")

# Also try alternative import paths
try:
    from payment.payments import payment_route
    print("✅ Alternative import successful!")
    print(f"Module: {payment_route}")
except ImportError as e:
    print(f"❌ Alternative import failed: {e}")

# Check if the files exist
import os
payment_route_path = "c:\\Users\\Admin\\Desktop\\Project\\final-year-project-\\payment\\payments\\payment_route.py"
print(f"File exists: {os.path.exists(payment_route_path)}")
