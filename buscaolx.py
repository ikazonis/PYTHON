# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

def buscar_uma_vez():
    # --- LISTA DE PRODUTOS ---
    # Agora com a categoria opcional para cada um
    meus_alvos = [
        {"termo": "lente canon", "preco": 500, "cat": "acessorios-para-cameras-e-filmadoras"},
        {"termo": "pedal boss", "preco": 250, "cat": "instrumentos-musicais"},
        {"termo": "guitarra vintage v100", "preco": 2400, "cat": "instrumentos-musicais"}
    ]

    options = Options()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    stealth(driver,
            languages=["pt-BR", "pt"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

    print(f"Iniciando busca para {len(meus_alvos)} produtos...")

    primeiro_item = True

    for item in meus_alvos:
        produto = item["termo"]
        preco_limite = item["preco"]
        categoria = item["cat"]
        
        termo_url = produto.replace(" ", "%20")
        
        # sf=1: Ordena pelos mais recentes primeiro
        # pe: Preco maximo
        #url = f"https://www.olx.com.br/{categoria}?q={termo_url}&pe={preco_limite}&sf=1"
        url = f"https://www.olx.com.br/{categoria}/estado-rj?pe={preco_limite}&q={termo_url}&sf=1"

        if primeiro_item:
            driver.get(url)
            primeiro_item = False
        else:
            driver.execute_script(f"window.open('{url}', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])

        print(f"Abrindo aba para: {produto} (ate R$ {preco_limite})...")
        time.sleep(4) 

        try:
            # Tenta encontrar os anuncios para confirmar que a pagina carregou
            anuncios = driver.find_elements(By.CSS_SELECTOR, 'section[data-testid="ad-list-item"]')
            if anuncios:
                print(f"   -> OK: Itens encontrados na pagina.")
            else:
                print(f"   -> Aviso: Nenhum item apareceu nos resultados.")
        except:
            pass

    print("\nPronto! Analise as abas abertas.")

if __name__ == "__main__":
    buscar_uma_vez()

