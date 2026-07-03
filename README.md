# 🔐 SecretWord API

A secure Password Manager REST API built with **FastAPI**, following Clean Architecture principles and modern backend development practices.

The project was developed as a portfolio application focused on authentication, encryption, security, Docker, and PostgreSQL.

---

# Features

* User registration and authentication
* JWT Access Token authentication
* Refresh Token support
* Secure password hashing with BCrypt
* Hybrid password encryption
* CRUD operations for stored passwords
* SQL database
* Alembic database migrations
* Docker & Docker Compose support
* OpenAPI / Swagger documentation
* Environment variables using `.env`

---

# Tech Stack

* Python 3.14
* FastAPI
* SQLAlchemy
* SQLlite
* Alembic
* Docker
* Docker Compose
* BCrypt
* JWT
* Pydantic

---

# Project Structure

```text
app/
│
├── core/
├── models/
├── routes/
├── schemas/
├── services/
├── dependencies/
│
tests/
│
├── auth/
├── passwords/
├── users/
├── security/
└── integration/
│
data/
│
alembic/
│
docker-compose.yml
Dockerfile
main.py
README.md
requirements
.env

```

---

# Installation

Clone the repository.

```bash
git clone https://github.com/nunesdepedro/SecretWord_API.git
```

Enter the project directory.

```bash
cd SecretWord_API
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install the dependencies.

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+psycopg2://secretword:password@localhost:5432/secretword

SECRET_KEY=your_secret_key

MASTER_KEY=your_master_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

REFRESH_EXPIRE_DAYS=30
```

---

# Running with Docker

```bash
docker compose up -d
```

Run the database migrations.

```bash
alembic upgrade head
```

Start the API.

```bash
uvicorn main:app --reload
```

---

# API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# Security

This project implements several security best practices:

* BCrypt password hashing
* JWT authentication
* Refresh Token mechanism
* Hybrid encryption for stored passwords
* Environment-based secrets
* SQL Injection protection via SQLAlchemy ORM
* Input validation using Pydantic
* Protected endpoints with OAuth2

---

# Learning Goals

This project was created to study and demonstrate knowledge in:

* REST API Design
* Authentication & Authorization
* Cryptography
* Database Design
* Docker
* Clean Architecture
* Backend Security
* Python Backend Development

---

# License

This project is licensed under the MIT License.
