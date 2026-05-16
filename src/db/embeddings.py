import ollama
from src.config import OLLAMA_URL, EMBEDDING_MODEL, MAX_EMBED_CHARS

# Initialize the client with the configured host
_client = ollama.Client(host=OLLAMA_URL)

def embed_query(text: str) -> list[float]:
    """Embed a query string using the official Ollama library."""
    if len(text) > MAX_EMBED_CHARS:
        text = text[:MAX_EMBED_CHARS]

    response = _client.embed(
        model=EMBEDDING_MODEL,
        input=text
    )
    
    # The library returns a response object where .embeddings is a list of lists
    return response.embeddings[0]
