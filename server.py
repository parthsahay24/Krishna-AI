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
    """Returns the health status of the Krishna AI service."""
    return {"status": "ok", "service": "Krishna AI", "websocket": "/ws"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint for real-time voice interaction with Krishna AI.
    Handles audio ingestion, STT, LLM response generation, TTS, and telemetry logging.
    """
    await websocket.accept()

    async def _safe_analytics_call(fn, *args):
        """Helper to offload blocking DB calls to threads without stalling the event loop."""
        try:
            await asyncio.to_thread(fn, *args)
        except Exception as e:
            print(f"⚠️ Analytics Logging Error: {e}")

    session_id = str(uuid.uuid4())
    await _safe_analytics_call(analytics_db.log_session_start, session_id)
    print("✅ Connection Established: Krishna is on the line.")
    
    try:
        while True:
            # 2. Receive Audio Data from the Browser
            audio_data = await websocket.receive_bytes()
            start_time = time.perf_counter()
           
            if len(audio_data) > MAX_AUDIO_SIZE:
                await websocket.send_json({
                    "text": "Tumhari voice file bahut badi hai, friend. Please short rakho.",
                    "audio": None,
                    "status": "error",
                    "error": "file_too_large"
                })
                continue
            
            unique_id = uuid.uuid4() 
            temp_filename = f"temp_{unique_id}.wav" 
            try:
                with open(temp_filename, "wb") as f:
                    f.write(audio_data)

                # EAR PHASE: Voice to Text
                user_text = await sarvam_handler.speech_to_text(temp_filename)
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)

                if user_text:
                    print(f"User said: {user_text}")
                    
                    # BRAIN PHASE: Krishna's response
                    llm_start_time = time.perf_counter()
                    krishna_text = llm_handler.get_krishna_response(user_text)
                    llm_latency_ms = (time.perf_counter() - llm_start_time) * 1000
                    print(f"Krishna responds: {krishna_text}")

                    # VOICE PHASE: Text to Speech
                    krishna_audio = await sarvam_handler.text_to_speech(krishna_text)

                    if krishna_audio:
                        audio_base64 = base64.b64encode(krishna_audio).decode('utf-8')
                        await websocket.send_json({
                            "text": krishna_text,
                            "audio": audio_base64,
                            "status": "ok"
                        })
                    else:
                        # Log and notify on TTS failure
                        await _safe_analytics_call(
                            analytics_db.log_error, 
                            datetime.now(timezone.utc), 
                            "TTS Failed - Text generated but audio not delivered", 
                            "VOICE_FAILURE", 
                            f"Session: {session_id}"
                        )
                        await websocket.send_json({
                            "text": krishna_text,
                            "audio": None,
                            "status": "tts_failed"
                        })

                    # Calculate total end-to-end latency and log to DB
                    total_latency_ms = (time.perf_counter() - start_time) * 1000
                    print(f"⚡ Total Latency: {total_latency_ms:.2f}ms (Brain: {llm_latency_ms:.2f}ms)")
                    
                    await _safe_analytics_call(
                        analytics_db.log_conversation, 
                        session_id, 
                        user_text, 
                        krishna_text, 
                        llm_latency_ms, 
                        total_latency_ms
                    )

                else:
                    await websocket.send_json({
                        "text": "I couldn't hear you clearly, friend.",
                        "audio": None,
                        "status": "error",
                        "error": "empty_speech"
                    })
                    await _safe_analytics_call(analytics_db.log_error, datetime.now(timezone.utc), "Empty speech detected", "STT_FAILURE", f"Session: {session_id}")

            except Exception as e:
                print(f"⚠️ Loop Error: {str(e)}")
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
    analytics_db.init_db() 
    uvicorn.run("server:app", host="0.0.0.0", port=config.SERVER_PORT, reload=True)
