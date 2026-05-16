# 🛒 Tokoku Assistant

Tokoku Assistant is a professional AI-powered shopping assistant built with **Streamlit** and the **Google ADK**. It features a Retrieval-Augmented Generation (RAG) system that connects to a **MongoDB Atlas** vector database and uses a local **Ollama** instance for high-performance multilingual embeddings.

## 🚀 Quick Start (with Docker)

This project is fully containerized using Docker Compose. The setup includes:
1.  **App**: The Streamlit frontend.
2.  **Ollama**: A local embedding server (sidecar).
3.  **Ollama-Init**: An automatic setup service that pulls the required embedding model on first run.

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- A **MongoDB Atlas** URI with vector search enabled.
- A **Cerebras API Key** (for the LLM).

### 2. Configuration
Create a `.env` file in the root directory and fill in your credentials:
```bash
cp .env.example .env
```
Edit `.env` with your keys:
- `MONGODB_URI`: Your MongoDB connection string.
- `CEREBRAS_API_KEY`: Your Cerebras API key.

### 3. Run the Application
In your terminal, run:
```bash
docker compose up --build
```

**What happens next?**
- Docker will build the application image.
- The `ollama-init` service will automatically download the `nomic-embed-text-v2-moe` model (~1.4 GB). **This only happens once.**
- Once the model is ready, the Streamlit app will start.

### 4. Access the App
Open your browser and go to:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 🎬 Demonstration

View the demo video here: [Tokoku Assistant Demonstration](https://drive.google.com/file/d/10q1anQvyYmMFS1oDWJF6wT444qSy8gA3/view?usp=sharing)

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Agent Framework**: Google ADK (Agent Development Kit)
- **LLM**: `qwen-3-235b-a22b-instruct-2507` (via [Cerebras](https://cloud.cerebras.ai/) API)
- **Embeddings**: `nomic-embed-text-v2-moe` (via local Ollama)
- **Database**: MongoDB Atlas (Vector Search)

## 📁 Project Structure
- `app/`: Streamlit UI components and main application logic.
- `src/`: Core logic, including the agent runner and database integrations.
- `config/`: YAML configuration for models and database indexes.
- `Dockerfile` & `docker-compose.yml`: Containerization setup.
- `requirements-app.txt`: Optimized dependencies for the production container.

---

## 🛑 Troubleshooting
- **Model Not Found**: If you see a "model not found" error, it means the `ollama-init` service is still pulling the model. Check your terminal logs for progress.
- **Connection Refused**: Ensure Docker Desktop is running and that your `.env` file contains valid credentials.
