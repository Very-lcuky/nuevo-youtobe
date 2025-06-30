from google.cloud import storage

# Configura tu bucket y proyecto
BUCKET_NAME = "you-tobe"
PREFIX = "videos/"
PROJECT_ID = "useful-memory-464107-d6"

def generar_html(videos_urls):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Mis Videos</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background: #f8f8f8; }
            video { margin: 10px 0; border: 1px solid #ccc; }
        </style>
    </head>
    <body>
        <h1>🎬 Mis Videos</h1>
    """
    for url in videos_urls:
        html += f"""
        <video width="640" controls>
            <source src="{url}" type="video/mp4">
            Tu navegador no soporta este video.
        </video><br>
        """
    html += "</body></html>"
    return html

def main():
    # Inicializa el cliente con proyecto explícito
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)

    # Lista los archivos del bucket
    blobs = bucket.list_blobs(prefix=PREFIX)
    videos_urls = []
    for blob in blobs:
        if blob.name.endswith((".mp4", ".webm", ".mov", ".mkv")):
            url = f"https://storage.googleapis.com/{BUCKET_NAME}/{blob.name}"
            videos_urls.append(url)

    if not videos_urls:
        print("⚠️ No se encontraron videos en el bucket.")
        return

    # Genera el HTML
    html = generar_html(videos_urls)

    # Guarda localmente
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # Sube a GCS
    blob = bucket.blob("index.html")
    blob.upload_from_filename("index.html", content_type="text/html")

    print("✅ index.html generado y subido correctamente.")

if __name__ == "__main__":
    main()

