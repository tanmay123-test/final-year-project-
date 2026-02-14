#!/usr/bin/env python3

import sqlite3
from config import WORKER_DB

def check_table_structure():
    """Check the actual table structure"""
    
    conn = sqlite3.connect(WORKER_DB)
    cursor = conn.cursor()
    
    print("🔍 CHECKING TABLE STRUCTURE")
    print("="*60)
    
    # Check worker_subscriptions table
    cursor.execute("PRAGMA table_info(worker_subscriptions)")
    columns = cursor.fetchall()
    
    print("📊 worker_subscriptions table columns:")
    for col in columns:
        print(f"   {col[1]}: {col[2]}")
    
    print("\n📊 Sample data:")
    cursor.execute("SELECT * FROM worker_subscriptions WHERE worker_id = 4 LIMIT 3")
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"   {row}")
    
    conn.close()

if __name__ == "__main__":
    check_table_structure()
