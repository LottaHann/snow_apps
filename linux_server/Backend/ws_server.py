import asyncio
import websockets
import json
from speech_pipeline import init_recording, stop_recording, get_clients, set_event_loop
import os
import sys
from log_funcs import log_status, log_type
import datetime

event_loop = asyncio.get_event_loop()

set_event_loop(event_loop)


async def handle_client(websocket):
    clients = get_clients()
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            command = data.get("command")
            log_type("speech")
            log_status(command, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            if command == "on":
                init_recording()

            elif command == "off":
                print("Stopping recording")
                stop_recording() 

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

async def start_server():
    """Start the WebSocket server."""
    server = await websockets.serve(handle_client, "0.0.0.0", 8765)
    print("WebSocket server started on ws://0.0.0.0:8765")
    await server.wait_closed()

# Run WebSocket server
event_loop.run_until_complete(start_server())
event_loop.run_forever()