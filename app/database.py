from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión para una base de datos SQLite local llamada 'sql_app.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Crear el motor de base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear una sesión para las transacciones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir los modelos de tablas
Base = declarative_base()