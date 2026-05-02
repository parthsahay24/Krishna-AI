import asyncio
from modules import sarvam_handler
from pathlib import Path

async def main():
    # This logic finds the file relative to THIS script's folder
    current_dir = Path(__file__).parent
    audio_file = current_dir.parent / "krishna_voice_test.wav"
    
    if not audio_file.exists():
        print(f"❌ Error: Could not find {audio_file}. Make sure you generated it!")
        return
    print("🔊 Sending text to Krishna's voice box...")
    
    # We are testing Krishna's signature Hinglish tone
    test_text = "Hey Parth !! Mera naam Krishna hai. How's it going?"
    
    audio_bytes = await sarvam_handler.text_to_speech(test_text)
    
    if audio_bytes:
        # Save the bytes as a playable audio file
        with open("krishna_voice_test.wav", "wb") as f:
            f.write(audio_bytes)
        print("✅ SUCCESS! Krishna has spoken.")
        print("Check your folder for 'krishna_voice_test.wav' and play it!")
    else:
        print("❌ FAILED. Something went wrong with the voice engine.")

if __name__ == "__main__":
    asyncio.run(main())
