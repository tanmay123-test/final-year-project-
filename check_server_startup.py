#!/usr/bin/env python3

import sys
import os

print("🔍 CHECKING SERVER STARTUP ISSUES")
print("="*60)

# Check if all required files exist
print("📋 File Existence Check:")
files_to_check = [
    "c:\\Users\\Admin\\Desktop\\Project\\final-year-project-\\.env",
    "c:\\Users\\Admin\\Desktop\\Project\\final-year-project-\\payment\\.env",
    "c:\\Users\\Admin\\Desktop\\Project\\final-year-project-\\payment\\payments\\payment_route.py",
    "c:\\Users\\Admin\\Desktop\\Project\\final-year-project-\\payment\\payments\\payment_db.py",
    "c:\\Users\\Admin\\Desktop\\Project\\final-year-project-\\payment\\payments\\razor_service.py",
    "c:\\Users\\Admin\\Desktop\\Project\\final-year-project-\\database.db"
]

for file_path in files_to_check:
    exists = os.path.exists(file_path)
    status = "✅" if exists else "❌"
    print(f"   {status} {os.path.basename(file_path)}")

# Check if payment files have correct content
print("\n📋 Payment File Content Check:")
try:
    with open("c:\\Users\\Admin\\Desktop\\Project\\final-year-project-\\payment\\payments\\payment_route.py", 'r') as f:
        content = f.read()
        if "create_order(amount, booking_id)" in content:
            print("   ✅ payment_route.py has correct function call")
        else:
            print("   ❌ payment_route.py function call incorrect")
            
    with open("c:\\Users\\Admin\\Desktop\\Project\\final-year-project-\\payment\\payments\\payment_db.py", 'r') as f:
        content = f.read()
        if '"created"' in content and "'paid'" in content:
            print("   ✅ payment_db.py has correct SQL syntax")
        else:
            print("   ❌ payment_db.py SQL syntax still incorrect")
            
except Exception as e:
    print(f"   ❌ Error reading files: {e}")

# Check environment variables
print("\n📋 Environment Variables Check:")
try:
    with open("c:\\Users\\Admin\\Desktop\\Project\\final-year-project-\\.env", 'r') as f:
        content = f.read()
        if "RAZORPAY_KEY_ID" in content and "RAZORPAY_KEY_SECRET" in content:
            print("   ✅ Main .env has Razorpay credentials")
        else:
            print("   ❌ Main .env missing Razorpay credentials")
            
    with open("c:\\Users\\Admin\\Desktop\\Project\\final-year-project-\\payment\\.env", 'r') as f:
        content = f.read()
        if "RAZORPAY_KEY_ID" in content:
            print("   ✅ Payment .env has Razorpay credentials")
        else:
            print("   ❌ Payment .env missing Razorpay credentials")
            
except Exception as e:
    print(f"   ❌ Error checking .env files: {e}")

print("\n🎯 LIKELY ISSUE:")
print("="*60)
print("Based on the CLI output showing errors:")
print("1. ❌ Server may have startup errors not visible")
print("2. ❌ Payment blueprint may not be registering correctly")
print("3. ❌ Database operations may be failing")
print("4. ❌ CLI may be calling wrong endpoints")

print("\n🔧 IMMEDIATE FIX:")
print("="*60)
print("1. Stop the server (Ctrl+C)")
print("2. Check server console for error messages")
print("3. Restart server with: python app.py")
print("4. Watch for startup messages")
print("5. Test with simple requests first")

if __name__ == "__main__":
    pass
