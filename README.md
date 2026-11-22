# 🚀 CI/CD Learning & AI Projects

This repository contains both a **FastAPI Calculator API** and a **Streamlit AI Chatbot (Groq + LangChain)**, configured with **automated testing, linting with Ruff, and Docker containerization**.

---

## 🤖 1. Groq AI Chatbot (LangChain + Streamlit)

An interactive conversational AI chatbot powered by **Groq Cloud** ultra-fast inference and **LangChain**, with a sleek **Streamlit** user interface.

### Features
- ⚡ **Ultra-fast inference** using Groq's Llama 3.3, Llama 3.1, Mixtral, and Gemma models.
- 🔐 **Secure Credential Handling**: Reads `GROQ_API_KEY` directly from `.env` file (or allows sidebar key input).
- 💬 **Streaming Responses**: Real-time token streaming as the LLM responds.
- 🎛️ **Sidebar Controls**: Model selection, temperature slider, custom system prompt, and chat clearing.

### Quickstart for the Chatbot

1. **Set your Groq API Key**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Add your API key inside `.env`:
   ```env
   GROQ_API_KEY=gsk_your_actual_groq_key_here
   ```
   *(Get your free API key at [https://console.groq.com/keys](https://console.groq.com/keys))*

2. **Run the Streamlit App**:
   ```bash
   streamlit run streamlit_app.py
   ```
   Open your browser at: [http://localhost:8501](http://localhost:8501)

---

## 🧮 2. FastAPI Calculator API

A simple REST API with 13 automated tests, ideal for CI/CD demonstration.

### Run FastAPI Locally:
```bash
uvicorn app.main:app --reload
```
- API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 🧪 Testing and Linting

Run automated test suite (18 unit and integration tests):
```bash
pytest -v
```

Run code formatting & linting checks:
```bash
ruff check .
```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

Located in [`.github/workflows/ci.yml`](.github/workflows/ci.yml):
- Runs automatically on every `git push` or `pull_request` to `main`.
- Sets up Python 3.12 with pip caching.
- Installs development dependencies.
- Runs `ruff check .` for code quality.
- Executes `pytest -v` across all test suites.
