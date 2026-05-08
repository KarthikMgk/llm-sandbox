import pytest
from agent.sidecar import AGENT_KEY, PORT

def test_agent_key():
    assert AGENT_KEY is not None

def test_agent_port():
    assert PORT == 8999