# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY bot.py .
COPY database.py .
COPY config.py .

# Copy config.yml only if it exists (optional, since we support env var only)
COPY config.yml* ./ || true

# Create volume for database persistence
VOLUME /app/data

# Set environment variable for database location
ENV DB_PATH=/app/data/bot_data.db

# Run the bot
CMD ["python", "-u", "bot.py"]
