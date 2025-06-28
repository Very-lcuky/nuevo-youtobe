FROM python:3.9-slim

WORKDIR /app

# Copiar requirements.txt y luego instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la app
COPY . .

# Exponer el puerto que usará gunicorn
EXPOSE 8080

# Comando para ejecutar la app con gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

