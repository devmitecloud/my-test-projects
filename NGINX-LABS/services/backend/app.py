import json
import os
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


APP_NAME = os.getenv("APP_NAME", "backend")
APP_PORT = int(os.getenv("APP_PORT", "8080"))
APP_ROLE = os.getenv("APP_ROLE", "service")
STARTED_AT = time.time()


class LabHandler(BaseHTTPRequestHandler):
    server_version = "LabBackend/1.0"

    def _read_body(self):
        content_length = int(self.headers.get("Content-Length", "0") or 0)
        if not content_length:
            return ""
        return self.rfile.read(content_length).decode("utf-8", errors="replace")

    def _payload(self):
        parsed = urllib.parse.urlparse(self.path)
        return {
            "service": APP_NAME,
            "role": APP_ROLE,
            "method": self.command,
            "path": parsed.path,
            "query": urllib.parse.parse_qs(parsed.query),
            "host": self.headers.get("Host"),
            "x_forwarded_for": self.headers.get("X-Forwarded-For"),
            "x_forwarded_host": self.headers.get("X-Forwarded-Host"),
            "x_forwarded_proto": self.headers.get("X-Forwarded-Proto"),
            "x_forwarded_port": self.headers.get("X-Forwarded-Port"),
            "timestamp": time.time(),
            "uptime_seconds": round(time.time() - STARTED_AT, 3),
        }

    def _send_json(self, status_code, payload, extra_headers=None):
        body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        if extra_headers:
            for key, value in extra_headers.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def _status_payload(self, status_code):
        payload = self._payload()
        payload["status"] = status_code
        return payload

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/healthz":
            payload = self._payload()
            payload["health"] = "ok"
            self._send_json(200, payload)
            return

        if path.startswith("/delay/"):
            delay_value = path.rsplit("/", 1)[-1] or "0"
            try:
                delay_seconds = max(0.0, min(float(delay_value), 10.0))
            except ValueError:
                self._send_json(400, {"error": "delay must be numeric", "value": delay_value})
                return
            time.sleep(delay_seconds)
            payload = self._payload()
            payload["delay_seconds"] = delay_seconds
            self._send_json(200, payload)
            return

        if path.startswith("/status/"):
            code_value = path.rsplit("/", 1)[-1] or "200"
            try:
                status_code = max(100, min(int(code_value), 599))
            except ValueError:
                self._send_json(400, {"error": "status must be numeric", "value": code_value})
                return
            self._send_json(status_code, self._status_payload(status_code))
            return

        if path.startswith("/cache/"):
            cache_key = path.removeprefix("/cache/") or "default"
            payload = self._payload()
            payload["cache_key"] = cache_key
            payload["generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            self._send_json(200, payload, {"Cache-Control": "public, max-age=30"})
            return

        if path == "/headers":
            payload = self._payload()
            payload["headers"] = {key: value for key, value in self.headers.items()}
            self._send_json(200, payload)
            return

        payload = self._payload()
        self._send_json(200, payload)

    def do_POST(self):
        payload = self._payload()
        payload["body"] = self._read_body()
        payload["headers"] = {key: value for key, value in self.headers.items()}
        self._send_json(200, payload)

    def log_message(self, fmt, *args):
        message = "%s - - [%s] %s\n" % (
            self.address_string(),
            self.log_date_time_string(),
            fmt % args,
        )
        print(message, end="")


def main():
    server = ThreadingHTTPServer(("0.0.0.0", APP_PORT), LabHandler)
    print(f"Serving {APP_NAME} on port {APP_PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
