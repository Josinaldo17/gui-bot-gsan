from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Padrao.config import carregar_configuracao
from Padrao.login import realizar_login
import tkinter as tk
import time

def Verificar_dados_os(os, driver):
    """Extrai os dados de uma OS específica."""
    try:
        configuracao = carregar_configuracao()
        # Acessar a página de consulta de OS
        driver.get(f"{configuracao['linkGsan']}filtrarOrdemServicoAction.do")

        unidade_input = driver.find_element(By.NAME, "numeroOSParametro")
        unidade_input.clear()
        unidade_input.send_keys(os)
        driver.find_element(By.CSS_SELECTOR, "input[value='Pesquisar']").click()

        # Extração dos campos
        situacaoOS = driver.find_element(By.NAME, "situacaoOS").get_attribute("value")
        unidadeAtual = driver.find_element(By.NAME, "unidadeAtualDescricao").get_attribute("value")
        tipoServico = driver.find_element(By.NAME, "tipoServicoDescricao").get_attribute("value")
        motivo = driver.find_element(By.NAME, "motivoEncerramento").get_attribute("value")
        parecer = driver.find_element(By.XPATH, "//textarea[@name='parecerEncerramento']").get_attribute("value")
        
        parecer = parecer.replace("\n", " ")

        return 'Sucesso', situacaoOS, unidadeAtual, tipoServico, motivo, parecer

    except Exception as e:
        print(f"Erro na OS {os}: {e}")
        return 'Erro', None, None, None, None, None

def executar_extracao_os(lista_os, txt_output, olhar_no_navegador):
    """Gerencia o loop de extração e o login."""
    configuracao = carregar_configuracao()
    
    # Realiza o login usando o seu padrão
    _, _, driver, wait = realizar_login(True, olhar_no_navegador)

    # Entra na tela inicial de filtro conforme seu código original
    driver.get(f"{configuracao['linkGsan']}exibirFiltrarOrdemServicoAction.do?menu=sim")

    situacaoOS_input = driver.find_element(By.NAME, "numeroOS")
    situacaoOS_input.send_keys(400000)
    Filtrar_button = driver.find_element(By.XPATH, "//input[@name='Button' and @value='Filtrar']").click()
    
    # Loop pelas OS enviadas pela interface
    for os in lista_os:
        os = os.strip()
        if os:
            status, situ, unid, tipo, mot, parc = Verificar_dados_os(os, driver)
            
            resultado = f"{situ}	{unid}	{tipo}	{mot}	{parc}\n"

            # Insere o resultado na tela em tempo real
            txt_output.insert(tk.END, resultado)
            txt_output.see(tk.END) # Scroll automático para o final
    

    if not olhar_no_navegador:
        driver.quit()
    