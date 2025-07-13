import os
import subprocess
import glob

# Manejar autenticación con Google Cloud desde variable de entorno (JSON en texto)
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    with open("gcloud-key.json", "w") as f:
        f.write(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud-key.json"

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

# Buscar todos los videos con extensión mp4 o MP4 (insensible)
videos = glob.glob("*.mp4") + glob.glob("*.MP4")

print("☁️ Subiendo videos al bucket...")

for video in videos:
    # Renombrar extensión a minúscula si hace falta
    base, ext = os.path.splitext(video)
    ext_lower = ext.lower()
    if ext != ext_lower:
        new_name = base + ext_lower
        print(f"Renombrando {video} a {new_name}")
        os.rename(video, new_name)
        video = new_name

    destino = f"gs://{BUCKET_NAME}/{RUTA_BUCKET}{video}"
    print(f"  ⬆️  {video} → {destino}")
    subprocess.run(["gsutil", "cp", video, destino])

print("✅ Proceso completo.")

