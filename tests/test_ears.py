import asyncio
from modules import sarvam_handler
from pathlib import Path

async def main():
    # This logic finds the file relative to THIS script's folder
    current_dir = Path(__file__).parent
    audio_file = current_dir / "krishna_voice_test.wav"
    
    if not audio_file.exists():
        print(f"❌ Error: Could not find {audio_file}. Make sure you generated it!")
        return
    print("👂 Krishna is listening to the test file...")
    
    # We are using the audio file YOU just generated!

    
    transcript = await sarvam_handler.speech_to_text(str(audio_file))

    
    if transcript:
        print(f"✅ SUCCESS! Krishna heard: '{transcript}'")
    else:
        print("❌ FAILED. Krishna's ears aren't working yet.")

if __name__ == "__main__":
    asyncio.run(main())
