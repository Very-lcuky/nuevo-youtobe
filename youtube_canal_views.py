import time
import random
import yt_dlp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# CONFIGURACIÓN
CANAL_URL = "https://www.youtube.com/@marisol_vrs/videos"
NUM_VISTAS_POR_VIDEO = 2  # Número de vistas por video
TIEMPO_MIN = 35
TIEMPO_MAX = 90
INTERVALO = 30 * 60  # 30 minutos en segundos

proxies = [
    # "45.131.6.108:80",
]

def obtener_videos(canal_url, max_videos=5):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'force_generic_extractor': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(canal_url, download=False)
        entries = info.get('entries', [])
        return [f"https://www.youtube.com/watch?v={e['id']}" for e in entries[:max_videos]]

def crear_navegador(proxy=None):
    options = Options()
    options.add_argument("--mute-audio")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--headless=new')  # modo headless para Cloud Run u otros entornos sin UI
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')

    user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(500,599)}.0 (KHTML, like Gecko) Chrome/{random.randint(100,120)}.0.{random.randint(1000,9999)}.100 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')

    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def ver_video(driver, url):
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
        duracion = random.randint(TIEMPO_MIN, TIEMPO_MAX)
        print(f"▶️ Viendo: {url} por {duracion} segundos")
        time.sleep(duracion)
    except Exception as e:
        print("⚠️ Error al reproducir:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    videos = obtener_videos(CANAL_URL, max_videos=3)
    
    while True:
        for video_url in videos:
            for _ in range(NUM_VISTAS_POR_VIDEO):
                proxy = random.choice(proxies) if proxies else None
                driver = crear_navegador(proxy)
                ver_video(driver, video_url)
                time.sleep(random.randint(5, 15))  # descanso entre vistas de un mismo video
        print(f"🕒 Esperando {INTERVALO // 60} minutos para la próxima ronda...")
        time.sleep(INTERVALO)

