# Secure Task Orchestrator (Flask)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/rudrajosh/secure-task-orchestrator)

## Project Overview

A secure, production-grade RESTful API built with Flask for managing personal tasks. Key features include Email-OTP authentication, JWT-based security, and resource-level authorization.

## Features

-   **Authentication**: Secure Email-OTP flow. No passwords stored.
-   **Task Management**: CRUD operations for tasks with strict ownership enforcement.
-   **Security**:
    -   JWT Access (15 min) and Refresh (7 days) tokens.
    -   Hashed OTPs.
    -   Rate limiting on API endpoints.
    -   Input validation and sanitization.
-   **Audit Logging**: Tracks authentication events and data modifications.
-   **Architecture**:
    -   Application Factory Pattern.
    -   Blueprints for modularity (`auth`, `tasks`).
    -   SQLAlchemy ORM.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rudrajosh/secure-task-orchestrator.git
    cd assignment
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration:**
    Create a `.env` file in the root directory with the following variables:
    ```env
    SECRET_KEY=your-secret-key
    DATABASE_URL=sqlite:///app.db
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=your-email@gmail.com
    MAIL_PASSWORD=your-email-password
    JWT_SECRET_KEY=your-jwt-secret
    ```

5.  **Initialize Database:**
    ```bash
    flask db upgrade
    ```

6.  **Run the Application:**
    ```bash
    flask run
    ```
    The API will be available at `http://localhost:5000`.

## Deployment

Detailed deployment instructions for Render are available in [DEPLOYMENT.md](DEPLOYMENT.md).

## API Endpoints

### Authentication

-   `POST /auth/otp/request`: Request an OTP for login/registration.
    -   Body: `{ "email": "user@example.com" }`
-   `POST /auth/otp/verify`: Verify OTP and get tokens.
    -   Body: `{ "email": "user@example.com", "otp": "123456" }`
-   `POST /auth/refresh`: Refresh access token.
    -   Header: `Authorization: Bearer <refresh_token>`

### Tasks

All task endpoints require `Authorization: Bearer <access_token>`.

-   `GET /tasks/`: List all tasks for the authenticated user.
-   `POST /tasks/`: Create a new task.
    -   Body: `{ "title": "My Task", "description": "...", "status": "Pending" }`
-   `GET /tasks/<id>`: Get a specific task.
-   `PUT /tasks/<id>`: Update a task.
-   `DELETE /tasks/<id>`: Delete a task.

## Audit Logs

Activity logs are stored in the database and track user actions like OTP requests, logins, and task modifications.

## Design Choices

-   **Flask Application Factory**: Allows for easier testing and configuration management.
-   **Blueprints**: Separates concerns into distinct modules (Auth, Tasks).
-   **JWT**: Stateless authentication suitable for REST APIs.
-   **Rate Limiting**: Protects against abuse and brute-force attacks.
