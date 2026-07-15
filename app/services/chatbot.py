import json
import os
from pathlib import Path
from urllib import request


class ChatbotService:
    def __init__(self):
        self._load_env()
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def _load_env(self):
        base_dir = Path(__file__).resolve().parent.parent.parent
        env_paths = [
            base_dir / "chatbot.env",
            base_dir / ".env",
        ]

        for env_path in env_paths:
            if not env_path.exists():
                continue

            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue

                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
                break

    def ask(self, message: str) -> str:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return "OpenAI API 키가 아직 없어요. chatbot.env에 OPENAI_API_KEY를 설정하면 바로 답변할 수 있어요."

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "당신은 구미·경북권 여행 정보 챗봇입니다. 관광지, 음식점, 축제, 숙박, 쇼핑 정보를 친절하고 짧게 답하세요."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        req = request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            return f"챗봇 호출 중 오류가 발생했어요: {exc}"

        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            return "챗봇 응답 형식이 올바르지 않았어요."