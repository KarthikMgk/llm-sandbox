from datetime import datetime
import uuid
from typing import Literal
from models import TimelineEvent

class Timeline:
    def __init__(self):
        self.events: list[TimelineEvent] = []

    def add_event(self, event_type: Literal["command", "output", "file_read", "file_write", "network", "llm_message", "container_state"], data: dict) -> TimelineEvent:
        event = TimelineEvent(
            id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            type=event_type,
            data=data
        )
        self.events.append(event)
        return event

    def get_events(self, limit: int = 100, offset: int = 0) -> list[TimelineEvent]:
        return self.events[offset:offset + limit]

timeline = Timeline()
