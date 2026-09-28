from sqlalchemy import Column, Integer, String
from app.database import Base

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    correo = Column(String, unique=True, index=True)
    edad = Column(Integer)
    hashed_password = Column(String)