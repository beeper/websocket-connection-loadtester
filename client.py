from concurrent.futures import ThreadPoolExecutor
from os import environ
from random import randint
from time import sleep, time

import websocket

COUNT = environ.get("COUNT", 100)

SERVER_IP = environ["SERVER_IP"]
SERVER_PORT = environ.get("SERVER_PORT", 8000)

SOCKS_IP = environ.get("SOCKS_IP")
SOCKS_USER = environ.get("SOCKS_USER", "proxy")
SOCKS_PASSWORD = environ.get("SOCKS_PASSWORD")
SOCKS_PORT = environ.get("SOCKS_PORT", 9000)

counter = []


def test_websocket(i):
    sleep(i * 0.1)

    ws = websocket.WebSocket()
    ws.connect(
        f"ws://{SERVER_IP}:{SERVER_PORT}",
        http_proxy_host=SOCKS_IP,
        http_proxy_port=SOCKS_PORT,
        proxy_type="socks5",
        http_proxy_auth=(SOCKS_USER, SOCKS_PASSWORD),
        timeout=5,
    )
    print(f"Connected server #{i}")
    counter.append(True)

    start = time()

    try:
        j = 0
        while True:
            sleep_time = randint(1, 3)
            ws.send(f"Hello, server #{i} (ping {j}), see you in {sleep_time}s")
            ws.recv()
            sleep(sleep_time)
            j += 1
    except KeyboardInterrupt:
        print("Exit!")
        ws.close()
    finally:
        counter.pop()
        end = time()
        duration = end - start
        print(f"Lasted {duration}s")


executor = ThreadPoolExecutor(max_workers=COUNT)

for i in range(COUNT):
    executor.submit(test_websocket, i)

sleep(10)

while True:
    if not counter:
        print("Break & failed")
        break
    print(f"Currently {len(counter)} connections open")
    sleep(1)
