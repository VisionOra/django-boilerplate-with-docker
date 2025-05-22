# Leads Analyser

A Django-based application for analyzing and managing leads with advanced AI features. Built with modern technologies and best practices for scalability and maintainability.

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-red?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
  - [Development Mode](#development-mode)
  - [Production Mode](#production-mode)
- [Docker Configuration](#docker-configuration)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Common Commands](#common-commands)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## ✨ Features

- Authentication and user management
- Lead tracking and analysis
- AI-powered resume parsing (via Azure OpenAI)
- RESTful API with comprehensive documentation
- Background task processing with Celery
- Containerized with Docker for easy deployment

## 🔧 Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Poetry (for local development)
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/leads_analyser.git
cd leads_analyser
```

### 2. Environment Setup

Create a `.env` file in the project root with the following variables (adjust as needed):

```
# Django Settings
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True

# Database Settings
DB_NAME=leads_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis Settings
REDIS_PORT=6379

# Web Settings
WEB_PORT=8000

# For AI Features (optional)
AZURE_OPENAI_ENDPOINT=https://your-azure-openai-endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2024-05-01-preview
AZURE_OPENAI_REGION=your-azure-region
```

## 🖥️ Running the Application

### Development Mode

Run the application in development mode with hot-reloading:

```bash
docker compose --profile development up --build
```

This starts:
- PostgreSQL database
- Redis for caching and Celery
- Django development server on port 8000

### Production Mode

Run the application in production mode:

```bash
docker compose --profile production up --build
```

This uses Gunicorn to serve the application with optimized settings.

## 🔄 Docker Configuration

The application uses Docker Compose with multiple service definitions:

- `db`: PostgreSQL database
- `redis`: Redis for caching and Celery
- `web`: Django application (production)
- `web-dev`: Django application (development)

### Multi-Stage Dockerfile

The application uses a multi-stage Dockerfile:
- `base`: Common dependencies and settings
- `development`: Includes dev dependencies and uses Django's development server
- `production`: Optimized for production with Gunicorn

## 📁 Project Structure

```
leads_analyser/
├── apps/
│   ├── authentication/    # User authentication and management
│   ├── config/            # Project configuration 
│   │   ├── settings/      # Environment-specific settings
│   │   ├── celery.py      # Celery configuration
│   │   └── urls.py        # URL routing configuration
│   ├── Dockerfile         # Multi-stage Dockerfile
│   └── manage.py          # Django management script
├── docker-compose.yml     # Docker Compose configuration
├── pyproject.toml         # Poetry project configuration
├── poetry.lock            # Poetry dependency lock
└── README.md              # Project documentation
```

## 🌐 Accessing the Application

Once running, you can access:

- API: http://localhost:8000/api/
- Admin Interface: http://localhost:8000/admin/
- API Documentation: http://localhost:8000/api/schema/swagger-ui/

## 📋 Environment Variables

Key environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | `None` (required) |
| `DJANGO_DEBUG` | Debug mode | `True` |
| `DB_NAME` | Database name | `leads_db` |
| `DB_USER` | Database username | `postgres` |
| `DB_PASSWORD` | Database password | `postgres` |
| `DB_HOST` | Database hostname | `db` |
| `DB_PORT` | Database port | `5432` |
| `WEB_PORT` | Web server port | `8000` |
| `REDIS_PORT` | Redis port | `6379` |

## ⚙️ Common Commands

### Running Migrations

```bash
# Create migrations
docker compose exec web python apps/manage.py makemigrations

# Apply migrations
docker compose exec web python apps/manage.py migrate
```

### Creating a Superuser

```bash
docker compose exec web python apps/manage.py createsuperuser
```

### Accessing Django Shell

```bash
docker compose exec web python apps/manage.py shell
```

### Running Tests

```bash
docker compose exec web python apps/manage.py test
```

### Viewing Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f web
```

## ❓ Troubleshooting

### Container Issues

If containers are not starting properly:

```bash
# Stop all containers
docker compose down

# Remove all containers and volumes
docker compose down -v

# Rebuild and start containers
docker compose up --build
```

### Database Issues

If you need to reset the database:

```bash
# Stop containers
docker compose down

# Remove volumes
docker compose down -v

# Start containers again
docker compose up -d

# Run migrations
docker compose exec web python apps/manage.py migrate
```

## 🧑‍💻 Local Development (without Docker)

For local development without Docker:

1. Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Setup local PostgreSQL and update environment variables accordingly.

4. Run the development server:
```bash
poetry run python apps/manage.py runserver
```

## 🔍 Code Quality

This project uses several tools to maintain code quality:

- `flake8` for linting
- `black` for code formatting
- `isort` for import sorting

To run these tools:

```bash
# Format code
poetry run black .
poetry run isort .

# Check code quality
poetry run flake8 .
```

## 🤝 Contributing

1. Create a new branch
2. Make your changes
3. Run tests and ensure code quality checks pass
4. Submit a pull request

## 📝 License

[Your License Information]

## Applications

1. **Authentication** - User authentication and management
2. **Blog** - Blog posts and categories management
3. **Portfolio** - Portfolio projects and categories management
4. **Contact** - Contact form and message management
5. **Email Service** - Email sending and management
6. **Reviews** - Client reviews management
7. **Newsletter** - Newsletter subscriptions management
8. **Visitor Event Tracking** - Analytics and event tracking
9. **Voice Assistant** - Voice assistant integration
10. **Jobs** - Career opportunities and job application management
11. **Candidates** - Talent management and candidate tracking

## AI Features

### Resume Parser with Azure OpenAI

The Candidates app includes an AI-powered resume parser that automatically extracts information from candidate resumes. This feature uses the Azure OpenAI service with Azure AD authentication to extract structured data from various resume formats (PDF, DOCX, TXT).

#### Setup

1. Ensure you have configured your Azure AD permissions for Azure OpenAI access, and set the Azure OpenAI details in your settings:

```python
AZURE_OPENAI_ENDPOINT = "https://your-azure-openai-endpoint.openai.azure.com/"
AZURE_OPENAI_DEPLOYMENT = "gpt-4"
AZURE_OPENAI_API_VERSION = "2024-05-01-preview"
AZURE_OPENAI_REGION = "your-azure-region"
```

2. Install the required dependencies:

```bash
pip install openai azure-identity langchain pydantic pypdf docx2txt
```

#### Features

- Automatic extraction of candidate details from resumes
- Identification of personal information, work experience, education, skills, and more
- Integration with the application process
- Azure AD authentication for secure access
- Optional API key authentication as fallback
