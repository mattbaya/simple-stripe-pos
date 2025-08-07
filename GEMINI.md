# GEMINI Project Context: Community POS System

## Project Overview

This project is a lightweight, containerized point-of-sale (POS) application designed for in-person donation and membership payments using the Stripe Terminal. It provides a simple web interface for volunteers to process payments without needing a complex backend system or local database.

**Key Technologies:**
*   **Backend:** Python 3, Flask
*   **Payments:** Stripe Terminal API
*   **Containerization:** Docker, Docker Compose
*   **Frontend:** Basic HTML with embedded CSS and JavaScript
*   **Email:** SMTP or Google OAuth2 for sending receipts and notifications

**Architecture:**
The application runs as a single Docker container orchestrated by Docker Compose.
*   `app/main.py`: The core Flask application that handles web requests, interacts with the Stripe API, and sends emails.
*   `templates/index.html`: A single-page web interface for volunteers to initiate payments.
*   `Dockerfile`: Defines the Docker image for the application, based on a Python image.
*   `docker-compose.yml`: Manages the application container, network, and environment variables.
*   `.env`: A file (gitignored) that stores all necessary secrets and configuration, such as Stripe API keys, email credentials, and location IDs. An example is provided in `.env.example`.
*   `generate_oauth_token.py`: A utility script to generate a Google OAuth2 refresh token for sending emails via Gmail.

## Building and Running

The application is designed to be run entirely through Docker Compose.

**1. Configuration:**
*   Copy the example environment file: `cp .env.example .env`
*   Edit the `.env` file to add your Stripe API keys, Stripe Location ID, and email credentials. Refer to the `README.md` for detailed instructions on obtaining these.

**2. Key Commands:**
*   **Start the application:**
    ```bash
    ./start.sh
    # or
    docker compose up -d
    ```
*   **Stop the application:**
    ```bash
    ./stop.sh
    # or
    docker compose down
    ```
*   **View logs:**
    ```bash
    docker compose logs -f
    ```
*   **Rebuild the image (after code changes):**
    ```bash
    docker compose build
    ```
*   **Check application health:**
    ```bash
    curl http://localhost:8080/health
    ```

## Development Conventions

*   **Configuration:** All secrets and environment-specific settings are managed in the `.env` file. Do not commit this file to version control.
*   **Dependencies:** Python dependencies are managed in `requirements.txt`. To add a new dependency, add it to the file and rebuild the Docker image (`docker compose build`).
*   **Email:** The application supports two methods for sending email: standard SMTP with a username/password and Google OAuth2. OAuth2 is the recommended and more secure method for Gmail. The `generate_oauth_token.py` script is provided to facilitate this setup.
*   **UI Customization:** The user interface can be modified by editing `templates/index.html`. All styles and scripts are contained within this single file.
*   **Security:** The `README.md` emphasizes keeping API keys out of version control. For production deployments, it is recommended to place the application behind a reverse proxy (like Nginx) to handle HTTPS.
*   **No Database:** The application is stateless and does not use a local database. All transaction data is stored within Stripe.
