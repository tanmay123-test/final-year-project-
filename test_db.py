import sqlite3
from config import WORKER_DB
conn = sqlite3.connect(WORKER_DB)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables:', [t[0] for t in tables])
conn.close()
