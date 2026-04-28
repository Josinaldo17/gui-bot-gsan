import tkinter as tk
from Padrao.login import realizar_login  # Supondo que está aqui
from Padrao.functFront import Padroes_Front
from Padrao.compoFront import BtnEscolheLink
import Padrao.config as configura
from tkinter import messagebox


class Configuracao(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=configura.BG)
        self.app = controller
        self.Padroes_Front = Padroes_Front()
 
        configuracao = configura.carregar_configuracao()
        usuario = configuracao["login"].get("usuario", "—")
 
        self.container = tk.Frame(self, bg=configura.BG)
        self.container.pack(expand=True, fill="both", padx=20, pady=16)
 
        # ══════════════════════════════════════════════════════════════════════
        # Card Único: Configurações Gerais
        # ══════════════════════════════════════════════════════════════════════
        card = tk.Frame(self.container, bg=configura.CARD_BG,
                        highlightbackground=configura.BORDER,
                        highlightthickness=1)
        card.pack(fill="x", pady=(0, 12))
 
        # Faixa azul no topo
        tk.Frame(card, bg=configura.ACCENT, height=3).pack(fill="x")
 
        # Título do card
        tk.Label(card, text="CONFIGURAÇÕES DO SISTEMA",
                 bg=configura.CARD_BG, fg=configura.SUBTEXT,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=14, pady=(10, 6))
 
        # --- SEPARADOR 1 ---
        tk.Frame(card, bg=configura.BORDER, height=1).pack(fill="x", padx=14)
 
        # ── Seção 1: Usuário e Servidor (Lado a Lado) ────────────────────────
        grid = tk.Frame(card, bg=configura.CARD_BG)
        grid.pack(fill="x", padx=14, pady=10)

        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(3, weight=1)

        # Lado Esquerdo: Usuário
        tk.Label(grid, text="👤 USUÁRIO:",
                bg=configura.CARD_BG, fg=configura.SUBTEXT,
                font=("Segoe UI", 8, "bold"),
                width=10, anchor="w").grid(row=0, column=0, sticky="w", pady=5)

        usuario_wrap = tk.Frame(grid, bg="#F8FAFC", highlightbackground=configura.BORDER, highlightthickness=1)
        usuario_wrap.grid(row=0, column=1, sticky="ew", padx=(8, 15), pady=4)

        tk.Label(usuario_wrap, text=usuario, bg="#F8FAFC", fg=configura.TEXT,
                 font=("Segoe UI", 9), anchor="w", padx=8).pack(fill="x", ipady=5)

        # Lado Direito: Servidor
        tk.Label(grid, text="🌐 SERVIDOR:",
                bg=configura.CARD_BG, fg=configura.SUBTEXT,
                font=("Segoe UI", 8, "bold"),
                width=10, anchor="w").grid(row=0, column=2, sticky="w", pady=5)

        servidor_wrap = tk.Frame(grid, bg=configura.CARD_BG)
        servidor_wrap.grid(row=0, column=3, sticky="w", padx=(8, 0), pady=4)

        self.interruptor = BtnEscolheLink(
            servidor_wrap, "Gsan Normal",
            self.ao_mudar_interruptor, configuracao
        )

        if configuracao["login"]["usuario"]:

            servidor_wrap2 = tk.Frame(grid, bg=configura.CARD_BG)
            servidor_wrap2.grid(row=0, column=3, sticky="e", padx=(8, 0), pady=4)

            btn_back = tk.Label(servidor_wrap2, text="⬅️ Sair",
                                bg="red", fg=configura.BG,
                                font=configura.FONT_BTN,
                                padx=14, pady=6, cursor="hand2")
            btn_back.pack(side="right", padx=16, pady=10)
            configura.hover_bg(btn_back, "red", configura.BTN_BACK_HV)
            btn_back.bind("<Button-1>", lambda _: self.sair_conta())

        else:

            servidor_wrap2 = tk.Frame(grid, bg=configura.CARD_BG)
            servidor_wrap2.grid(row=0, column=3, sticky="e", padx=(8, 0), pady=4)

            btn_back = tk.Label(servidor_wrap2, text="Login",
                                bg="blue", fg=configura.BG,
                                font=configura.FONT_BTN,
                                padx=14, pady=6, cursor="hand2")
            btn_back.pack(side="right", padx=16, pady=10)
            configura.hover_bg(btn_back, "blue", configura.BTN_BACK_HV)
            btn_back.bind("<Button-1>", lambda _: self.app.switch_to_login(""))


        # --- SEPARADOR 2 ---
        tk.Frame(card, bg=configura.BORDER, height=1).pack(fill="x", padx=14)
 
        # ── Seção 2: Geckodriver ──────────────────────────────────────────────
        self.picker_driver = FilePickerRow(
            card, # Agora o pai é o card
            titulo="ARQUIVO GECKODRIVER",
            comando=self.selecionar_arquivo_getdriver,
        )
        self.picker_driver.pack(fill="x", padx=2, pady=2) # Padding interno leve
        
        caminho_driver = configuracao.get("caminho_driver", "")
        self.picker_driver.set_arquivo(caminho_driver)
 
        # --- SEPARADOR 3 ---
        tk.Frame(card, bg=configura.BORDER, height=1).pack(fill="x", padx=14)
 
        # ── Seção 3: Caminho dos mapas ────────────────────────────────────────
        self.picker_mapas = FilePickerRow(
            card, # Agora o pai é o card
            titulo="CAMINHO DOS MAPAS",
            comando=self.selecionar_arquivo_mapas,
        )
        self.picker_mapas.pack(fill="x", padx=2, pady=2)
 
        caminho_mapas = configuracao.get("caminho_pdfs_mapas", "")
        self.picker_mapas.set_arquivo(caminho_mapas)
 
        # ── Rodapé ────────────────────────────────────────────────────────────
        self.rodape = configura.adicionar_rodape_com_link(self.container)

    def selecionar_arquivo_getdriver(self):
        configuracao = configura.carregar_configuracao()

        caminho, arquivo = self.Padroes_Front.selecionar_arquivo()

        if not caminho.endswith(".exe"):
            tk.messagebox.showerror("Erro", f"O arquivo {arquivo} nao e valido!")
        
        else: 
            configuracao["caminho_driver"] = caminho.replace('/', '\\')

            configura.salvar_configuracao(configuracao)

            if self.app.fezlogin:
                self.app.switch_to_configuracao()
            else:
                self.app.config_login()


    def selecionar_arquivo_mapas(self):
        configuracao = configura.carregar_configuracao()

        self.caminho = self.Padroes_Front.selecionar_pasta()

        if self.caminho:
            configuracao["caminho_pdfs_mapas"] = self.caminho.replace('/', '\\')

            configura.salvar_configuracao(configuracao)

            if self.app.fezlogin:
                self.app.switch_to_configuracao()
            else:
                self.app.config_login()
        
        else: 
            tk.messagebox.showerror("Erro", f"O arquivo {self.caminho} nao e valido!")
            

    def sair_conta(self):
        configuracao = configura.carregar_configuracao()

        resposta = messagebox.askyesno("Redefinir acesso", "Você está prestes a redefinir o usuário e a senha do sistema.\nEssa ação não pode ser desfeita.\n\nDeseja continuar?")

        if resposta:
            try:
                configuracao["login"]["usuario"] =  ""
                configuracao["login"]["senha"] =  ""
                configura.salvar_configuracao(configuracao)
            except:
                tk.messagebox.showerror("Erro", f"Erro ao redefinir o usuário")
            
            self.app.switch_to_login("")
            self.fezlogin = False

        else:
            return


   

    def ao_mudar_interruptor(self):
        pass


class FilePickerRow(tk.Frame):
    def __init__(self, parent, titulo, comando, **kwargs):
        # Removido highlightthickness e highlightbackground para fundir com o card pai
        super().__init__(parent, bg=configura.CARD_BG, **kwargs)

        tk.Label(self, text=titulo,
                 bg=configura.CARD_BG, fg=configura.SUBTEXT,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12, pady=(8, 4))

        row = tk.Frame(self, bg=configura.CARD_BG)
        row.pack(fill="x", padx=12, pady=(0, 10))

        self._btn = tk.Label(row,
                             text="  📂  Escolher Arquivo  ",
                             bg=configura.ACCENT, fg="white",
                             font=("Segoe UI", 9, "bold"),
                             padx=4, pady=7, cursor="hand2")
        self._btn.pack(side="left")
        self._btn.bind("<Button-1>", lambda _: comando())
        self._btn.bind("<Enter>", lambda _: self._btn.config(bg="#005f8e"))
        self._btn.bind("<Leave>", lambda _: self._btn.config(bg=configura.ACCENT))

        self._lbl_arquivo = tk.Label(row,
                                     text="Nenhum arquivo selecionado",
                                     bg=configura.CARD_BG, fg=configura.SUBTEXT,
                                     font=("Segoe UI", 8, "italic"))
        self._lbl_arquivo.pack(side="left", padx=(10, 0))

    def set_arquivo(self, caminho: str):
        """Atualiza o nome exibido ao lado do botão."""
        if caminho:
            self._lbl_arquivo.config(text=caminho, fg=configura.TEXT)
        else:
            self._lbl_arquivo.config(text="Nenhum arquivo selecionado",
                                     fg=configura.SUBTEXT)
