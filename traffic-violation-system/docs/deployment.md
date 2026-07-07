# Deployment Documentation

This document describes the instructions, setup steps, and environment variables needed to build and run the system in a Docker containerized production environment.

---

## 1. System Components

* **db**: PostgreSQL 15 database container.
* **backend**: FastAPI application running on Python 3.10 with Uvicorn.
* **frontend**: React SPA built with Vite and Tailwind CSS v4.
* **nginx**: Reverse proxy mapping incoming traffic (routing requests to backend APIs or frontend static assets).

---

## 2. Docker Compose Commands

To deploy the entire stack, run the following command from the `deployment/` directory:

```bash
cd traffic-violation-system/deployment
docker-compose up -d --build
```

### Useful Management Commands:

* **Stop services**:
  ```bash
  docker-compose down
  ```
* **View container logs**:
  ```bash
  docker-compose logs -f [service_name]
  ```
* **Rebuild a specific service**:
  ```bash
  docker-compose up -d --build backend
  ```

---

## 3. Environment Variables Configuration

The backend reads credentials from `.env`. In the production environment, the DB host is mapped to the PostgreSQL service container:

| Variable | Development Value | Production Value |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/traffic_violations` | `postgresql://postgres:postgres@db:5432/traffic_violations` |
| `APP_ENV` | `development` | `production` |
| `DEBUG` | `true` | `false` |
