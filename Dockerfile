# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the package
COPY horizon_core/ ./horizon_core/
COPY pyproject.toml setup.py README.md LICENSE ./

# Install the package
RUN pip install --no-cache-dir -e .

# Create non-root user
RUN useradd -m -u 1000 horizon && \
    chown -R horizon:horizon /app

# Switch to non-root user
USER horizon

# Set Python path
ENV PYTHONPATH=/app

# Default command
CMD ["python", "-m", "horizon_core"]
