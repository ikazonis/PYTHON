# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def buscar_pedais():
    chrome_options = Options()
    # DESATIVADO o headless para voce ver o que acontece:
    # chrome_options.add_argument("--headless") 
    
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL filtrada: Pedal Boss ate 250 reais
    url = "https://www.olx.com.br/instrumentos-musicais?q=pedal%20boss&pe=250"

    try:
        print("Abrindo o navegador...")
        driver.get(url)

        print("Aguardando 10 segundos para carregamento manual/visual...")
        time.sleep(10) # Tempo para voce ver se abriu o site ou o erro do Cloudflare

        # Tenta buscar os anuncios usando uma classe mais generica caso o data-testid falhe
        print("Buscando anuncios...")
        
        # Lista de possíveis seletores (o OLX muda as vezes)
        seletores = ['section[data-testid="ad-list-item"]', '.olx-ad-card', 'div[data-component="ads-list"]']
        
        anuncios = []
        for seletor in seletores:
            anuncios = driver.find_elements(By.CSS_SELECTOR, seletor)
            if len(anuncios) > 0:
                print(f"Sucesso com o seletor: {seletor}")
                break

        if not anuncios:
            print("Nenhum anuncio encontrado na tela. Verifique se apareceu um desafio 'Sou Humano'.")
        else:
            print(f"Encontrados {len(anuncios)} itens.")
            for anuncio in anuncios[:5]: # Mostra os 5 primeiros
                try:
                    titulo = anuncio.find_element(By.TAG_NAME, 'h2').text
                    print(f"Item encontrado: {titulo}")
                except:
                    continue

    except Exception as e:
        print(f"Erro detalhado: {e}")

    finally:
        print("O navegador ficara aberto por 30 segundos para voce conferir...")
        time.sleep(30)
        driver.quit()

if __name__ == "__main__":
    buscar_pedais()