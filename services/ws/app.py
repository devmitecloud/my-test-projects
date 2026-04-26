import asyncio
import json
import os
import time

import websockets


WS_NAME = os.getenv("WS_NAME", "ws")
WS_PORT = int(os.getenv("WS_PORT", "8765"))


async def handle_connection(websocket):
    peer = websocket.remote_address
    await websocket.send(
        json.dumps(
            {
                "event": "connected",
                "service": WS_NAME,
                "peer": str(peer),
                "timestamp": time.time(),
            }
        )
    )

    async for message in websocket:
        await websocket.send(
            json.dumps(
                {
                    "event": "echo",
                    "service": WS_NAME,
                    "message": message,
                    "timestamp": time.time(),
                }
            )
        )


async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", WS_PORT):
        print(f"Serving {WS_NAME} websocket endpoint on port {WS_PORT}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
