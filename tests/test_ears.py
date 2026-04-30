import asyncio
from modules import sarvam_handler

async def main():
    print("👂 Krishna is listening to the test file...")
    
    # We are using the audio file YOU just generated!
    audio_file = "krishna_voice_test.wav"
    
    transcript = await sarvam_handler.speech_to_text(audio_file)
    
    if transcript:
        print(f"✅ SUCCESS! Krishna heard: '{transcript}'")
    else:
        print("❌ FAILED. Krishna's ears aren't working yet.")

if __name__ == "__main__":
    asyncio.run(main())
