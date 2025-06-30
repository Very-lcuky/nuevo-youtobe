import os
import subprocess
import glob
from flask import Flask

# Si la variable de entorno GOOGLE_APPLICATION_CREDENTIALS_JSON contiene JSON, guardarla
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
yt_dlp_cmd = [
    "yt-dlp", CANAL_URL,
    "--download-archive", "descargados.txt",
    "--output", "%(title)s.%(ext)s",
    "--cookies", "/app/cookies.txt"  # Opcional: si incluyes cookies.txt en el Dockerfile
]

result = subprocess.run(yt_dlp_cmd, capture_output=True, text=True)

if result.returncode != 0:
    print("⚠️ Error al ejecutar yt-dlp:")
    print(result.stderr)
else:
    print("✅ Descarga completada correctamente.")

# Buscar videos
videos = glob.glob("*.mp4") + glob.glob("*.MP4")
print("☁️ Subiendo videos al bucket...")

for video in videos:
    base, ext = os.path.splitext(video)
    ext_lower = ext.lower()
    if ext != ext_lower:
        new_name = base + ext_lower
        print(f"🔁 Renombrando {video} a {new_name}")
        os.rename(video, new_name)
        video = new_name

    destino = f"gs://{BUCKET_NAME}/{RUTA_BUCKET}{video}"
    print(f"⬆️ Subiendo {video} → {destino}")
    subprocess.run(["gsutil", "cp", video, destino], check=True)

print("✅ Proceso completo.")

# ----------------------
# Mantener contenedor vivo con Flask
# ----------------------
app = Flask(__name__)

@app.route("/")
def index():
    return "🟢 YouTube Sync Service activo y funcionando."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

