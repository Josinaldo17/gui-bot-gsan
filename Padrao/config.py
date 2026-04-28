import os
import json
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.service import Service
from selenium.webdriver.chrome.service import Service
from Padrao.manipular_pastas import verificar_e_criar_arquivo, verificar_e_criar_pasta
import webbrowser
import tkinter as tk
from tkinter import ttk



# ── Paleta ───────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────────

BG          = "#F0F4F8"
CARD_BG     = "#FFFFFF"
HEADER_BG   = "#1A2E4A"
ACCENT      = "#0077B6"
ACCENT2     = "#00B4D8"
GREEN       = "#2DC653"
GREEN_HV    = "#25A244"
BTN_BACK    = "#E2E8F0"
BTN_BACK_HV = "#CBD5E1"
TEXT        = "#1E293B"
SUBTEXT     = "#64748B"
BORDER      = "#CBD5E1"
CHECK_ACT   = "#0077B6"

SIDEBAR_BG       = "#162438"
SIDEBAR_ITEM     = "#1E3450"
SIDEBAR_ACTIVE   = "#0077B6"
SIDEBAR_HOVER    = "#243a55"
SIDEBAR_TEXT     = "#94A3B8"
SIDEBAR_TEXT_ACT = "#FFFFFF"

TAB_BG       = "#E2E8F0"
TAB_ACTIVE   = "#FFFFFF"
TAB_HOVER    = "#CBD5E1"
TAB_TEXT     = "#64748B"
TAB_TEXT_ACT = "#0077B6"

FONT_HEADER = ("Segoe UI", 13, "bold")
FONT_MODULE = ("Segoe UI", 10, "bold")
FONT_TAB    = ("Segoe UI", 9,  "bold")
FONT_LABEL  = ("Segoe UI", 9,  "bold")
FONT_SMALL  = ("Segoe UI", 9)
FONT_BTN    = ("Segoe UI", 9,  "bold")


RED      = "#E53E3E"
RED_HV   = "#C53030"
# ─────────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────────


user_proxy = os.environ.get('USERNAME')
caminho_download = f"C:\\Users\\{user_proxy}\\Downloads"
caminho_arquivo_principal = os.path.join(caminho_download, "caema_bot")
caminho_config = os.path.join(caminho_arquivo_principal, "config.json")

# Garante a pasta
verificar_e_criar_pasta(caminho_arquivo_principal, criar=True)

# Verifica se o arquivo existe (e cria se não)
existe, criado = verificar_e_criar_arquivo(caminho_config, criar=True)

# Se o arquivo foi criado agora, escreve os dados padrão
if not existe and criado:
    estrutura_inicial = {
        "login": {
            "usuario": "",
            "senha": ""
        },
        "caminho_driver": f"{caminho_arquivo_principal}\\geckodriver\\geckodriver.exe",
        "caminho_download": caminho_download,
        "caminho_pdfs_mapas": "Z:\\JOSINALDO VS CODE\\MAPAS",
        "tamanho_tela": "980x660+400+100",
        "linkGsan": "http://gsan.caema.ma.gov.br:8080/gsan/",
        "config_imprir_os": {
            "arquivos_deletedos": [],
            "data": "",
            "dados": [],
            "data_os": "",
            "dados_fiscais": []
        }
    }

    

    with open(caminho_config, 'w', encoding='utf-8') as f:
        json.dump(estrutura_inicial, f, indent=4, ensure_ascii=False)
    # print(f'Arquivo de configuração criado em: {caminho_config}')



ARQUIVO_CONFIG = caminho_config


def hover_bg(widget, normal, over):
    widget.bind("<Enter>", lambda _: widget.config(bg=over))
    widget.bind("<Leave>", lambda _: widget.config(bg=normal))


def carregar_configuracao():
    try:
        with open(ARQUIVO_CONFIG, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Função para salvar configuração
def salvar_configuracao(config):
    with open(ARQUIVO_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def corrigir_caminho(caminho):
    caminho_corrigido = caminho.replace("\\", "/")
    return caminho_corrigido

config = carregar_configuracao()

def carregar_driver(olhar_navegador):
    config = carregar_configuracao()

    options = Options()
    if not olhar_navegador:
        options.add_argument('--headless') 
    geckodriver_path = config["caminho_driver"]
    service = Service(executable_path=geckodriver_path)

    try:
        driver = webdriver.Firefox(service=service, options=options)
        print("Driver iniciado com sucesso!")
    except Exception as e:
        print(f"Erro ao iniciar o driver: {e}")
        driver = None

    return driver

def adicionar_rodape_com_link(janela):
    # --- Configurações de Estilo ---
    COR_PADRAO = "#555555"      # Cinza escuro discreto
    COR_HOVER = "#0056b3"       # Azul mais elegante para o hover
    FONTE_RODAPE = ("Segoe UI", 9) # Fonte moderna (Windows)
    
    def abrir_link(event):
        webbrowser.open("https://josinaldodev.com")

    def ao_entrar(event):
        rodape.config(fg=COR_HOVER, font=(FONTE_RODAPE[0], FONTE_RODAPE[1], "underline"))

    def ao_sair(event):
        rodape.config(fg=COR_PADRAO, font=FONTE_RODAPE)

    # Container para o rodapé (para organizar melhor o espaçamento)
    frame_rodape = tk.Frame(janela, bg=janela.cget("bg"))
    frame_rodape.pack(side="bottom", fill="x", pady=(0, 10))

    # Linha separadora sutil
    separador = ttk.Separator(frame_rodape, orient='horizontal')
    separador.pack(fill='x', padx=20, pady=(0, 10))

    # O Label do rodapé
    rodape_texto = "© 2025 Josinaldodev"
    rodape = tk.Label(
        frame_rodape, 
        text=rodape_texto, 
        font=FONTE_RODAPE,
        fg=COR_PADRAO, 
        cursor="hand2",
        bg=janela.cget("bg") # Garante que o fundo combine com a janela
    )
    
    rodape.pack()

    # Eventos
    rodape.bind("<Button-1>", abrir_link)
    rodape.bind("<Enter>", ao_entrar) # Mouse por cima
    rodape.bind("<Leave>", ao_sair)   # Mouse saiu

    return frame_rodape
