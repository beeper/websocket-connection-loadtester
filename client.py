from concurrent.futures import ThreadPoolExecutor
from os import environ
from random import randint
from time import sleep, time
from prometheus_client import start_http_server, Counter, Gauge

import websocket

COUNT = int(environ.get("COUNT", 100))
RECONNECT = bool(int(environ.get("RECONNECT", 0)))

SERVER_IP = environ["SERVER_IP"]
SERVER_PORT = environ.get("SERVER_PORT", 8000)

PROXY_TYPE = environ.get("PROXY_TYPE", "socks5")
PROXY_IP = environ.get("PROXY_IP")
PROXY_USER = environ.get("PROXY_USER", "proxy")
PROXY_PASSWORD = environ.get("PROXY_PASSWORD")
PROXY_PORT = environ.get("PROXY_PORT", 8000)

Gauge("wanted_connections", "Target number of connections").set(COUNT)
counter = Gauge("connections", "Current number of connection")
disconnects = Counter("disconnects", "Number of disconnections")

def test_websocket(i):
    while True:
        sleep(i * 0.1)
        print(f"Connecting server #{i} (reconnect: {RECONNECT})")

        ws = websocket.WebSocket()
        try:
            ws.connect(
                f"ws://{SERVER_IP}:{SERVER_PORT}",
                http_proxy_host=PROXY_IP,
                http_proxy_port=PROXY_PORT,
                proxy_type=PROXY_TYPE,
                http_proxy_auth=(PROXY_USER, PROXY_PASSWORD),
                timeout=5,
            )
            print(f"Connected server #{i}")
            counter.inc()
        except Exception as e:
            print(e)

            disconnects.inc()

            if not RECONNECT:
                return

            continue

        start = time()

        try:
            j = 0
            while True:
                sleep_time = randint(1, 10)
                ws.send(f"Hello, server #{i} (ping {j}), see you in {sleep_time}s")
                ws.recv()
                sleep(sleep_time)
                j += 1
        except KeyboardInterrupt:
            print("Exit!")
            ws.close()
        finally:
            counter.dec()
            end = time()
            duration = end - start
            disconnects.inc()
            print(f"Lasted {duration}s")

            if not RECONNECT:
                return

        print(f"Reconnecting server #{i} after wait")

start_http_server(8000)
executor = ThreadPoolExecutor(max_workers=COUNT)

for i in range(COUNT):
    executor.submit(test_websocket, i)

sleep(10)

while True:
    conns = counter._value.get()
    if not RECONNECT and conns == 0:
        print("Break & failed")
        break

    print(f"Currently {conns} connections open, {disconnects._value.get()} disconnects")
    sleep(1)
