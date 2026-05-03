import sqlite3
import os
from datetime import datetime

DB_PATH = "data/krishna_analytics.db"

def init_db():
    """Initializes the database and creates the necessary tables if they don't exist."""
    os.makedirs("data", exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # 1. Conversations Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp DATETIME,
                user_input TEXT,
                bot_response TEXT,
                latency_ms REAL
            )
        ''')
        
        # 2. Sessions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                start_time DATETIME,
                end_time DATETIME,
                status TEXT
            )
        ''')
        
        # 3. Errors Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                error_message TEXT,
                error_type TEXT,
                context TEXT
            )
        ''')

def log_conversation(session_id, user_input, bot_response, latency_ms):
    """Inserts a new conversation record."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (session_id, timestamp, user_input, bot_response, latency_ms)
            VALUES (?, ?, ?, ?, ?)
        ''', (session_id, datetime.now(), user_input, bot_response, latency_ms))

def log_session_start(session_id):
    """Logs the start of a WebSocket connection."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO sessions (session_id, start_time, status)
            VALUES (?, ?, ?)
        ''', (session_id, datetime.now(), 'active'))

def log_session_end(session_id):
    """Logs the end of a WebSocket connection."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE sessions SET end_time = ?, status = ? WHERE session_id = ?
        ''', (datetime.now(), 'completed', session_id))

def log_error(timestamp, error_message, error_type, context):
    """Logs an error to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO errors (timestamp, error_message, error_type, context)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, error_message, error_type, context))
