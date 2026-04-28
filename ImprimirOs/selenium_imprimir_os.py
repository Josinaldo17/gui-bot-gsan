
import datetime
import time
import pyautogui
import os
from ImprimirOs.selenium_imprimir_lista import imprimir_lista
from Padrao.login import realizar_login 
from ImprimirOs.manipular_pdf_os import ler_pdf_extrair_dados, inserir_nome_no_pdf 
from Padrao.manipular_pdf import pegar_ultimo_pdf, verificar_pegar_ultimo_pdf_atu_
from Padrao.config import carregar_configuracao, salvar_configuracao
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select






# Função para rolar até o elemento
def rolar_para_elemento(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(1)




def marcar_checkbox_os(driver, wait, n_OS, valores_ja_clidados=None):

    try:
       
        configuracao = carregar_configuracao()

        if valores_ja_clidados is None:
            valores_ja_clidados = []
        # 1. Localiza todos os links que expandem a tabela
        links = driver.find_elements(By.XPATH, "//a[contains(@href, 'extendeTabela')]")

        for i, link in enumerate(links):
        
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
            href_value = link.get_attribute("href")
            identifier = href_value.split("'")[1]

            # print(f"\n🔎 Grupo {i+1} | identifier: {identifier}")

            # IMPORTANTE: pegar o container do grupo (ajuste se necessário)
            grupo = link.find_element(By.XPATH, "./ancestor::tr")

            # Buscar checkboxes SOMENTE dentro do grupo
            checkboxes = grupo.find_elements(By.XPATH, f".//input[@type='checkbox' and contains(@value, '{n_OS}')]")

            # print(f"Encontrei {len(checkboxes)} checkboxes nesse grupo")

            valores = []

            for checkbox in checkboxes:

                value_str = str(checkbox.get_attribute("value")).strip()
                url = value_str.split("___")
                numero_os = url[0]
                nomeurl = url[1]

                
                try:
                    if nomeurl not in valores_ja_clidados:
                        
                        link_expandir = WebDriverWait(driver, 1).until(
                            EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, 'javascript:extendeTabela') and contains(@href, '{nomeurl}')]"))
                        )
                        
                        valores_ja_clidados.append(nomeurl)                       
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link_expandir)
                        link_expandir.click()

                except Exception as e:
                    print(f"Erro ao tentar encontrar o link para {nomeurl}: {e}")
                    return False, valores_ja_clidados

                # FAZER CLICA APENAS EM UM LINK POR VEZ
                # afdafdsfdsfsfsdfsdf


                if not checkbox.is_selected():
                    checkbox.click()
                    sucesso = True
                else:
                    sucesso = False   


              
            
            
                

            return True, valores_ja_clidados


           
       
        
        
        
        
    except Exception as e:
        print(f"Erro ao marcar checkboxes: {e}")




def imprimir_os(data_escolhida, numeros_OS, olhar_no_avegador):
    configuracao = carregar_configuracao()
    valores_acumulados = []
    dados_local = []




    data_os = data_escolhida.replace("/","_")

    caminho_download = configuracao["caminho_download"]

    try:
        try:

            _, _, driver, wait = realizar_login(True, olhar_no_avegador)

            # # Aguarda um momento para garantir que a tela esteja pronta
            # time.sleep(2)

            # # Pressiona a tecla "Windows" + "seta para a direita"
            # pyautogui.hotkey('win', 'left')

            # # Aguarda um momento para que a janela se ajuste
            # time.sleep(1)

            # # Pressiona "Enter"
            # pyautogui.press('enter')

            

            driver.get(f"{configuracao['linkGsan']}exibirAcompanharRoteiroProgramacaoOrdemServicoAction.do?menu=sim&filtro=0&dataRoteiro={data_os[:2]}/{data_os[3:5]}/{data_os[-4:]}")
        except Exception as e:
            print(f"Possivelmente erro de acesso, senha e matrícula invalida ")
            print(f"Erro no processo: {e}")


        
        for n_OS in numeros_OS:
            sucesso, valores_acumulados = marcar_checkbox_os(driver, wait, n_OS, valores_acumulados)
            if not sucesso:
                print(f"❌ Erro ou OS não encontrada: {n_OS}")

        
        checkboxes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, f"//input[@name='osSelecionada' and @type='checkbox']"))
        )

        for checkbox in checkboxes:
            if checkbox.is_selected():

                value_str = str(checkbox.get_attribute("value")).strip()
                url = value_str.split("___")
                numero_os = url[0]
                nomeurl = url[1]
            
                # Localiza o link da OS
                os_link_xpath = f"//a[contains(text(), '{numero_os}')]"
                os_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, os_link_xpath))
                )
                

                # Clica no link da OS
                os_link.click()

                # Troca para a janela popup
                driver.switch_to.window(driver.window_handles[-1])

                # Espera os campos da OS serem carregados
                matricula_imovel = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "matriculaImovel"))
                )
                inscricao_imovel = driver.find_element(By.NAME, "inscricaoImovel")

                rota = driver.find_element(By.NAME, "rota")

                # Coleta os dados de matrícula e inscrição
                matricula_imovel_val = matricula_imovel.get_attribute("value")
                inscricao_imovel_val = inscricao_imovel.get_attribute("value")
                rota = rota.get_attribute("value")


                # Dividindo a inscriçãoImovel para pegar a localidade e setor
                localidade = inscricao_imovel_val[:3]  # Primeiros 3 números da inscrição
                setor = inscricao_imovel_val[4:7]  # 3 números seguintes

                # Fecha a janela de detalhes da OS
                close_button = driver.find_element(By.NAME, "ButtonFechar")
                close_button.click()

                # Volta para a janela principal
                driver.switch_to.window(driver.window_handles[0])

                link_elemento = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, \"javascript:extendeTabela('{nomeurl}',false);\")]")))

                nome = link_elemento.find_element(By.TAG_NAME, "b").text


                dados_local.append({
                    "nome": nome,
                    "os": numero_os,
                    "matricula": matricula_imovel_val,
                    "inscricao": inscricao_imovel_val,
                    "localidade": localidade,
                    "setor": setor,
                    "rota": rota  # Por enquanto não estamos pegando a rota
                })

        configuracao["config_imprir_os"]["dados"] = dados_local           
        salvar_configuracao(configuracao)

        print("Finalizndo processo de marca checkblok.....")

        configuracao = carregar_configuracao()
        dados =  configuracao["config_imprir_os"]["dados"]

        ultimo_pdf = pegar_ultimo_pdf(caminho_download)
        
        imprimir_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='ButtonImprimirOs']")))
        imprimir_button.click()

        # Ler o PDF e verificar se os dados estão corretos
        nome_pdf_baixado = verificar_pegar_ultimo_pdf_atu_(caminho_download, ultimo_pdf )
        caminho_arquivo = f"{caminho_download}\\{nome_pdf_baixado}"
        print(f"\n-------------\nPossivelmente o arquivo baixado foi '{nome_pdf_baixado}'\n------------")
        if nome_pdf_baixado:
            pdf_path = os.path.join(caminho_download, nome_pdf_baixado)

            nomes_pr_inserir = ler_pdf_extrair_dados(pdf_path)


            inserir_nome_no_pdf(pdf_path, nomes_pr_inserir, data_os)


            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)  # Apaga o arquivo
                print(f"O arquivo {nome_pdf_baixado} foi deletado...")




            configuracao["config_imprir_os"]["dados"] = dados      
            configuracao["config_imprir_os"]["data_os"] = data_os
            configuracao["config_imprir_os"]["data"] = data_escolhida

        else:
            print("Nenhum PDF encontrado.")


        salvar_configuracao(configuracao)


    except Exception as e:
        print(f"Erro no processo: {e}")
    finally:
        # print(f"\n{'=' * 50}\n{'=' * 50}\nImpressão terminada com sucesso\n\n{'=' * 50}\n{'=' * 50}{'\n' * 20}")
        #josinaldo

        if not olhar_no_avegador:
            driver.quit()
        else:
            print("O navegador permanecerá aberto para inspeção.")
            




def pegar_os_para_filtrar(data_escolhida, olhar_no_avegador):
    configuracao = carregar_configuracao()
    configuracao["config_imprir_os"]["dados"] = []
    configuracao["config_imprir_os"]["dados_fiscais"] = []         
    salvar_configuracao(configuracao)


    data_os = data_escolhida.replace("/","_")




    caminho_download = configuracao["caminho_download"]

    try:
        try:

            _, _, driver, wait = realizar_login(True, olhar_no_avegador)         

            driver.get(f"{configuracao['linkGsan']}exibirAcompanharRoteiroProgramacaoOrdemServicoAction.do?menu=sim&filtro=0&dataRoteiro={data_os[:2]}/{data_os[3:5]}/{data_os[-4:]}")
        except Exception as e:
            print(f"Possivelmente erro de acesso, senha e matrícula invalida ")
            print(f"Erro no processo: {e}")


        # Espera até que todos os links com 'extendeTabela' no href sejam encontrados
        links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'extendeTabela')]")))

        for i, link in enumerate(links):
            try:


                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                href_value = link.get_attribute("href")
                identifier = href_value.split("'")[1]

                # print(f"\n🔎 Grupo {i+1} | identifier: {identifier}")

                # IMPORTANTE: pegar o container do grupo (ajuste se necessário)
                grupo = link.find_element(By.XPATH, "./ancestor::tr")

                # Buscar checkboxes SOMENTE dentro do grupo
                checkboxes = grupo.find_elements(By.XPATH, f".//input[@type='checkbox' and @name='osSelecionada']")

                dados_pego = []

                for checkbox in checkboxes:
                    value_str = str(checkbox.get_attribute("value")).strip()
                    url = value_str.split("___")
                    numero_os = url[0]
                    nomeurl = url[1]

                    # Ajuste no XPath para lidar com as aspas simples do JavaScript
                    # Usamos aspas duplas fora e aspas simples dentro, ou vice-versa
                    xpath_link = f"//a[contains(@href, \"javascript:extendeTabela('{nomeurl}',true);\")]"
                    
                    try:
                        # Localiza o link
                        link_elemento = wait.until(EC.presence_of_element_located((By.XPATH, xpath_link)))
                        
                        # Pega o texto da tag <b> que está dentro dele
                        # .text geralmente resolve, mas se quiser ser específico:
                        nome_no_b = link_elemento.find_element(By.TAG_NAME, "b").text

                        dados_pego.append({
                            "nome": nome_no_b,
                            "os": numero_os,
                            "matricula": "",
                            "inscricao": "",
                            "localidade": "",
                            "setor": "",
                            "rota": ""  # Por enquanto não estamos pegando a rota
                        })
                        
                    except Exception as e:
                        print(f"Erro ao encontrar o nome para {nomeurl}: {e}")

                
                configuracao["config_imprir_os"]["data"] = data_escolhida
                configuracao["config_imprir_os"]["data_os"] = data_os
                configuracao["config_imprir_os"]["dados_fiscais"] = dados_pego                  
                salvar_configuracao(configuracao)


            except Exception as e:
                print(f"Aviso: Erro ao processar as matriculas: {e}")

            break
                

    except Exception as e:
        print(f"Erro no link [{i + 1}]: {e}")

    finally:
        driver.quit()


