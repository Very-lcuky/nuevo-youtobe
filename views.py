from google.cloud import storage, firestore

# Inicializar cliente Storage y Firestore
storage_client = storage.Client()
firestore_client = firestore.Client()

BUCKET_NAME = "you-tobe"
FOLDER = "videos/"

def listar_videos(bucket_name, prefix):
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    return [blob for blob in blobs if blob.name.endswith('.mp4')]

def guardar_metadata_en_firestore(video_id, metadata):
    doc_ref = firestore_client.collection('videos').document(video_id)
    doc_ref.set(metadata)
    print(f'Metadata guardada para video {video_id}')

def main():
    videos = listar_videos(BUCKET_NAME, FOLDER)
    
    for video in videos:
        video_id = video.name.split('/')[-1].replace('.mp4', '')
        
        precio_por_venta = 1.0  # Precio fijo de 1 USD por video
        
        metadata = {
            "video_name": video.name,
            "url": f"https://storage.googleapis.com/{BUCKET_NAME}/{video.name}",
            "royalties_percentage": 10,
            "price_per_sale": precio_por_venta,
            "estimated_sales": 0,  # Puedes actualizar con ventas reales luego
            "estimated_revenue": 0,  # Lo mismo para ingresos estimados
            "creator_wallet": "AjahiviTvhPsthFUYKb5ho6Wtu8H7bDDQq78LVYYnyAf"
        }
        
        guardar_metadata_en_firestore(video_id, metadata)

if __name__ == "__main__":
    main()

