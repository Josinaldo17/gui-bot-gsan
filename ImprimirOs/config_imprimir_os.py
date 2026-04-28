from Padrao.config import carregar_configuracao, salvar_configuracao
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.service import Service
from selenium.webdriver.chrome.service import Service

configuracao = carregar_configuracao()

arquivos_delete = []

data = ""

data_formatada = data.replace("/", "_")

data_os = data_formatada

# Lista global para armazenar os dados
dados =  [
    # {'nome': 'JOSEDERIBAMARNUNE', 'os': '4716098', 'matricula': '1508563', 'inscricao': '145.120.453.1944.000', 'localidade': '145', 'setor': '120', 'rota': '3'},
    # {'nome': 'CELSONCARLOSCORREA', 'os': '4719969', 'matricula': '9122494', 'inscricao': '133.125.365.0138.000', 'localidade': '133', 'setor': '125', 'rota': '5'},
    # {'nome': 'LUIZITOGEMALIMA', 'os': '4719946', 'matricula': '2157012', 'inscricao': '133.121.017.0097.001', 'localidade': '133', 'setor': '121', 'rota': '17'},
     ]

# Lista global para armazenar os dados

