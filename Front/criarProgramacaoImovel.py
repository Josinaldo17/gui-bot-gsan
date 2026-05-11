from Padrao.login import realizar_login 
from CriarProgramacaoImovel.selenium_criar_roteiro_imovel import criar_add_roteiro_imovel
from Padrao.functFront import Arquivo_excel_check
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import openpyxl
import os
import tkinter as tk
import Padrao.config as configura


# Classe para a Tela 1
class CriarProgramacaoImovel(tk.Frame):
    def __init__(self, parent, controller):
        # 1. Inicializa o Frame pai
        super().__init__(parent, bg=configura.BG)
        self.app = controller  # Referência para trocar de tela
        self.ExcelCheck = Arquivo_excel_check()


        
        # =================================================================================================================
        # ========================    ISSO E TEMPORARIOOOOOOOOOOO           =============================================
        # =================================================================================================================
        # =================================================================================================================
        # =================================================================================================================
        # =================================================================================================================
        # =================================================================================================================
        # --- Cabeçalho Padrão (Sair e Configurações) ---

        self.opcoes_cadastrador = [
    "",  # equivalente a opção vazia (&nbsp;)
    "CEL-01 - MG SETEL",
    "CEL-02 - MG SETEL",
    "CEL-03 - MG SETEL",
    "CEL-04 - MG SETEL",
    "CEL-05- MG SETEL",
    "CEL-06 - MG SETEL",
    "CEL-07 - MG SETEL",
    "CEL-08- MG SETEL",
    "CEL-09 - MG SETEL",
    "CEL-1000 - MG SETEL",
    "CEL-10 - MG SETEL",
    "CEL-11 - MG SETEL",
    "CEL-12 - MG SETEL",
    "CEL-13 - MG SETEL",
    "CEL-14 - MG SETEL",
    "CEL-15 - MG SETEL",
    "CEL-16 - MG SETEL",
    "CEL-17 - MG SETEL",
    "CEL-19 - MG SETEL",
    "CEL-21 - MG SETEL",
    "CEL-22 - MG SETEL",
    "CEL-23 - MG SETEL",
    "CEL-24 - MG SETEL",
    "CEL-25 - MG SETEL",
    "CEL-26 - MG SETEL",
    "CEL-28 - MG SETEL",
    "CEL-29 - MG SETEL",
    "CEL-32 - MG SETEL",
    "CEL-34 - MG SETEL",
    "CEL-36 - MG SETEL",
    "CEL-36 - MG SETEL",
    "CEL-38 - MG SETEL",
    "cel-40 - mg setel",
    "CEL-42 - MG SETEL",
    "CEL-44 - MG SETEL",
    "CEL-46 - MG SETEL",
    "CEL-47 - MG SETEL",
    "CEL-52 - MG SETEL",
    "CEL-54 - MG SETEL",
    "CEL-55 - MG SETEL",
    "CEL-56 - MG SETEL",
    "CEL-58 - MG SETEL",
    "CEL-61 - MG SETEL",
    "CEL-63 - MG SETEL",
    "CEL-66 - MG SETEL",
    "CEL-67 - MG SETEL",
    "CEL-68 - MGSETEL",
    "CEL-70 - MG SETEL",
    "CEL-72 - MG SETEL",
    "CEL-74 - MG SETEL",
    "CEL-77 - MG SETEL",
    "CEL-78 - MG SETEL",
    "CEL-79 - MG SETEL",
    "CEL-81 - MG SETEL",
    "CEL-82 - MG SETEL",
    "CEL-999 - MG SETEL",
    "CESAR LOURENCO AMADO FONSECA"
]
        
        # =================================================================================================================
        # =================================================================================================================
        # =================================================================================================================
        # =================================================================================================================
        # =================================================================================================================
        # =================================================================================================================
        # =================================================================================================================


        configuracao = configura.carregar_configuracao()

        self.container = tk.Frame(self, bg=configura.BG)
        self.container.pack(expand=True)

        frame_top = tk.Frame(self.container, bg=configura.BG)
        frame_top.pack(pady=0, padx=5, fill="x")

        scroll_frame = tk.Frame(self, bg=configura.BG)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=16)

        # ── Seção: Arquivo ───────────────────────────────────────────────────
        card_file = ModernCard(scroll_frame)
        card_file.pack(fill="x", pady=(0, 14))

        # Comboboxes style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Modern.TCombobox",
                        fieldbackground=configura.CARD_BG,
                        background=configura.CARD_BG,
                        foreground=configura.TEXT,
                        bordercolor=configura.BORDER,
                        arrowcolor=configura.ACCENT)

        inner = tk.Frame(card_file, bg=configura.CARD_BG)
        inner.pack(fill="x", padx=16, pady=12)

        # ── Coluna 1: Selecionar Arquivo ────────────────────────────────────
        col1 = tk.Frame(inner, bg=configura.CARD_BG)
        col1.pack(side="left", padx=(0, 20))

        tk.Label(col1, text="SELECIONAR ARQUIVO", bg=configura.CARD_BG,
                 fg=configura.SUBTEXT, font=configura.FONT_LABEL).pack(anchor="w", pady=(0, 4))

        btn_row = tk.Frame(col1, bg=configura.CARD_BG)
        btn_row.pack(anchor="w")

        btn_choose = tk.Label(btn_row, text="  📂  Escolher Arquivo  ",
                              bg=configura.ACCENT, fg="white",
                              font=configura.FONT_BTN, padx=4,
                              cursor="hand2", pady=7)
        btn_choose.pack(side="left")
        btn_choose.bind("<Button-1>", self.selecionar_arquivo)
        hover(btn_choose, configura.ACCENT, "#005f8e")

        self.label_resultado = tk.Label(btn_row,
                                 text="Nenhum arquivo selecionado",
                                 bg=configura.CARD_BG, fg=configura.SUBTEXT,
                                 font=("Segoe UI", 8, "italic"))
        self.label_resultado.pack(side="left", padx=(8, 0))

        # Separador vertical
        tk.Frame(inner, bg=configura.BORDER, width=1).pack(side="left", fill="y", padx=(0, 20), pady=4)

        # ── Coluna 2: Selecionar Empresa ─────────────────────────────────────
        col2 = tk.Frame(inner, bg=configura.CARD_BG)
        col2.pack(side="left", padx=(0, 20))

        tk.Label(col2, text="SELECIONAR EMPRESA", bg=configura.CARD_BG,
                 fg=configura.SUBTEXT, font=configura.FONT_LABEL).pack(anchor="w", pady=(0, 4))

        self.combo_empresa = ttk.Combobox(col2, values=["", "MG SETEL", "CAEMA"], width=18,
                                          style="Modern.TCombobox",
                                          state="readonly")
        self.combo_empresa.pack(ipady=4)

        # Separador vertical
        tk.Frame(inner, bg=configura.BORDER, width=1).pack(side="left", fill="y", padx=(0, 20), pady=4)

        # ── Coluna 3: Selecionar Cadastrador ─────────────────────────────────
        col3 = tk.Frame(inner, bg=configura.CARD_BG)
        col3.pack(side="left")

        tk.Label(col3, text="SELECIONAR CADASTRADOR", bg=configura.CARD_BG,
                 fg=configura.SUBTEXT, font=configura.FONT_LABEL).pack(anchor="w", pady=(0, 4))

        self.TKcadastrador_select = ttk.Combobox(col3, values=self.opcoes_cadastrador, width=20,
                                              style="Modern.TCombobox",
                                              state="readonly")

        self.TKcadastrador_select.set("")
        self.TKcadastrador_select.pack(ipady=4)

        # ── Seção: Cliente Usuário ───────────────────────────────────────────
        SectionLabel(scroll_frame, "CLIENTE USUÁRIO").pack(anchor="w", pady=(0, 4))
        card_cli = ModernCard(scroll_frame)
        card_cli.pack(fill="x", pady=(0, 14))

        row_cli = tk.Frame(card_cli, bg=configura.CARD_BG)
        row_cli.pack(fill="x", padx=16, pady=12)

        self.var_cliente_usuario = tk.StringVar()
        for text, val in [("Com CPF/CNPJ", "1"),
                          ("Sem CPF/CNPJ", "2"),
                          ("Todos",        "3")]:
            ModernRadio(row_cli, text, self.var_cliente_usuario, val).pack(side="left", padx=(0, 20))

        # ── Seção: Situação de Ligação Água ─────────────────────────────────
        SectionLabel(scroll_frame, "SITUAÇÃO DE LIGAÇÃO ÁGUA").pack(anchor="w", pady=(0, 4))
        card_agua = ModernCard(scroll_frame)
        card_agua.pack(fill="x", pady=(0, 14))

        row_agua = tk.Frame(card_agua, bg=configura.CARD_BG)
        row_agua.pack(fill="x", padx=16, pady=12)
        self.vars_agua = {}

        textos = ["POTENCIAL", "FACTIVEL", "LIGADO", "CORTADO", "SUPRIMIDO"]
        valores = ["1", "2", "3", "5", "6"]


        for texto, valor in zip(textos, valores):
            v = tk.BooleanVar()
            self.vars_agua[valor] = v 
            ModernCheckbox(row_agua, texto, v).pack(side="left", padx=(0, 18))

        # ── Seção: Categoria Imóvel ──────────────────────────────────────────
        textos_cat = ["RESIDENCIAL", "COMERCIAL", "INDUSTRIAL", "PÚBLICO"]
        valores_cat = ["1", "2", "3", "4"]

        SectionLabel(scroll_frame, "CATEGORIA DO IMÓVEL").pack(anchor="w", pady=(0, 4))
        card_cat = ModernCard(scroll_frame)
        card_cat.pack(fill="x", pady=(0, 14))

        row_cat = tk.Frame(card_cat, bg=configura.CARD_BG)
        row_cat.pack(fill="x", padx=16, pady=12)

        self.vars_cat = {}
        # Usamos zip para percorrer nome e código juntos
        for texto, valor in zip(textos_cat, valores_cat):
            v = tk.BooleanVar()
            self.vars_cat[valor] = v  # A chave será "1", "2", etc.
            ModernCheckbox(row_cat, texto, v).pack(side="left", padx=(0, 22))

        # ── Seção: Situação Imóvel ───────────────────────────────────────────
        textos_sit = ["Atualizados", "Não Atualizados", "Retornar para Campo"]
        valores_sit = ["1", "2", "3"]

        SectionLabel(scroll_frame, "SITUAÇÃO DO IMÓVEL").pack(anchor="w", pady=(0, 4))
        card_sit = ModernCard(scroll_frame)
        card_sit.pack(fill="x", pady=(0, 14))

        row_sit = tk.Frame(card_sit, bg=configura.CARD_BG)
        row_sit.pack(fill="x", padx=16, pady=12)

        self.vars_sit = {}
        for texto, valor in zip(textos_sit, valores_sit):
            v = tk.BooleanVar()
            self.vars_sit[valor] = v  # A chave será "1", "2", etc.
            ModernCheckbox(row_sit, texto, v).pack(side="left", padx=(0, 22))


        # ── Rodapé / Ações ───────────────────────────────────────────────────
        footer = ModernCard(scroll_frame)
        footer.pack(fill="x")

        row_foot = tk.Frame(footer, bg=configura.CARD_BG)
        row_foot.pack(fill="x", padx=16, pady=12)

        # QUANT MAX
        tk.Label(row_foot, text="QUANT MAX:", bg=configura.CARD_BG,
                 fg=configura.TEXT, font=configura.FONT_LABEL).pack(side="left")
        self.entry_quant_minima = tk.Entry(row_foot, width=8,
                                    font=configura.FONT_SMALL,
                                    bg="#F8FAFC", fg=configura.TEXT,
                                    relief="flat",
                                    highlightbackground=configura.BORDER,
                                    highlightthickness=1)
        self.entry_quant_minima.pack(side="left", padx=(6, 20), ipady=4)

        # TIME
        tk.Label(row_foot, text="TIME (s):", bg=configura.CARD_BG,
                 fg=configura.TEXT, font=configura.FONT_LABEL).pack(side="left")
        self.entry_quant_tempo = tk.Entry(row_foot, width=8,
                                   font=configura.FONT_SMALL,
                                   bg="#F8FAFC", fg=configura.TEXT,
                                   relief="flat",
                                   highlightbackground=configura.BORDER,
                                   highlightthickness=1)
        self.entry_quant_tempo.pack(side="left", padx=(6, 20), ipady=4)

        # Ocultar Navegador
        self.olhar_no_navegador = tk.BooleanVar(value=False)
        ModernCheckbox(row_foot, "Ocultar Navegador",
                       self.olhar_no_navegador).pack(side="left", padx=(0, 20))

        # Botão Iniciar
        btn_ini = tk.Label(row_foot, text="  ▶  Iniciar  ",
                           bg=configura.GREEN, fg="white",
                           font=("Segoe UI", 10, "bold"),
                           padx=10, pady=8,
                           cursor="hand2")
        btn_ini.pack(side="right")
        btn_ini.bind("<Button-1>", self.iniciar_processo)
        hover(btn_ini, configura.GREEN, configura.GREEN_HV)



        style.configure("TEntry", font=("Arial", 11))

    
    def selecionar_arquivo(self, _=None):
        resultado, caminho = self.ExcelCheck.selecionar_arquivo_exel(self.label_resultado)
        if resultado:
            self.caminho_arquivo_global = caminho

    def iniciar_processo(self, _=None):

        aguaSituacao = [codigo for codigo, var in self.vars_agua.items() if var.get()]
        categoriaImovel = [cod for cod, var in self.vars_cat.items() if var.get()]
        situacaoImovel = [cod for cod, var in self.vars_sit.items() if var.get()]


        idEmpresa = self.combo_empresa.get()
        clienteUsuario = self.var_cliente_usuario.get()
        olhar_no_navegador = self.olhar_no_navegador.get()
        olhar_no_avegador = not olhar_no_navegador
        Ncadastrador = self.TKcadastrador_select.get()

        quant_minima = self.entry_quant_minima.get()
        tempo = self.entry_quant_tempo.get()

        if idEmpresa == "CAEMA":
            idEmpresa = 1
        elif idEmpresa == "MG SETEL":
            idEmpresa = 54 
        else:
            idEmpresa = "" 
     
        if self.label_resultado.cget("text") == "Caminho do arquivo aparecerá aqui":
            messagebox.showerror("Erro", "Por favor, selecione um arquivo.")
            return
        
        if idEmpresa == "":
            messagebox.showerror("Erro", "Por favor, selecione uma empresa antes de continuar.")
            return
        
        if Ncadastrador == "":
            messagebox.showerror("Erro", "Por favor, selecione um Cadastrador antes de continuar.")
            return
        
        if not clienteUsuario:
            messagebox.showerror("Erro", "Selecione um Cliente Usuário.")
            return

        if not aguaSituacao:
            messagebox.showerror("Erro", "Selecione ao menos uma Situação de Água.")
            return

        if not categoriaImovel:
            messagebox.showerror("Erro", "Selecione ao menos uma Categoria de Imóvel.")
            return

        if not situacaoImovel:
            messagebox.showerror("Erro", "Selecione ao menos uma Situação de Imóvel.")
            return

        if not quant_minima.isdigit() or int(quant_minima) < 1:
            messagebox.showerror("Erro", "Digite uma quantidade numérica válida.")
            return
        
        if not tempo.isdigit() or int(tempo) < 1:
            messagebox.showerror("Erro", "Digite uma quantidade de tempo válido.")
            return

        if self.caminho_arquivo_global == "":
            messagebox.showerror("Erro", "Selecione um arquivo Excel válido para continuar.")
            return

        if not self.ExcelCheck.verificar_colunas_no_excel(self.caminho_arquivo_global, ['SETOR', 'LOCALIDADE', 'ROTA']):
            return
                
        
        # print("Iniciando roteiro...")
        # print("  Caminho:", self.caminho_arquivo_global)
        # print("  empresa:", idEmpresa)
        # print("  Cliente:",clienteUsuario)
        # print("  Cadastrador:",Ncadastrador)
        # print("  Água:", aguaSituacao)
        # print("  Categoria:", categoriaImovel)
        # print("  Situação:",situacaoImovel)
        # print("  Quant Max:", quant_minima)
        # print("  Time:", tempo)
        # print("  Ocultar Nav:", olhar_no_avegador)
        
        _, _, driver, _ = realizar_login(True, olhar_no_avegador)


        df = pd.read_excel(self.caminho_arquivo_global)

            
        dados_novo_arquivo = []

        for index, row in df.iterrows():

            if not pd.isna(row['SETOR']) and not pd.isna(row['LOCALIDADE']) and not pd.isna(row['ROTA']):
            

                setor = int(row['SETOR'])
                localidade = int(row['LOCALIDADE'])
                rota = int(row['ROTA'])

                resultado, quant = criar_add_roteiro_imovel(idEmpresa, localidade, setor, rota, aguaSituacao, clienteUsuario, categoriaImovel, situacaoImovel, Ncadastrador, quant_minima, tempo, driver)
                
                dados_novo_arquivo.append({
                "LOCALIDADE": row['LOCALIDADE'],
                "SETOR": row['SETOR'],
                "ROTA": row['ROTA'],
                "RESULTADO": resultado,
                "QUANTIDADE": quant,
                })
                
            else:
                print("Pular para novo grupo")



        diretorio, arquivo = os.path.split(self.caminho_arquivo_global)
        df_resultados = pd.DataFrame(dados_novo_arquivo)
        novo_arquivo = os.path.join(diretorio, "resultado.xlsx")
        df_resultados.to_excel(novo_arquivo, index=False)   
        print(f"Arquivo Excel salvo em: {novo_arquivo}")
    
    def voltar_menu(self):        
        self.app.switch_to_menu()



class ModernCard(tk.Frame):
    """Frame com visual de card (borda sutil + sombra simulada)."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=configura.CARD_BG,
                         highlightbackground=configura.BORDER,
                         highlightthickness=1,
                         **kwargs)


class SectionLabel(tk.Label):
    def __init__(self, parent, text, **kwargs):
        super().__init__(parent, text=text,
                         bg=configura.BG, fg=configura.SUBTEXT,
                         font=configura.FONT_LABEL,
                         **kwargs)


class ModernCheckbox(tk.Frame):
    def __init__(self, parent, text, var, **kwargs):
        super().__init__(parent, bg=configura.CARD_BG, **kwargs)
        self.var = var

        self.box = tk.Label(self, width=2, height=1,
                            bg=configura.CARD_BG,
                            relief="flat",
                            font=("Segoe UI", 9),
                            cursor="hand2")
        self.box.pack(side="left")
        self._draw()

        self.lbl = tk.Label(self, text=text,
                            bg=configura.CARD_BG, fg=configura.TEXT,
                            font=configura.FONT_SMALL,
                            cursor="hand2")
        self.lbl.pack(side="left", padx=(2, 0))

        self.box.bind("<Button-1>", self._toggle)
        self.lbl.bind("<Button-1>", self._toggle)

    def _draw(self):
        if self.var.get():
            self.box.config(text="✔", fg=configura.ACCENT, bg="#EBF5FF",
                            highlightbackground=configura.ACCENT,
                            highlightthickness=1,
                            relief="flat")
        else:
            self.box.config(text=" ", fg=configura.CARD_BG, bg=configura.CARD_BG,
                            highlightbackground=configura.BORDER,
                            highlightthickness=1,
                            relief="flat")

    def _toggle(self, _=None):
        self.var.set(not self.var.get())
        self._draw()


class ModernRadio(tk.Frame):
    def __init__(self, parent, text, variable, value, **kwargs):
        super().__init__(parent, bg=configura.CARD_BG, **kwargs)
        self.var   = variable
        self.value = value

        self.circle = tk.Label(self, width=2, height=1,
                               bg=configura.CARD_BG, font=("Segoe UI", 9),
                               cursor="hand2")
        self.circle.pack(side="left")

        self.lbl = tk.Label(self, text=text,
                            bg=configura.CARD_BG, fg=configura.TEXT,
                            font=configura.FONT_SMALL, cursor="hand2")
        self.lbl.pack(side="left", padx=(2, 0))

        self._draw()
        self.circle.bind("<Button-1>", self._select)
        self.lbl.bind("<Button-1>", self._select)

    def _draw(self):
        if self.var.get() == self.value:
            self.circle.config(text="●", fg=configura.ACCENT)
        else:
            self.circle.config(text="○", fg=configura.SUBTEXT)

    def _select(self, _=None):
        self.var.set(self.value)
        # redesenha todos os irmãos
        for w in self.master.winfo_children():
            if isinstance(w, ModernRadio):
                w._draw()


def hover(widget, normal, over):
    widget.bind("<Enter>", lambda _: widget.config(bg=over))
    widget.bind("<Leave>", lambda _: widget.config(bg=normal))


