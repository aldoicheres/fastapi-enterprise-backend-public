from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal
from app.models import UsuarioModel

router = APIRouter(prefix="/api/analytics", tags=["Módulo Analítico y BI"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/metrics/summary")
def obtener_metricas_usuarios(db: Session = Depends(get_db)):
    """
    Endpoint analítico que calcula indicadores clave de rendimiento (KPIs) 
    sobre los registros de la base de datos en tiempo real.
    """
    total_usuarios = db.query(func.count(UsuarioModel.id)).scalar()
    edad_promedio = db.query(func.avg(UsuarioModel.edad)).scalar() or 0

    return {
        "estado": "exitoso",
        "modulo": "Business Intelligence & Analytics",
        "metricas": {
            "total_registros": total_usuarios,
            "edad_promedio_usuarios": round(edad_promedio, 2),
            "sistema_operativo": "FastAPI Enterprise Core"
        }
    }