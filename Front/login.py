from Padrao.compoFront import BtnEscolheLink
import webbrowser
from tkinter import messagebox
import tkinter as tk
import Padrao.config as configura



class Login:
    def __init__(self, root, mesagem, app):
        cor_botao = "#34495E"  # Azul petróleo para os botões (padrão sênior)
        self.root = root
        self.app = app
        self.mesagem = mesagem

        self._show_password = False


        configuracao = configura.carregar_configuracao()

        
        for widget in self.root.winfo_children():
            widget.destroy()

        self.frame = tk.Frame(self.root, bg=configura.SIDEBAR_BG)
        self.frame.pack(fill="both", expand=True)


        self.card = tk.Frame(self.frame, bg=configura.CARD_BG,
                        highlightbackground=configura.BORDER,
                        highlightthickness=1)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=460, height=490)

        self.stripe = tk.Frame(self.card, bg=configura.ACCENT, height=4)
        self.stripe.pack(fill="x")

        self.frame_buttontop = tk.Frame(self.card, bg=configura.CARD_BG)
        self.frame_buttontop.pack(pady=0,anchor='center', padx=10,  fill="x")

        self.button_tela2 = tk.Button(self.frame_buttontop, text="⚙", command=self.ir_para_configuracao)
        self.button_tela2.pack(side='right')

        self.inner = tk.Frame(self.card, bg=configura.CARD_BG)
        self.inner.pack(fill="both", expand=True, padx=100, pady=4)


        self.label_espaco1 = tk.Label(self.inner, text="", bg=configura.CARD_BG)
        self.label_espaco1.pack(pady=10)
  
        # Cabeçalho com título
        self.header_label = tk.Label(self.inner, text="Login", font=("Arial", 24, "bold"), fg="#3b5998", bg=configura.CARD_BG)
        self.header_label.pack(pady=0)

        self.interruptor = BtnEscolheLink(self.inner, "Gsan Normal", self.ao_mudar_interruptor, configuracao)


        self.label_espaco = tk.Label(self.inner, text="", bg=configura.CARD_BG)
        self.label_espaco.pack(pady=10)


        # ── Campo Usuário ────────────────────────────────────────────────────
        tk.Label(self.inner, text="USUÁRIO", bg=configura.CARD_BG, fg=configura.SUBTEXT,
                 font=configura.FONT_LABEL).pack(anchor="w")

        user_wrap = tk.Frame(self.inner, bg=configura.BG,
                             highlightbackground=configura.BORDER,
                             highlightthickness=1)
        user_wrap.pack(fill="x", pady=(2, 10))

        tk.Label(user_wrap, text=" 👤 ", bg=configura.BG,
                 font=("Segoe UI", 10)).pack(side="left")

        self.entry_usuario = tk.Entry(user_wrap, font=configura.FONT_MODULE,
                                   bg=configura.BG, fg=configura.TEXT,
                                   relief="flat", bd=0)
        self.entry_usuario.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 6))
        self._focus_border(user_wrap, self.entry_usuario)

        # ── Campo Senha ──────────────────────────────────────────────────────
        tk.Label(self.inner, text="SENHA", bg=configura.CARD_BG, fg=configura.SUBTEXT,
                 font=configura.FONT_LABEL).pack(anchor="w")

        self.pass_wrap = tk.Frame(self.inner, bg=configura.BG,
                             highlightbackground=configura.BORDER,
                             highlightthickness=1)
        self.pass_wrap.pack(fill="x", pady=(2, 6))

        tk.Label(self.pass_wrap, text=" 🔒 ", bg=configura.BG,
                 font=("Segoe UI", 10)).pack(side="left")

        self.entry_senha = tk.Entry(self.pass_wrap, font=configura.FONT_MODULE,
                                   bg=configura.BG, fg=configura.TEXT,
                                   relief="flat", bd=0, show="●")
        self.entry_senha.pack(side="left", fill="x", expand=True, ipady=6)
        self._focus_border(self.pass_wrap, self.entry_senha)

        # Olho — mostrar/ocultar senha
        self.eye_lbl = tk.Label(self.pass_wrap, text="👁", bg=configura.BG,
                                fg=configura.SUBTEXT, font=("Segoe UI", 10),
                                cursor="hand2", padx=6)
        self.eye_lbl.pack(side="right")
        self.eye_lbl.bind("<Button-1>", self._toggle_password)

        # Botão de login
        self.button_login = tk.Button(self.inner, text="Entrar", font=("Arial", 11, "bold"), width=25, height=2, bg=cor_botao, fg="white", relief="flat", command=self.login)
        self.button_login.pack(pady=20)

        # Texto simples na tela 1
        self.label = tk.Label(self.inner, text=f"{mesagem}", fg="red", bg=configura.CARD_BG)
        self.label.pack(pady=20)


    def executar_login(self):
        # Após validar o login, chama a função de sucesso na App principal
        print("Login realizado!")
        self.app.finalizar_login()
        
    def close(self):
        
        # Fecha a janela da Tela 1
        self.inner.destroy()

    def login(self):
        configuracao = configura.carregar_configuracao()

        

        # Obtém os valores do usuário e senha informados
        usuario_input = self.entry_usuario.get()
        senha_input = self.entry_senha.get()

        if usuario_input != "" or senha_input != "":
            configuracao = configura.carregar_configuracao()
            configuracao["login"]["usuario"] =  usuario_input
            configuracao["login"]["senha"] =  senha_input

            configura.salvar_configuracao(configuracao)

        
        configuracao = configura.carregar_configuracao()

        # Dados de usuário e senha (internos)
        usuario = configuracao["login"]["usuario"]
        senha = configuracao["login"]["senha"]
            
        if usuario == "" and senha == "":
            messagebox.showerror("Erro", "Insira Usuário e senha!\nNao tem nehum salvo no sistema!")
        
        elif not configuracao["caminho_driver"]:
            messagebox.showerror("Erro", "É necessário selecionar um arquivo 'geckodriver' para que o programa funcione.\nEscolha um arquivo válido.")
            self.app.config_login()

        elif usuario_input == "" and senha_input == "":
            self.app.switch_to_loading()  # Chama o método switch_to_loading da classe Aplicacao

        else:
            self.app.switch_to_loading() 

    # Exibe a animação de carregamento
    def show_loading(self):
        self.loading_label = tk.Label(self.inner, text="Carregando...", font=("Arial", 14), bg=configura.BG)
        self.loading_label.pack(pady=20)

    def ao_mudar_interruptor(self):
        # Esse método pode ser ajustado se necessário
        pass
    
    def ir_para_configuracao(self):
        self.app.config_login()


  # ── helpers ──────────────────────────────────────────────────────────────
    def _focus_border(self, wrap, entry):
        entry.bind("<FocusIn>",  lambda _: wrap.config(highlightbackground=configura.ACCENT, highlightthickness=1))
        entry.bind("<FocusOut>", lambda _: wrap.config(highlightbackground=configura.BORDER, highlightthickness=1))

    def _toggle_password(self, _=None):
        self._show_password = not self._show_password
        self.entry_senha.config(show="" if self._show_password else "●")
        self.eye_lbl.config(fg=configura.ACCENT if self._show_password else configura.SUBTEXT)

    # def _login(self, _=None):
    #     user = self.entry_usuario.get().strip()
    #     pwd  = self.entry_senha.get().strip()
    #     if not user or not pwd:
    #         messagebox.showwarning("Atenção", "Preencha usuário e senha.")
    #         return
    #     # Substitua aqui pela sua lógica de autenticação real
    #     messagebox.showinfo("Login", f"Bem-vindo, {user}! ✔")