import asyncio
import docker
from typing import AsyncGenerator


class TerminalHandler:
    def __init__(self, docker_client: docker.DockerClient):
        self.client = docker_client

    def exec_command(self, container_id: str, command: str) -> tuple[str, int]:
        container = self.client.containers.get(container_id)
        result = container.exec_run(
            ["bash", "-c", command],
            stdout=True,
            stderr=True
        )
        output = result.output.decode("utf-8")
        exit_code = result.exit_code
        return output, exit_code

    async def stream_output(
        self, container_id: str, fifo_path: str
    ) -> AsyncGenerator[str, None]:
        container = self.client.containers.get(container_id)
        try:
            container.exec_run(
                ["bash", "-c", f"mkfifo {fifo_path} && tail -f {fifo_path}"],
                detach=True
            )
        except Exception:
            pass

        while True:
            await asyncio.sleep(0.1)
            yield ""