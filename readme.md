# FastAPI Enterprise Backend - Sistema de Gestión
## 📋 Descripción del Proyecto
Este repositorio forma parte de mi portfolio profesional orientado a demostrar la transición y aplicación de sólidos patrones arquitectónicos empresariales desde el ecosistema .NET hacia tecnologías modernas en **Python**. 

El proyecto implementa una **API RESTful robusta y escalable**, diseñada bajo estándares corporativos para simular un entorno de gestión operativa (control de recursos, autenticación segura, trazabilidad y validación estricta de datos), replicando los niveles de exigencia de sistemas de misión crítica.

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.10+
* **Framework Web:** FastAPI (Alto rendimiento, tipado estático y documentación automática).
* **Validación de Datos:** Pydantic (Equivalente a DTOs y validación estricta de modelos).
* **ORM & Base de Datos:** SQLAlchemy + SQLite/PostgreSQL (Mapeo objeto-relacional avanzado).
* **Migraciones:** Alembic (Control de versiones de esquemas de bases de datos).
* **Seguridad:** JWT (JSON Web Tokens) con encriptación bcrypt para autenticación y autorización.
* **Testing:** Pytest (Pruebas unitarias e integración de endpoints).

## 🚀 Características Principales
1. **Autenticación Segura (JWT):** Endpoints protegidos mediante tokens de acceso y encriptación de credenciales.
2. **Validación Automática:** Uso de esquemas Pydantic para garantizar la integridad de los datos de entrada y salida.
3. **Arquitectura Limpia:** Separación clara de responsabilidades en capas (Routers, CRUD/Repositorios, Modelos de Base de Datos y Esquemas).
4. **Documentación Interactiva:** Generación automática de especificaciones mediante Swagger UI y ReDoc.
5. **Suite de Pruebas:** Cobertura de tests unitarios utilizando Pytest.

## ⚙️ Instrucciones de Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/fastapi-enterprise-backend.git](https://github.com/tu-usuario/fastapi-enterprise-backend.git)
   cd fastapi-enterprise-backend
