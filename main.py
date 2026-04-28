import tkinter as tk
from tkinter import ttk
import Padrao.config as configura
from Front import menu , configuracoes 
import time

print("Só um instante... estamos configurando tudo para você! ⚙️", flush=True)

class Aplicacao:

    def __init__(self, root):
        self.root = root
        self.app = None
        self._usuario = "Usuario"
        self.switch_to_login("")
        self.fezlogin = False

    # ── Login / Loading ───────────────────────────────────────────────────────
    def switch_to_login(self, mensagem):
        """Destroi tudo e abre a tela de login."""
        self._fechar_tudo()

        # from Front import login
        # login.Login(self.root, mensagem, self)

        frame = tk.Frame(self.root, bg=configura.HEADER_BG)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="Tela de Login",
                 bg=configura.HEADER_BG, fg="white",
                 font=("Segoe UI", 18, "bold")).pack(expand=True)
        btn = tk.Label(frame, text="  Entrar  ->",
                       bg=configura.GREEN, fg="white",
                       font=("Segoe UI", 11, "bold"),
                       padx=16, pady=10, cursor="hand2")
        btn.pack(pady=(0, 80))
        btn.bind("<Button-1>", lambda _: self.finalizar_login())

    def switch_to_loading(self):
        
        self._fechar_tudo()

        from Front import loading
        loading.Carregar_login(self.root, self)

    def finalizar_login(self, usuario="Usuario"):
        """Chamado apos login bem-sucedido. Abre o menu principal."""
        configuracao = configura.carregar_configuracao()
        usuario = configuracao["login"]["usuario"]
        self._usuario = usuario
        self._fechar_tudo()
        self.app = menu.Menu(self.root, controller=self)
        self.app.set_usuario(usuario)
        self.fezlogin = True



    def config_login(self):
        self._fechar_tudo()
        
        main_container = tk.Frame(self.root, bg=configura.BG)
        main_container.pack(expand=True, fill="both")

        self.frame_buttontop = tk.Frame(main_container, bg=configura.BG)
        self.frame_buttontop.pack(pady=0,anchor='center', padx=10,  fill="x")

        tk.Label(self.frame_buttontop, text="⚙️", bg=configura.BG,
                 font=("Segoe UI", 18)).pack(side="left", padx=(16, 6), pady=8)
        tk.Label(self.frame_buttontop, text="Configuração",
                 bg=configura.BG, fg="Black",
                 font=configura.FONT_HEADER).pack(side="left", pady=8)

        self.btn_back = tk.Label(self.frame_buttontop, text="⬅️ Voltar",
                            bg="blue", fg=configura.BG,
                            font=configura.FONT_BTN,
                            padx=14, pady=6, cursor="hand2")
        self.btn_back.pack(side="right", padx=16, pady=10)
        configura.hover_bg(self.btn_back, "blue", configura.BTN_BACK_HV)
        self.btn_back.bind("<Button-1>", lambda _: self.switch_to_login(""))

        self.tela_config = configuracoes.Configuracao(parent=main_container, controller=self)
        self.tela_config.pack(expand=True, fill="both", padx=20, pady=10)


  # ---------------------------------------------------------------------


    def switch_to_menu(self):
        if not self.app:
            self.finalizar_login(self._usuario)

    def switch_to_criarProgramacaoImovel(self):
        self._navegar("M2", "programacao_imovel")

    def switch_to_imprimirOS(self):
        self._navegar("M1", "imprimir_os")

    def switch_to_imprimir_os_fiscais(self, **kwargs):
        self._navegar("M0", "imprimir_os_fiscais", **kwargs)

    def switch_to_extrato_parecer_os(self):
        self._navegar("M0", "extrato_parecer_os")

    def switch_to_menu_obter_dados(self):
        self._navegar("M0", "menu_obter_dados")

    def switch_to_os_gerar(self):
        self._navegar("M1", "gerar_os")

    def switch_to_os_encerrar(self):
        self._navegar("M0", "encerrar_os")

    def switch_to_menu_os(self):
        self._navegar("M1", "criar_os")

    def switch_to_menu_encerrar_os(self):
        self._navegar("M0", "menu_encerrar_os")

    def switch_to_menu_imovel(self):
        self._navegar("M3", "m3_t1")

    def switch_to_menu_cliente(self):
        self._navegar("M4", "m4_t1")

    def switch_to_menu_ordem_corte(self):
        self._navegar("M1", "criar_os")

    def switch_to_criar_os_cort_cvlt(self):
        self._navegar("M1", "criar_os_cort_cvlt")

    def switch_to_configuracao(self):
        self._navegar("M5", "configuracoes") 

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _navegar(self, mod_id, frame_key, **kwargs):
        if not self.app:
            self.finalizar_login(self._usuario)
        self.app.navigate_to(mod_id, frame_key, **kwargs)

    def _fechar_tudo(self):
        """Destroi todos os widgets do root."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.app = None


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Automacoes Gsan")
    root.geometry(configura.carregar_configuracao()["tamanho_tela"])
    root.minsize(780, 520)

    app = Aplicacao(root)
    root.mainloop()
