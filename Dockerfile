# Usamos una imagen oficial y ligera de Python 3.9
FROM python:3.9-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema necesarias si fuera requerido
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos e instalamos los requerimientos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código del proyecto en el contenedor
COPY . .

# Exponemos el puerto en el que corre Uvicorn
EXPOSE 8000

# Comando por defecto para iniciar la API en producción/desarrollo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]