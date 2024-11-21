# Usa una imagen ligera de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación FastAPI al contenedor
COPY . .

# Exponer el puerto en el que correrá FastAPI
EXPOSE 8000

# Comando para ejecutar el servidor FastAPI
CMD ["uvicorn", "principal:app", "--host", "0.0.0.0", "--port", "8000"]
