"""A tiny read-only JSON API plus the static dashboard, using only the standard library.

    python -m collateral_iq serve      -> http://localhost:8000

Endpoints
    GET /api/dashboard                 portfolio roll-up for the web page
    GET /api/subjects                  list of subject properties
    GET /api/value?subject_id=SUBJ-001 full adjustment grid for one subject
    GET /api/market?submarket=...      monthly trend for one submarket
"""
from __future__ import annotations

import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import metrics, valuation
from .loader import load_subjects

WEB_DIR = Path(__file__).resolve().parents[2] / "web"
PORT = 8000


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def log_message(self, fmt, *args):  # quieter console
        if "/api/" in (args[0] if args else ""):
            super().log_message(fmt, *args)

    def do_GET(self):  # noqa: N802 - name required by the base class
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/"):
            return super().do_GET()

        params = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        try:
            payload = self._route(parsed.path, params)
        except KeyError as exc:
            return self._send(404, {"error": str(exc)})
        except Exception as exc:  # noqa: BLE001 - demo server, surface the message
            return self._send(500, {"error": f"{type(exc).__name__}: {exc}"})
        self._send(200, payload)

    def _route(self, path: str, params: dict) -> dict | list:
        if path == "/api/dashboard":
            return metrics.dashboard_payload()
        if path == "/api/subjects":
            return [
                {k: (v.isoformat() if hasattr(v, "isoformat") else v) for k, v in s.items()}
                for s in load_subjects()
            ]
        if path == "/api/value":
            return valuation.value_subject(params.get("subject_id", "SUBJ-001"))
        if path == "/api/market":
            return metrics.market_trend(params.get("submarket", "Peoria - Vistancia"))
        raise KeyError(f"No such endpoint: {path}")

    def _send(self, status: int, payload) -> None:
        body = json.dumps(payload, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def serve(port: int = PORT) -> None:
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"Collateral IQ running at http://localhost:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()
