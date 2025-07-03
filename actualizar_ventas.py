from google.cloud import firestore

firestore_client = firestore.Client()

def actualizar_ventas(video_id, vistas, royalties, precio):
    # Calculamos las ventas basadas en vistas y royalties
    # Por ejemplo, una fórmula simple (puedes cambiarla):
    ventas_calculadas = int(vistas * (royalties / 100))

    doc_ref = firestore_client.collection('videos').document(video_id)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        data['estimated_sales'] = ventas_calculadas
        doc_ref.set(data)
        print(f"Video {video_id} actualizado con ventas: {ventas_calculadas}")
    else:
        print(f"No existe video con ID {video_id}")

def main():
    # Ejemplo de datos (puedes obtener estas vistas desde donde sea)
    videos = [
        {'id': 'youtube video #-YQQM8W7D-I', 'vistas': 1000, 'royalties_percentage': 10, 'price_per_sale': 1.0},
        {'id': 'youtube video #7Wti06PLn-c', 'vistas': 500, 'royalties_percentage': 10, 'price_per_sale': 1.0},
        # agrega más videos...
    ]

    for video in videos:
        actualizar_ventas(video['id'], video['vistas'], video['royalties_percentage'], video['price_per_sale'])

if __name__ == "__main__":
    main()
