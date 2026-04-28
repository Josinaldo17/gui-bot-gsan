import tkinter as tk
from Padrao.login import realizar_login  # Supondo que está aqui
import Padrao.config as configura



class Carregar_login:
    def __init__(self, root, app):

        configuracao = configura.carregar_configuracao()

        self.root = root
        self.app = app

        self.frame = tk.Frame(self.root, bg=configura.HEADER_BG)
        self.frame.pack(fill="both", expand=True)
        tk.Label(self.frame, text="Carregando...",
                 bg=configura.HEADER_BG, fg="white",
                 font=("Segoe UI", 14)).pack(expand=True)
        self.root.update()

        # Espera a tela ser exibida, e depois executa o login
        self.root.after(200, self.executar_login)

    def executar_login(self):

        try:
            mensagem, situacao, _, _ = realizar_login(False, False)

            if situacao:
                print("Login concluido com Sucesso")
                self.ir_para_menu()
            else:
                print("Falha no login")
                self.finalizar_login(mensagem)

        except Exception as e:
            print(f"Erro ao fazer login : {e}")
            self.ir_para_login("Erro ao usar Selenio")

    def ir_para_menu(self):
        self.app.switch_to_menu()

    def ir_para_login(self, mensagem):
        self.app.mensagem = mensagem
        self.app.switch_to_login(mensagem)




        

    