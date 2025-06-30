FROM python:3.10-slim

# Instala dependencias necesarias
RUN apt-get update && apt-get install -y \
    curl gnupg ca-certificates unzip ffmpeg \
    && apt-get clean

# Agrega la clave y repositorio de Google Cloud SDK
RUN mkdir -p /usr/share/keyrings && \
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update && apt-get install -y google-cloud-sdk

# Establece el directorio de trabajo
WORKDIR /app

# Copia todos los archivos del proyecto
COPY . .

# Instala dependencias de Python
RUN pip install --no-cache-dir yt-dlp google-cloud-storage flask

# Permisos de ejecución para yt-dlp (en caso de que se instale manualmente)
# RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && chmod a+rx /usr/local/bin/yt-dlp

# Exponer puerto
EXPOSE 8080

# Comando por defecto
CMD ["python", "sync_youtube_to_bucket_sync.py"]

