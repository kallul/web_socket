import asyncio
import websockets

connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)
    print("✅ A client connected.")
    try:
        async for message in websocket:
            # Send back to sender
            await websocket.send(f"You said: {message}")
            print(f"📩 Received from client: {message}")
            # Broadcast to others
            await asyncio.gather(*[
                client.send(f"Someone says: {message}")
                for client in connected_clients if client != websocket
            ])
    finally:
        connected_clients.remove(websocket)
        print("❌ A client disconnected.")

async def server_input():
    while True:
        try:
            # Use asyncio.to_thread to make input non-blocking
            msg = await asyncio.to_thread(input, "[Server] Type message to broadcast: ")
            if connected_clients:  # Check if there are any connected clients
                await asyncio.gather(*[
                    client.send(f"🟢 Server: {msg}")
                    for client in connected_clients
                ])
                print(f"📤 Server broadcast: {msg}")
            else:
                print("❗ No clients connected to receive message")
        except Exception as e:
            print(f"Error in server input: {e}")

async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    print("✅ Server is running on ws://localhost:8765")
    print("Waiting for client connections...")
    
    # Run both server input handling and keep the server alive
    await asyncio.gather(
        server_input(),
        asyncio.Future()  # This future never completes, keeping the server running
    )


if __name__ == "__main__":
    asyncio.run(main())