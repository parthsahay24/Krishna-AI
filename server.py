import asyncio
from datetime import datetime, timezone
import time
from modules import analytics_db
import base64
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from modules import config, llm_handler, sarvam_handler
import uuid

MAX_AUDIO_SIZE = 5 * 1024 * 1024  # 5MB limit (plenty for voice clips)


app = FastAPI(title="Krishna AI")

@app.get("/")
async def status():
    return {"status": "ok", "service": "Krishna AI", "websocket": "/ws"}

#Establishing phone line
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 1. Open the Phone Line
    await websocket.accept()

    # --- HELPER FOR NON-BLOCKING DB CALLS ---
    async def _safe_analytics_call(fn, *args):
        try:
            await asyncio.to_thread(fn, *args)
        except Exception as e:
            print(f"⚠️ Analytics Logging Error: {e}")

    # Generate a unique ID for this specific session
    session_id = str(uuid.uuid4())
    await _safe_analytics_call(analytics_db.log_session_start, session_id)
    print("✅ Connection Established: Krishna is on the line.")
    
    try:
        while True:
             # 2. Receive Audio Data from the Browser
            # The browser will send the user's voice as raw bytes.
            audio_data = await websocket.receive_bytes()
            # --- START THE TIMER HERE ---
            start_time = time.perf_counter()
           
            # PROFESSOR'S SECURITY ADDITION: Check file size
            if len(audio_data) > MAX_AUDIO_SIZE:
                await websocket.send_json({
                    "text": "Tumhari voice file bahut badi hai, friend. Please short rakho.",
                    "audio": None,
                    "status": "error",
                    "error": "file_too_large"
                })
                continue # Skip processing and wait for next message
            
            # 3. Save the audio to a temp file so the 'Ears' can read it
            # temp_filename = "temp_user_voice.wav"
            # Generate a random unique ID
            unique_id = uuid.uuid4() 
            temp_filename = f"temp_{unique_id}.wav" 
            try:
                with open(temp_filename, "wb") as f:
                    f.write(audio_data)


                # 4. EAR PHASE: Translate voice to text
                user_text = await sarvam_handler.speech_to_text(temp_filename)
                # Delete the file as soon as you're done with it!
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)

            
                if user_text:
                    print(f"User said: {user_text}")
                    # 5. BRAIN PHASE: Get Krishna's Hinglish response
                    krishna_text = llm_handler.get_krishna_response(user_text)
                    print(f"Krishna responds: {krishna_text}")
                    latency_ms = (time.perf_counter() - start_time) * 1000
                    await _safe_analytics_call(analytics_db.log_conversation, session_id, user_text, krishna_text, latency_ms)

                    # 6. VOICE PHASE: Translate Krishna's response to audio
                    krishna_audio = await sarvam_handler.text_to_speech(krishna_text)

                    if krishna_audio:
                        # Sending the audio back through the pipe
                        # 1. Turn audio bytes into a string
                        audio_base64 = base64.b64encode(krishna_audio).decode('utf-8')
                        # 2. Send both text and audio back
                        await websocket.send_json({
                            "text": krishna_text,
                            "audio": audio_base64
                        })
                        

                else:
                    # Don't leave the user hanging!
                    await websocket.send_json({
                        "text": "I couldn't hear you clearly, friend.",
                        "audio": None,
                        "status": "error",
                        "error": "empty_speech"
                    })
                     # Log the failure for analysis
                    await _safe_analytics_call(analytics_db.log_error, datetime.now(timezone.utc), "Empty speech detected", "STT_FAILURE", f"Session: {session_id}")

            except Exception as e:
                print(f"⚠️ Loop Error: {str(e)}")
                # Clean up if an error happened mid-way
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)

    except WebSocketDisconnect:
        print("❌ Connection Closed: The user hung up.")
        

    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
    finally:
        await _safe_analytics_call(analytics_db.log_session_end, session_id)


            
if __name__ == "__main__":
    import uvicorn
    # Initialize the database before the server starts
    analytics_db.init_db() 
    uvicorn.run("server:app", host="0.0.0.0", port=config.SERVER_PORT, reload=True)
