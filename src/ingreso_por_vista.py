from datetime import datetime, timezone
from google.cloud import firestore

def actualizar_ingresos_por_vista():
    db = firestore.Client()
    hoy = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    # Consulta todos los videos
    videos = db.collection('videos').stream()

    total_ingresos = 0

    for video in videos:
        try:
            data = video.to_dict()
            vistas_hoy = data.get('vistas_por_dia', {}).get(hoy, 0)
            precio_por_vista = data.get('precio_por_vista', 0.01)  # por ejemplo

            ingresos_hoy = vistas_hoy * precio_por_vista

            # Actualiza campos en Firestore
            video.reference.update({
                'ingresos_por_dia.' + hoy: ingresos_hoy,
                'ingresos_totales': firestore.Increment(ingresos_hoy)
            })

            print(f"Actualizado {video.id}: vistas hoy={vistas_hoy}, ingresos hoy={ingresos_hoy:.2f}")

            total_ingresos += ingresos_hoy
        except Exception as e:
            print(f"Error al actualizar video {video.id}: {e}")

    print(f"Resumen total ingresos hoy: {total_ingresos:.2f}")

if __name__ == '__main__':
    actualizar_ingresos_por_vista()

