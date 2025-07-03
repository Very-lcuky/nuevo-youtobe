from google.cloud import firestore

firestore_client = firestore.Client()

def listar_metadata_videos():
    videos_ref = firestore_client.collection('videos')
    docs = videos_ref.stream()
    
    for doc in docs:
        print(f"ID: {doc.id}")
        print(f"Data: {doc.to_dict()}")
        print("------")

if __name__ == "__main__":
    listar_metadata_videos()
