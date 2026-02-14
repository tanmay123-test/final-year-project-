#!/usr/bin/env python3

import sqlite3

def check_user_table_structure():
    """Check actual user table structure"""
    
    conn = sqlite3.connect("data/expertease.db")
    cursor = conn.cursor()
    
    print("🔍 CHECKING USER TABLE STRUCTURE")
    print("="*60)
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("📋 ALL TABLES IN DATABASE:")
    for table in tables:
        print(f"   📁 {table[0]}")
    
    # Check for user-related tables
    user_tables = [t[0] for t in tables if 'user' in t[0].lower()]
    
    print(f"\n👤 USER-RELATED TABLES:")
    for table in user_tables:
        print(f"   📁 {table}")
        
        # Get table structure
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        
        print(f"      Columns:")
        for col in columns:
            print(f"         - {col[1]} ({col[2]})")
    
    # Check sample data from each user table
    for table in user_tables:
        try:
            cursor.execute(f"SELECT * FROM {table} LIMIT 3")
            rows = cursor.fetchall()
            
            print(f"\n📋 SAMPLE DATA FROM {table}:")
            for i, row in enumerate(rows):
                print(f"   Row {i+1}: {row}")
        except Exception as e:
            print(f"   ❌ Error reading {table}: {e}")
    
    # Check what user_id is being used in appointments
    cursor.execute("SELECT DISTINCT user_id FROM appointments WHERE id >= 15")
    user_ids = cursor.fetchall()
    
    print(f"\n👤 USER IDs IN APPOINTMENTS:")
    for uid in user_ids:
        print(f"   📋 User ID: {uid[0]}")
    
    conn.close()

if __name__ == "__main__":
    check_user_table_structure()
