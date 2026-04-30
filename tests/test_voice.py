import asyncio
from modules import sarvam_handler

async def main():
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
