import base64
import httpx
from . import config

# Sarvam AI Endpoints
TTS_URL = "https://api.sarvam.ai/text-to-speech"

async def text_to_speech(text: str):
    """
    Turns Krishna's text into high-quality Hinglish audio bytes.
    """
    if not config.SARVAM_API_KEY or config.SARVAM_API_KEY == "your_sarvam_key_here":
        print("⚠️ Warning: SARVAM_API_KEY is missing or a placeholder!")
        return None

    headers = {
        "api-subscription-key": config.SARVAM_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "speaker": "kabir",
        "model": "bulbul:v3",
        "target_language_code": "hi-IN",
        "pace": 1,                 # Slow and meditative
        "temperature": 0.4,          # Stable and calm
        "speech_sample_rate": 22050, 
        "enable_preprocessing": True 
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(TTS_URL, json=payload, headers=headers, timeout=10.0)
            
            if response.status_code == 200:
                data = response.json()

                if 'audios' in data and len(data['audios']) > 0:
                    return base64.b64decode(data['audios'][0])
                else:
                    print(f"❌ Unusual Response (No Audio): {data}")
                    return None
            else:
                print(f"❌ Sarvam Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Connection Error: {str(e)}")
            return None

STT_URL = "https://api.sarvam.ai/speech-to-text"

async def speech_to_text(audio_file_path: str):
    """
    Translates your voice (audio file) into text that the Brain can read.
    """
    headers = {
        "api-subscription-key": config.SARVAM_API_KEY
    }
    
    # We send the audio file as 'multipart/form-data'
    # 'saaras:v3' is the smartest ear model Sarvam has.
    files = {
        "file": open(audio_file_path, "rb")
    }
    data = {
        "model": "saaras:v3"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(STT_URL, headers=headers, files=files, data=data)
            
            if response.status_code == 200:
                # Returns the transcription (what you said)
                return response.json().get("transcript", "")
            else:
                print(f"❌ STT Error: {response.status_code}")
                return ""
        except Exception as e:
            print(f"❌ Ear Engine Error: {str(e)}")
            return ""
