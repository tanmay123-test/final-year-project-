#!/usr/bin/env python3

import sqlite3
from config import WORKER_DB

def check_subscription_database():
    """Check the actual state of subscriptions in database"""
    
    conn = sqlite3.connect(WORKER_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("🔍 CHECKING SUBSCRIPTION DATABASE STATE")
    print("="*60)
    
    # Check worker 4's subscriptions
    worker_id = 4
    
    cursor.execute("""
        SELECT ws.id, ws.plan_id, ws.status, ws.created_at, ws.start_date, ws.end_date,
               sp.name as plan_name, sp.daily_appointment_limit, sp.price
        FROM worker_subscriptions ws
        JOIN subscription_plans sp ON ws.plan_id = sp.id
        WHERE ws.worker_id = ?
        ORDER BY ws.created_at DESC
    """, (worker_id,))
    
    subscriptions = cursor.fetchall()
    
    print(f"📊 Worker {worker_id} Subscriptions:")
    for sub in subscriptions:
        print(f"   ID: {sub['id']}")
        print(f"   Plan: {sub['plan_name']} (ID: {sub['plan_id']})")
        print(f"   Status: {sub['status']}")
        print(f"   Daily Limit: {sub['daily_appointment_limit']}")
        print(f"   Created: {sub['created_at']}")
        print(f"   Start: {sub['start_date']}")
        print(f"   End: {sub['end_date']}")
        print("   " + "-"*40)
    
    # Check current active subscription
    cursor.execute("""
        SELECT ws.*, sp.name as plan_name, sp.price, sp.daily_appointment_limit, sp.is_trial
        FROM worker_subscriptions ws
        JOIN subscription_plans sp ON ws.plan_id = sp.id
        WHERE ws.worker_id = ? AND ws.status = 'active'
        ORDER BY ws.created_at DESC
        LIMIT 1
    """, (worker_id,))
    
    current = cursor.fetchone()
    
    if current:
        print(f"✅ Current Active Subscription:")
        print(f"   Plan: {current['plan_name']}")
        print(f"   Daily Limit: {current['daily_appointment_limit']}")
        print(f"   Status: {current['status']}")
    else:
        print("❌ No active subscription")
    
    conn.close()

if __name__ == "__main__":
    check_subscription_database()
