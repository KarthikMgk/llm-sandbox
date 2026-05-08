from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sse_starlette.sse import EventSourceResponse

from config import config
from models import Sandbox
from sandbox_manager import manager
from timeline import timeline
from llm_client import LLMClient, get_system_prompt
from terminal_handler import TerminalHandler
import docker

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="LLM Sandbox", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

terminal_handler = TerminalHandler(docker.from_env())

@app.post("/api/config")
async def set_config(api_key: str, model: str, container_image: str, agent_key: str):
    config.api_key = api_key
    config.model = model
    config.container_image = container_image
    config.agent_key = agent_key
    return {"status": "ok"}

@app.post("/api/sandbox/start")
async def start_sandbox():
    if not config.agent_key:
        raise HTTPException(status_code=400, detail="Agent key not configured")
    sandbox = manager.start_sandbox(config.container_image, config.agent_key)
    timeline.add_event("container_state", {"action": "started", "sandbox_id": sandbox.id})
    return sandbox

@app.post("/api/sandbox/stop")
async def stop_sandbox(sandbox_id: str):
    success = manager.stop_sandbox(sandbox_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sandbox not found")
    timeline.add_event("container_state", {"action": "stopped", "sandbox_id": sandbox_id})
    return {"status": "stopped"}

@app.get("/api/sandbox/status")
async def get_status(sandbox_id: str):
    sandbox = manager.get_status(sandbox_id)
    if not sandbox:
        raise HTTPException(status_code=404, detail="Sandbox not found")
    return sandbox

@app.get("/api/timeline")
async def get_timeline(limit: int = 100, offset: int = 0):
    return timeline.get_events(limit, offset)

@app.post("/api/sandbox/terminal/input")
async def send_command(sandbox_id: str, command: str):
    sandbox = manager.get_status(sandbox_id)
    if not sandbox or not sandbox.container_id:
        raise HTTPException(status_code=404, detail="Sandbox not found")
    output, exit_code = terminal_handler.exec_command(sandbox.container_id, command)
    timeline.add_event("command", {"sandbox_id": sandbox_id, "command": command})
    timeline.add_event("output", {"sandbox_id": sandbox_id, "output": output, "exit_code": exit_code})
    return {"output": output, "exit_code": exit_code}

@app.post("/api/llm/chat")
async def send_to_llm(sandbox_id: str, user_message: str):
    if not config.api_key:
        raise HTTPException(status_code=400, detail="API key not configured")
    llm = LLMClient(config.api_key, config.model)
    messages = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": user_message}
    ]
    response = llm.chat(messages)
    timeline.add_event("llm_message", {"sandbox_id": sandbox_id, "response": response})
    return {"response": response}

@app.get("/api/sandbox/terminal")
async def terminal_stream(sandbox_id: str):
    sandbox = manager.get_status(sandbox_id)
    if not sandbox or not sandbox.container_id:
        raise HTTPException(status_code=404, detail="Sandbox not found")

    async def event_generator():
        for line in terminal_handler.stream_output(sandbox.container_id):
            yield {"event": "output", "data": line}
    return EventSourceResponse(event_generator())
