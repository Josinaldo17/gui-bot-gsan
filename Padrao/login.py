from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Padrao.config import carregar_driver
from Padrao.config import carregar_configuracao




def realizar_login(manter_aberto, olhar_navegador):
    config = carregar_configuracao()

    driver = carregar_driver(olhar_navegador)
    

    try:
        usuario = config["login"]["usuario"]
        senha = config["login"]["senha"]
        
        driver.get(f"{config['linkGsan']}")
        
        wait = WebDriverWait(driver, 5)
        usuario_input = wait.until(EC.presence_of_element_located((By.NAME, 'login')))
        usuario_input.send_keys(usuario)
        
        senha_input = wait.until(EC.presence_of_element_located((By.NAME, 'senha')))
        senha_input.send_keys(senha)

        login_button = wait.until(EC.element_to_be_clickable((By.NAME, 'buttonLogin')))
        login_button.click()

        em_element1 = driver.find_element(By.TAG_NAME, "em")
        mensagem1 = em_element1.text

        driver.get(f"{config['linkGsan']}efetuarLoginAction.do")  # Altere para o caminho do arquivo HTML ou URL

        # Encontrar o conteúdo dentro da tag <em>
        em_element = driver.find_element(By.TAG_NAME, "em")
        mensagem = em_element.text

        mesagem_final = f"{mensagem}\n{mensagem1}"

        print(mesagem_final)

        resultado = False

    except Exception as e:
        
        print(f"Login Valido...")

        resultado =  True

        mesagem_final = "sUCESSO"
    
    finally:
        
        if not manter_aberto:
            driver.quit()
        else:
            print("O navegador permanecerá aberto....")

        return mesagem_final, resultado , driver, wait
            



# "login": {
#         "usuario": "ANAFRAZAO",
#         "senha": "45742@P"
#     },