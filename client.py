from concurrent.futures import ThreadPoolExecutor
from os import environ
from random import randint
from time import sleep, time

import websocket

COUNT = int(environ.get("COUNT", 100))

SERVER_IP = environ["SERVER_IP"]
SERVER_PORT = environ.get("SERVER_PORT", 8000)

PROXY_TYPE = environ.get("PROXY_TYPE", "socks5")
PROXY_IP = environ.get("PROXY_IP")
PROXY_USER = environ.get("PROXY_USER", "proxy")
PROXY_PASSWORD = environ.get("PROXY_PASSWORD")
PROXY_PORT = environ.get("PROXY_PORT", 8000)

counter = []


def test_websocket(i):
    sleep(i * 0.1)

    ws = websocket.WebSocket()
    ws.connect(
        f"ws://{SERVER_IP}:{SERVER_PORT}",
        http_proxy_host=PROXY_IP,
        http_proxy_port=PROXY_PORT,
        proxy_type=PROXY_TYPE,
        http_proxy_auth=(PROXY_USER, PROXY_PASSWORD),
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
