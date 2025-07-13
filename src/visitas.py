from flask import Flask
from views import main  # o tu función principal

app = Flask(__name__)

@app.route("/")
def home():
    return "Servicio activo"

@app.route("/procesar")
def procesar():
    main()  # llama a tu lógica
    return "Procesamiento completado"
