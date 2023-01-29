#!/usr/bin/env python

# Lifted straight from :https://websockets.readthedocs.io/en/stable/

import asyncio

import websockets


async def echo(websocket):
    try:
        async for message in websocket:
            print(f"Got message: {message}")
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosedError:
        print("Client connection closed")


async def main():
    async with websockets.serve(echo, "0.0.0.0", 8000):
        await asyncio.Future()


asyncio.run(main())
