# Deployment Guide

This application is ready to be deployed on Render. Follow these steps:

## Prerequisites
1.  **GitHub Account**: You need a GitHub account to host your code.
2.  **Render Account**: Sign up at [render.com](https://render.com/).

## Step 1: Push Code to GitHub
1.  Create a new repository on GitHub.
2.  Push your code to the new repository:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin <your-repo-url>
    git push -u origin main
    ```

## Step 2: Create Web Service on Render
1.  Log in to your Render dashboard.
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub account and select the repository you just created.
4.  Configure the service:
    *   **Name**: Choose a name for your app.
    *   **Region**: Select the region closest to you.
    *   **Branch**: `main`
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app:app` (Render should auto-detect this from `Procfile`)
5.  Select **Free** instance type.
6.  Click **Create Web Service**.

## Step 3: Monitor Deployment
Render will start building your app. You can watch the logs in the dashboard. Once the build finishes, your app will be live at the provided URL (e.g., `https://your-app-name.onrender.com`).
