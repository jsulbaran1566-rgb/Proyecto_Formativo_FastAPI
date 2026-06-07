from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cambia estos valores por los de tu pgAdmin:
# postgresql://usuario:contraseña@host:puerto/nombre_base_datos
DATABASE_URL = "postgresql://postgres:tu_contraseña@localhost:5432/agro_mercado"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
