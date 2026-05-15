import requests
from src.config import OLLAMA_URL, EMBEDDING_MODEL, MAX_EMBED_CHARS

def embed_query(text: str) -> list[float]:
    """Embed a query string using the configured Ollama embedding model."""
    if len(text) > MAX_EMBED_CHARS:
        text = text[:MAX_EMBED_CHARS]

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBEDDING_MODEL,
            "prompt": text
        }
    )
    response.raise_for_status()
    return response.json()["embedding"]
