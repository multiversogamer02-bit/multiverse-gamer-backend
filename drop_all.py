from sqlalchemy import create_engine, text
import os

engine = create_engine(os.environ["DATABASE_URL"])

with engine.connect() as conn:
    print("Borrando tablas existentes...")
    conn.execute(text("DROP TABLE IF EXISTS sessions CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS plans CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
    conn.commit()
    print("Listo. Tablas eliminadas.")
