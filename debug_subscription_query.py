#!/usr/bin/env python3

import sqlite3
from config import WORKER_DB

def debug_subscription_query():
    """Debug the subscription query to see what's being returned"""
    
    conn = sqlite3.connect(WORKER_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("🔍 DEBUGGING SUBSCRIPTION QUERY")
    print("="*60)
    
    # Run the exact same query as in subscription_db.py
    cursor.execute("""
            SELECT ws.*, sp.name as plan_name, sp.price, sp.daily_appointment_limit, sp.is_trial
            FROM worker_subscriptions ws
            JOIN subscription_plans sp ON ws.plan_id = sp.id
            WHERE ws.worker_id = ? AND ws.status = 'active'
            ORDER BY ws.created_at DESC, ws.id DESC
            LIMIT 1
        """, (4,))
    
    result = cursor.fetchone()
    
    if result:
        print("✅ Query Result:")
        print(f"   Keys available: {list(result.keys())}")
        for key, value in result.items():
            print(f"   {key}: {value}")
    else:
        print("❌ No result found")
    
    conn.close()

if __name__ == "__main__":
    debug_subscription_query()
