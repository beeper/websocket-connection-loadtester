FROM alpine:latest
RUN apk add --no-cache py3-python-socks py3-websockets py3-websocket-client py3-prometheus-client
COPY server.py client.py /
CMD ["/usr/bin/python3", "-u", "/client.py"]
