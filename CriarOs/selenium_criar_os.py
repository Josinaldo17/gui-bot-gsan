from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Padrao.config import carregar_configuracao
from Padrao.login import realizar_login
import tkinter as tk
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException, TimeoutException, UnexpectedAlertPresentException
import re
import pandas as pd
import time


def Criar_os_sms(matricula_ra, unidade, observacao, driver):
    try:
        configuracao = carregar_configuracao()
        # Acessar a página de cadastro
        driver.get(f"{configuracao['linkGsan']}exibirInserirRegistroAtendimentoAction.do?menu=sim")

        unidade_input = driver.find_element(By.NAME, "unidade")
        unidade_input.clear()
        unidade_input.send_keys(f'{unidade}')
        unidade_input.send_keys(Keys.RETURN)
        time.sleep(1)

        
        # Selecionar as opções do formulário
        tipoSolicitacao_select = Select(driver.find_element(By.NAME, "tipoSolicitacao"))
        tipoSolicitacao_select.select_by_visible_text("2.04 - CADASTRO")

        especificacao_select = Select(driver.find_element(By.NAME, "especificacao"))
        especificacao_select.select_by_visible_text("LEVANTAMENTO DE DADOS PARA ATUALIZACAO CADASTRAL")

        observacao_input = driver.find_element(By.NAME, "observacao")
        observacao_input.send_keys(f'''{observacao}''')

        # Avançar no processo
        Avançar_button = driver.find_element(By.XPATH, "//input[@name='avancar' and @value='Avançar']")
        Avançar_button.click()

        idImovel_input = driver.find_element(By.NAME, "idImovel")
        idImovel_input.send_keys(f'{int(matricula_ra)}')
        idImovel_input.send_keys(Keys.RETURN)
        time.sleep(1)


        try:
            alert = driver.switch_to.alert
            alert.accept()
            print("Alerta aceito.")
        except NoAlertPresentException:
            print("Nenhum alerta presente.")


        Avançar_button = driver.find_element(By.XPATH, "//input[@name='avancar' and @value='Avançar']")
        Avançar_button.click()
        time.sleep(0.5)


        try:
            # Clicar no botão "Avançar" e aguardar
            avancar_btn = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='Avançar']"))
            )
            avancar_btn.click()
            print("Botão 'Avançar' clicado com sucesso!")
        except TimeoutException:
            print("Erro: Botão 'Avançar' não encontrado!")

        try:
            # Clicar no botão "Avançar" e aguardar
            avancar_btn = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='Avançar']"))
            )
            avancar_btn.click()
            print("Botão 'Avançar' clicado com sucesso!")
        except TimeoutException:
            print("Erro: Botão 'Avançar' não encontrado!")

        time.sleep(0.5)

        # Finalizar o processo
        concluirIncompletor_button = driver.find_element(By.XPATH, "//input[@name='concluir' and @value='Concluir']")
        concluirIncompletor_button.click()
        time.sleep(0.5)

        # Capturar o número da OS
        link = driver.find_element(By.XPATH, "//a[contains(@href, 'gerarRelatorioOrdemServicoAction.do')]")

        href = link.get_attribute('href')

        # Usar regex para extrair o número da OS
        match = re.search(r"idsOS=(\d+)", href)

        if match:
            os_number = match.group(1)
            print(f"O número da OS é: {os_number}")
        else:
            print("Número da OS não encontrado.")
            os_number = None

        
        return os_number

    except Exception as e:
        print(f"Erro no processo: {e}")
        
        return None
    


def executar_criar_os(lista_matricula, txt_output, unidade, observacao, olhar_no_navegador):
    """Gerencia o loop de extração e o login."""
    configuracao = carregar_configuracao()
    
    # Realiza o login usando o seu padrão
    _, _, driver, _ = realizar_login(True, olhar_no_navegador)
    
    
    for matricula in lista_matricula:
        matricula = matricula.strip()
        if matricula:
        
        


            os = Criar_os_sms(matricula, unidade, observacao,  driver)
            
            resultado = f"{os}\n"

        else:
            resultado = f"ERRO CAPTURA MATRICULA\n"



        # Insere o resultado na tela em tempo real
        txt_output.insert(tk.END, resultado)
        txt_output.see(tk.END) # Scroll automático para o final
    

    if not olhar_no_navegador:
        driver.quit()
    