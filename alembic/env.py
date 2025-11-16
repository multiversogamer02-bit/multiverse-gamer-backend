from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Importar settings y Base del proyecto
from app.core.config import settings
from app.db.base import Base

# Importar modelos para que Alembic los detecte
from app.models.user import User  # noqa: F401
from app.models.plan import Plan  # noqa: F401
from app.models.session import Session  # noqa: F401

# -------------------------------------------------------------------
# Configuración básica de Alembic
# -------------------------------------------------------------------

config = context.config

# Si hay archivo de logging de Alembic, lo cargamos
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata se usa para autogenerate
target_metadata = Base.metadata

# -------------------------------------------------------------------
# Configuración de la URL de la base de datos
# -------------------------------------------------------------------
# Si hay DATABASE_URL en settings (Render / .env), se usa esa.
# Si NO hay (entorno local sin .env), usamos SQLite para generar migraciones.
# Esto evita el error "option values must be strings".

DATABASE_URL = settings.DATABASE_URL or "sqlite:///./local_migrations.db"
config.set_main_option("sqlalchemy.url", DATABASE_URL)


# -------------------------------------------------------------------
# Funciones de migración OFFLINE / ONLINE
# -------------------------------------------------------------------

def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline'.

    No necesita un engine real, solo la URL.
    """
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online'.

    Crea un engine y una conexión real.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
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


# -------------------------------------------------------------------
# Punto de entrada
# -------------------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
