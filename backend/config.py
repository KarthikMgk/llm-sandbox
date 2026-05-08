from pydantic import BaseModel
from typing import Optional

class Config(BaseModel):
    api_key: Optional[str] = None
    model: str = "minimax-01"
    container_image: str = "ubuntu:22.04"
    agent_key: Optional[str] = None
    agent_url: str = "http://localhost:8999"
    sandbox_timeout: int = 300

config = Config()
