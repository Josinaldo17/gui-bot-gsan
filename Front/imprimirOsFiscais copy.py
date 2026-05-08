import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
import json


# --- Mock do objeto de configuração (substitua pelo seu import real) ---
class Configura:
    BG       = "#F0F4F8"
    CARD_BG  = "#FFFFFF"
    BORDER   = "#CBD5E1"
    TEXT     = "#1E293B"
    SUBTEXT  = "#64748B"
    ACCENT   = "#0077B6"
    ACCENT2  = "#00B4D8"
    GREEN    = "#2DC653"
    GREEN_HV = "#25A244"
    RED      = "#E53E3E"
    RED_HV   = "#C53030"

configura = Configura()

# ── Helpers ───────────────────────────────────────────────────────────────────
def hover(widget, normal, over):
    widget.bind("<Enter>", lambda _: widget.config(bg=over))
    widget.bind("<Leave>", lambda _: widget.config(bg=normal))


def card(parent, **kwargs):
    return tk.Frame(parent, bg=configura.CARD_BG,
                    highlightbackground=configura.BORDER,
                    highlightthickness=1, **kwargs)


# ── Checkbox moderno (mesmo padrão do projeto) ────────────────────────────────
class ModernCheck(tk.Frame):
    def __init__(self, parent, var, on_change=None, **kwargs):
        super().__init__(parent, bg=parent.cget("bg"), **kwargs)
        self.var = var
        self.on_change = on_change

        self.box = tk.Label(self, width=2, height=1,
                            bg=self.cget("bg"), relief="flat",
                            font=("Segoe UI", 9), cursor="hand2")
        self.box.pack()
        self._draw()
        self.box.bind("<Button-1>", self._toggle)

    def _draw(self):
        bg_parent = self.cget("bg")
        if self.var.get():
            self.box.config(text="✔", fg=configura.ACCENT, bg="#EBF5FF",
                            highlightbackground=configura.ACCENT,
                            highlightthickness=1)
        else:
            self.box.config(text=" ", fg=bg_parent, bg=bg_parent,
                            highlightbackground=configura.BORDER,
                            highlightthickness=1)

    def _toggle(self, _=None):
        self.var.set(not self.var.get())
        self._draw()
        if self.on_change:
            self.on_change()

    def set(self, value):
        self.var.set(value)
        self._draw()


# ══════════════════════════════════════════════════════════════════════════════
# TELA PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════
class TelaAcompanhamento(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg=configura.BG)
        self.controller = controller

        # Estado
        self._grupos: dict       = {}   # nome -> {"open": bool, "check": BoolVar, "os_items": [...]}
        self._os_checks: dict    = {}   # os_id -> {"var": BoolVar, "dados": dict}
        self._frames_os: dict    = {}   # nome -> frame filho (expandível)

        self._build_ui()
        self._popular_dados()

    # ── Build UI ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Cabeçalho ─────────────────────────────────────────────────────────
        header = tk.Frame(self, bg=configura.ACCENT, height=52)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="📋", bg=configura.ACCENT,
                 font=("Segoe UI", 18)).pack(side="left", padx=(16, 6), pady=8)
        tk.Label(header, text="Acompanhamento de Ordens de Serviço",
                 bg=configura.ACCENT, fg="white",
                 font=("Segoe UI", 12, "bold")).pack(side="left", pady=8)

        # ── Barra de ações ────────────────────────────────────────────────────
        toolbar = tk.Frame(self, bg=configura.BG)
        toolbar.pack(fill="x", padx=20, pady=(14, 6))

        # Contador de selecionados
        self._lbl_count = tk.Label(toolbar, text="0 OS selecionadas",
                                   bg=configura.BG, fg=configura.SUBTEXT,
                                   font=("Segoe UI", 9))
        self._lbl_count.pack(side="left")

        # Botões lado direito
        btn_frame = tk.Frame(toolbar, bg=configura.BG)
        btn_frame.pack(side="right")

        # Selecionar / Desmarcar todos
        self._btn_sel_todos = tk.Label(btn_frame, text="  ☑  Selecionar Todos  ",
                                       bg="#E2E8F0", fg=configura.TEXT,
                                       font=("Segoe UI", 9, "bold"),
                                       padx=4, pady=6, cursor="hand2")
        self._btn_sel_todos.pack(side="left", padx=(0, 6))
        self._btn_sel_todos.bind("<Button-1>", lambda _: self._toggle_todos(True))
        hover(self._btn_sel_todos, "#E2E8F0", "#CBD5E1")

        self._btn_desel_todos = tk.Label(btn_frame, text="  ☐  Desmarcar Todos  ",
                                         bg="#E2E8F0", fg=configura.TEXT,
                                         font=("Segoe UI", 9, "bold"),
                                         padx=4, pady=6, cursor="hand2")
        self._btn_desel_todos.pack(side="left", padx=(0, 16))
        self._btn_desel_todos.bind("<Button-1>", lambda _: self._toggle_todos(False))
        hover(self._btn_desel_todos, "#E2E8F0", "#CBD5E1")

        # Separador
        tk.Frame(btn_frame, bg=configura.BORDER, width=1).pack(side="left", fill="y", padx=(0, 16))

        # Cancelar
        btn_cancelar = tk.Label(btn_frame, text="  ✕  Cancelar  ",
                                bg="#FED7D7", fg=configura.RED,
                                font=("Segoe UI", 9, "bold"),
                                padx=4, pady=6, cursor="hand2")
        btn_cancelar.pack(side="left", padx=(0, 6))
        btn_cancelar.bind("<Button-1>", lambda _: self._cancelar())
        hover(btn_cancelar, "#FED7D7", "#FEB2B2")

        # Salvar
        btn_salvar = tk.Label(btn_frame, text="  ✔  Salvar Seleção  ",
                              bg=configura.GREEN, fg="white",
                              font=("Segoe UI", 9, "bold"),
                              padx=4, pady=6, cursor="hand2")
        btn_salvar.pack(side="left")
        btn_salvar.bind("<Button-1>", lambda _: self._salvar())
        hover(btn_salvar, configura.GREEN, configura.GREEN_HV)

        # ── Card da lista ─────────────────────────────────────────────────────
        card_lista = card(self)
        card_lista.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        tk.Frame(card_lista, bg=configura.ACCENT, height=3).pack(fill="x")

        # Cabeçalho das colunas
        self._build_col_header(card_lista)

        # Área scrollável
        scroll_container = tk.Frame(card_lista, bg=configura.CARD_BG)
        scroll_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(scroll_container, bg=configura.CARD_BG,
                           highlightthickness=0)
        sb = ttk.Scrollbar(scroll_container, orient="vertical",
                           command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)

        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._list_frame = tk.Frame(canvas, bg=configura.CARD_BG)
        self._canvas_window = canvas.create_window(
            (0, 0), window=self._list_frame, anchor="nw")

        self._list_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
            lambda e: canvas.itemconfig(self._canvas_window, width=e.width))
        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        self._canvas = canvas

    def _build_col_header(self, parent):
        """Linha de cabeçalho das colunas."""
        hdr = tk.Frame(parent, bg="#F8FAFC",
                       highlightbackground=configura.BORDER,
                       highlightthickness=1)
        hdr.pack(fill="x", padx=2, pady=(2, 0))

        cols = [
            ("",          40,  "center"),
            ("CLIENTE",   220, "w"),
            ("OS",        90,  "center"),
            ("MATRÍCULA", 110, "center"),
            ("INSCRIÇÃO", 190, "center"),
            ("LOC.",      60,  "center"),
            ("SETOR",     60,  "center"),
            ("ROTA",      60,  "center"),
        ]
        for text, w, anchor in cols:
            tk.Label(hdr, text=text,
                     bg="#F8FAFC", fg=configura.SUBTEXT,
                     font=("Segoe UI", 8, "bold"),
                     width=w // 8, anchor=anchor).pack(side="left", padx=2, pady=6)

    # ── Dados ─────────────────────────────────────────────────────────────────
    def _popular_dados(self):
        dados = [
            {"nome": "JOSE BENEDITO PINTO",  "os": "5071122", "matricula": "3247910", "inscricao": "151.130.002.0109.000", "localidade": "151", "setor": "130", "rota": "2"},
            {"nome": "JOAO BATISTA COBRA",    "os": "5071719", "matricula": "348430",  "inscricao": "111.104.043.0110.000", "localidade": "111", "setor": "104", "rota": "43"},
            {"nome": "JOSE DE RIBAMAR NUNE",  "os": "5071270", "matricula": "350079",  "inscricao": "111.104.038.0185.000", "localidade": "111", "setor": "104", "rota": "38"},
            {"nome": "JADIEL RIBEIRO REIS",   "os": "5068807", "matricula": "322849",  "inscricao": "111.104.024.0369.000", "localidade": "111", "setor": "104", "rota": "24"},
            {"nome": "JADIEL RIBEIRO REIS",   "os": "5068814", "matricula": "322822",  "inscricao": "111.104.024.0370.000", "localidade": "111", "setor": "104", "rota": "24"},
            {"nome": "MARIA LUCIA SANTOS",    "os": "5071500", "matricula": "410023",  "inscricao": "112.105.010.0088.000", "localidade": "112", "setor": "105", "rota": "10"},
            {"nome": "MARIA LUCIA SANTOS",    "os": "5071501", "matricula": "410024",  "inscricao": "112.105.010.0089.000", "localidade": "112", "setor": "105", "rota": "10"},
        ]

        agrupado = defaultdict(list)
        for item in dados:
            agrupado[item["nome"]].append(item)

        for nome, registros in agrupado.items():
            self._adicionar_grupo(nome, registros)

    # ── Renderização de grupos ────────────────────────────────────────────────
    def _adicionar_grupo(self, nome: str, registros: list):
        """Cria uma linha de grupo (cliente) e suas OS filhas (ocultas)."""
        var_grupo = tk.BooleanVar(value=False)

        # ── Linha do grupo ────────────────────────────────────────────────────
        row_grupo = tk.Frame(self._list_frame, bg=configura.CARD_BG,
                             highlightbackground=configura.BORDER,
                             highlightthickness=1)
        row_grupo.pack(fill="x", padx=2, pady=(2, 0))

        # Hover no grupo (só aplica nos widgets que não são o checkbox)
        def _enter_grupo(_, r=row_grupo): r.config(bg="#F0F9FF")
        def _leave_grupo(_, r=row_grupo): r.config(bg=configura.CARD_BG)
        row_grupo.bind("<Enter>", _enter_grupo)
        row_grupo.bind("<Leave>", _leave_grupo)

        # ── Checkbox do grupo — isolado em frame próprio para não disparar expand
        chk_wrap = tk.Frame(row_grupo, bg=configura.CARD_BG)
        chk_wrap.pack(side="left", padx=(10, 4), pady=8)

        chk_grupo = ModernCheck(chk_wrap, var_grupo,
                                on_change=lambda n=nome: self._on_grupo_check(n))
        chk_grupo.pack()

        # Bloqueia propagação do clique do checkbox para o row_grupo
        for w in [chk_wrap, chk_grupo, chk_grupo.box]:
            w.bind("<Button-1>", lambda e: "break", add="+")

        # ── Seta expand/collapse
        arrow = tk.Label(row_grupo, text="▶", bg=configura.CARD_BG,
                         fg=configura.SUBTEXT, font=("Segoe UI", 8),
                         cursor="hand2")
        arrow.pack(side="left", padx=(0, 6))

        # ── Nome do cliente
        nome_lbl = tk.Label(row_grupo,
                            text=f"👤  {nome}",
                            bg=configura.CARD_BG, fg=configura.TEXT,
                            font=("Segoe UI", 10, "bold"),
                            cursor="hand2", anchor="w")
        nome_lbl.pack(side="left", fill="x", expand=True, pady=8)

        # ── Badge contagem OS
        badge = tk.Label(row_grupo,
                         text=f"  {len(registros)} OS  ",
                         bg="#EBF5FF", fg=configura.ACCENT,
                         font=("Segoe UI", 8, "bold"))
        badge.pack(side="right", padx=12)

        # ── Frame filho (OS — oculto por padrão) ──────────────────────────────
        frame_filho = tk.Frame(self._list_frame, bg="#FAFCFF")

        os_items = []
        for r in registros:
            var_os = tk.BooleanVar(value=False)
            os_id  = r["os"]
            self._os_checks[os_id] = {"var": var_os, "dados": r}

            row_os = tk.Frame(frame_filho, bg="#FAFCFF",
                              highlightbackground=configura.BORDER,
                              highlightthickness=1)
            row_os.pack(fill="x", padx=(20, 2), pady=(1, 0))

            def _enter_os(_, rw=row_os): rw.config(bg="#EBF5FF")
            def _leave_os(_, rw=row_os): rw.config(bg="#FAFCFF")
            row_os.bind("<Enter>", _enter_os)
            row_os.bind("<Leave>", _leave_os)

            chk_os = ModernCheck(row_os, var_os,
                                 on_change=lambda n=nome: self._on_os_check(n))
            chk_os.pack(side="left", padx=(10, 4), pady=6)

            tk.Label(row_os, text="  ", bg="#FAFCFF",
                     font=("Segoe UI", 8)).pack(side="left")

            cols_data = [
                ("",              220),
                (r["os"],          90),
                (r["matricula"],  110),
                (r["inscricao"],  190),
                (r["localidade"],  60),
                (r["setor"],       60),
                (r["rota"],        60),
            ]
            for val, w in cols_data:
                tk.Label(row_os, text=val,
                         bg="#FAFCFF", fg=configura.TEXT,
                         font=("Segoe UI", 9),
                         width=w // 8, anchor="center").pack(side="left", padx=2)

            os_items.append({"os_id": os_id, "chk": chk_os, "var": var_os})

        self._grupos[nome] = {
            "open":       False,
            "check":      var_grupo,
            "chk_widget": chk_grupo,
            "os_items":   os_items,
            "frame_filho": frame_filho,
            "arrow":      arrow,
            "row":        row_grupo,
        }
        self._frames_os[nome] = frame_filho

        # Bind expand/collapse apenas nos widgets que não são o checkbox
        for w in [arrow, nome_lbl, row_grupo]:
            w.bind("<Button-1>", lambda _, n=nome: self._toggle_grupo(n))

    # ── Expand / Collapse ─────────────────────────────────────────────────────
    def _toggle_grupo(self, nome: str):
        g = self._grupos[nome]
        if g["open"]:
            g["frame_filho"].pack_forget()
            g["arrow"].config(text="▶")
            g["open"] = False
        else:
            # Insere o frame_filho logo abaixo da row do grupo
            g["frame_filho"].pack(fill="x", padx=2, pady=(0, 2),
                                  after=g["row"])
            g["arrow"].config(text="▼")
            g["open"] = True

        self._canvas.update_idletasks()
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    # ── Lógica de checkboxes ──────────────────────────────────────────────────
    def _on_grupo_check(self, nome: str):
        """Marcar/desmarcar grupo marca/desmarca todos as OS do grupo."""
        g    = self._grupos[nome]
        val  = g["check"].get()
        for item in g["os_items"]:
            item["var"].set(val)
            item["chk"]._draw()
        self._atualizar_contador()

    def _on_os_check(self, nome: str):
        """Atualiza o estado do checkbox do grupo baseado nas OS filhas."""
        g       = self._grupos[nome]
        valores = [item["var"].get() for item in g["os_items"]]
        if all(valores):
            g["check"].set(True)
        elif any(valores):
            g["check"].set(False)   # indeterminado → desmarca o grupo
        else:
            g["check"].set(False)
        g["chk_widget"]._draw()
        self._atualizar_contador()

    def _toggle_todos(self, valor: bool):
        for nome, g in self._grupos.items():
            g["check"].set(valor)
            g["chk_widget"]._draw()
            for item in g["os_items"]:
                item["var"].set(valor)
                item["chk"]._draw()
        self._atualizar_contador()

    def _atualizar_contador(self):
        total = sum(1 for v in self._os_checks.values() if v["var"].get())
        self._lbl_count.config(
            text=f"{total} OS selecionada{'s' if total != 1 else ''}")

    # ── Salvar / Cancelar ─────────────────────────────────────────────────────
    def _salvar(self):
        selecionados = [
            v["dados"]
            for v in self._os_checks.values()
            if v["var"].get()
        ]

        if not selecionados:
            messagebox.showwarning("Atenção", "Nenhuma OS selecionada.")
            return

        # Imprime no mesmo formato do dados = [] original
        print("\n── OS Selecionadas ──")
        print(json.dumps(selecionados, ensure_ascii=False, indent=2))

        # Aqui você pode chamar seu controller ou salvar num arquivo:
        # self.controller.salvar_os(selecionados)

        messagebox.showinfo(
            "Salvo",
            f"{len(selecionados)} OS salva{'s' if len(selecionados) != 1 else ''}!\n"
            "Verifique o console para os dados."
        )

    def _cancelar(self):
        self._toggle_todos(False)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Acompanhamento de OS")
    root.geometry("1000x620")
    root.configure(bg=configura.BG)

    app = TelaAcompanhamento(root)
    app.pack(fill="both", expand=True)
    root.mainloop()