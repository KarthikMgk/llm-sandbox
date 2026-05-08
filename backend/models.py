from pydantic import BaseModel
from typing import Literal, Optional, Any
from datetime import datetime


class Sandbox(BaseModel):
    id: str
    status: Literal["running", "stopped", "error"]
    container_id: Optional[str] = None
    started_at: Optional[datetime] = None
    image: str = "ubuntu:22.04"


class TimelineEvent(BaseModel):
    id: str
    timestamp: datetime
    type: Literal[
        "command", "output", "file_read", "file_write",
        "network", "llm_message", "container_state"
    ]
    data: dict[str, Any]
    container_id: Optional[str] = None


class TerminalMessage(BaseModel):
    type: Literal["input", "output", "error"]
    content: str
    timestamp: datetime