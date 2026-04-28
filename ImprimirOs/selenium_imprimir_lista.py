from Padrao.config import carregar_configuracao, salvar_configuracao
from Padrao.login import realizar_login 
import datetime
import time
import os
from ImprimirOs.manipular_pdf_lista import procurar_matricula,extrair_adicionar_todas_as_paginas,extrair_pagina_isolada, adicionar_texto_ao_pdf
from Padrao.manipular_pdf import pegar_ultimo_pdf, verificar_pegar_ultimo_pdf_atu_, deletar_arquivo,copiar_pdf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter
import fitz  # PyMuPDF
import time


def imprimir_lista(dados, data, olhar_no_avegador):

    configuracao = carregar_configuracao()
    data_os = configuracao["config_imprir_os"]['data_os'] 
    data_escolhida = configuracao["config_imprir_os"]['data'] 
    arquivos_delete = configuracao["config_imprir_os"]['arquivos_deletedos'] 

    caminho_download = configuracao["caminho_download"]

    

    try:
        numero_de_listas = 0
        print(f"\n{'=' * 20}\nIniciando Gerencia de Listagem.....\n{'=' * 20}")
        print(f"\n\n\n{'=' * 20}")
        # print(dados)
        # print(arquivos_delete)
        # print(len(dados))

        contador = 0

        _, _, driver, wait = realizar_login(True, olhar_no_avegador)


    
        for dado in dados:
            contador = contador + 1  


            if dado['matricula'] == '':
                 print(f"Os {dado['os']} sem matricula ......")
                

            else:           

                driver.get(f"{configuracao['linkGsan']}exibirFiltrarImovelOutrosCriteriosConsumidoresInscricao.do?menu=sim&gerarRelatorio=RelatorioCadastroConsumidoresInscricao&limpar=S")


            # Preencher o campo 'localidadeOrigemID'
                localidade_input = wait.until(EC.presence_of_element_located((By.NAME, 'localidadeOrigemID')))
                localidade_input.clear()  # Limpar campo antes de preencher
                localidade_input.send_keys(dado['localidade'])
                localidade_input.send_keys(Keys.RETURN)  # Simula pressionamento da tecla Enter
                time.sleep(1)  # Espera um pouco entre os passos

                # Preencher o campo 'setorComercialOrigemCD'
                setor_input = wait.until(EC.presence_of_element_located((By.NAME, 'setorComercialOrigemCD')))
                setor_input.clear()
                setor_input.send_keys(dado['setor'])
                setor_input.send_keys(Keys.RETURN)  # Simula pressionamento da tecla Enter
                time.sleep(1)

                # Preencher o campo 'cdRotaInicial'
                rota_input = wait.until(EC.presence_of_element_located((By.NAME, 'cdRotaInicial')))
                rota_input.clear()
                rota_input.send_keys(dado['rota'])
                rota_input.send_keys(Keys.RETURN)  # Simula pressionamento da tecla Enter
                time.sleep(1)

                ordenacao_select = wait.until(EC.presence_of_element_located((By.NAME, 'ordenacaoRelatorio')))
                select = Select(ordenacao_select)
                select.select_by_value("rota")  # Selecionar a opção "ROTA"
                print("Opção 'ROTA' selecionada.")

                # Clicar no botão "Concluir"
                concluir_button = wait.until(EC.element_to_be_clickable((By.NAME, 'concluir')))
                concluir_button.click()
                print("Botão 'Concluir' clicado.")

                # Esperar o pop-up ou a caixa de escolha do relatório ser exibida
                wait.until(EC.presence_of_element_located((By.NAME, 'escolhaTipoRelatorio')))

                # Selecionar o rádio "PDF"
                pdf_radio = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='escolhaTipoRelatorio'][@value='1']")))
                pdf_radio.click()
                print("Opção 'PDF' selecionada.")

                # Verificar arquivos baixados
                # caminho_download = "C:\\Users\\equipehidro\\Downloads"
                ultimo_pdf = pegar_ultimo_pdf(caminho_download)

                # Clicar no botão "Gerar"
                gerar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='botao'][@value='Gerar']")))
                gerar_button.click()
                print(f"Botão 'Gerar' clicado.\n")

                
                # Verificar atualizaçao em arquivos baixados
                nome_pdf_baixado = verificar_pegar_ultimo_pdf_atu_(caminho_download, ultimo_pdf )

                # caminho padao dos arquivos baixados
                caminho_arquivo = f"{caminho_download}\\{nome_pdf_baixado}"
                print(f"\n{'-' * 50}\nPossivelmente o arquivo baixado foi '{nome_pdf_baixado}'\n{'-' * 50}")

                print(f"\nA matricula a ser procurada e {dado['matricula']}")

                # Procura matricula no arquivo

                print(caminho_download)

                pagina_encontrada = procurar_matricula(caminho_arquivo, dado['matricula'])
                
                pdf_lista_sem_nome = f"{configuracao['caminho_download']}\\caema_bot\\LIST_EXT_{dado['matricula']}.pdf" 
                pdf_lista_com_nome= f"{configuracao['caminho_download']}\\caema_bot\\LIST_{dado['matricula']}.pdf"

                             
            
                extrair_pagina_isolada(caminho_arquivo, pagina_encontrada, pdf_lista_sem_nome)

                ultima_lista = adicionar_texto_ao_pdf(pdf_lista_sem_nome, pdf_lista_com_nome , dado['nome'])
                deletar_arquivo(pdf_lista_sem_nome)
                
        

                if numero_de_listas == 0:
                    print(pdf_lista_com_nome)
                    todas_listas = ultima_lista
                    print(todas_listas)

                else:
                    todas_listas = extrair_adicionar_todas_as_paginas(pdf_lista_com_nome, todas_listas, numero_de_listas)
                

                deletar_arquivo(caminho_arquivo)

                

                    
                numero_de_listas = numero_de_listas + 1


            # print("Tamo na lista ",numero_de_listas)
            # print("o total e  ", len(dados))
            # print("estamos lendo a ", contador)
            # print("o total e  ", len(dados) - 1)

            if contador == len(dados) :
                                # print("Entrou aquiiiiii")
                                # print(f"{caminho_download}\\Lista{data_os}.pdf")
                                copiar_pdf(todas_listas,f"{caminho_download}\\Lista{data_os}.pdf")
                                # print(todas_listas)

                                time.sleep(3) 

                                arquivos_delete.append(todas_listas)


    except Exception as e:
        print(f"Erro no processo: {e}")
    finally:
        configuracao = carregar_configuracao()
        arquivos_delete = configuracao["config_imprir_os"]['arquivos_deletedos'] 

        # print(arquivos_delete)


        for arquivo in arquivos_delete:
            # print("agora e o " ,arquivo)
            deletar_arquivo(arquivo)  

        salvar_configuracao(configuracao)    
 
        if not olhar_no_avegador:
            driver.quit()
        else:   
            print("O navegador permanecerá aberto para inspeção.")
