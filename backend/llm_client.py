import httpx
from config import config

class LLMClient:
    def __init__(self, api_key: str, model: str = "minimax-01"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.minimax.chat/v1"

    def chat(self, messages: list[dict]) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages
        }
        response = httpx.post(f"{self.base_url}/text/chatcompletion_v2", json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

def get_system_prompt() -> str:
    return config.system_prompt
