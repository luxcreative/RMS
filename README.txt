# Rental Management System (RMS) API

This project provides a FastAPI backend backed by PostgreSQL. It manages rental inventory, clients, jobs and quotes. Authentication is handled with JSON Web Tokens.

## Setup

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt]
   ```
2. Set the `DATABASE_URL` environment variable. Example:
   ```bash
   export DATABASE_URL=postgresql://user:password@localhost/rms
   ```
3. Create the database tables:
   ```bash
   python -m rms.database
   ```
4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

The API exposes CRUD endpoints for inventory items, clients, jobs and quotes. Most routes require authentication using JWT tokens returned from the `/login` endpoint.
