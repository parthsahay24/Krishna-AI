import asyncio
import websockets
import json
import base64

async def test_krishna():
    uri = "ws://localhost:8000/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("🔗 Connected to Krishna's Phone Line!")
            
            # 1. Prepare a "Voice Message" to send
            # We use the file we generated earlier
            audio_file = "krishna_voice_test.wav"
            with open(audio_file, "rb") as f:
                audio_bytes = f.read()
            
            print(f"📤 Sending voice data from '{audio_file}'...")
            await websocket.send(audio_bytes)
            
            # 2. Wait for Krishna's response
            print("⏳ Waiting for Krishna to think...")
            response = await websocket.recv()
            
            # 3. Decode the JSON response
            data = json.loads(response)
            
            # 4. Display the Results
            print(f"\n✨ Krishna says: {data['text']}")
            
            if 'audio' in data:
                # Turn the text-audio back into real sound bytes
                audio_reply_bytes = base64.b64decode(data['audio'])
                
                # Save the reply so you can listen to it!
                output_file = "krishna_reply.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_reply_bytes)
                
                print(f"✅ Success! Voice saved to '{output_file}'")
                print("\nTHE SERVER IS WORKING 100%! READY FOR FRONTEND.")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_krishna())
