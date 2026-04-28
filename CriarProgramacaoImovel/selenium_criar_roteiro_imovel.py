from selenium.webdriver.common.by import By
from Padrao.config import carregar_configuracao
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time


# Função para preencher o roteiro
def criar_add_roteiro_imovel(idEmpresa, localidade, setor, rota, AguaSituacao, clienteUsuario, categoriaImovel, situacaoImovel, Ncadastrador, quant_minima, tempo, driver):
    configuracao = carregar_configuracao()
    quantidade_selecionada = 0
    
    try:
        driver.get(f"{configuracao['linkGsan']}exibirGerarRoteiroDispositivoMovelAction.do?menu=sim")

        Select(driver.find_element(By.NAME, "idEmpresa")).select_by_value(str(idEmpresa))
        Select(driver.find_element(By.NAME, "idLocalidade")).select_by_value(str(localidade))
        Select(driver.find_element(By.NAME, "codigoSetorComercial")).select_by_value(str(setor))
        Select(driver.find_element(By.NAME, "rota")).select_by_value(str(rota))

        driver.find_element(By.XPATH, "//input[@class='bottonRightCol' and @value=' >> ']").click()

        agua_select = Select(driver.find_element(By.NAME, "ligacaoAguaSituacao"))
        for item in AguaSituacao:
            agua_select.select_by_value(str(item))

        driver.find_element(By.XPATH, f"//input[@name='clienteUsuario' and @value='{clienteUsuario}']").click()

        cat_select = Select(driver.find_element(By.NAME, "categoriaImovel"))
        for item in categoriaImovel:
            cat_select.select_by_value(str(item))

        # Situação do Imóvel - usando JavaScript por serem checkboxes
        for item in situacaoImovel:
            checkbox = driver.find_element(By.XPATH, f"//input[@name='indicadorSituacaoImovel' and @value='{item}']")
            if not checkbox.is_selected():
                checkbox.click()

        driver.find_element(By.XPATH, "//input[@name='Button' and @value='Pesquisar']").click()

        try:
            totalMatriculas_input = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.NAME, "totalMatriculas")))
            totalMatriculas = totalMatriculas_input.get_attribute("value")
        except:
            totalMatriculas = 0
  
        totalMatriculas = int(totalMatriculas)
        quant_minima = int(quant_minima)

        if totalMatriculas ==  0:

            if clienteUsuario != 3:

                print("A primeira quantida foi", totalMatriculas)


                clienteUsuario = 3

                driver.find_element(By.XPATH, "//input[@name='botaoVoltar' and @value='Voltar']").click()

                driver.find_element(By.XPATH, f"//input[@name='clienteUsuario' and @value='{clienteUsuario}']").click()

                driver.find_element(By.XPATH, "//input[@name='Button' and @value='Pesquisar']").click()

            
                try:
                    totalMatriculas_input = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.NAME, "totalMatriculas")))
                    totalMatriculas = int(totalMatriculas_input.get_attribute("value"))
                except Exception as e:
                    return f"Erro na segunda tentativa de achar as matriculas: {e}", quantidade_selecionada
                
            else:

                return f"Nenhuma matricula encontrada: {e}", quantidade_selecionada
            
        print("A quantidade de checkboxes achada", totalMatriculas)
        


        if totalMatriculas <= quant_minima:
            quantidade_selecionada = totalMatriculas
        else:
            quantidade_selecionada = quant_minima

        print(f"A quantidade a ser selecionada e {quantidade_selecionada}\n{ '=' * 10}")

        checkboxes_xpath = "//input[@name='idsRegistros']"  # Corrigido o XPath
        # Esperando os checkboxes estarem presentes
        checkboxes = WebDriverWait(driver, 1.5).until(
            EC.presence_of_all_elements_located((By.XPATH, checkboxes_xpath))
        )
        # Selecionando as checkboxes
        for i in range(min(quantidade_selecionada, len(checkboxes))):  # Garantir que não se ultrapasse o número de checkboxes disponíveis
            checkbox = checkboxes[i]
            if not checkbox.is_selected():
                checkbox.click()

        
        cadastrador_select = Select(driver.find_element(By.NAME, "cadastrador"))
        cadastrador_select.select_by_visible_text(Ncadastrador)
       

        driver.find_element(By.XPATH, "//input[@name='Button' and @value='Atualizar']").click()

        time.sleep(int(tempo))

        return "Sucesso", quantidade_selecionada


    except Exception as e:
        print(f"Erro no processo: {e}")
        quantidade_selecionada = 0

        return f"Erro: {e}", quantidade_selecionada
    
    

