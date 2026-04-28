from Padrao.config import carregar_configuracao, salvar_configuracao, adicionar_rodape_com_link
import webbrowser

configuracao = carregar_configuracao()


import tkinter as tk


import Padrao.config as configura

class MenuObterDados(tk.Frame):
    def __init__(self, parent, controller):
        # 1. Inicializa o Frame pai
        super().__init__(parent, bg=configura.BG)
        self.app = controller 
     
        self.container = tk.Frame(self, bg=configura.BG)
        self.container.pack(expand=True)

        self.frame_empresa = tk.Frame(self.container, bg=configura.BG)
        self.frame_empresa.pack(pady=5, padx=10,  fill="none")
 
        # Cabeçalho com título
        self.header_label = tk.Label(self.frame_empresa, text="Tipos de Dados OS", font=("Arial", 15, "bold"), fg="#3b5998", bg=configura.BG)
        self.header_label.grid(row=0, column=0, pady=7, padx=100)

        # Cria os 4 botões com espaçamento e estilo
        self.button_imprimir = tk.Button(self.frame_empresa, text="Extrair\nParecer", font=("Arial", 11, "bold"), width=25, height=2,  bg=configura.SIDEBAR_ACTIVE, fg="white", relief="flat", command=self.extrairpareceros)
        self.button_imprimir.grid(row=1, column=0, pady=7)

        self.button_2 = tk.Button(self.frame_empresa, text="Módulo Indisponível", font=("Arial", 11), width=25, height=2, bg="#D5D8DC", fg="#7F8C8D", relief="flat", state="disabled")
        self.button_2.grid(row=2, column=0, pady=7)

        self.button_3 = tk.Button(self.frame_empresa, text="Módulo Indisponível", font=("Arial", 11), width=25, height=2, bg="#D5D8DC", fg="#7F8C8D", relief="flat", state="disabled")
        self.button_3.grid(row=3, column=0, pady=7)

        self.button_4 = tk.Button(self.frame_empresa, text="Módulo Indisponível", font=("Arial", 11), width=25, height=2, bg="#D5D8DC", fg="#7F8C8D", relief="flat", state="disabled")
        self.button_4.grid(row=4, column=0, pady=10)


        # Função que abre o link no navegador
    
    def extrairpareceros(self):
        self.app.switch_to_extrato_parecer_os()