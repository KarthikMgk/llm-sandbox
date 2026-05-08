import pytest
from unittest.mock import MagicMock, patch

from backend.sandbox_manager import SandboxManager


@pytest.fixture
def mock_docker():
    with patch("docker.from_env") as mock:
        container = MagicMock()
        container.id = "mock-container-id"
        mock.return_value.containers.run.return_value = container
        yield mock


def test_sandbox_creation(mock_docker):
    manager = SandboxManager()
    sandbox = manager.start_sandbox("ubuntu:22.04", "test-key")
    assert sandbox.status == "running"
    assert sandbox.image == "ubuntu:22.04"


def test_sandbox_stop(mock_docker):
    manager = SandboxManager()
    sandbox = manager.start_sandbox("ubuntu:22.04", "test-key")
    result = manager.stop_sandbox(sandbox.id)
    assert result is True
    assert sandbox.status == "stopped"


def test_get_status_nonexistent(mock_docker):
    manager = SandboxManager()
    result = manager.get_status("nonexistent")
    assert result is None