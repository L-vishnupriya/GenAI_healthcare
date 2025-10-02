FROM python:3.11-slim-bookworm

WORKDIR /app

# Install dependencies using built-in pip
# The system python has pip pre-installed, no need to install 'uv' or 'pip install uv'
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Create data directory for SQLite DB (will be mounted by volume)
RUN mkdir -p data

EXPOSE 8000