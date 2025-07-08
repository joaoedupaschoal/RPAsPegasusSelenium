from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urlparse



# Configuração do WebDriver
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)

# Abre a página
url = 'http://curso-python-selenium.netlify.app/aula_04_b.html'
browser.get(url)



url_parseada = urlparse(browser.current_url)







# Aguarda permissão do usuário para fechar
input("Pressione Enter para fechar o navegador...")

browser.quit()
