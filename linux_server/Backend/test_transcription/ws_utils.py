import asyncio
import websockets
import json
from ws_server import get_clients



def broadcast_status(status):
    message = json.dumps({"status": status})
    asyncio.create_task(send_to_all_clients(message))

async def send_to_all_clients(message):
    clients = get_clients()
    if clients:
        await asyncio.wait([client.send(message) for client in clients])