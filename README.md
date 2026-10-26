# DevOps Task Manager

A full-stack task management application built using Docker Compose, Flask, MySQL, and Nginx. This project demonstrates containerization, API development, database integration, and deployment practices used in DevOps.

## Architecture

- **Frontend:** HTML, CSS, JavaScript, and Nginx
- **Backend:** Python and Flask REST API
- **Database:** MySQL 8.4
- **Containerization:** Docker and Docker Compose

The frontend communicates with the Flask backend through Nginx. The backend connects to MySQL to store and retrieve tasks.

## Features

- Create tasks
- View saved tasks
- Mark tasks as completed
- Delete tasks
- Persistent database storage
- Container health checks
- Separate Docker networks for frontend and backend services
- Environment variables for database credentials

## Project Structure

```text
devops-capstone-task-manager/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── database/
│   └── init.sql
├── frontend/
│   ├── index.html
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Prerequisites

- Docker Engine
- Docker Compose v2
- Git

## Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/pranavchangan2005-cyber/devops-capstone-task-manager.git
   cd devops-capstone-task-manager
   ```

2. Create a `.env` file:

   ```bash
   nano .env
   ```

3. Add database credentials:

   ```dotenv
   DB_PASSWORD=replace_with_a_strong_password
   DB_ROOT_PASSWORD=replace_with_a_strong_root_password
   ```

   Use your own strong passwords. Do not commit `.env` to Git.

4. Start the application:

   ```bash
   docker compose up -d --build
   ```

5. Open the application in your browser:

   `http://localhost:8080`

## Useful Commands

Check container status:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs
```

Stop the application:

```bash
docker compose down
```

Stop containers without deleting the database volume:

```bash
docker compose down
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Check application and database health |
| GET | `/api/tasks` | List tasks |
| POST | `/api/tasks` | Create a task |
| PATCH | `/api/tasks/<id>` | Update task completion |
| DELETE | `/api/tasks/<id>` |
