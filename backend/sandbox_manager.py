import docker
import uuid
from datetime import datetime

from backend.models import Sandbox


client = docker.from_env()


class SandboxManager:
    def __init__(self):
        self.sandboxes: dict[str, Sandbox] = {}

    def start_sandbox(self, image: str, agent_key: str) -> Sandbox:
        container = client.containers.run(
            image,
            detach=True,
            tty=True,
            stdin_open=True,
            environment={"AGENT_KEY": agent_key}
        )
        sandbox = Sandbox(
            id=str(uuid.uuid4())[:8],
            status="running",
            container_id=container.id,
            started_at=datetime.utcnow(),
            image=image
        )
        self.sandboxes[sandbox.id] = sandbox
        return sandbox

    def stop_sandbox(self, sandbox_id: str) -> bool:
        if sandbox_id not in self.sandboxes:
            return False
        sandbox = self.sandboxes[sandbox_id]
        if sandbox.container_id:
            container = client.containers.get(sandbox.container_id)
            container.stop()
        sandbox.status = "stopped"
        return True

    def get_status(self, sandbox_id: str) -> Sandbox | None:
        return self.sandboxes.get(sandbox_id)


manager = SandboxManager()