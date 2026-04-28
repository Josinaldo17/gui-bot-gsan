from Padrao.config import carregar_configuracao, salvar_configuracao
from ImprimirOs.selenium_imprimir_os import imprimir_os, pegar_os_para_filtrar
import webbrowser
from tkcalendar import Calendar
from tkinter import messagebox
import time

configuracao = carregar_configuracao()


import tkinter as tk

import Padrao.config as configura

class Imprimir_OS(tk.Frame):
    def __init__(self, parent, controller):
        # 1. Inicializa o Frame pai
        super().__init__(parent, bg=configura.BG)
        self.app = controller 
     
        self.container = tk.Frame(self, bg=configura.BG)
        self.container.pack(expand=True)

        frame_buttontop = tk.Frame(self.container, bg=configura.BG)
        frame_buttontop.pack(pady=0,anchor='center', padx=10,  fill="x")

        # Botão para limpar, alinhado à direita
        self.button_tela2 = tk.Button(frame_buttontop, text="Limpar", command=self.limpar_dados , bg=configura.BG) 
        self.button_tela2.pack(side='right')

        # Cria o calendário
        self.cal = Calendar(self.container, selectmode='day', date_pattern='dd/mm/yyyy', locale='pt_BR',  font=("Arial", 18))
        self.cal.pack(pady=20)

        # Olha navegador
        self.olhar_no_avegador = tk.BooleanVar(value=True)
        olharnavegador_radio = tk.Checkbutton(self.container, text="Ocultar Navegador", variable=self.olhar_no_avegador, onvalue=False, offvalue=True, font=('Arial', 10))
        olharnavegador_radio.pack( pady=10) 

        frame_buttonprincipais = tk.Frame(self.container , bg=configura.BG)
        frame_buttonprincipais.pack(pady=0, padx=10,  fill="x")          

        # Botão para confirmar a data escolhida
        self.button_confirmar = tk.Button(frame_buttonprincipais, text=f"Imprimir \nOs", font=("Arial", 11, "bold"), width=25, height=2, bg=configura.SIDEBAR_ACTIVE, fg="white", relief="flat", command=self.selecionar_data)
        self.button_confirmar.pack(side="left", padx=5, pady=10)

        # Botão para cimprimir listagem
        self.button_confirmar = tk.Button(frame_buttonprincipais, text=f"Imprimir \nListagem", font=("Arial", 11, "bold"), width=25, height=2, bg=configura.SIDEBAR_ACTIVE, fg="white", relief="flat", command=self.click_imprimir_listagem)
        self.button_confirmar.pack(side="left", padx=5, pady=10)

        # Botão para imprimir mapa
        self.button_confirmar = tk.Button(frame_buttonprincipais, text=f"Imprimir \nMapas", font=("Arial", 11, "bold"), width=25, height=2, bg=configura.SIDEBAR_ACTIVE, fg="white", relief="flat", command=self.click_imprimir_mapas)
        self.button_confirmar.pack(side="left", padx=5, pady=10)


        
    
        # Função para selecionar a data
    def selecionar_data(self):
        self.data = self.cal.get_date()
        olhar_no_avegador = self.olhar_no_avegador.get()
        # resposta1 = messagebox.askyesno("Filtar Os", f"Deseja Filtrar as OS ?")

        pegar_os_para_filtrar(self.data, olhar_no_avegador)
        
        # if resposta1:
        configuracao = configura.carregar_configuracao()
        dados = configuracao["config_imprir_os"]['dados_fiscais'] 
        self.app.switch_to_imprimir_os_fiscais(Titulo="Imprimir Ordens de Serviço", NomeBotao= "Imprimir OS", Dados=dados, Metodo="Imprimir", Data=self.data,  OlharNoNavegador=olhar_no_avegador )
        # return
            
        # else:
        #     configuracao = carregar_configuracao()            
        #     numeros_OS = [item["os"] for item in configuracao["config_imprir_os"]["dados_fiscais"]]
            # imprimir_os(self.data, numeros_OS, olhar_no_avegador)

            # resposta2 = messagebox.askyesno("Imprimir listagem", f"Deseja a listagem ?")
            # resposta3 = messagebox.askyesno("Imprimir Mapas", f"Deseja os Mapas ?")

        # if resposta2:
        #     self.click_imprimir_listagem()

        # if resposta3:
        #     self.click_imprimir_mapas()


        # messagebox.showinfo("Imprimir", f"Processo Concluido!")

    def click_imprimir_listagem(self):
        configuracao = carregar_configuracao()
        dados = configuracao["config_imprir_os"]['dados'] 
        data = configuracao["config_imprir_os"]['data'] 
        olhar_no_avegador = self.olhar_no_avegador.get()

        if dados == [] or data == "":
            messagebox.showinfo("Erro", f"Sem dados salvos para tirar a listagem\n\n Escolha uma data e click no botao 'Imprimir Os'")
            return

        self.app.switch_to_imprimir_os_fiscais(Titulo="Organizar Listagem das\nOrdens de Serviço", NomeBotao= "Iniciar", Dados=dados, Metodo="Listar" )
        
        # messagebox.showinfo("Concluido", f"Impressao concluida comm sucesso")


        
    def click_imprimir_mapas(self):
        
        configuracao = carregar_configuracao()
        dados = configuracao["config_imprir_os"]['dados'] 
        data = configuracao["config_imprir_os"]['data'] 


        if dados == [] or data == "":
            messagebox.showinfo("Erro", f"Sem dados salvos para tirar os mapas\n\n Escolha uma data e click no botao 'Imprimir Os'")
            return

        elif not configuracao["caminho_pdfs_mapas"]:
            messagebox.showerror("Erro", "É necessário selecionar uma pasta que contenha os mapas em PDF.\nOs arquivos devem estar organizados por localidade, setor e rota.\nEscolha uma pasta válida.")
            self.app.switch_to_configuracao()
            return

        self.app.switch_to_imprimir_os_fiscais(Titulo="Organizar Mapas das\nOrdens de Serviço", NomeBotao= "Iniciar", Dados=dados,  Metodo="Mapas" )

        # messagebox.showinfo("Concluido", f"Mapas prontos para impressao")


        
    def close(self):
        
        self.container.destroy()
    
    
    def voltar_menu(self):        
        self.app.switch_to_menu_os()
    
    def limpar_dados(self):  
        resposta = messagebox.askyesno("Limpar", f"Você está prestes a limpar os dados da última impressão. \n\nDeseja continuar?")

        if resposta:         
            configuracao = carregar_configuracao()

            configuracao["config_imprir_os"]['arquivos_deletedos'] = [] 
            configuracao["config_imprir_os"]['data'] = "" 
            configuracao["config_imprir_os"]['dados'] = [] 
            configuracao["config_imprir_os"]['dados_fiscais'] = [] 
            configuracao["config_imprir_os"]['data_os'] = ""

            salvar_configuracao(configuracao) 



