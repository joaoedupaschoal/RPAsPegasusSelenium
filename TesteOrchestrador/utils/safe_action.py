from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def safe_action(driver, descricao, locator, timeout=10, action=None):
    from utils.helpers import log, error, take_screenshot

    try:
        log(f"➡️ {descricao}")
        elemento = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        if action:
            action(elemento)
        take_screenshot(driver, descricao)
    except TimeoutException:
        error(f"⛔ Timeout em: {descricao}")
        take_screenshot(driver, f"ERRO_{descricao}")
        raise
