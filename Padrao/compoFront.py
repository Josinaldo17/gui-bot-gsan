import tkinter as tk
from Padrao.config import carregar_configuracao, salvar_configuracao


configuracao = carregar_configuracao()

class BtnEscolheLink:
    def __init__(self, parent_window, texto_inicial, command, configuracao):
        self.window = parent_window
        self.command = command
        self.configuracao = configuracao

        self.interruptor_estado = tk.BooleanVar()

        link_salvo = configuracao.get("linkGsan", "")

        if link_salvo == "https://c1.caema.ma.gov.br/gsan/":
            self.interruptor_estado.set(True)
            texto_inicial = "Homologação"
        else:
            self.interruptor_estado.set(False)
            texto_inicial = "Gsan Normal"

        self.toggle = tk.Checkbutton(
            self.window, 
            text=texto_inicial, 
            variable=self.interruptor_estado,
            onvalue=True, 
            offvalue=False,
            indicatoron=False, 
            width=12,
            command=self.ao_mudar_interruptor
        )
        self.toggle.pack(pady=0)

    def ao_mudar_interruptor(self):
        if self.interruptor_estado.get():
            self.toggle.config(text="Homologação")
            novo_link = "https://c1.caema.ma.gov.br/gsan/"
        else:
            self.toggle.config(text="Gsan Normal")
            novo_link = "http://gsan.caema.ma.gov.br:8080/gsan/"
        
        self.mudar_link_gsan(novo_link)

    def mudar_link_gsan(self, novo_link):
        self.configuracao["linkGsan"] = novo_link
        # Salvar a configuração novamente, se necessário
        salvar_configuracao(self.configuracao)

