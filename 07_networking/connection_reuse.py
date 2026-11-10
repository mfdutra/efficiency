"""Creating a new connection per request vs reusing one (HTTP keep-alive).

Run: python3 07_networking/connection_reuse.py

Runs against a local server, so the gap is small. Over the internet every new
connection also pays TCP handshake + TLS handshake (2-3 extra round trips).
"""
import http.client
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # required for keep-alive

    def do_GET(self):
        body = b"ok"
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
port = server.server_address[1]
threading.Thread(target=server.serve_forever, daemon=True).start()
N = 1000

# BAD: urlopen() opens a fresh TCP connection (and closes it) every call.
start = time.perf_counter()
for _ in range(N):
    urllib.request.urlopen(f"http://127.0.0.1:{port}/").read()
print(f"new connection each time: {(time.perf_counter() - start) * 1e3:7.1f} ms")

# GOOD: one connection, many requests. (With the `requests` library, use a
# requests.Session() -- calling requests.get() in a loop is the same mistake.)
start = time.perf_counter()
conn = http.client.HTTPConnection("127.0.0.1", port)
for _ in range(N):
    conn.request("GET", "/")
    conn.getresponse().read()
conn.close()
print(f"one reused connection   : {(time.perf_counter() - start) * 1e3:7.1f} ms")
server.shutdown()
