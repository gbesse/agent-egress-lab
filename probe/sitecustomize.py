"""Loaded by Python at startup through PYTHONPATH."""
import http.client
import json
import os
import socket

_EVENTS = os.environ.get('EGRESS_LAB_EVENTS')
_CANARY = os.environ.get('EGRESS_LAB_CANARY', '').encode()
_original_connect = socket.socket.connect
_original_send = http.client.HTTPConnection.send


def _record(event):
    if not _EVENTS:
        return
    try:
        handle = os.open(_EVENTS, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        try:
            os.write(handle, (json.dumps(event, sort_keys=True) + '\n').encode())
        finally:
            os.close(handle)
    except OSError:
        pass


def _connect(self, address):
    if isinstance(address, tuple):
        _record({'type': 'connect', 'host': str(address[0]), 'port': address[1]})
    return _original_connect(self, address)


def _send(self, data):
    payload = data.encode() if isinstance(data, str) else bytes(data)
    _record({'type': 'http_send', 'canary_seen': bool(_CANARY and _CANARY in payload), 'bytes': len(payload)})
    return _original_send(self, data)


if _EVENTS:
    socket.socket.connect = _connect
    http.client.HTTPConnection.send = _send
