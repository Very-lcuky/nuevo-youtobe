import os
import subprocess
import glob

# Si la variable de entorno GOOGLE_APPLICATION_CREDENTIALS contiene JSON, guardarlo en archivo
cred_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")

if cred_json:
    with open("gcloud-key.json", "w") as f:
        f.write(cred_json)
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
], check=True)

# Buscar videos mp4 o mp4 (insensible)
videos = glob.glob("*.mp4") + glob.glob("*.MP4")

print("☁️ Subiendo videos al bucket...")

for video in videos:
    base, ext = os.path.splitext(video)
    ext_lower = ext.lower()
    if ext != ext_lower:
        new_name = base + ext_lower
        print(f"Renombrando {video} a {new_name}")
        os.rename(video, new_name)
        video = new_name

    destino = f"gs://{BUCKET_NAME}/{RUTA_BUCKET}{video}"
    print(f"  ⬆️  {video} → {destino}")
    subprocess.run(["gsutil", "cp", video, destino], check=True)

print("✅ Proceso completo.")

