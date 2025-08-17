# Use Python 3.13 slim base image for smaller size
FROM python:3.13-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies for Python packages and curl for health check
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

COPY 

# Install Python dependencies using uv and clean up cache
RUN uv sync --frozen --no-dev && \
    uv cache clean && \
    rm -rf /tmp/* /var/tmp/*

# Expose Streamlit's default port
EXPOSE 8501

# Set environment variables for Streamlit and resource optimization
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false \
    STREAMLIT_SERVER_MAX_UPLOAD_SIZE=50 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Health check to ensure the app is running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the Streamlit application
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
