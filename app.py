from flask import Flask, render_template
from google.cloud import storage

app = Flask(__name__)

BUCKET_NAME = "you-tobe"
VIDEOS_PREFIX = "videos/"

@app.route('/')
def index():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=VIDEOS_PREFIX)

    videos = []
    for blob in blobs:
        if blob.name.endswith((".mp4", ".webm", ".mkv", ".mov")):
            url = f"https://storage.googleapis.com/{BUCKET_NAME}/{blob.name}"
            videos.append(url)

    return render_template('index.html', videos=videos)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
