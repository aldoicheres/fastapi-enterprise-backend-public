import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app, get_db
from app.database import Base

# Configuración de base de datos en memoria exclusiva para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_registrar_usuario():
    response = client.post(
        "/api/Registrousuarios/",
        json={
            "nombre": "Usuariotest",
            "correo": "test@portfolio.com",
            "edad": 35,
            "password": "securepassword123"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["correo"] == "test@portfolio.com"

def test_login_usuario():
    response = client.post(
        "/api/login/",
        json={
            "correo": "test@portfolio.com",
            "password": "securepassword123"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"