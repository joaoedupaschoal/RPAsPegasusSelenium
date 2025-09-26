# session_guard.py
import os, time, functools
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

LOGIN_URL_FRAGMENT = "/login"                # ajuste conforme seu sistema
SELECTOR_POS_LOGIN = (By.ID, "menuPrincipal")# algo que só exista logado

USUARIO = os.getenv("PEGASUS_USER", "joaoeduardo.gold@outlook.com")
SENHA   = os.getenv("PEGASUS_PASS", "071999gs")

def is_logged_in(driver) -> bool:
    # 1) checa URL
    if LOGIN_URL_FRAGMENT in (driver.current_url or ""):
        return False
    # 2) checa um elemento que só existe após login
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located(SELECTOR_POS_LOGIN))
        return True
    except:
        return False


def do_login(driver):

    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.ID, "username"))).clear()
    wait.until(EC.presence_of_element_located((By.ID, "j_id15:email"))).send_keys(USUARIO)
    driver.find_element(By.ID, "password").clear()
    wait.until(EC.presence_of_element_located((By.ID, "j_id15:senha"))).send_keys(SENHA, Keys.ENTER)

    # confirma que logou
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))


def ensure_session(driver):
    if not is_logged_in(driver):
        do_login(driver)

def retry_on_expired_session(func):
    """Decora steps/cenários: se expirar no meio, reloga e tenta 1x de novo."""
    @functools.wraps(func)
    def wrapper(driver, *args, **kwargs):
        ensure_session(driver)
        try:
            return func(driver, *args, **kwargs)
        except Exception:
            # se redirecionou para login no meio do passo, reloga e repete 1x
            if not is_logged_in(driver):
                do_login(driver)
                return func(driver, *args, **kwargs)
            raise
    return wrapper
