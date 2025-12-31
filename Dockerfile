FROM python:3.11-slim

# Install ping utility (iputils-ping) for network checks
RUN apt-get update && apt-get install -y \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main application and entrypoint script
COPY main.py .
COPY docker-entrypoint.sh .

# Make entrypoint script executable
RUN chmod +x docker-entrypoint.sh

# Run as non-root user for security (ping will still work with proper capabilities)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Default entrypoint
ENTRYPOINT ["./docker-entrypoint.sh"]

