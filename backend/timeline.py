import uuid
from datetime import datetime

from backend.models import TimelineEvent


class Timeline:
    def __init__(self):
        self.events: list[TimelineEvent] = []

    def add_event(
        self,
        event_type: str,
        data: dict,
        container_id: str | None = None
    ) -> TimelineEvent:
        event = TimelineEvent(
            id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            type=event_type,
            data=data,
            container_id=container_id
        )
        self.events.append(event)
        return event

    def get_events(self, limit: int = 100, offset: int = 0) -> list[TimelineEvent]:
        return self.events[offset:offset + limit]


timeline = Timeline()