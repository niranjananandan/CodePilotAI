import json
import urllib.error
import urllib.request


MODEL_NAME = "qwen2.5-coder:1.5b"
OLLAMA_API_URL = "http://127.0.0.1:11434/api/chat"


def chat_with_model(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are CodePilot AI, a coding and debugging assistant. "
                    "Give clear, accurate and practical answers."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "stream": False,
    }

    request = urllib.request.Request(
        OLLAMA_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        message = result.get("message", {})
        answer = message.get("content", "").strip()

        if not answer:
            raise RuntimeError("The AI model returned an empty response.")

        return answer

    except urllib.error.URLError as error:
        raise RuntimeError(
            "Cannot connect to Ollama. Check whether Ollama is running."
        ) from error


if __name__ == "__main__":
    print("CodePilot AI: Connecting to the local AI model...")

    try:
        answer = chat_with_model(
            "Explain in one sentence what a Python debugging agent does."
        )
        print("\nAI Response:")
        print(answer)
        print("\nConnection test completed.")

    except (RuntimeError, TimeoutError) as error:
        print(f"\nError: {error}")