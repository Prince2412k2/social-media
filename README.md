# Project Setup Guide

This guide explains how to set up and run the backend and frontend of this project using Docker, `uv`, `npm`, and Python virtual environments.

## Requirements

* [Node.js / npm](https://nodejs.org/)
* [Python 3.12+](https://www.python.org/)
* [uv](https://pypi.org/project/uv/)
* [Docker](https://www.docker.com/)

---

## Step 0: Environment Setup

1. Copy the example environment file:

```bash
cp .example.env .env
```

2. Edit `.env` to match your local configuration:

```env
# Logging
DJANGO_LOG_LEVEL="INFO"

# GitHub OAuth
GITHUB_CLIENT_ID=<get from GitHub>
GITHUB_CLIENT_SECRET=<get from GitHub>
GITHUB_EMAIL_URL="https://api.github.com/user/emails"

# Google OAuth
GOOGLE_CLIENT_ID=<get from Google>
GOOGLE_CLIENT_SECRET=<get from Google>
GOOGLE_REDIRECT_URI="http://localhost:8080/auth/callback"

# Database
POSTGRES_LOCAL="postgresql://postgres:12345678@localhost:5432/postgres"

# Django secret key
SECRET_KEY="django-insecure-wq0zj0ai6oq6wsn0q5ja$w5xwn_v6s(dokpi1@m1apputpde!x"
```

> Make sure to replace placeholders with your actual client IDs and secrets.

---

## Step 1: Run `uv` sync at Root

From the project root:

```bash
uv sync
```

---

## Step 2: Activate Python Virtual Environment

```bash
source .venv/bin/activate
```

---

## Step 3: Start MinIO and PostgreSQL Servers

### PostgreSQL

```bash
docker run -d \
  --name bookish \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=12345678 \
  -e POSTGRES_DB=postgres \
  -p 5432:5432 \
  postgres:16
```

### MinIO

```bash
docker run -p 9000:9000 -p 9001:9001 \
  --name minio \
  -e "MINIO_ROOT_USER=123456789" \
  -e "MINIO_ROOT_PASSWORD=123456789" \
  -v $(pwd)/data:/data \
  quay.io/minio/minio server /data --console-address ":9001"
```

> **Note:** There are bash scripts in the root directory if you need shortcuts for starting these services.

---

## Step 4: Run Backend

Use `poe` to run backend tasks:

```bash
poe make
poe migrate
poe run
```

---

## Step 5: Run Frontend

1. Navigate to the frontend folder:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

---

After these steps, your backend, frontend, PostgreSQL, and MinIO services should be running and ready for development.

---

