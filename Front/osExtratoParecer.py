import tkinter as tk
from tkinter import scrolledtext
from Padrao.config import carregar_configuracao, adicionar_rodape_com_link
from OsParecer.selenium_parecer_os import executar_extracao_os 
from tkinter import messagebox
import Padrao.config as configura


class TelaExtratorOS(tk.Frame):
    def __init__(self, parent, controller):
        # 1. Inicializa o Frame pai
        super().__init__(parent, bg=configura.BG)
        self.app = controller 
     
        self.container = tk.Frame(self, bg=configura.BG)
        self.container.pack(expand=True)

        self.configuracao = carregar_configuracao()

        frame_top = tk.Frame(self.container, bg=configura.BG)
        frame_top.pack(pady=5, padx=10, fill="x")

        tk.Button(frame_top, text="Voltar", command=self.voltar).pack(side='left')
        

        # --- Título ---
        tk.Label(self.container, text="Extrato OS(Parecer)", font=("Arial", 16, "bold"), 
                 fg="#3b5998", bg=configura.BG).pack(pady=5)

        # --- Área de Input ---
        tk.Label(self.container, text="Cole as OSs (uma por linha):", bg=configura.BG).pack()
        self.txt_input = scrolledtext.ScrolledText(self.container, width=45, height=8)
        self.txt_input.pack(padx=10, pady=5)

        # --- Botão de Ação ---
        frame_acao = tk.Frame(self.container, bg=configura.BG)
        frame_acao.pack(pady=10)

        # Botão de Ação (agora dentro do frame_acao)
        self.btn_processar = tk.Button(
            frame_acao, 
            text="INICIAR EXTRAÇÃO", 
            font=("Arial", 10, "bold"),
            bg="#4CAF50", 
            fg="white", 
            height=2, 
            width=20,
            command=self.iniciar_thread
        )
        self.btn_processar.pack(side='left', padx=10)

        # Checkbutton (agora dentro do frame_acao)
        self.olhar_no_avegador = tk.BooleanVar(value=True)
        self.olharnavegador_radio = tk.Checkbutton(
            frame_acao, 
            text="Ocultar Navegador", 
            variable=self.olhar_no_avegador, 
            onvalue=False, 
            offvalue=True, 
            font=('Arial', 10),
            bg=configura.BG # Mantendo a cor de fundo
        )
        self.olharnavegador_radio.pack(side='left', padx=10)

        # --- Área de Resultado ---
        tk.Label(self.container, text="Resultado:\nSITUACAO |  UNI_ATUAL  | SERVICO |  MOTIVO | PARECER", bg=configura.BG, font=("Arial", 10)).pack()
        self.txt_output = scrolledtext.ScrolledText(self.container, width=45, height=10, fg="blue")
        self.txt_output.pack(padx=10, pady=5)


    def iniciar_thread(self):
        """Lê os dados e inicia a automação sem travar a tela."""
        conteudo = self.txt_input.get("1.0", tk.END).strip()
        if not conteudo:
            return
            
        lista_os = conteudo.split("\n")
        self.txt_output.delete("1.0", tk.END)
        olhar_no_avegador = self.olhar_no_avegador.get()
        
        executar_extracao_os(lista_os, self.txt_output, olhar_no_avegador)
        
        messagebox.showinfo("Concluido", f"Parecer extraido com Sucesso")


    def voltar(self):        
        self.app.switch_to_menu_obter_dados()

    