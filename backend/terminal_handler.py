import docker
import asyncio
from typing import AsyncGenerator
from datetime import datetime

class TerminalHandler:
    def __init__(self, docker_client: docker.DockerClient):
        self.client = docker_client

    def exec_command(self, container_id: str, command: str) -> tuple[str, int]:
        container = self.client.containers.get(container_id)
        result = container.exec_run(["bash", "-c", command], stdout=True, stderr=True)
        output = result.output.decode("utf-8")
        exit_code = result.exit_code
        return output, exit_code

    async def stream_output(self, container_id: str) -> AsyncGenerator[str, None]:
        container = self.client.containers.get(container_id)
        container.exec_run(
            ["bash", "-c", "mkfifo /tmp/terminal_stream && tail -f /tmp/terminal_stream"],
            socket=True,
            demux=False,
            stream=True
        )
        with open("/tmp/terminal_stream", "r") as fifo:
            while True:
                line = fifo.readline()
                if line:
                    yield line.rstrip("\n")
                else:
                    await asyncio.sleep(0.1)
