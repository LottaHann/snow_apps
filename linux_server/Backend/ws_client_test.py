import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8765"  # Adjust the port if needed
    async with websockets.connect(uri) as websocket:
        # Send "on" command as JSON
        message = json.dumps({"command": "on"})
        await websocket.send(message)
        print(f"> Sent: {message}")

        # Receive response
        response = await websocket.recv()
        print(f"< Received: {response}")

        # Wait a bit before sending "off"
        await asyncio.sleep(3)

        # Send "off" command as JSON
        message = json.dumps({"command": "off"})
        await websocket.send(message)
        print(f"> Sent: {message}")

        # Receive response
        response = await websocket.recv()
        print(f"< Received: {response}")
        response_data = json.loads(response)  # Parse the JSON string
        while response_data["status"] != "processing":
            response = await websocket.recv()
            response_data = json.loads(response)  # Parse the next response
            print(f"< Received: {response_data}")
asyncio.run(test_websocket())
