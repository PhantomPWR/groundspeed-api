"""
Alembic environment configuration for database migrations.
"""

import os                                     # Standard: OS path tools
import sys                                    # Standard: System path tools
from logging.config import fileConfig         # Standard: Logging config
from sqlalchemy import engine_from_config     # Third Party: Engine tool
from sqlalchemy import pool                   # Third Party: Connection pool
from alembic import context                   # Third Party: Alembic core

# Add the project root directory to the Python path
# This allows Alembic to find the 'app' package
sys.path.append(os.getcwd())

# Local: Import the Base metadata and models so Alembic can see them
# Note: Importing 'models' ensures all tables are registered with Base
from app.database import Base                 
from app import models                        

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for autogenerate support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True  # Required for full SQLite support
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            render_as_batch=True  # Required for full SQLite support
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()