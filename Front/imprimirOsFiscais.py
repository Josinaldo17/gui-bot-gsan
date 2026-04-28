import tkinter as tk
from tkinter import ttk, messagebox
import Padrao.config as configura
from ImprimirOs.selenium_imprimir_os import imprimir_os
from ImprimirOs.selenium_imprimir_lista import imprimir_lista
from ImprimirOs.imprimir_mapas import juntas_map
from collections import defaultdict
import json


def card(parent, **kwargs):
    return tk.Frame(parent, bg=configura.CARD_BG,
                    highlightbackground=configura.BORDER,
                    highlightthickness=1, **kwargs)

class ModernCheck(tk.Frame):
    def __init__(self, parent, var, on_change=None, **kwargs):
        super().__init__(parent, bg=parent.cget("bg"), **kwargs)
        self.var = var
        self.on_change = on_change

        self.box = tk.Label(self, width=2, height=1,
                            bg=self.cget("bg"), relief="flat",
                            font=("Segoe UI", 9), cursor="hand2")
        self.box.pack()

        if self.var is not None:
            self._draw()

        self.box.bind("<Button-1>", self._toggle)

    def _draw(self):

        if not hasattr(self, 'var') or self.var is None:
            return

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
class Imprimir_OS_Fiscais(tk.Frame):
    def __init__(self, parent, controller=None, **kwargs):
        super().__init__(parent, bg=configura.BG)
        self.controller = controller

        self.Titulo_recebido = kwargs.get('Titulo', 'Erro: Volte para a tela anterior!')
        self.NomeBotao_recebido = kwargs.get('NomeBotao', "Erro critico")
        self.Metodo_recebido = kwargs.get('Metodo', "")
        self.Data_recebido = kwargs.get('Data', "")
        self.OlharNoNavegador_recebido = kwargs.get('OlharNoNavegador', "")
        self.Dados_recebido = kwargs.get('Dados', [])
        
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
        tk.Label(header, text=f"{self.Titulo_recebido}",
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
        configura.hover_bg(self._btn_sel_todos, "#E2E8F0", "#CBD5E1")

        self._btn_desel_todos = tk.Label(btn_frame, text="  ☐  Desmarcar Todos  ",
                                         bg="#E2E8F0", fg=configura.TEXT,
                                         font=("Segoe UI", 9, "bold"),
                                         padx=4, pady=6, cursor="hand2")
        self._btn_desel_todos.pack(side="left", padx=(0, 16))
        self._btn_desel_todos.bind("<Button-1>", lambda _: self._toggle_todos(False))
        configura.hover_bg(self._btn_desel_todos, "#E2E8F0", "#CBD5E1")

        # Separador
        tk.Frame(btn_frame, bg=configura.BORDER, width=1).pack(side="left", fill="y", padx=(0, 16))

        # Cancelar
        btn_cancelar = tk.Label(btn_frame, text="  ✕  Cancelar  ",
                                bg="#FED7D7", fg=configura.RED,
                                font=("Segoe UI", 9, "bold"),
                                padx=4, pady=6, cursor="hand2")
        btn_cancelar.pack(side="left", padx=(0, 6))
        btn_cancelar.bind("<Button-1>", lambda _: self._cancelar())
        configura.hover_bg(btn_cancelar, "#FED7D7", "#FEB2B2")

        # Salvar
        btn_salvar = tk.Label(btn_frame, text=f"  ✔  {self.NomeBotao_recebido}  ",
                              bg=configura.GREEN, fg="white",
                              font=("Segoe UI", 9, "bold"),
                              padx=4, pady=6, cursor="hand2")
        btn_salvar.pack(side="left")
        btn_salvar.bind("<Button-1>", lambda _: self._salvar())
        configura.hover_bg(btn_salvar, configura.GREEN, configura.GREEN_HV)

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
        
        dados = self.Dados_recebido 

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

        # Hover no grupo
        def _enter_grupo(_, r=row_grupo): r.config(bg="#F0F9FF")
        def _leave_grupo(_, r=row_grupo): r.config(bg=configura.CARD_BG)
        row_grupo.bind("<Enter>", _enter_grupo)
        row_grupo.bind("<Leave>", _leave_grupo)

        # Seta expand/collapse
        self._arrow_lbl = {}
        arrow = tk.Label(row_grupo, text="▶", bg=configura.CARD_BG,
                         fg=configura.SUBTEXT, font=("Segoe UI", 8),
                         cursor="hand2")
        arrow.pack(side="left", padx=(0, 6))

        # Nome do cliente
        nome_lbl = tk.Label(row_grupo,
                            text=f"👤  {nome}",
                            bg=configura.CARD_BG, fg=configura.TEXT,
                            font=("Segoe UI", 10, "bold"),
                            cursor="hand2", anchor="w")
        nome_lbl.pack(side="left", fill="x", expand=True, pady=8)

        # ── Frame filho (OS — oculto por padrão) ──────────────────────────────
        frame_filho = tk.Frame(self._list_frame, bg="#FAFCFF")
        # NÃO faz pack ainda

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

            # Espaçador alinha com seta do grupo
            tk.Label(row_os, text="  ", bg="#FAFCFF",
                     font=("Segoe UI", 8)).pack(side="left")

            cols_data = [
                ("", 220),
                (r["os"],          90),
                (r["matricula"],   110),
                (r["inscricao"],   190),
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
            "open":     False,
            "check":    var_grupo,
            "os_items": os_items,
            "frame_filho": frame_filho,
            "arrow":    arrow,
            "row":      row_grupo,
        }
        self._frames_os[nome] = frame_filho

        # Bind expand/collapse
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
        self._atualizar_contador()

    def _toggle_todos(self, valor: bool):
        for nome, g in self._grupos.items():
            g["check"].set(valor)
            for item in g["os_items"]:
                item["var"].set(valor)
                item["chk"]._draw()
        self._atualizar_contador()

    def _atualizar_contador(self):
        total = sum(1 for v in self._os_checks.values() if v["var"].get())
        self._lbl_count.config(
            text=f"{total} OS selecionada{'s' if total != 1 else ''}")

    # ── Salvar / Cancelar ─────────────────────────────────────────────────────
    def _salvar(self, _=None):
        selecionados = [
            v["dados"]
            for v in self._os_checks.values()
            if v["var"].get()
        ]
        configuracao = configura.carregar_configuracao()

        if not selecionados:
            messagebox.showwarning("Atenção", "Nenhuma OS selecionada.")
            return

        numeros_OS = [item["os"] for item in selecionados]

        print(self.Metodo_recebido)
        

        if self.Metodo_recebido == "Imprimir" :
            imprimir_os(configuracao["config_imprir_os"]["data"] , numeros_OS, True)
            messagebox.showinfo("Imprimir", f"Processo Concluido!")
        elif self.Metodo_recebido == "Listar" :
            imprimir_lista(selecionados, self.Data_recebido, self.OlharNoNavegador_recebido)
        elif self.Metodo_recebido == "Mapas" :
            juntas_map(selecionados, rf"{configuracao['caminho_pdfs_mapas']}", f"{configuracao['caminho_download']}\\mapas_{configuracao['config_imprir_os']['data_os']}.pdf")
        else:
            print("Erro, volte a pagina anterior")
            messagebox.showwarning("Atenção", "Erro, volte a pagina anterior")


                    


    def _cancelar(self, _=None):
        resposta = messagebox.askyesno("Cancelar", f"Você está prestes a cancelar o filtro")

        if resposta:        
            self.controller.switch_to_imprimirOS()
