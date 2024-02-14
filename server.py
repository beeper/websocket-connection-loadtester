#!/usr/bin/env python

# Lifted straight from :https://websockets.readthedocs.io/en/stable/

import asyncio

from os import environ

import websockets


SERVER_PORT = environ.get("SERVER_PORT", 8000)

async def echo(websocket):
    print(f"Connected websocket from: {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"Got message: {message}")
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosedError:
        print("Client connection closed")


async def main():
    async with websockets.serve(echo, "0.0.0.0", SERVER_PORT):
        await asyncio.Future()


asyncio.run(main())
