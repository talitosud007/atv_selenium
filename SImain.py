# Extração de conteúdo da Wikipedia sobre Formigas
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class TestWikipediaFormiga():
    def setup_method(self):
        # Inicializa o navegador Firefox
        self.driver = webdriver.Firefox()
        self.vars = {}
    
    def teardown_method(self):
        # Fecha o navegador
        self.driver.quit()
    
    def test_extrair_conteudo_formiga(self):
        self.driver.get("https://pt.wikipedia.org/wiki/Formiga")
        self.driver.set_window_size(1200, 900)
        
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "mw-content-text")))
        
        time.sleep(2)
        
        pagina = self.driver.page_source
        
        with open("wikipedia_formiga.html", "w", encoding="utf-8") as arquivo:
            arquivo.write(pagina)
        print("✓ Arquivo HTML salvo: wikipedia_formiga.html")
        
        soup = BeautifulSoup(pagina, 'html.parser')
        
        titulo = soup.find('h1', {'id': 'firstHeading'})
        if titulo:
            print(f"\n=== TÍTULO ===\n{titulo.get_text()}\n")
        
        conteudo_principal = soup.find('div', {'id': 'mw-content-text'})
        
        if conteudo_principal:
            paragrafos = conteudo_principal.find_all('p')
            
            with open("formiga_conteudo.txt", "w", encoding="utf-8") as arquivo:
                arquivo.write(f"TÍTULO: {titulo.get_text() if titulo else 'N/A'}\n")
                arquivo.write("="*50 + "\n\n")
                
                for i, paragrafo in enumerate(paragrafos, 1):
                    texto = paragrafo.get_text().strip()
                    if texto:
                        arquivo.write(f"{texto}\n\n")
            
            print("✓ Arquivo de texto salvo: formiga_conteudo.txt")
            
            print("\n=== PRIMEIROS PARÁGRAFOS ===")
            count = 0
            for paragrafo in paragrafos:
                texto = paragrafo.get_text().strip()
                if texto and count < 3:
                    print(f"\n{texto}")
                    count += 1
        
        infobox = soup.find('table', {'class': 'infobox'})
        if infobox:
            print("\n\n=== INFORMAÇÕES DA CAIXA ===")
            linhas = infobox.find_all('tr')
            with open("formiga_infobox.txt", "w", encoding="utf-8") as arquivo:
                for linha in linhas:
                    texto = linha.get_text().strip()
                    if texto:
                        print(texto)
                        arquivo.write(f"{texto}\n")
            print("\n✓ Arquivo infobox salvo: formiga_infobox.txt")
        
        print("\n✓ Extração concluída com sucesso!")

if __name__ == "__main__":
    teste = TestWikipediaFormiga()
    teste.setup_method()
    try:
        teste.test_extrair_conteudo_formiga()
    finally:
        teste.teardown_method()