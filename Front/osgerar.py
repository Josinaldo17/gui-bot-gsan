import tkinter as tk
from tkinter import scrolledtext
from Padrao.config import carregar_configuracao, adicionar_rodape_com_link
from CriarOs.selenium_criar_os import executar_criar_os
from tkinter import messagebox


import Padrao.config as configura


class TelaGerarOs(tk.Frame):
    def __init__(self, parent, controller):
        # 1. Inicializa o Frame pai
        super().__init__(parent, bg=configura.BG)
        self.app = controller 
     
        self.container = tk.Frame(self, bg=configura.BG)
        self.container.pack(expand=True)

        
        # --- Cabeçalho Padrão ---
        frame_top = tk.Frame(self.container, bg=configura.BG)
        frame_top.pack(pady=5, padx=10, fill="x")
        tk.Button(frame_top, text="Voltar", command=self.voltar).pack(side='left')


        # --- Título ---
        tk.Label(self.container, text="GERAR OS", font=("Arial", 16, "bold"), 
                 fg="#3b5998", bg=configura.BG).pack(pady=5)
        

                # --- Unidade de Atendimento ---
        tk.Label(self.container, text="Unidade de Atendimento", bg=configura.BG).pack(pady=(10, 0))
        self.txt_unidade = tk.Entry(self.container, width=5) # Usei Entry por ser valor único, mas mantive se preferir
        self.txt_unidade.pack(pady=5)


        # --- ÁREA LADO A LADO (Matrícula e Observação) ---
        frame_inputs_horiz = tk.Frame(self.container, bg=configura.BG)
        frame_inputs_horiz.pack(pady=5, padx=10)

        # Coluna Matrícula
        col_matricula = tk.Frame(frame_inputs_horiz, bg=configura.BG)
        col_matricula.pack(side="left", padx=5)
        tk.Label(col_matricula, text="Cole as:\n MATRICULA", bg=configura.BG).pack()
        self.txt_matricula = scrolledtext.ScrolledText(col_matricula, width=12, height=4)
        self.txt_matricula.pack()

        # Coluna Observação
        col_obs = tk.Frame(frame_inputs_horiz, bg=configura.BG)
        col_obs.pack(side="left", padx=5)
        tk.Label(col_obs, text="Observação\n", bg=configura.BG).pack()
        self.txt_observacao = scrolledtext.ScrolledText(col_obs, width=28, height=4)
        self.txt_observacao.pack()




        # --- Botão de Ação ---
        frame_acao = tk.Frame(self.container, bg=configura.BG)
        frame_acao.pack(pady=10)

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
        self.btn_processar.pack(side='left', padx=10)

        self.olhar_no_avegador = tk.BooleanVar(value=True)
        self.olharnavegador_radio = tk.Checkbutton(
            frame_acao, 
            text="Ocultar Navegador", 
            variable=self.olhar_no_avegador, 
            onvalue=False, 
            offvalue=True, 
            bg=configura.BG
        )
        self.olharnavegador_radio.pack(side='left', padx=10)

        # --- Área de Resultado ---
        tk.Label(self.container, text="Resultado: OS", bg=configura.BG, font=("Arial", 10)).pack()
        self.txt_output = scrolledtext.ScrolledText(self.container, width=45, height=10, fg="blue")
        self.txt_output.pack(padx=10, pady=5)


    def iniciar_thread(self):
        """Lê os dados e inicia a automação."""
        # Coletando os dados de cada campo individualmente
        matriculas = self.txt_matricula.get("1.0", tk.END).strip()
        observacao = self.txt_observacao.get("1.0", tk.END).strip()
        unidade = self.txt_unidade.get() if hasattr(self.txt_unidade, 'get') else self.txt_unidade.get("1.0", tk.END).strip()
        
        if not matriculas:
            messagebox.showwarning("Atenção", "Por favor, insira as matrículas.")
            return
        
        if not unidade:
            messagebox.showwarning("Atenção", "Por favor, insira o numero da Unidade de Atendimento.")
            return
            
        lista_matricula = matriculas.split("\n")
        self.txt_output.delete("1.0", tk.END)
        olhar_no_avegador = self.olhar_no_avegador.get()
        
        # --- Chamada com a ordem exata que você pediu ---
        # (lista_matricula, txt_output, unidade, observacao, olhar_no_navegador)
        executar_criar_os(lista_matricula, self.txt_output, unidade, observacao, olhar_no_avegador)
        
        messagebox.showinfo("Concluído", "Processo finalizado com sucesso!")

    def voltar(self):        
        self.app.switch_to_menu_os()