FROM python:3.9-slim

# Instala dependencias necesarias del sistema
RUN apt-get update && apt-get install -y curl gnupg ca-certificates ffmpeg

# Instala dependencias de Python, incluyendo yt-dlp y gsutil
RUN pip install --no-cache-dir yt-dlp google-cloud-storage

# Crear carpeta de trabajo
WORKDIR /app

# Copiar todos los archivos del proyecto
COPY . .

# Ejecutar el script cuando se arranca el contenedor
CMD ["python", "sync_youtube_to_bucket.py"]
