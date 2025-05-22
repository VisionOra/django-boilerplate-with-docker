FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONPATH="/app"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Development stage
FROM base as development

# Install all dependencies including dev dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# The source code will be mounted as a volume during development
# so we don't need to copy it here

# Expose the port
EXPOSE 8000

# Run the development server
CMD ["python", "apps/manage.py", "runserver", "0.0.0.0:8000"]

# Production/Staging stage
FROM base as production

# Install only production dependencies
RUN poetry install --no-interaction --no-ansi --no-root --without dev

# Copy the project
COPY . .

# Expose the port
EXPOSE 8000

# Run with gunicorn for production
CMD ["gunicorn", "--chdir", "apps", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
