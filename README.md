# Advocate Case Information System

A simple, responsive Case Information System for Advocates built with Python, Flask, and SQLite.

## Features

*   **Dashboard**: View upcoming hearings (next 7 days) and case statistics.
*   **Client Management**: Create, edit, and list clients.
*   **Case Management**: Track case details, status, next hearing dates, and notes.
*   **Authentication**: Secure login/logout for advocates.
*   **Responsive UI**: Built with Bootstrap 5.

## Tech Stack

*   Python 3
*   Flask
*   Flask-SQLAlchemy (ORM)
*   Flask-Login
*   Flask-WTF
*   SQLite
*   Bootstrap 5

## Setup Instructions

1.  **Clone the repository**

2.  **Create a virtual environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database**

    First, set the FLASK_APP environment variable:

    ```bash
    export FLASK_APP=run.py
    ```

    Then initialize the migration repository and apply migrations (or create db directly):

    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

    Alternatively, you can open a python shell and create the database:

    ```bash
    python3
    >>> from app import create_app, db
    >>> app = create_app()
    >>> with app.app_context():
    ...     db.create_all()
    ...     # Create a test user
    ...     from app.models import User
    ...     u = User(name='Advocate', email='admin@example.com')
    ...     u.set_password('password')
    ...     db.session.add(u)
    ...     db.session.commit()
    ...
    >>> exit()
    ```

5.  **Run the application**

    ```bash
    flask run
    ```

    The application will be available at `http://127.0.0.1:5000/`.

6.  **Login**

    Use the credentials you created in step 4 (e.g., `admin@example.com` / `password`).
