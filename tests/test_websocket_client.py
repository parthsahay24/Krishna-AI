"""
Krishna AI - WebSocket Integration Test Client
-----------------------------------------------
Sends a real .wav audio file to the running Krishna AI server,
receives the response, and prints a DB analytics report.

HOW TO USE:
1. Start the server in Terminal 1: python server.py
2. Run this script in Terminal 2: python tests/test_websocket_client.py
"""

import asyncio
import websockets
import json
import sqlite3
import os
import sys
import base64

# Ensure we can import from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

SERVER_URL = "ws://localhost:8000/ws"
AUDIO_FILE = "tests/TEST_KRISHNA.wav"
DB_PATH    = "data/krishna_analytics.db"

async def run_test():
    print("="*60)
    print("🔌 Krishna AI WebSocket Integration Test")
    print("="*60)

    if not os.path.exists(AUDIO_FILE):
        print(f"❌ Audio file not found: {AUDIO_FILE}")
        return

    print(f"📁 Audio File: {AUDIO_FILE}")
    print(f"🌐 Connecting to: {SERVER_URL}")

    try:
        async with websockets.connect(SERVER_URL) as ws:
            print("✅ Connected to Krishna AI Server!\n")

            # Read and send the audio file
            with open(AUDIO_FILE, "rb") as f:
                audio_bytes = f.read()

            print(f"🎤 Sending audio ({len(audio_bytes)} bytes)...")
            await ws.send(audio_bytes)

            # Wait for Krishna's response
            print("⏳ Waiting for Krishna's response...")
            response = await asyncio.wait_for(ws.recv(), timeout=30)
            data = json.loads(response)

            print("\n" + "="*60)
            print("📨 KRISHNA'S RESPONSE:")
            print("="*60)
            print(f"  Status : {data.get('status', 'N/A')}")
            print(f"  Text   : {data.get('text', 'N/A')}")
            print(f"  Audio  : {'✅ Received' if data.get('audio') else '❌ Not received'}")

            if data.get('audio'):
                try:
                    audio_bytes = base64.b64decode(data['audio'])
                    out_path = "tests/krishna_reply_live.wav"
                    with open(out_path, "wb") as f:
                        f.write(audio_bytes)
                    print(f"\n  🎧 SUCCESS! Krishna's voice has been saved to:")
                    print(f"  👉 {out_path}")
                    print(f"  (Double-click this file in VS Code or File Explorer to listen!)")
                except Exception as e:
                    print(f"  ❌ Failed to save audio file: {e}")

    except ConnectionRefusedError:
        print("❌ Could not connect. Make sure 'python server.py' is running first!")
        return
    except asyncio.TimeoutError:
        print("❌ Server took too long to respond. Check your API keys.")
        return
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return

    # Print DB Analytics Report
    if not os.path.exists(DB_PATH):
        print("\n⚠️ DB not found. Ensure server.py ran init_db() on startup.")
        return

    print("\n" + "="*60)
    print("📊 ANALYTICS DB REPORT (After Live Test)")
    print("="*60)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        print("\n[SESSIONS]")
        cursor.execute("SELECT session_id, start_time, status FROM sessions ORDER BY start_time DESC LIMIT 5")
        for row in cursor.fetchall():
            print(f"  {row[0][:12]}... | {row[1]} | {row[2]}")

        print("\n[CONVERSATIONS]")
        cursor.execute("SELECT user_input, llm_latency_ms, total_latency_ms FROM conversations ORDER BY timestamp DESC LIMIT 5")
        rows = cursor.fetchall()
        if rows:
            print(f"  {'USER INPUT':<30} | {'BRAIN':<10} | {'TOTAL':<10}")
            print("  " + "-"*56)
            for row in rows:
                u = (row[0][:27] + '..') if row[0] and len(row[0]) > 27 else (row[0] or 'N/A')
                print(f"  {u:<30} | {row[1]:>7.1f}ms | {row[2]:>7.1f}ms")
        else:
            print("  No conversations logged yet.")

        print("\n[ERRORS]")
        cursor.execute("SELECT error_type, error_message FROM errors ORDER BY timestamp DESC LIMIT 5")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(f"  TYPE: {row[0]:<15} | {row[1]}")
        else:
            print("  ✅ No errors logged.")

    print("\n" + "="*60)
    print("✅ Integration Test Complete!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(run_test())
