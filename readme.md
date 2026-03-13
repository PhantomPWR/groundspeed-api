# Groundspeed Records API

A high-performance, modular REST API built with FastAPI to manage aviation groundspeed records, aircraft hierarchies, and user roles.

## 1. Technologies & Packages

- **Python 3.13.7:** Leveraging the latest stable language features.
- **FastAPI:** Chosen for native type-hinting, high performance, and automatic Swagger (OpenAPI) documentation.
- **SQLAlchemy 2.0:** Used as the ORM to manage relational data via Python classes.
- **Alembic:** Handles database migrations, allowing schema changes without data loss.
- **Bcrypt:** Standard password hashing (used directly to ensure Python 3.13 stability).
- **Python-JOSE:** Implements JWT (JSON Web Tokens) for secure, stateless authentication.
- **SQLite:** A lightweight, file-based database used for portability and development speed.

## 2. Architecture & Modules

- **Routers (`app/routers/`):** Segmented into `auth.py`, `aircraft.py`, `records.py`, and `users.py` to keep logic isolated and maintainable.
- **Schemas (`app/schemas.py`):** Defines the "Contract" for data. Uses Pydantic to validate incoming requests and filter outgoing responses.
- **Dependencies (`app/dependencies.py`):** Centralized security guards that enforce Role-Based Access Control (RBAC) for Owner, Admin, and User roles.
- **CRUD (`app/crud.py`):** Decoupled database logic to keep routers clean and testable.
- **Utils (`app/utils.py`):** Core logic for SEO-friendly filename generation and string slugification.

## 3. Issues & Solutions

- **SQLite Naming Conventions:** Alembic initially failed on Foreign Key constraints.
    - _Solution:_ Implemented a global `MetaData` naming convention in `database.py`.
- **Absolute Imports:** Resolved "relative import beyond top-level" errors.
    - _Solution:_ Standardized on absolute imports (e.g., `from app import crud`).
- **Bcrypt Compatibility:** `passlib` showed versioning errors on Python 3.13.
    - _Solution:_ Bypassed passlib to use the standalone `bcrypt` library directly.

## 4. Key Teachings

- **Decoupled Design:** Learned that the Database Model and the API Schema are separate entities; adding a column to one does not automatically expose it to the other.
- **Role-Based Security:** Implemented a WordPress-style hierarchy where permissions are checked via FastAPI dependencies before reaching the logic.
- **Asset Management:** Storing physical files on disk while maintaining path references in the database ensures high performance and SEO benefits.
