FROM python:3.12-slim

WORKDIR /app

# Set environment variables:
# - PYTHONDONTWRITEBYTECODE: prevents Python from writing .pyc files
# - PYTHONUNBUFFERED: ensures logs are output immediately to console
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/

# Expose the port FastAPI runs on
EXPOSE 8000

# Run FastAPI using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
