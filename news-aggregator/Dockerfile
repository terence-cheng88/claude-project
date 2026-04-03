# News Aggregator - Dockerfile
# Multi-stage build for production

# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Development stage
FROM python:3.11-slim as dev

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Install dev dependencies
RUN pip install --no-cache-dir black isort mypy pytest pytest-asyncio

# Copy application
COPY . .

# Development commands
CMD ["python", "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy requirements
COPY requirements.txt .

# Run pip install
RUN pip install --no-cache-dir -r requirements.txt

# Copy application (exclude dev files)
COPY --from=dev /app/app /app/app
COPY --from=dev /app/agents /app/agents
COPY --from=dev /app/utils /app/utils
COPY --from=dev /app/models /app/models
COPY --from=dev /app/frontend /app/frontend
COPY --from=dev /app/config /app/config
COPY --from=dev /app/requirements.txt /app/requirements.txt

# Set permissions for Python scripts
RUN chmod +x /app/*.py 2>/dev/null || true

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
