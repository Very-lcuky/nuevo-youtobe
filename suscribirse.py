from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import uuid
import os
import time

def abrir_canal_y_suscribirse(url_canal):
    # Crear perfil temporal único
    user_data_dir = f"/tmp/selenium_profile_{uuid.uuid4()}"
    os.makedirs(user_data_dir, exist_ok=True)

    options = Options()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("start-maximized")
    options.add_argument("lang=es")

    driver = webdriver.Chrome(options=options)

    # Ocultar que es automatizado
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
        """
    })

    driver.get(url_canal)
    wait = WebDriverWait(driver, 15)

    try:
        boton_sub = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//tp-yt-paper-button[contains(normalize-space(.), 'Suscribirme')]")
        ))
        boton_sub.click()
        print("✅ ¡Botón Suscribirme clickeado!")
    except Exception as e:
        print("⚠️ No se encontró el botón Suscribirme o ya estás suscrito.", e)

    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    abrir_canal_y_suscribirse("https://www.youtube.com/@marisol_vrs")

