import os
import yaml
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
_ROOT = Path(__file__).parent.parent
load_dotenv(dotenv_path=_ROOT / ".env")

# External Services
MONGODB_URI = os.getenv("MONGODB_URI")
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")

if not MONGODB_URI:
    print("Warning: MONGODB_URI not found in environment.")
if not CEREBRAS_API_KEY:
    print("Warning: CEREBRAS_API_KEY not found in environment.")

# Load YAML configuration
_CONFIG_PATH = _ROOT / "config" / "config.yaml"
with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
    _config = yaml.safe_load(f)

# MongoDB Configuration
DB_NAME = _config["database"]["name"]
MANUAL_COLLECTION = _config["database"]["collections"]["manual"]
PRODUCTS_COLLECTION = _config["database"]["collections"]["products"]
MANUAL_INDEX_NAME = _config["database"]["indexes"]["manual"]
PRODUCTS_INDEX_NAME = _config["database"]["indexes"]["products"]

# Ollama Configuration
# Prefer OLLAMA_URL env var so Docker Compose can inject the sidecar hostname
# without modifying config.yaml. Falls back to config.yaml for local runs.
OLLAMA_URL = os.getenv("OLLAMA_URL") or _config["embedding"]["ollama_url"]
EMBEDDING_MODEL = _config["embedding"]["model"]
EMBEDDING_DIM = _config["embedding"]["dimension"]
MAX_EMBED_CHARS = _config["embedding"]["max_chars"]

# Agent Configuration
AGENT_MODEL = _config["agent"]["model"]

# Streamlit App Configuration
APP_TITLE = _config["app"]["title"]
APP_ICON = _config["app"]["icon"]
APP_LAYOUT = _config["app"]["layout"]
APP_WELCOME = _config["app"]["welcome_message"]
