import tkinter as tk
from tkinter import scrolledtext, messagebox
from Padrao.config import carregar_configuracao, adicionar_rodape_com_link, hover_bg
from CriarOs.selenium_criar_os import executar_criar_os


import Padrao.config as configura


class ModernCheckbox(tk.Frame):
    """Checkbox no padrão visual do projeto."""
    def __init__(self, parent, text, var, **kwargs):
        super().__init__(parent, bg=configura.CARD_BG, **kwargs)
        self.var = var

        self.box = tk.Label(self, width=2, height=1,
                            bg=configura.CARD_BG, relief="flat",
                            font=("Segoe UI", 9), cursor="hand2")
        self.box.pack(side="left")
        self._draw()

        self.lbl = tk.Label(self, text=text,
                            bg=configura.CARD_BG, fg=configura.TEXT,
                            font=("Segoe UI", 9), cursor="hand2")
        self.lbl.pack(side="left", padx=(2, 0))

        self.box.bind("<Button-1>", self._toggle)
        self.lbl.bind("<Button-1>", self._toggle)

    def _draw(self):
        if self.var.get():
            self.box.config(text="✔", fg=configura.ACCENT, bg="#EBF5FF",
                            highlightbackground=configura.ACCENT,
                            highlightthickness=1)
        else:
            self.box.config(text=" ", fg=configura.CARD_BG, bg=configura.CARD_BG,
                            highlightbackground=configura.BORDER,
                            highlightthickness=1)

    def _toggle(self, _=None):
        self.var.set(not self.var.get())
        self._draw()


def section_label(parent, text):
    """Label de seção padrão do projeto."""
    tk.Label(parent, text=text,
             bg=configura.CARD_BG, fg=configura.SUBTEXT,
             font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 4))


def card(parent, **kwargs):
    """Card branco com borda."""
    return tk.Frame(parent, bg=configura.CARD_BG,
                    highlightbackground=configura.BORDER,
                    highlightthickness=1, **kwargs)


def input_field(parent, height=1, width=30):
    """Campo de entrada estilizado."""
    if height == 1:
        e = tk.Entry(parent, width=width,
                     font=("Segoe UI", 9),
                     bg="#F8FAFC", fg=configura.TEXT,
                     relief="flat",
                     highlightbackground=configura.BORDER,
                     highlightthickness=1)
        e.pack(fill="x", ipady=5)
        return e
    else:
        e = scrolledtext.ScrolledText(parent, width=width, height=height,
                                      font=("Segoe UI", 9),
                                      bg="#F8FAFC", fg=configura.TEXT,
                                      relief="flat",
                                      highlightbackground=configura.BORDER,
                                      highlightthickness=1)
        e.pack(fill="x")
        return e


class TelaEncerrarOs(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=configura.BG)
        self.app = controller
        self._arquivo_excel = ""

        # ── Layout raiz: esquerda | direita ───────────────────────────────────
        root_row = tk.Frame(self, bg=configura.BG)
        root_row.pack(fill="both", expand=True, padx=20, pady=16)

        # Coluna esquerda (inputs + resultado)
        col_esq = tk.Frame(root_row, bg=configura.BG)
        col_esq.pack(side="left", fill="both", expand=True)

        # ══════════════════════════════════════════════════════════════════════
        # CARD 1 — Entradas
        # ══════════════════════════════════════════════════════════════════════
        card_input = card(col_esq)
        card_input.pack(fill="x", pady=(0, 12))

        tk.Frame(card_input, bg=configura.ACCENT, height=3).pack(fill="x")

        inner = tk.Frame(card_input, bg=configura.CARD_BG)
        inner.pack(fill="x", padx=14, pady=12)

        # ── Unidade de Atendimento ────────────────────────────────────────────
        section_label(inner, "UNIDADE DE ATENDIMENTO")
        self.txt_unidade = input_field(inner, width=20)

        # ── Linha: Matrícula + Observação ─────────────────────────────────────
        tk.Frame(inner, bg=configura.BORDER, height=1).pack(fill="x", pady=10)

        cols = tk.Frame(inner, bg=configura.CARD_BG)
        cols.pack(fill="x")
        cols.columnconfigure(0, weight=1)
        cols.columnconfigure(1, weight=3)

        # Matrícula
        col_mat = tk.Frame(cols, bg=configura.CARD_BG)
        col_mat.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        section_label(col_mat, "MATRÍCULAS")
        tk.Label(col_mat, text="Cole uma por linha",
                 bg=configura.CARD_BG, fg=configura.SUBTEXT,
                 font=("Segoe UI", 7, "italic")).pack(anchor="w", pady=(0, 4))
        self.txt_matricula = input_field(col_mat, height=5, width=14)

        # Separador vertical
        tk.Frame(cols, bg=configura.BORDER, width=1).grid(
            row=0, column=1, sticky="ns", padx=4)

        # Observação
        col_obs = tk.Frame(cols, bg=configura.CARD_BG)
        col_obs.grid(row=0, column=2, sticky="nsew", padx=(8, 0))
        cols.columnconfigure(2, weight=3)
        section_label(col_obs, "OBSERVAÇÃO")
        tk.Label(col_obs, text=" ",   # espaçador alinha com o "Cole uma por linha"
                 bg=configura.CARD_BG,
                 font=("Segoe UI", 7)).pack(anchor="w", pady=(0, 4))
        self.txt_observacao = input_field(col_obs, height=5, width=28)

        # ── Fonte: Manual ou Excel ────────────────────────────────────────────
        tk.Frame(inner, bg=configura.BORDER, height=1).pack(fill="x", pady=10)

        section_label(inner, "FONTE DAS MATRÍCULAS")

        fonte_row = tk.Frame(inner, bg=configura.CARD_BG)
        fonte_row.pack(fill="x")

        self.var_fonte = tk.StringVar(value="manual")

        # Radio "Manual"
        for txt, val in [("Manual (colar acima)", "manual"),
                         ("Extrair de arquivo Excel", "excel")]:
            rb_wrap = tk.Frame(fonte_row, bg=configura.CARD_BG)
            rb_wrap.pack(side="left", padx=(0, 16))
            circle = tk.Label(rb_wrap, width=2, height=1,
                              bg=configura.CARD_BG, font=("Segoe UI", 9),
                              cursor="hand2")
            circle.pack(side="left")
            lbl = tk.Label(rb_wrap, text=txt,
                           bg=configura.CARD_BG, fg=configura.TEXT,
                           font=("Segoe UI", 9), cursor="hand2")
            lbl.pack(side="left", padx=(2, 0))

            def _draw_radios(*_):
                for w in fonte_row.winfo_children():
                    c = w.winfo_children()[0]
                    c.config(text="●" if self.var_fonte.get() == c._val else "○",
                             fg=configura.ACCENT if self.var_fonte.get() == c._val else configura.SUBTEXT)
                # Mostra/esconde picker Excel
                if self.var_fonte.get() == "excel":
                    self._excel_row.pack(fill="x", pady=(8, 0))
                else:
                    self._excel_row.pack_forget()

            circle._val = val
            lbl._val    = val
            for w in [circle, lbl]:
                w.bind("<Button-1>", lambda _, v=val: [self.var_fonte.set(v), _draw_radios()])

        # Inicializa visual dos radios
        def _init_radios():
            for w in fonte_row.winfo_children():
                c = w.winfo_children()[0]
                c.config(text="●" if self.var_fonte.get() == c._val else "○",
                         fg=configura.ACCENT if self.var_fonte.get() == c._val else configura.SUBTEXT)
        self.after(50, _init_radios)

        # ── Picker Excel (oculto inicialmente) ───────────────────────────────
        self._excel_row = tk.Frame(inner, bg=configura.CARD_BG)
        # NÃO faz pack aqui — só aparece quando "Excel" for selecionado

        section_label(self._excel_row, "SELECIONAR ARQUIVO EXCEL")

        btn_row_xl = tk.Frame(self._excel_row, bg=configura.CARD_BG)
        btn_row_xl.pack(anchor="w")

        btn_excel = tk.Label(btn_row_xl, text="  📂  Escolher Arquivo  ",
                             bg=configura.ACCENT, fg="white",
                             font=("Segoe UI", 9, "bold"),
                             padx=4, pady=7, cursor="hand2")
        btn_excel.pack(side="left")
        btn_excel.bind("<Button-1>", self._selecionar_excel)
        hover_bg(btn_excel, configura.ACCENT, "#005f8e")

        self._lbl_excel = tk.Label(btn_row_xl,
                                   text="Nenhum arquivo selecionado",
                                   bg=configura.CARD_BG, fg=configura.SUBTEXT,
                                   font=("Segoe UI", 8, "italic"))
        self._lbl_excel.pack(side="left", padx=(10, 0))

        # ══════════════════════════════════════════════════════════════════════
        # CARD 2 — Ação
        # ══════════════════════════════════════════════════════════════════════
        card_acao = card(col_esq)
        card_acao.pack(fill="x", pady=(0, 12))

        acao_inner = tk.Frame(card_acao, bg=configura.CARD_BG)
        acao_inner.pack(fill="x", padx=14, pady=12)

        btn_processar = tk.Label(acao_inner,
                                 text="  ▶  ENCERRAR OS's  ",
                                 bg="#2DC653", fg="white",
                                 font=("Segoe UI", 10, "bold"),
                                 padx=10, pady=9, cursor="hand2")
        btn_processar.pack(side="left")
        btn_processar.bind("<Button-1>", lambda _: self.iniciar_thread())
        hover_bg(btn_processar, "#2DC653", "#25A244")

        self.var_ocultar = tk.BooleanVar(value=True)
        ModernCheckbox(acao_inner, "Ocultar Navegador",
                       self.var_ocultar).pack(side="left", padx=(20, 0))

        # ══════════════════════════════════════════════════════════════════════
        # CARD 3 — Resultado
        # ══════════════════════════════════════════════════════════════════════
        card_result = card(col_esq)
        card_result.pack(fill="both", expand=True)

        tk.Frame(card_result, bg=configura.ACCENT, height=3).pack(fill="x")

        result_inner = tk.Frame(card_result, bg=configura.CARD_BG)
        result_inner.pack(fill="both", expand=True, padx=14, pady=10)

        section_label(result_inner, "RESULTADO")

        self.txt_output = scrolledtext.ScrolledText(
            result_inner,
            font=("Segoe UI", 9),
            bg="#F8FAFC", fg="#0077B6",
            relief="flat",
            highlightbackground=configura.BORDER,
            highlightthickness=1,
            height=10
        )
        self.txt_output.pack(fill="both", expand=True)

    # ── Callbacks ─────────────────────────────────────────────────────────────
    def _selecionar_excel(self, _=None):
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            title="Selecione o arquivo Excel",
            filetypes=[("Excel", "*.xlsx *.xls *.xlsm"), ("Todos", "*.*")]
        )
        if path:
            import os
            self._arquivo_excel = path
            self._lbl_excel.config(text=os.path.basename(path),
                                   fg=configura.TEXT)

    def iniciar_thread(self):
        unidade   = self.txt_unidade.get().strip()
        observacao = self.txt_observacao.get("1.0", tk.END).strip()

        if self.var_fonte.get() == "excel":
            if not self._arquivo_excel:
                messagebox.showwarning("Atenção", "Selecione um arquivo Excel.")
                return
            # Lê as matrículas do Excel
            try:
                import openpyxl
                wb = openpyxl.load_workbook(self._arquivo_excel)
                ws = wb.active
                matriculas = [str(row[0].value).strip()
                              for row in ws.iter_rows(min_row=2)
                              if row[0].value]
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível ler o arquivo:\n{e}")
                return
        else:
            raw = self.txt_matricula.get("1.0", tk.END).strip()
            if not raw:
                messagebox.showwarning("Atenção", "Cole as matrículas no campo.")
                return
            matriculas = [m.strip() for m in raw.split("\n") if m.strip()]

        if not unidade:
            messagebox.showwarning("Atenção", "Informe a Unidade de Atendimento.")
            return

        self.txt_output.delete("1.0", tk.END)
        executar_criar_os(matriculas, self.txt_output,
                          unidade, observacao,
                          self.var_ocultar.get())
        messagebox.showinfo("Concluído", "Processo finalizado com sucesso!")

    def voltar(self):
        self.app.switch_to_menu_encerrar_os()