import asyncio
import signal
from os import environ
from random import randint
from time import time

import websockets
from prometheus_client import Counter, Gauge, start_http_server
from python_socks.async_.asyncio import Proxy

signal.signal(signal.SIGINT, signal.SIG_DFL)

COUNT = int(environ.get("COUNT", 100))
RECONNECT = bool(int(environ.get("RECONNECT", 0)))

SERVER_IP = environ["SERVER_IP"]
SERVER_PORT = int(environ.get("SERVER_PORT", 8000))

PROXY_URL = environ.get("PROXY_URL")

Gauge("wanted_connections", "Target number of connections").set(COUNT)
counter = Gauge("connections", "Current number of connection")
disconnects = Counter("disconnects", "Number of disconnections")


async def main():
    proxy = Proxy.from_url(PROXY_URL) if PROXY_URL is not None else None

    async def test_websocket(i):
        while True:
            await asyncio.sleep(i * 0.1)
            print(f"Connecting server #{i} (reconnect: {RECONNECT})")

            ws = None
            try:
                sock = None
                if proxy is not None:
                    sock = await proxy.connect(
                        dest_host=SERVER_IP, dest_port=SERVER_PORT, timeout=9
                    )

                ws = await websockets.connect(
                    f"ws://{SERVER_IP}:{SERVER_PORT}",
                    sock=sock,
                    ping_interval=10,
                    ping_timeout=30,
                    open_timeout=30,
                )
                print(f"Connected server #{i}")
                counter.inc()
            except Exception as e:
                print(repr(e))

                disconnects.inc()

                if not RECONNECT:
                    return

                continue

            start = time()

            try:
                j = 0
                while True:
                    sleep_time = randint(1, 10)
                    await ws.send(
                        f"Hello, server #{i} (ping {j}), see you in {sleep_time}s"
                    )
                    await ws.recv()
                    await asyncio.sleep(sleep_time)
                    j += 1
            except asyncio.CancelledError:
                return
            except Exception as e:
                print(e)
                if not RECONNECT:
                    return
            finally:
                counter.dec()
                end = time()
                duration = end - start
                disconnects.inc()
                print(f"Lasted {duration}s")

            print(f"Reconnecting server #{i} after wait")

    start_http_server(8000)

    for i in range(COUNT):
        asyncio.create_task(test_websocket(i))

    await asyncio.sleep(10)

    while True:
        conns = counter._value.get()
        if not RECONNECT and conns == 0:
            print("Break & failed")
            break

        print(
            f"Currently {conns} connections open, {disconnects._value.get()} disconnects"
        )
        await asyncio.sleep(1)


asyncio.run(main())
