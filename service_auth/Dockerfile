# Usa la imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que Django usa
EXPOSE 8000

# Comando para ejecutar el servidor de desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
