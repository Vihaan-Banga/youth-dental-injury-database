#!/usr/bin/env python3
"""Tiny local HTTP server that accepts PDF uploads from the Chrome MCP browser.

Run in the background while the JS in Chrome POSTs PDF blobs to it:

    POST http://127.0.0.1:8765/upload?name=<pmid>.pdf
    body: raw PDF bytes

Saves to data/raw/papers/_oa_pdfs/<name>. CORS-permissive (Access-Control-Allow-Origin: *).
"""
from __future__ import annotations
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import urllib.parse as up

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "data/raw/papers/_oa_pdfs"
DEST.mkdir(parents=True, exist_ok=True)

ALLOWED_PREFIX = ("oa_", "")  # any name is fine — we trust JS we wrote
PORT = 8765


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        try:
            qs = up.urlparse(self.path).query
            params = dict(up.parse_qsl(qs))
            name = params.get("name", "untitled.pdf")
            # sanitize: strip slashes, force .pdf
            name = Path(name).name
            if not name.endswith(".pdf"):
                name += ".pdf"
            length = int(self.headers.get("Content-Length") or 0)
            data = self.rfile.read(length) if length else b""
            (DEST / name).write_bytes(data)
            ok = data[:4] == b"%PDF"
            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                f'{{"ok":true,"name":"{name}","size":{len(data)},"is_pdf":{str(ok).lower()}}}'.encode()
            )
            print(f"saved {name}  size={len(data)}  pdf={ok}")
        except Exception as exc:
            self.send_response(500)
            self._cors()
            self.end_headers()
            self.wfile.write(str(exc).encode())

    def log_message(self, *args, **kwargs):
        pass  # quiet


def main():
    print(f"listening on http://127.0.0.1:{PORT}/upload  dest={DEST}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
