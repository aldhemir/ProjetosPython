"""
Aldhemir Macedo - 2025
Atualizado para Selenium 4 e melhores práticas
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# --- CONFIGURAÇÕES ---
# O diretório do perfil permite salvar o login (QR Code)
# Usando 'os.getcwd()' salvamos na pasta atual do projeto para não dar erro de caminho
dir_path = os.getcwd()
profile = os.path.join(dir_path, "profile", "wpp")

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile}")

# Inicializa o Driver (Sintaxe Selenium 4)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

print("Abrindo WhatsApp Web...")
driver.get('https://web.whatsapp.com/')

# Aguarda até que a lista de conversas apareça (Sinal que o login foi feito/carregado)
# Se for a primeira vez, você terá tempo para escanear o QR Code
try:
    wait = WebDriverWait (driver, 30) # Espera até 30 segundos
    wait.until(EC.presence_of_element_located((By.ID, "side")))
    print("Login verificado/carregado com sucesso!")
except:
    print("Tempo limite excedido. Escaneie o QR Code se necessário.")

# --- DADOS DE ENVIO ---
contatos = ['Nome Exato Contato 1', 'Nome Exato Grupo'] # Tem que ser igual ao que aparece no WPP
mensagem = 'Olá, eu sou um bot do Aldhemir. 🤖'

# --- FUNÇÕES ---

def buscar_contato(contato):
    try:
        print(f"Buscando: {contato}")
        # XPath para a caixa de pesquisa (lado esquerdo)
        # Procuramos um div que seja editável e esteja na estrutura lateral
        search_box = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        ))
        
        search_box.clear()
        search_box.send_keys(contato)
        time.sleep(1) # Pequena pausa para o WPP processar a busca
        search_box.send_keys(Keys.ENTER)
        return True
    except Exception as e:
        print(f"Erro ao buscar contato {contato}: {e}")
        return False

def enviar_mensagem(msg):
    try:
        # XPath para a caixa de mensagem (rodapé da conversa)
        message_box = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        ))
        
        message_box.click()
        message_box.send_keys(msg)
        time.sleep(0.5)
        message_box.send_keys(Keys.ENTER)
        print(f"Mensagem enviada.")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

# --- EXECUÇÃO ---
for contato in contatos:
    if buscar_contato(contato):
        # Pausa de segurança para carregar o chat
        time.sleep(2) 
        enviar_mensagem(mensagem)
        # Pausa entre contatos para evitar bloqueio por spam
        time.sleep(5) 

print("Envios finalizados.")
# driver.quit() # Descomente se quiser fechar o navegador ao final