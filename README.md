# Websocket Connection Loadtester

Simple client/server that opens N websocket connections sending back & fourth pings to test how many parallel connections can be sustained. Optionally using a SOCKS5 proxy.

## Setup Server

```sh
pip install websockets
python3 server.py
```

## Run Client

```sh
pip install websockets python-socks[asyncio] prometheus-client

# Basic no proxy
SERVER_IP=1.2.3.4 COUNT=1000 python3 client.py

# With SOCKS5 proxy
SERVER_IP=1.2.3.4 PROXY_URL=socks5://user:password@5.6.7.8 python3 client.py
```
