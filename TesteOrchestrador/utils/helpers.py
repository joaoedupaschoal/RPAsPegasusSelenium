import os
import time
import config
from datetime import datetime

def log(msg):
    hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mensagem = f"🟢 {hora} - {msg}"
    print(mensagem)
    gravar_log(mensagem)

def error(msg):
    hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mensagem = f"🔴 {hora} - {msg}"
    print(mensagem)
    gravar_log(mensagem)

def gravar_log(mensagem):
    with open(config.LOG_FILE, "a", encoding="utf-8") as f:
        f.write(mensagem + "\n")

def take_screenshot(driver, nome):
    os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = os.path.join(config.SCREENSHOT_DIR, f"{nome}_{timestamp}.png")
    driver.save_screenshot(caminho)
    log(f"📸 Screenshot salva: {caminho}")

def marcar_inicio():
    return time.time()

def marcar_fim(inicio):
    return round(time.time() - inicio, 2)
