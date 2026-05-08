import pytest
from sandbox_manager import SandboxManager
from unittest.mock import MagicMock, patch

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
