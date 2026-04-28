from Padrao.config import carregar_configuracao, salvar_configuracao, adicionar_rodape_com_link
import webbrowser

configuracao = carregar_configuracao()


import tkinter as tk

# Classe para a Tela 1
import Padrao.config as configura

class TelaMenuOsEncerrar(tk.Frame):
    def __init__(self, parent, controller):
        # 1. Inicializa o Frame pai
        super().__init__(parent, bg=configura.BG)
        self.app = controller 
     
        self.container = tk.Frame(self, bg=configura.BG)
        self.container.pack(expand=True)

        # Botão para ir para a Tela Login
        frame_buttontop = tk.Frame(self.container, bg=configura.BG)
        frame_buttontop.pack(pady=0,anchor='center', padx=10,  fill="x")
         
        self.frame_buttontop = tk.Frame(self.container , bg=configura.BG)
        self.frame_buttontop.pack(pady=5, padx=10,  fill="none")

        # Cria os 4 botões com espaçamento e estilo
        self.button_imprimir = tk.Button(self.frame_buttontop, text="Ausência  de\nDocumento", font=("Arial", 11, "bold"), width=25, height=2, bg=configura.SIDEBAR_ACTIVE, fg="white", relief="flat", command=self.encerrarOs)
        self.button_imprimir.grid(row=1, column=0, pady=7)

        self.button_2 = tk.Button(self.frame_buttontop, text="Módulo Indisponível", font=("Arial", 11), width=25, height=2, bg="#D5D8DC", fg="#7F8C8D", relief="flat", state="disabled")
        self.button_2.grid(row=2, column=0, pady=7)

       
    # def menuOrdemdeCorte(self):
    #     self.app.switch_to_menu_ordem_corte()

    def encerrarOs(self):
        self.app.switch_to_os_encerrar()
 
    # def ir_para_configuracao(self):
    #     self.app.switch_to_configuracao(self.app.switch_to_menu_os)
