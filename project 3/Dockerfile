# Build stage for frontend
FROM node:18-slim AS frontend-builder

WORKDIR /app

# Copy frontend files
COPY package*.json ./
COPY vite.config.ts ./
COPY tsconfig*.json ./
COPY postcss.config.js ./
COPY tailwind.config.js ./
COPY templates/ ./templates/

# Install dependencies and build
RUN npm install


# Final stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=jobfinder.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy Django project files
COPY manage.py .
COPY jobfinder/ ./jobfinder/
COPY jobs/ ./jobs/
COPY job_dashboard/ ./job_dashboard/
COPY jobs/templates/ ./jobs/templates/
COPY templates/ ./templates/

# Copy built frontend from builder stage


# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Create volume for database
VOLUME ["/app/db"]

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"] 