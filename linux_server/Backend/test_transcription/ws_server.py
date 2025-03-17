import asyncio
import websockets
import json
from recorder import init_recording, stop_recording 

clients = set()

def get_clients():
    return clients

async def handle_client(websocket, path):
    clients.add(websocket)
    global recording
    try:
        async for message in websocket:
            data = json.loads(message)
            command = data.get("command")

            if command == "on":
                init_recording()

            elif command == "off":
                stop_recording() 

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

async def main():
    server = await websockets.serve(handle_client, "0.0.0.0", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
