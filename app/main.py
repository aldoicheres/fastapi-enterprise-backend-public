from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models import UsuarioModel
from app.schemas import UsuarioRegistro, UsuarioLogin, Token

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Optional
from app.security import (
    obtener_password_hash,
    verificar_password,
    crear_access_token,
    decodificar_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Gestión  API", version="1.0")

# Esquema OAuth2 que apunta al endpoint de login para extraer el token Bearer

oauth2_scheme = APIKeyHeader(name="Authorization")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependencia para obtener el usuario actual a partir del token JWT
def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Limpiar el prefijo 'Bearer ' si el usuario lo incluye al pegar el token
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    payload = decodificar_access_token(token)
    if payload is None:
        raise credentials_exception

    correo: str = payload.get("sub")
    if correo is None:
        raise credentials_exception

    user = db.query(UsuarioModel).filter(UsuarioModel.correo == correo).first()
    if user is None:
        raise credentials_exception

    return user


@app.post("/api/Registrousuarios")
def registrar_usuario(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    db_usuario = (
        db.query(UsuarioModel).filter(UsuarioModel.correo == usuario.correo).first()
    )
    if db_usuario:
        raise HTTPException(
            status_code=400, detail="El correo electrónico ya está registrado"
        )

    hashed_password = obtener_password_hash(usuario.password)

    nuevo_usuario = UsuarioModel(
        nombre=usuario.nombre,
        correo=usuario.correo,
        edad=usuario.edad,
        hashed_password=hashed_password,
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "mensaje": "Usuario registrado exitosamente con seguridad cifrada",
        "correo": nuevo_usuario.correo,
    }


@app.post("/api/login", response_model=Token)
def login_usuario(form_data: UsuarioLogin, db: Session = Depends(get_db)):
    user = (
        db.query(UsuarioModel).filter(UsuarioModel.correo == form_data.correo).first()
    )

    if not user or not verificar_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crear_access_token(
        data={"sub": user.correo}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# --- RUTA PROTEGIDA ---
@app.get("/api/perfil")
def ver_perfil_protegido(
    usuario_actual: UsuarioModel = Depends(obtener_usuario_actual),
):
    """Ruta protegida que devuelve los datos del usuario autenticado mediante su token JWT."""
    return {
        "mensaje": "Acceso autorizado a ruta protegida",
        "usuario": {
            "id": usuario_actual.id,
            "nombre": usuario_actual.nombre,
            "correo": usuario_actual.correo,
            "edad": usuario_actual.edad,
        },
    }


from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


# Manejador global para errores HTTP (como 401, 400, 404, etc.)
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "estado": "error",
            "codigo_http": exc.status_code,
            "mensaje": exc.detail,
        },
    )


# Manejador global para errores de validación de Pydantic (datos mal formados en schemas)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "estado": "error",
            "codigo_http": 422,
            "mensaje": "Error de validación en los datos enviados",
            "detalles": exc.errors(),
        },
    )
# --- RUTA PROTEGIDA CON PAGINACIÓN Y FILTROS ---
@app.get("/api/usuariosOT")
def listar_usuarios(
    skip: int = 0, 
    limit: int = 10, 
    filtro_nombre: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario_actual: UsuarioModel = Depends(obtener_usuario_actual)
):
    """
    Lista usuarios de forma paginada y permite filtrar opcionalmente por coincidencia en el nombre.
    Requiere autenticación mediante token JWT (ruta protegida).
    """
    query = db.query(UsuarioModel)
    
    # Aplicar filtro si se proporciona un nombre o parte de él
    if filtro_nombre:
        query = query.filter(UsuarioModel.nombre.ilike(f"%{filtro_nombre}%"))
    
    # Aplicar paginación (skip: registros a saltar, limit: cantidad máxima a retornar)
    total_registros = query.count()
    usuarios = query.offset(skip).limit(limit).all()
    
    return {
        "estado": "exito",
        "total": total_registros,
        "saltados": skip,
        "limite": limit,
        "resultados": [
            {
                "id": u.id,
                "nombre": u.nombre,
                "correo": u.correo,
                "edad": u.edad
            } for u in usuarios
        ]
    }