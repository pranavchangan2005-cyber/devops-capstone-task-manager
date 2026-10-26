import os
import time
import logging

import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "user": os.getenv("DB_USER", "appuser"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "taskmanager"),
    "connection_timeout": 5,
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def initialize_database():
    for attempt in range(30):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.commit()
            cursor.close()
            connection.close()
            logger.info("Database initialized")
            return
        except Error as exc:
            logger.warning("Database not ready (attempt %s): %s",
                           attempt + 1, exc)
            time.sleep(2)

    raise RuntimeError("Could not connect to MySQL")


@app.get("/api/health")
def health():
    try:
        connection = get_connection()
        connection.close()
        return jsonify(status="healthy", database="connected"), 200
    except Error:
        return jsonify(status="unhealthy", database="disconnected"), 503


@app.get("/api/tasks")
def list_tasks():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, title, completed, created_at FROM tasks ORDER BY id DESC"
    )
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()

    for task in tasks:
        task["completed"] = bool(task["completed"])
        task["created_at"] = task["created_at"].isoformat()

    return jsonify(tasks)


@app.post("/api/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()

    if not title:
        return jsonify(error="Task title is required"), 400

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
    task_id = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()

    logger.info("Created task id=%s", task_id)
    return jsonify(id=task_id, title=title, completed=False), 201


@app.patch("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True) or {}

    if not isinstance(data.get("completed"), bool):
        return jsonify(error="completed must be true or false"), 400

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE tasks SET completed = %s WHERE id = %s",
        (data["completed"], task_id),
    )
    updated = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()

    if not updated:
        return jsonify(error="Task not found"), 404

    return jsonify(message="Task updated")


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    deleted = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()

    if not deleted:
        return jsonify(error="Task not found"), 404

    logger.info("Deleted task id=%s", task_id)
    return jsonify(message="Task deleted")


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)
