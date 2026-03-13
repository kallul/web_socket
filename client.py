import asyncio
import websockets
import sys

async def chat():
    uri = "ws://localhost:8765"
    try:
        print(f"Connecting to server at {uri}...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to server!")
            print("Start chatting (type messages and press Enter)")
            
            async def receive():
                try:
                    async for message in websocket:
                        print(f"\n📩 {message}")
                        print("You: ", end="", flush=True)  # Prompt again after receiving
                except websockets.exceptions.ConnectionClosed:
                    print("\n❌ Connection to server closed")
                    return
                except Exception as e:
                    print(f"\n❌ Error receiving message: {e}")
                    return

            async def send():
                try:
                    while True:
                        # Use asyncio.to_thread to make input non-blocking
                        msg = await asyncio.to_thread(input, "You: ")
                        if msg.lower() == "exit":
                            print("Exiting chat...")
                            sys.exit(0)
                        await websocket.send(msg)
                except websockets.exceptions.ConnectionClosed:
                    print("\n❌ Connection to server closed")
                    return
                except Exception as e:
                    print(f"\n❌ Error sending message: {e}")
                    return

            await asyncio.gather(receive(), send())
    except ConnectionRefusedError:
        print("❌ Could not connect to server. Is the server running?")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(chat())
    except KeyboardInterrupt:
        print("\nExiting chat client...")
        sys.exit(0)
