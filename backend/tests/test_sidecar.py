import pytest
import json
import threading
import time
import urllib.request
import urllib.error

from agent.sidecar import AgentHandler, ThreadedHTTPServer, AGENT_KEY, RATE_LIMIT, requests_log, requests_lock

@pytest.fixture
def server():
    with requests_lock:
        requests_log.clear()
    server = ThreadedHTTPServer(("localhost", 0), AgentHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    time.sleep(0.2)
    yield port
    server.shutdown()

def make_request(port, path, method="GET", data=None, headers=None):
    headers = headers or {}
    url = f"http://localhost:{port}{path}"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.code, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        raise

def test_status_endpoint_returns_valid_json(server):
    port = server
    code, body = make_request(port, "/status")
    assert code == 200
    assert body is not None
    assert "status" in body
    assert "timestamp" in body

def test_execute_endpoint_requires_authentication(server):
    port = server
    code, body = make_request(port, "/execute", method="POST", data=json.dumps({"command": "echo test"}).encode())
    assert code == 401

def test_execute_with_correct_key_succeeds(server):
    port = server
    headers = {"X-Agent-Key": AGENT_KEY, "Content-Type": "application/json"}
    code, body = make_request(port, "/execute", method="POST", data=json.dumps({"command": "echo hello"}).encode(), headers=headers)
    assert code == 200
    assert body is not None
    assert "output" in body

def test_rate_limit_enforced(server):
    port = server
    headers = {"X-Agent-Key": AGENT_KEY, "Content-Type": "application/json"}
    time.sleep(1.1)
    with requests_lock:
        requests_log.clear()
    for i in range(RATE_LIMIT):
        code, _ = make_request(port, "/execute", method="POST", data=json.dumps({"command": "echo test"}).encode(), headers=headers)
        assert code == 200, f"Request {i+1} failed with code {code}"
    code, _ = make_request(port, "/execute", method="POST", data=json.dumps({"command": "echo test"}).encode(), headers=headers)
    assert code == 429

def test_rate_limit_resets_after_window(server):
    port = server
    headers = {"X-Agent-Key": AGENT_KEY, "Content-Type": "application/json"}
    time.sleep(1.1)
    with requests_lock:
        requests_log.clear()
    for i in range(RATE_LIMIT):
        make_request(port, "/execute", method="POST", data=json.dumps({"command": "echo test"}).encode(), headers=headers)
    code, _ = make_request(port, "/execute", method="POST", data=json.dumps({"command": "echo test"}).encode(), headers=headers)
    assert code == 429
    time.sleep(1.1)
    code, _ = make_request(port, "/execute", method="POST", data=json.dumps({"command": "echo test"}).encode(), headers=headers)
    assert code == 200

def test_unknown_endpoint_returns_404(server):
    port = server
    code, _ = make_request(port, "/unknown")
    assert code == 404