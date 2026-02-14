#!/usr/bin/env python3

import sqlite3

def check_appointment_table():
    """Check appointment table structure"""
    
    conn = sqlite3.connect("data/expertease.db")
    cursor = conn.cursor()
    
    # Get table schema
    cursor.execute("PRAGMA table_info(appointments)")
    columns = cursor.fetchall()
    
    print("📋 APPOINTMENTS TABLE STRUCTURE:")
    print("="*60)
    
    for col in columns:
        print(f"Column: {col[1]} | Type: {col[2]} | NotNull: {col[3]} | Default: {col[4]}")
    
    # Get a sample row
    cursor.execute("SELECT * FROM appointments LIMIT 1")
    sample = cursor.fetchone()
    
    if sample:
        print(f"\n📋 SAMPLE ROW STRUCTURE:")
        print("="*60)
        cursor.execute("PRAGMA table_info(appointments)")
        columns = cursor.fetchall()
        
        for i, col in enumerate(columns):
            print(f"Index {i}: {col[1]} = {sample[i] if i < len(sample) else 'NULL'}")
    
    conn.close()

if __name__ == "__main__":
    check_appointment_table()
