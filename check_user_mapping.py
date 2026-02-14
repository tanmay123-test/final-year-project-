#!/usr/bin/env python3

import sqlite3

def check_user_databases():
    """Check both user databases to understand the issue"""
    
    print("🔍 CHECKING USER DATABASES")
    print("="*60)
    
    # Check users.db
    try:
        conn = sqlite3.connect("data/users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        print(f"👤 USERS IN users.db (Total: {len(users)})")
        print("-"*40)
        
        for user in users:
            print(f"👤 User ID: {user['id']}")
            print(f"   📧 Username: {user['username']}")
            print(f"   📧 Email: {user['email']}")
            print(f"   📝 Name: {user['name']}")
            print(f"   ✅ Verified: {user['is_verified']}")
            print("-"*40)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading users.db: {e}")
    
    # Check expertease.db for user references
    try:
        conn = sqlite3.connect("data/expertease.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT user_id, user_name, COUNT(*) as appointment_count
            FROM appointments 
            WHERE id >= 15
            GROUP BY user_id, user_name
        """)
        
        user_refs = cursor.fetchall()
        
        print(f"\n👥 USER REFERENCES IN expertease.db")
        print("-"*40)
        
        for ref in user_refs:
            print(f"👤 User ID: {ref['user_id']}")
            print(f"   📝 Name: {ref['user_name']}")
            print(f"   📋 Appointments: {ref['appointment_count']}")
            print("-"*40)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading expertease.db: {e}")
    
    # Check if Sarthy user exists
    try:
        conn = sqlite3.connect("data/users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = 'Sarthy'")
        sarthy_user = cursor.fetchone()
        
        if sarthy_user:
            print(f"\n✅ FOUND SARTHY USER:")
            print(f"   👤 User ID: {sarthy_user['id']}")
            print(f"   📧 Username: {sarthy_user['username']}")
            print(f"   📧 Email: {sarthy_user['email']}")
            print(f"   📝 Name: {sarthy_user['name']}")
        else:
            print(f"\n❌ SARTHY USER NOT FOUND in users.db")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking Sarthy: {e}")
    
    print(f"\n🎯 DIAGNOSIS:")
    print("="*60)
    print("📋 The issue is that appointments are created with user_id=6")
    print("📋 But the user Sarthy might have a different ID in users.db")
    print("📋 This causes the appointment fetching to fail")
    print("📋 Solution: Fix the user_id mapping between databases")

if __name__ == "__main__":
    check_user_databases()
