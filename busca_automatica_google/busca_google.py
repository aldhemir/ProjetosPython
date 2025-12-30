# import das bibs
from random import random
from select import select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import requests
import random
from selenium.common.exceptions import NoSuchElementException

class Busca:
    def __init__(self, url, palavra, quero_esse_link, total_paginas_busca):
        self.url = url
        self.palavra = palavra
        self.quero_esse_link = quero_esse_link
        self.total_paginas_busca = total_paginas_busca

        #start no google chrome maximizado, Configurando as opções dos drivers do Selenium
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        #chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")    
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def pesquisar(self):
        driver = self.driver
         #mostrando IP externo de conexão com a internet
        try:
            ip_publico = requests.get("https://api.ipify.org").text
            print("IP externo: " + ip_publico)
            print("--------------------------")
        except:
            print("Não foi possível obter o IP externo")      

        driver.get(self.url)
        time.sleep(3)

        try:
            driver.switch_to.frame(driver.find_element_by_id("yDmH0d"))
            driver.find_element_by_id("yDmH0d").send_keys(Keys.ESCAPE)
        except:
            pass

        try:
            # Tenta encontrar pelo text area (padrao novo) ou input
            try:
                campo_pesquisa_google = driver.find_element_by_tag_name("textarea")
            except:
                 campo_pesquisa_google = driver.find_element_by_tag_name("input")
            
            campo_pesquisa_google.click()
            campo_pesquisa_google.clear()

            palavra_random = random.choice(self.palavra) # escolhendo uma palavra randomica do array

            campo_pesquisa_google.send_keys(palavra_random)
            campo_pesquisa_google.send_keys(Keys.RETURN)
            time.sleep(3)       

            # verifica se o texto existe na página e se exister vou clicar nele, isso se ele for igual a variavel quero_esse_link
            if self.existe_texto(self.quero_esse_link):
                links = driver.find_elements_by_tag_name("a")
                for link in links:
                    if self.quero_esse_link in link.text:
                        link.click()
                        time.sleep(5) # tempo para carregar a página
                        break
                
                print("Busca finalizada sem proxy")
                #aqui vou começar novamente a busca + trocando o servidor de conexão com a internet usando um proxy
                self.proxy()  
            else:
                print("Não encontrei o texto. Procurando nas próximas páginas") 
                for i in range(self.total_paginas_busca): # procurando nas próximas páginas
                    driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    try:
                        # Tenta encontrar o botão "Próxima" (o ID pode variar dependendo da região/versão do Google)
                        proxima_pag = None
                        try:
                            proxima_pag = driver.find_element(By.ID, "pnnext")
                        except:
                            pass
                        
                        if proxima_pag:
                            proxima_pag.click()
                            time.sleep(3)
                            if self.existe_texto(self.quero_esse_link):
                                links = driver.find_elements_by_tag_name("a")
                                for link in links:
                                    if self.quero_esse_link in link.text:
                                        link.click()
                                        time.sleep(5) # tempo para o link carregar
                                        break
                                break
                            else:
                                continue
                        else:
                             print("Botão de próxima página não encontrado.")
                             break

                    except NoSuchElementException:
                        print("Não encontrei mais paginas para procurar")
                        continue
                
                print("Busca finalizada sem proxy (não encontrado ou fim das páginas)")
                #aqui vou começar novamente a busca com o proxy
                self.proxy()
        except Exception as e:
            print(f"Erro durante a pesquisa: {e}")
            self.driver.quit()

    def proxy(self):
        driver = self.driver
        try:
            driver.get('https://www.proxysite.com/pt/') # abre a página do proxy
            time.sleep(5)
            select = Select(driver.find_element_by_class_name('server-option')) # seleciona o servidor
           
            # select.select_by_value('us1') # seleciona o servidor
            todos_servidores = [x.get_attribute('value') for x in select.options] # pega todos os servidores
            #print(todos_servidores)
            numero_servidor = random.randint(1,20) # numero do servidor
            nome_servidor = 'us'
           
            # aqui vou testar qual Servidor está no select, se não estiver ele vai para o próximo. As vezes o servidor us1 não tá na lista, ai ele vai para o próximo us2.
            # Depois que o numero de servidor chegar a 20, mudo o nome do servidor para eu e reseto o numero de servidor para 1
            for servidor in todos_servidores:
                if numero_servidor == 21:
                    nome_servidor = "eu"
                    numero_servidor = 1

                if servidor == nome_servidor+str(numero_servidor):
                    select.select_by_value(servidor)
                    break
                numero_servidor += 1

            campo_proxy_input = driver.find_element_by_tag_name("input")# seleciona o campo de input do proxy
            campo_proxy_input.click()
            campo_proxy_input.clear()
            campo_proxy_input.send_keys(self.url)
            campo_proxy_input.send_keys(Keys.RETURN)
            time.sleep(3)

            #depedendo do servidor escolhido, o google irá pedir para aceitar alguns termos de cookies. Geralmente é servidores da França
            #neses caso, não continuo a busca, volto a escolher outro servidor e tento novamente
            if self.existe_texto("Avant d'accéder à Google"):
                time.sleep(2)
                try:
                    driver.find_element(By.ID, "L2AGLb").click()
                except:
                    pass
                time.sleep(5)
                self.proxy()
                time.sleep(5)

            try:
                campo_pesquisa_google = driver.find_element_by_css_selector('[title="Search"]')
            except:
                 # Fallback caso o seletor mude no proxy
                 try:
                    campo_pesquisa_google = driver.find_element_by_name("q")
                 except:
                    print("Campo de busca não encontrado no Proxy")
                    return

            campo_pesquisa_google.click()
            campo_pesquisa_google.clear()

            palavra_random = random.choice(self.palavra) # escolhendo uma palavra randomica do array

            campo_pesquisa_google.send_keys(palavra_random)
            campo_pesquisa_google.send_keys(Keys.RETURN)
            time.sleep(3)    

            if self.existe_texto("Go to Google Home"):
        
                # verifica se o texto existe na página e se exister vou clicar nele, isso se ele for igual a variavel quero_esse_link
                if self.existe_texto(self.quero_esse_link):
                    links = driver.find_elements_by_tag_name("a")
                    for link in links:
                        if self.quero_esse_link in link.text:
                            link.click()
                            time.sleep(5) # espera 5 segundos para carregar a página
                            break

                    print("Busca finalizada com proxy")
                    #aqui vou começar novamente a busca + trocando o servidor de conexão com a internet usando um proxy
                    self.proxy()     
                else:
                    print("Não encontrei o texto. Procurando nas próximas páginas")
                    for i in range(self.total_paginas_busca): # procurando nas próximas páginas
                        driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(3)
                        try:
                            if(driver.find_elements(By.ID, "pnnext")): # Verifica se existe antes de clicar
                                driver.find_element(By.ID, "pnnext").click()
                                time.sleep(3)
                                if self.existe_texto(self.quero_esse_link):
                                    links = driver.find_elements_by_tag_name("a")
                                    for link in links:
                                        if self.quero_esse_link in link.text:
                                            link.click()
                                            time.sleep(5) #tempo para carregar o site quando é encontrado
                                            break  
                                    break    
                                else:
                                    continue
                            else:
                                print("Botão next não encontrado no proxy")
                                break
                        except NoSuchElementException:
                            print("Não tem mais páginas para procurar")
                            break
            else:
                print("Estou na página errada ou captcha")
                self.proxy()
                
            print("Busca finalizada com proxy")
            #aqui vou começar novamente a busca + trocando o servidor de conexão com a internet usando um proxy
            self.proxy()

        except Exception as e:
            print(f"Erro no proxy: {e}")


    # procura dentro da página algum texto
    def existe_texto(self, text):
        return str(text) in self.driver.page_source


# fazendo a busca no google
url = "https://www.google.com.br/"

# MODIFICAÇÃO AQUI: Substituição de nomes e locais
palavra = [
    "que horas tem ônibus + Aldhemir Macedo + Porto Alegre", 
    "horário de ônibus em Porto Alegre + Aldhemir Macedo", 
    "ônibus em Porto Alegre que horas tem ônibus + Aldhemir Macedo"
]

# Exemplos comentados também atualizados para referência
#palavra = ["me guia Porto Alegre  Aldhemir Macedo guiaportoalegre.com.br ", "guia online Porto Alegre me guia Porto Alegre guiaportoalegre.com.br ", "ponto turístico Porto Alegre  me guia Porto Alegre  Aldhemir Macedo"]
#palavra = ['farmacia de plantao em Porto Alegre farmaciadeplantaopa Aldhemir Macedo', 'farmacia de plantao farmaciadeplantaopa', 'farmacias de plantão Porto Alegre farmaciadeplantaopa']

# o link exato que quero que seja clicado
quero_esse_link = "https://www.quehorastemonibus.com.br"
#quero_esse_link = "https://www.guiaportoalegre.com.br"
#quero_esse_link = "https://www.farmaciadeplantaopa.com.br"

# quantas páginas de busca quero que seja feita
total_paginas_busca = 3

buscarPalavra = Busca(url, palavra, quero_esse_link, total_paginas_busca)
buscarPalavra.pesquisar()