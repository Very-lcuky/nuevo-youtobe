import os
import subprocess
import glob

# Configuración
CANAL_URL = "https://www.youtube.com/@marisol_vrs"
BUCKET_NAME = "you-tobe"
RUTA_BUCKET = "videos/"

# Crear carpeta temporal
os.makedirs("tmp_videos", exist_ok=True)
os.chdir("tmp_videos")

# Descargar videos nuevos
print("📥 Descargando videos nuevos...")
subprocess.run([
    "yt-dlp", CANAL_URL,
    "--download-archive", "descargados.txt",
    "--output", "%(title)s.%(ext)s"
])

# Subir los archivos .mp4 al bucket
print("☁️ Subiendo videos al bucket...")
videos = glob.glob("*.mp4")

for video in videos:
    destino = f"gs://{BUCKET_NAME}/{RUTA_BUCKET}{video}"
    print(f"  ⬆️  {video} → {destino}")
    subprocess.run(["gsutil", "cp", video, destino])

print("✅ Proceso completo.")
