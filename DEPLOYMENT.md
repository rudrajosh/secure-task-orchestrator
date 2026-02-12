# Deployment Guide (Render.com)

This guide explains how to deploy the Secure Task Orchestrator to **Render**, a cloud platform that offers a free tier for web services.

## Prerequisites

1.  **Code on GitHub**: Ensure your latest code (including `Procfile` and `requirements.txt`) is pushed to GitHub.
2.  **Render Account**: Sign up at [render.com](https://render.com/).

## Step 1: Prepare the Project (Already Done)

We have already:
-   Added `gunicorn` to `requirements.txt` (This is the production server).
-   Created a `Procfile` with the command `web: gunicorn run:app`.

## Step 2: Create a Web Service on Render

1.  Log in to your Render dashboard.
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub account and select the `secure-task-orchestrator` repository.
4.  **Name**: Give your service a name (e.g., `secure-task-orchestrator`).
5.  **Region**: Choose the one closest to you (e.g., Singapore, Frankfurt).
6.  **Branch**: `main`.
7.  **Root Directory**: Leave blank.
8.  **Runtime**: Python 3.
9.  **Build Command**: `pip install -r requirements.txt`
10. **Start Command**: `gunicorn run:app`
11. **Instance Type**: Select **Free**.

## Step 3: Configure Environment Variables

Scroll down to the **Environment Variables** section and add the following keys (matching your `.env` file):

| Key | Value |
| :--- | :--- |
| `SECRET_KEY` | (Generate a strong random string) |
| `JWT_SECRET_KEY` | (Generate a strong random string) |
| `MAIL_SERVER` | `smtp.gmail.com` |
| `MAIL_PORT` | `587` |
| `MAIL_USE_TLS` | `True` |
| `MAIL_USERNAME` | `your-email@gmail.com` |
| `MAIL_PASSWORD` | `your-app-password` |
| `DATABASE_URL` | (See Note below) |

**Note on Database**:
-   For the **Free Tier**, Render might not persist SQLite data if the instance restarts.
-   Ideally, use a **PostgreSQL** database.
    -   On Render, click **New +** -> **PostgreSQL**.
    -   Create the database.
    -   Copy the `Internal Database URL`.
    -   Paste it as the `DATABASE_URL` environment variable in your Web Service.

## Step 4: Deploy

1.  Click **Create Web Service**.
2.  Render will start building your app. Watch the logs.
3.  Once the build finishes, you will see a green **Live** badge.
4.  Your URL will be something like `https://secure-task-orchestrator.onrender.com`.

## Step 5: Initialize Database (If using Postgres)

If you switched to Postgres, you'll need to run migrations on the live server.
1.  Go to the **Shell** tab in your Render dashboard for the service.
2.  Run: `flask db upgrade`

## Testing

Use Postman or curl to test your new live URL:
`https://<your-app-name>.onrender.com/auth/otp/request`
