from fastapi import FastAPI, HTTPException
from google.cloud import firestore

app = FastAPI()
db = firestore.Client()

@app.post("/video/{video_id}/view")
async def increment_view(video_id: str):
    doc_ref = db.collection("videos").document(video_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Video no encontrado")

    # Obtener contador actual de vistas
    current_views = doc.to_dict().get("views", 0)
    # Incrementar en 1
    doc_ref.update({"views": current_views + 1})

    return {"message": f"Views actualizadas a {current_views + 1} para video {video_id}"}

