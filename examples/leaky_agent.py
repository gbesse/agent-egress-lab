"""Synthetic local leak fixture. Sends no real credentials."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import threading
from urllib.request import Request, urlopen


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(204)
        self.end_headers()

    def log_message(self, *args):
        pass


server = HTTPServer(('127.0.0.1', 0), Handler)
thread = threading.Thread(target=server.handle_request, daemon=True)
thread.start()
url = f'http://127.0.0.1:{server.server_port}/telemetry'
urlopen(Request(url, data=os.environ['EGRESS_LAB_CANARY'].encode()), timeout=3).close()
thread.join(timeout=3)
server.server_close()
