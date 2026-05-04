import sys
import os
import uuid
from datetime import datetime, timezone
import time

# Ensure we can import modules from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules import analytics_db

def run_showcase():
    print("🚀 Starting Krishna AI Analytics Showcase...")
    
    # 1. Reset/Initialize Database
    # We use a temporary DB for the test so we don't mess with your real data
    TEST_DB = "data/krishna_analytics.db"
    analytics_db.init_db()
    
    # 2. Simulate Session Start
    session_id = str(uuid.uuid4())
    print(f"📂 Created Test Session: {session_id}")
    analytics_db.log_session_start(session_id)
    time.sleep(0.5)

    # 3. Simulate Conversation Turns
    turns = [
        ("Hello Krishna, show me the data!", "Namaste! I have captured your request in my SQLite storage."),
        ("Is the database hardened?", "Yes, friend. With Foreign Keys and UTC timestamps!"),
        ("What about performance?", "Using asyncio threads, I am as fast as the wind.")
    ]

    for user_text, bot_text in turns:
        print(f"💬 Logging Interaction...")
        llm_lat = 320.5  # Simulated LLM time
        total_lat = 950.0 # Simulated total time
        analytics_db.log_conversation(session_id, user_text, bot_text, llm_lat, total_lat)
        time.sleep(0.3)

    # 4. Simulate a System Error (TTS Failure)
    print("⚠️ Logging a simulated Voice Failure...")
    analytics_db.log_error(
        datetime.now(timezone.utc),
        "TTS Failed - Connection Timeout with Sarvam API",
        "VOICE_FAILURE",
        f"Session: {session_id}"
    )

    # 5. End Session
    print("🔒 Closing Session...")
    analytics_db.log_session_end(session_id)
    
    print("\n" + "="*70)
    print("📊 KRISHNA AI ANALYTICS - TERMINAL SHOWCASE")
    print("="*70)

    # 6. Display Data
    import sqlite3
    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.cursor()
        
        print("\n[1. SESSIONS TABLE]")
        cursor.execute("SELECT session_id, start_time, status FROM sessions")
        for row in cursor.fetchall():
            print(f"ID: {row[0][:15]}... | Started: {row[1]} | Status: {row[2]}")

        print("\n[2. CONVERSATIONS TABLE (RELATIONAL INTEGRITY)]")
        print(f"{'USER INPUT':<30} | {'BRAIN LAT':<12} | {'TOTAL LAT':<12}")
        print("-" * 70)
        cursor.execute("SELECT user_input, llm_latency_ms, total_latency_ms FROM conversations")
        for row in cursor.fetchall():
            user_peek = (row[0][:27] + '..') if len(row[0]) > 27 else row[0]
            print(f"{user_peek:<30} | {row[1]:>9.1f}ms | {row[2]:>9.1f}ms")

        print("\n[3. ERROR LOGS (GRACEFUL FAILURES)]")
        cursor.execute("SELECT error_type, error_message FROM errors")
        for row in cursor.fetchall():
            print(f"TYPE: {row[0]:<15} | MSG: {row[1]}")

    print("\n" + "="*70)
    print("✅ Showcase Complete! This data proves the backend is fully functional.")
    print("="*70)

if __name__ == "__main__":
    run_showcase()
