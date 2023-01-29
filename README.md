# Websocket Connection Loadtester

Simple client/server that opens N websocket connections sending back & fourth pings to test how many parallel connections can be sustained. Optionally using a SOCKS5 proxy.

## Setup Server

```sh
pip install websockets
python3 server.py
```

## Run Client

```sh
pip install websocket-client

# Basic no proxy
SERVER_IP=1.2.3.4 COUNT=1000 python3 client.py

# With SOCKS5 proxy
SERVER_IP=1.2.3.4 SOCKS_IP=5.6.7.8 SOCKS_USER=user SOCKS_PASSWORD=password python3 client.py
```
