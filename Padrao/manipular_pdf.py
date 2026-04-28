import datetime
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter
import fitz  # PyMuPDF
import time


def pegar_ultimo_pdf(caminho):
    
    arquivos = [f for f in os.listdir(caminho) if f.endswith(".pdf")]
    if arquivos:
        arquivos.sort(key=lambda f: os.path.getctime(os.path.join(caminho, f)), reverse=True)
        return arquivos[0]
    return None

def verificar_pegar_ultimo_pdf_atu_(caminho, ultimo_arquivo):
    print(f"{ultimo_arquivo}")

    # A primeira verificação para ver se há PDFs no diretório
    novo_arquivo = [f for f in os.listdir(caminho) if f.endswith(".pdf")]

    # print("agora",novo_arquivo)
    # print("Ultimo",ultimo_arquivo)

    
    encontrou = False
    while not encontrou:
        # print(f"\nProcurando novo arquivo......")
        
        # Filtra novamente os arquivos PDF
        novo_arquivo = [f for f in os.listdir(caminho) if f.endswith(".pdf")]
        # print("Todos aquivos", novo_arquivo )
        if novo_arquivo:
            novo_arquivo.sort(key=lambda f: os.path.getctime(os.path.join(caminho, f)), reverse=True)
            
            
            # Compara se o arquivo atual é diferente do anterior
            if ultimo_arquivo != novo_arquivo[0]:
                
                encontrou = True
                print(f"\nO novo arquivo é {novo_arquivo[0]}")
                return novo_arquivo[0]
        
        # Espera 1 segundo antes de tentar novamente (pode ajustar conforme necessário)
        time.sleep(1)


def deletar_arquivo(pdf):
    if os.path.exists(pdf):                
            os.remove(pdf)
            print(f"\nO arquivo {pdf} foi deletado...")
    # else:
    #     print("ERRO")


def copiar_pdf(pdf_origem, novo_pdf):
    # Abrir o PDF de origem
    with open(pdf_origem, "rb") as file_origem:
        reader_origem = PdfReader(file_origem)

        # Criar um novo PDF para salvar o conteúdo copiado
        writer = PdfWriter()

        # Adicionar todas as páginas ao novo PDF
        for pagina in range(len(reader_origem.pages)):
            writer.add_page(reader_origem.pages[pagina])

        # Salvar o novo PDF com o novo nome
        with open(novo_pdf, "wb") as output_pdf:
            writer.write(output_pdf)