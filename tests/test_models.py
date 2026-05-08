import pytest
from datetime import datetime

from backend.models import Sandbox, TimelineEvent, TerminalMessage


def test_sandbox_model():
    sandbox = Sandbox(
        id="test123",
        status="running",
        container_id="abc123",
        started_at=datetime.utcnow(),
        image="ubuntu:22.04"
    )
    assert sandbox.id == "test123"
    assert sandbox.status == "running"
    assert sandbox.image == "ubuntu:22.04"


def test_timeline_event_model():
    event = TimelineEvent(
        id="evt1",
        timestamp=datetime.utcnow(),
        type="command",
        data={"command": "ls"}
    )
    assert event.type == "command"
    assert event.data["command"] == "ls"


def test_terminal_message_model():
    msg = TerminalMessage(
        type="output",
        content="hello world",
        timestamp=datetime.utcnow()
    )
    assert msg.type == "output"
    assert msg.content == "hello world"