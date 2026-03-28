import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://127.0.0.1:8000/ws"  # Corrected URL
    async with websockets.connect(uri) as ws:
        # Send a test message
        await ws.send(json.dumps({"type": "ping"}))
        
        # Receive a response from server
        response = await ws.recv()
        print("Server response:", response)

# Run the test
asyncio.run(test_ws())