import Padrao.config as configura
import webbrowser
from Front import login, criarProgramacaoImovel ,imprimirOs ,configuracoes ,loading , osExtratoParecer, osnotificacaoCorteData, menuObterDados, osgerar, menuOsGerar, osEncerrar, menuEncerrarOs, imprimirOsFiscais
import tkinter as tk


configuracao = configura.carregar_configuracao()


# ── Estrutura de módulos e tabs ───────────────────────────────────────────────
# Cada tab tem:
#   "label"  -> texto exibido na aba
#   "frame"  -> chave usada pelo controller para saber qual tela carregar
MODULES = [
    {
        "id": "M1",
        "label": "Ordem de\nServico",
        "icon": "📋",
        "tabs": [
            {"label": "Gerar OS",        "frame": "criar_os"},
            {"label": "Imprimir OS\nMapa, Listagem",     "frame": "imprimir_os"},
            {"label": "Obter Dados",     "frame": "menu_obter_dados"},
            {"label": "Encerrar OS",     "frame": "menu_encerrar_os"},
        ],
    },
    {
        "id": "M2",
        "label": "Elaborar Roteiro\nTerceirizada",
        "icon": "📊",
        "tabs": [
            {"label": "Programacao",     "frame": "programacao_imovel"},
        ],
    },
    {
        "id": "M3",
        "label": "Gerenciar\nImoveis",
        "icon": "🏠",
        "tabs": [
            {"label": "Indisponível",       "frame": "cadastra"},
            {"label": "Indisponível",          "frame": "editar"},
        ],
    },
    {
        "id": "M4",
        "label": "Gerenciar\nClientes",
        "icon": "👤",
        "tabs": [
            {"label": "Indisponível",       "frame": "cadastra"},
            {"label": "Indisponível",          "frame": "editar"},
        ],
    },
]


class Menu(tk.Frame):

    def __init__(self, root, controller, **kwargs):
        super().__init__(root, bg=configura.BG, **kwargs)
        self.pack(fill="both", expand=True)
        self.controller = controller
        self._active_mid = None

        self._build_header()
        self._build_main()
        self.sidebar.select_first()

    def _build_header(self):
        hdr = tk.Frame(self, bg=configura.HEADER_BG, height=52)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="🤖", bg=configura.HEADER_BG, fg=configura.SIDEBAR_TEXT,
                 font=("Segoe UI", 18)).pack(side="left", padx=(16, 6), pady=8)
        tk.Label(hdr, text="Automacoes Gsan",
                 bg=configura.HEADER_BG, fg=configura.SIDEBAR_TEXT,
                 font=configura.FONT_HEADER).pack(side="left", pady=8)

        
    def _build_main(self):
        main = tk.Frame(self, bg=configura.BG)
        main.pack(fill="both", expand=True)

        self.sidebar = Sidebar(main, on_select=self._on_module_select, controller=self.controller)
        self.sidebar.pack(side="left", fill="y")

        tk.Frame(main, bg=configura.BORDER, width=1).pack(side="left", fill="y")

        right = tk.Frame(main, bg=configura.BG)
        right.pack(side="left", fill="both", expand=True)

        self.tab_bar = TabBar(right, on_select=self._on_tab_select)
        self.tab_bar.pack(fill="x")
        tk.Frame(right, bg=configura.BORDER, height=1).pack(fill="x")

        self.content = ContentArea(right, controller=self.controller)
        self.content.pack(fill="both", expand=True, padx=16, pady=16)

    def _on_module_select(self, mid):
        self._active_mid = mid
        if mid == "M5":            
            self.tab_bar.load_tabs([{"label": "Configurações", "frame": "configuracoes"}], mid)
        else:            
            mod = next(m for m in MODULES if m["id"] == mid)
            self.tab_bar.load_tabs(mod["tabs"], mid)

    def _on_tab_select(self, tid):
        # tid = "M1_criar_os"
        parts = tid.split("_", 1)
        frame_key = parts[1] if len(parts) == 2 else tid
        if self._active_mid:
            self.content.show(self._active_mid, frame_key)

    def navigate_to(self, mod_id, frame_key, **kwargs):
        """Navega programaticamente para um modulo + frame."""
        self.sidebar._select(mod_id)
        self.content.show(mod_id, frame_key, **kwargs)

    def set_usuario(self, nome):
        self.sidebar.set_usuario(nome)


# ==============================================================================
# SIDEBAR
# ==============================================================================

class Sidebar(tk.Frame):
    def __init__(self, parent, on_select, controller, usuario="Usuario", **kwargs):
        super().__init__(parent, bg=configura.SIDEBAR_BG, width=180, **kwargs)
        self.pack_propagate(False)
        self.on_select = on_select
        self.controller = controller  # <--- Salva o controller aqui
        self._buttons = {}
        self._active_mid = None
        self._build(usuario)

    def _build(self, usuario):
        logo_frame = tk.Frame(self, bg=configura.SIDEBAR_BG, height=80)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)
        tk.Label(logo_frame, text="👤", bg=configura.SIDEBAR_BG, fg=configura.BG,
                 font=("Segoe UI", 24)).pack(pady=(14, 0))
        self._usuario_lbl = tk.Label(logo_frame, text=usuario,
                                     bg=configura.SIDEBAR_BG, fg=configura.SIDEBAR_TEXT,
                                     font=("Segoe UI", 8))
        self._usuario_lbl.pack()

        tk.Frame(self, bg=configura.BORDER, height=1).pack(fill="x", pady=(8, 4))

        for mod in MODULES:
            self._make_item(mod)

        tk.Frame(self, bg=configura.SIDEBAR_BG).pack(fill="both", expand=True)
        tk.Frame(self, bg=configura.BORDER, height=1).pack(fill="x")

        cfg_outer = tk.Frame(self, bg=configura.SIDEBAR_BG, pady=2)
        cfg_outer.pack(fill="x", padx=8, side="top", pady=(0, 20)) # Posiciona no rodapé
        
        # ID para as configurações
        cfg_mid = "M5"

        cfg_btn = tk.Frame(cfg_outer, bg=configura.SIDEBAR_ITEM, cursor="hand2")
        cfg_btn.pack(fill="x")

        # Barra lateral de destaque (igual aos outros itens)
        cfg_bar = tk.Frame(cfg_btn, bg=configura.SIDEBAR_ITEM, width=4)
        cfg_bar.pack(side="left", fill="y")

        cfg_icon = tk.Label(cfg_btn, text="⚙️", bg=configura.SIDEBAR_ITEM, fg=configura.BG,
                           font=("Segoe UI", 13), padx=6, pady=8)
        cfg_icon.pack(side="left")

        cfg_lbl = tk.Label(cfg_btn, text="Configuração", bg=configura.SIDEBAR_ITEM,
                           fg=configura.SIDEBAR_TEXT, font=configura.FONT_MODULE, anchor="w")
        cfg_lbl.pack(side="left", fill="x", expand=True)

        # REGISTRO NO DICIONÁRIO DE BOTÕES
        self._buttons[cfg_mid] = {
            "frame": cfg_btn, "bar": cfg_bar,
            "icon": cfg_icon, "text": cfg_lbl, "id_lbl": tk.Label() # Label vazio para não quebrar a lógica
        }

        # BINDINGS (Igual ao _make_item)
        for w in [cfg_btn, cfg_bar, cfg_icon, cfg_lbl]:
            w.bind("<Button-1>", lambda _, m=cfg_mid: self._select(m))
            w.bind("<Enter>",    lambda _, m=cfg_mid: self._on_hover(m, True))
            w.bind("<Leave>",    lambda _, m=cfg_mid: self._on_hover(m, False))

            # Adicionando o comando de clique para ir para a tela de configuração
        cfg_btn.bind("<Button-1>", lambda e: self.controller.switch_to_configuracao())
        cfg_lbl.bind("<Button-1>", lambda e: self.controller.switch_to_configuracao())

        # Efeito de Hover (passar o mouse)
        for w in [cfg_btn, cfg_bar, cfg_lbl, cfg_icon]:
            configura.hover_bg(w, configura.SIDEBAR_BG, configura.SIDEBAR_HOVER)


        tk.Label(self, text="V3.0.2", bg=configura.SIDEBAR_BG,
                 fg="#FFFFFF", font=("Segoe UI", 7)).pack(pady=4)

        self.rodape = configura.adicionar_rodape_com_link(self)
        

    def _make_item(self, mod):
        mid = mod["id"]
        outer = tk.Frame(self, bg=configura.SIDEBAR_BG, pady=2)
        outer.pack(fill="x", padx=8)

        btn = tk.Frame(outer, bg=configura.SIDEBAR_ITEM, cursor="hand2")
        btn.pack(fill="x")

        bar = tk.Frame(btn, bg=configura.SIDEBAR_ITEM, width=4)
        bar.pack(side="left", fill="y")

        icon_lbl = tk.Label(btn, text=mod["icon"], bg=configura.SIDEBAR_ITEM,fg=configura.BG,
                            font=("Segoe UI", 13), padx=6, pady=10)
        icon_lbl.pack(side="left")

        text_lbl = tk.Label(btn, text=mod["label"], bg=configura.SIDEBAR_ITEM,
                            fg=configura.SIDEBAR_TEXT, font=configura.FONT_MODULE,
                            anchor="w", justify="left")
        text_lbl.pack(side="left", fill="x", expand=True)

        id_lbl = tk.Label(btn, text=mid, bg=configura.SIDEBAR_ITEM,
                          fg="#334155", font=("Segoe UI", 7, "bold"), padx=8)
        id_lbl.pack(side="right")

        self._buttons[mid] = {
            "frame": btn, "bar": bar,
            "icon": icon_lbl, "text": text_lbl, "id_lbl": id_lbl,
        }

        for w in [btn, bar, icon_lbl, text_lbl, id_lbl]:
            w.bind("<Button-1>", lambda _, m=mid: self._select(m))
            w.bind("<Enter>",    lambda _, m=mid: self._on_hover(m, True))
            w.bind("<Leave>",    lambda _, m=mid: self._on_hover(m, False))

    def _on_hover(self, mid, entering):
        if mid == self._active_mid:
            return
        color = configura.SIDEBAR_HOVER if entering else configura.SIDEBAR_ITEM
        for key in self._buttons[mid]:
            self._buttons[mid][key].config(bg=color)

    def _select(self, mid):
        if self._active_mid and self._active_mid in self._buttons:
            prev = self._buttons[self._active_mid]
            for key in prev:
                prev[key].config(bg=configura.SIDEBAR_ITEM)
            prev["text"].config(fg=configura.SIDEBAR_TEXT)
            prev["id_lbl"].config(fg="#334155")

        if mid == "M0":
            self._active_mid = None
            return
        
        self._active_mid = mid
        cur = self._buttons[mid]
        for key in ["frame", "icon", "text", "id_lbl"]:
            cur[key].config(bg=configura.SIDEBAR_ACTIVE)
        cur["bar"].config(bg=configura.ACCENT2)
        cur["text"].config(fg=configura.SIDEBAR_TEXT_ACT)
        cur["id_lbl"].config(fg=configura.ACCENT2)

        self.on_select(mid)
        
    def select_first(self):
        self._select(MODULES[0]["id"])

    def set_usuario(self, nome):
        if self._usuario_lbl:
            self._usuario_lbl.config(text=nome)


# ==============================================================================
# TAB BAR
# ==============================================================================

class TabBar(tk.Frame):
    def __init__(self, parent, on_select, **kwargs):
        super().__init__(parent, bg=configura.TAB_BG, height=38, **kwargs)
        self.pack_propagate(False)
        self.on_select = on_select
        self._tabs = {}
        self._active_tid = None

    def load_tabs(self, tabs, module_id):
        for w in self.winfo_children():
            w.destroy()
        self._tabs = {}
        self._active_tid = None

        for i, tab in enumerate(tabs):
            tid = "{}_{}".format(module_id, tab["frame"])
            self._make_tab(tid, tab["label"], i == 0)

    def _make_tab(self, tid, label, select=False):
        tab = tk.Label(self,
                       text="  {}  ".format(label),
                       bg=configura.TAB_BG, fg=configura.TAB_TEXT,
                       font=configura.FONT_TAB, padx=4,
                       cursor="hand2", relief="flat")
        tab.pack(side="left", fill="y", padx=(0, 1))
        self._tabs[tid] = tab
        tab.bind("<Button-1>", lambda _, t=tid: self._select(t))
        tab.bind("<Enter>",    lambda _, t=tid: self._on_hover(t, True))
        tab.bind("<Leave>",    lambda _, t=tid: self._on_hover(t, False))
        if select:
            self._select(tid)

    def _on_hover(self, tid, entering):
        if tid == self._active_tid:
            return
        self._tabs[tid].config(bg=configura.TAB_HOVER if entering else configura.TAB_BG)

    def _select(self, tid):
        if self._active_tid and self._active_tid in self._tabs:
            self._tabs[self._active_tid].config(bg=configura.TAB_BG, fg=configura.TAB_TEXT)
        self._active_tid = tid
        self._tabs[tid].config(bg=configura.TAB_ACTIVE, fg=configura.TAB_TEXT_ACT)
        self.on_select(tid)

# ==============================================================================
# CONTENT AREA
# ==============================================================================


class ContentArea(tk.Frame):
    """
    Area central. Mantem cache de frames ja criados (lazy).
    Chame show(mod_id, frame_key) para trocar o conteudo.
    """
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, bg=configura.BG, **kwargs)
        self.controller = controller
        self._cache = {}
        self._current = None

    def show(self, mod_id, frame_key, **kwargs):
        key = "{}_{}".format(mod_id, frame_key)

        # Telas que sempre precisam ser recriadas com dados frescos
        NO_CACHE = {"imprimir_os_fiscais"}

        # Se está no no-cache e já existe, destroi o antigo
        if frame_key in NO_CACHE and key in self._cache:
            self._cache[key].destroy()
            del self._cache[key]

        if key not in self._cache:
            FRAME_MAP = {
                "criar_os":           menuOsGerar.TelaMenuOsGerar,
                "imprimir_os":        imprimirOs.Imprimir_OS,
                "imprimir_os_fiscais": imprimirOsFiscais.Imprimir_OS_Fiscais,
                "menu_obter_dados":        menuObterDados.MenuObterDados,
                "menu_encerrar_os":        menuEncerrarOs.TelaMenuOsEncerrar,
                "gerar_os":           osgerar.TelaGerarOs,
                "programacao_imovel": criarProgramacaoImovel.CriarProgramacaoImovel,
                "criar_os_cort_cvlt": osnotificacaoCorteData.TelaNotificacaoSmsData,
                "configuracoes": configuracoes.Configuracao,
                "extrato_parecer_os": osExtratoParecer.TelaExtratorOS,
                "encerrar_os": osEncerrar.TelaEncerrarOs,
            }

            cls = FRAME_MAP.get(frame_key)
            if cls:
                frame = cls(self, self.controller, **kwargs)
            else:
                frame = TelaPlaceholder(self, self.controller, frame_key, mod_id)

            self._cache[key] = frame

        if self._current:
            self._current.pack_forget()

        self._cache[key].pack(fill="both", expand=True)
        self._current = self._cache[key]

    def invalidate(self, frame_key):
        """Remove do cache para forcar recriacao na proxima vez."""
        keys = [k for k in self._cache if k.endswith("_{}".format(frame_key))]
        for k in keys:
            self._cache[k].destroy()
            del self._cache[k]



# ==============================================================================
# TELAS PLACEHOLDER
# Substitua cada classe por sua tela real, mantendo a assinatura:
#   __init__(self, parent, controller)
# ==============================================================================

class TelaPlaceholder(tk.Frame):
    """Placeholder generico. Substitua por suas telas reais."""
    def __init__(self, parent, controller, frame_key, mod_id):
        super().__init__(parent, bg=configura.BG)
        mod = next((m for m in MODULES if m["id"] == mod_id), None)
        tab = next((t for m in MODULES for t in m["tabs"] if t["frame"] == frame_key), None)

        card = tk.Frame(self, bg=configura.CARD_BG,
                        highlightbackground=configura.BORDER,
                        highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center",
                   relwidth=0.86, relheight=0.80)

        tk.Frame(card, bg=configura.ACCENT, height=4).pack(fill="x")

        inner = tk.Frame(card, bg=configura.CARD_BG)
        inner.pack(fill="both", expand=True, padx=40, pady=36)

        tk.Label(inner, text=mod["icon"] if mod else "📄",
                 bg=configura.CARD_BG, font=("Segoe UI", 36)).pack(pady=(16, 6))

        tk.Label(inner,
                 text=mod["label"].replace("\n", " ") if mod else mod_id,
                 bg=configura.CARD_BG, fg=configura.SUBTEXT,
                 font=("Segoe UI", 9, "bold")).pack()

        tk.Label(inner,
                 text=tab["label"] if tab else frame_key,
                 bg=configura.CARD_BG, fg=configura.TEXT,
                 font=("Segoe UI", 16, "bold")).pack(pady=(4, 14))

        tk.Frame(inner, bg=configura.BORDER, height=1).pack(fill="x", pady=(0, 14))

        tk.Label(inner,
                 text="Tela '{}' ainda nao implementada.".format(frame_key),
                 bg=configura.CARD_BG, fg=configura.SUBTEXT,
                 font=("Segoe UI", 9), justify="center").pack()


