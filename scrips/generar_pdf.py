from fpdf import FPDF

# Datos que me diste, resumidos para el PDF
data = {
    "name": "MarisolVRS Canal NFT",
    "description": ("Este NFT representa el canal completo de YouTube de MarisolVRS. "
                    "Es la representación digital de todos los videos del canal, donde MarisolVRS "
                    "conserva el 100% de los derechos de autor y recibe regalías del 10% de las reventas. "
                    "Cualquier uso comercial de los videos requiere autorización previa por parte de MarisolVRS."),
    "creator": "MarisolVRS",
    "creator_address": "0xc5190A86545c8bdbeEA24F6938F631AD38Fc6787",
    "royalties": {
        "percentage": 10,
        "recipient": "0xc5190A86545c8bdbeEA24F6938F631AD38Fc6787"
    },
    "rights_of_author": {
        "description": ("MarisolVRS mantiene el 100% de los derechos de autor sobre todos los videos del canal. "
                        "Cualquier uso comercial de los videos debe ser aprobado por MarisolVRS y las regalías del 10% se asignan a MarisolVRS por cada transacción secundaria.")
    },
    "terms_and_conditions": {
        "commercial_use": ("El contenido del canal solo podrá ser utilizado con fines comerciales bajo autorización previa de MarisolVRS. "
                           "Cualquier uso sin autorización estará sujeto a penalizaciones y acciones legales."),
        "royalties": ("El 10% de cada transacción secundaria será entregado a MarisolVRS como regalía. "
                      "Además, el 100% de las regalías generadas por el uso comercial deberán ser acordadas directamente con MarisolVRS.")
    },
    "license": {
        "type": "Creative Commons",
        "rights": "Todos los derechos de autor están reservados exclusivamente a MarisolVRS. El uso comercial sin autorización está prohibido.",
        "restrictions": "El uso comercial requiere autorización previa de MarisolVRS. El uso no autorizado estará sujeto a penalizaciones legales."
    },
    "social_links": {
        "YouTube": "https://www.youtube.com/@marisol_vrs",
        "Instagram": "https://www.instagram.com/marisolvrs",
        "Facebook": "https://www.facebook.com/marisolb",
        "TikTok": "https://www.tiktok.com/@marisolvrs",
        "Web": "https://marisolvrs.fun"
    },
    "bio": ("¡Hola! Soy Marisol, y este es mi canal: marisolvrs. Aquí comparto mi vida en videos: "
            "Viajes a lugares increíbles, momentos con mi perro, vlogs personales llenos de buena vibra y autenticidad. "
            "Si te gusta viajar, los animales y seguir historias reales, ¡este canal es para ti! Suscríbete y acompáñanos en cada nueva aventura. ¡Nos vemos en el próximo video!")
}

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, data["name"], ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def add_title(pdf, title):
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, title, ln=True)
    pdf.ln(3)

def add_paragraph(pdf, text):
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, text)
    pdf.ln(4)

def main():
    pdf = PDF()
    pdf.add_page()

    add_title(pdf, "Descripción")
    add_paragraph(pdf, data["description"])

    add_title(pdf, "Creador y Dirección")
    add_paragraph(pdf, f"Creador: {data['creator']}")
    add_paragraph(pdf, f"Dirección: {data['creator_address']}")

    add_title(pdf, "Regalías")
    add_paragraph(pdf, f"Porcentaje de regalías: {data['royalties']['percentage']}%")
    add_paragraph(pdf, f"Receptor de regalías: {data['royalties']['recipient']}")

    add_title(pdf, "Derechos de Autor")
    add_paragraph(pdf, data["rights_of_author"]["description"])

    add_title(pdf, "Términos y Condiciones")
    add_paragraph(pdf, "Uso Comercial:")
    add_paragraph(pdf, data["terms_and_conditions"]["commercial_use"])
    add_paragraph(pdf, "Regalías:")
    add_paragraph(pdf, data["terms_and_conditions"]["royalties"])

    add_title(pdf, "Licencia")
    add_paragraph(pdf, f"Tipo: {data['license']['type']}")
    add_paragraph(pdf, f"Derechos: {data['license']['rights']}")
    add_paragraph(pdf, f"Restricciones: {data['license']['restrictions']}")

    add_title(pdf, "Redes Sociales")
    for key, link in data["social_links"].items():
        add_paragraph(pdf, f"{key}: {link}")

    add_title(pdf, "Biografía")
    add_paragraph(pdf, data["bio"])

    # Guardar archivo PDF
    pdf.output("MarisolVRS_NFT_Contrato.pdf")
    print("✅ PDF generado: MarisolVRS_NFT_Contrato.pdf")

if __name__ == "__main__":
    main()
