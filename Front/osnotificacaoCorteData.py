import tkinter as tk
from tkinter import scrolledtext
from Padrao.config import carregar_configuracao, adicionar_rodape_com_link
from CriarOsCorteCVLT.selenium_sms_noti_data import executar_criar_os_cort_cvlt 
from tkinter import messagebox

import Padrao.config as configura



class TelaNotificacaoSmsData(tk.Frame):
    def __init__(self, parent, controller):
        # 1. Inicializa o Frame pai
        super().__init__(parent, bg=configura.BG)
        self.app = controller 
     
        self.container = tk.Frame(self, bg=configura.BG)
        self.container.pack(expand=True)

        # --- Cabeçalho Padrão (Sair e Configurações) ---
        frame_top = tk.Frame(self.container, bg=configura.BG)
        frame_top.pack(pady=5, padx=0, fill="x")

        tk.Button(frame_top, text="Voltar", command=self.voltar).pack(side='left')
        

        # --- Título ---
        tk.Label(self.container, text="GERAR OS CORTE", font=("Arial", 16, "bold"), 
                 fg="#3b5998", bg=configura.BG).pack(pady=5)

        # --- Área de Input ---
        tk.Label(self.container, text="Cole as:\n NOTIFICAÇAO  | MATRICULA  | DATA ENTREGA \n (uma por linha): nessa ordem", bg=configura.BG).pack()
        self.txt_input = scrolledtext.ScrolledText(self.container, width=45, height=8)
        self.txt_input.pack(padx=10, pady=5)

        # --- Botão de Ação ---
        frame_acao = tk.Frame(self.container, bg=configura.BG)
        frame_acao.pack(pady=10)

        # Botão de Ação (agora dentro do frame_acao)
        self.btn_processar = tk.Button(
            frame_acao, 
            text="GERAR OS's", 
            font=("Arial", 10, "bold"),
            bg="#4CAF50", 
            fg="white", 
            height=2, 
            width=20,
            command=self.iniciar_thread
        )
        self.btn_processar.pack(side='left', padx=2)

        # Checkbutton (agora dentro do frame_acao)
        self.olhar_no_avegador = tk.BooleanVar(value=True)
        self.olharnavegador_radio = tk.Checkbutton(
            frame_acao, 
            text="Ocultar\n Navegador", 
            variable=self.olhar_no_avegador, 
            onvalue=False, 
            offvalue=True, 
            font=('Arial', 10),
            bg=configura.BG # Mantendo a cor de fundo
        )
        self.olharnavegador_radio.pack(side='left', padx=10)

        self.txt_unidade = tk.Entry(frame_acao, width=5) # Usei Entry por ser valor único, mas mantive se preferir
        self.txt_unidade.pack(side='left',pady=5)
        tk.Label(frame_acao, text="Unidade de\n Atendimento", bg=configura.BG).pack(pady=(10, 0))
        


        # --- Área de Resultado ---
        tk.Label(self.container, text="Resultado:  OS ", bg=configura.BG, font=("Arial", 10)).pack()
        self.txt_output = scrolledtext.ScrolledText(self.container, width=45, height=10, fg="blue")
        self.txt_output.pack(padx=10, pady=5)


    def iniciar_thread(self):
        """Lê os dados e inicia a automação sem travar a tela."""
        conteudo = self.txt_input.get("1.0", tk.END).strip()
        if not conteudo:
            return
        
        unidade = self.txt_unidade.get() if hasattr(self.txt_unidade, 'get') else self.txt_unidade.get("1.0", tk.END).strip()
        
        if not unidade:
            messagebox.showwarning("Atenção", "Por favor, insira o numero da Unidade de Atendimento.")
            return        
            
        lista_os = conteudo.split("\n")
        self.txt_output.delete("1.0", tk.END)
        olhar_no_avegador = self.olhar_no_avegador.get()
        
        executar_criar_os_cort_cvlt(lista_os, self.txt_output, unidade, olhar_no_avegador)
        
        messagebox.showinfo("Concluido", f"Parecer extraido com Sucesso")


    def voltar(self):        
        self.app.switch_to_menu_os()

    