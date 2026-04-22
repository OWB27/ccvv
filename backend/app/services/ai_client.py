import json
import urllib.error
import urllib.request
from typing import Any

from app.core.config import settings


class AiClientError(Exception):
    """Raised when the configured AI provider cannot return valid JSON."""


def request_json_object(
    system_prompt: str,
    user_prompt: str,
    timeout: int = 30,
) -> dict[str, Any]:
    if not settings.AI_API_KEY:
        raise AiClientError("AI_API_KEY or OPENAI_API_KEY is not configured.")

    payload = {
        "model": settings.AI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }

    request = urllib.request.Request(
        url=f"{settings.AI_BASE_URL.rstrip('/')}/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.AI_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
        content = response_payload["choices"][0]["message"]["content"]
        data = json.loads(content)
    except (
        urllib.error.URLError,
        TimeoutError,
        json.JSONDecodeError,
        KeyError,
        IndexError,
        TypeError,
    ) as exc:
        raise AiClientError("AI request failed or returned invalid JSON.") from exc

    if not isinstance(data, dict):
        raise AiClientError("AI response content is not a JSON object.")

    return data
