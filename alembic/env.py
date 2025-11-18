import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool, create_engine

# -------------------------------------------------------
# Añadir ruta del proyecto
# -------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

# -------------------------------------------------------
# Importar Base y modelos
# -------------------------------------------------------
from backend.app.db.base import Base
from backend.app.models.user import User
from backend.app.models.plan import Plan
from backend.app.models.session import Session

# -------------------------------------------------------
config = context.config

# Registro de logs
if config.config_file_name:
    fileConfig(config.config_file_name)

# Metadatos de modelos
target_metadata = Base.metadata

# -----------------------------
# Cargar URL desde variable de entorno
# -----------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no está definida en las variables de entorno.")

# Reemplazar por URL real
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline():
    """Modo offline: genera SQL sin ejecutar en DB."""
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Modo online: conecta a la DB y ejecuta migrations."""
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# Ejecutar según modo
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
