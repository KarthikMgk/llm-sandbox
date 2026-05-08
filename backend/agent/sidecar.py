import http.server
import socketserver
import json
import subprocess
import threading
from datetime import datetime

AGENT_KEY = "default-key-change-me"
PORT = 8999
RATE_LIMIT = 5
requests_log: list[float] = []
requests_lock = threading.Lock()

class AgentHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def check_auth(self) -> bool:
        key = self.headers.get("X-Agent-Key", "")
        return key == AGENT_KEY

    def check_rate_limit(self) -> bool:
        now = datetime.utcnow().timestamp()
        global requests_log
        with requests_lock:
            requests_log = [t for t in requests_log if now - t < 1]
            if len(requests_log) >= RATE_LIMIT:
                return False
            requests_log.append(now)
        return True

    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "timestamp": datetime.utcnow().isoformat()}).encode())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/execute":
            if not self.check_auth():
                self.send_error(401, "Unauthorized")
                return
            if not self.check_rate_limit():
                self.send_error(429, "Rate limited")
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            command = data.get("command", "")

            try:
                result = subprocess.run(
                    ["bash", "-c", command],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                response = {
                    "output": result.stdout[:10000],
                    "stderr": result.stderr[:10000],
                    "exit_code": result.returncode
                }
            except subprocess.TimeoutExpired:
                response = {"output": "", "stderr": "Command timed out", "exit_code": -1}
            except Exception as e:
                response = {"output": "", "stderr": str(e), "exit_code": -1}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    server = ThreadedHTTPServer(("localhost", PORT), AgentHandler)
    print(f"Agent listening on localhost:{PORT}")
    server.serve_forever()