# Usa una imagen de Python ligera
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos al contenedor
COPY requirements.txt .
COPY main.py .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000 para la API
EXPOSE 8000

# Ejecuta la API con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
