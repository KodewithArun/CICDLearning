# 🧮 Calculator API (FastAPI)

A simple Calculator REST API built using **FastAPI** and **Pytest**, containerized with **Docker**, designed for learning CI/CD pipelines.

---

## 📁 Project Structure

```text
CICDLearning/
├── app/
│   ├── __init__.py
│   ├── calculator.py       # Core calculator logic (add, subtract, multiply, divide)
│   └── main.py             # FastAPI web routes and request validation
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py  # Unit tests for core calculator math
│   └── test_main.py        # API endpoint tests using TestClient
├── Dockerfile              # Docker container definition
├── docker-compose.yml      # Multi-container orchestration (optional convenience)
├── .dockerignore           # Excluded files from Docker build context
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Testing & development dependencies
└── README.md
```

---

## 🚀 Getting Started Locally

### 1. Create and Activate a Virtual Environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements-dev.txt
```

### 3. Run the Development Server

```bash
uvicorn app.main:app --reload
```

The API will be live at:
- **Root**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 🐳 Running with Docker

### Option A: Using Docker CLI

1. **Build the image**:
   ```bash
   docker build -t cicd-calculator:latest .
   ```

2. **Run the container**:
   ```bash
   docker run -d -p 8000:8000 --name calculator-app cicd-calculator:latest
   ```

3. **Stop the container**:
   ```bash
   docker stop calculator-app && docker rm calculator-app
   ```

### Option B: Using Docker Compose

```bash
# Start container in detached mode
docker compose up -d --build

# View logs
docker compose logs -f

# Stop and remove container
docker compose down
```

---

## 🧪 Running Tests Locally

Run all unit and integration tests with `pytest`:

```bash
pytest -v
```

---

## 📡 API Example Usage

### Calculate endpoint: `POST /calculate`

**Request Body:**
```json
{
  "operation": "add",
  "a": 15,
  "b": 25
}
```

**Response:**
```json
{
  "operation": "add",
  "a": 15.0,
  "b": 25.0,
  "result": 40.0
}
```
Supported operations: `"add"`, `"subtract"`, `"multiply"`, `"divide"`.
