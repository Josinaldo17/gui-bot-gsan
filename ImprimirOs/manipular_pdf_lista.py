from Padrao.config import carregar_configuracao, salvar_configuracao
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



def procurar_matricula(pdf_path, matricula_procurada):

    print(f"Procurar marciula {pdf_path}, {matricula_procurada}")

    with pdfplumber.open(pdf_path) as pdf:
        print(f"\nLendo arquivo e procurando matricula {matricula_procurada} ...")
        for i, pagina in enumerate(pdf.pages):            
            texto = pagina.extract_text()

            primeiros_300 = texto[:690]
        
            ultimos_300 = texto[-360:]

            
            if matricula_procurada in texto:
                
                
                if matricula_procurada in primeiros_300:
                    print(f"Matrícula {matricula_procurada} encontrada na página {i + 1}")
                    print(f"Encontrada No inicio da pagina.")
                    if i == 0:
                        return [i] 
                    else:
                        return [i - 1, i ]  
                
                if matricula_procurada in ultimos_300:
                    print(f"Matrícula {matricula_procurada} encontrada na página {i + 1}")
                    print(f"Encontrada No final da pagina.")
                    if i == len(pdf.pages) - 1:
                        return [i ] 
                    else:
                        return [i, i + 1 ]  
                else:
                    print(f"Matrícula {matricula_procurada} encontrada na página {i + 1}.")
                    return [i ]  
                
            elif i == len(pdf.pages) - 1:
                print(f"'{matricula_procurada}' NÃO encontrado no texto.")
                return -1

            


                        

        print(f"Matrícula {matricula_procurada} não encontrada no documento.")
        return None

def extrair_pagina_isolada(pdf_origem, pagina_extraida, novo_pdf):

    # print(f"Extrair pagina isolada {pdf_origem}, {pagina_extraida}, {novo_pdf} ")

    # Abrir o PDF de origem
    with open(pdf_origem, "rb") as file_origem:
        reader_origem = PdfReader(file_origem)

        # Criar um novo PDF para salvar as páginas extraídas
        writer = PdfWriter()

        # Adicionar as páginas desejadas (índices começam de 0)
        for pagina in pagina_extraida:
            writer.add_page(reader_origem.pages[pagina])

        # Salvar o novo PDF com as páginas extraídas
        with open(novo_pdf, "wb") as output_pdf:
            writer.write(output_pdf)


def adicionar_texto_ao_pdf(input_pdf, output_pdf, texto):

    print(f"Adicionar texto {input_pdf}, {output_pdf}, {texto} ")

    # Abrir o PDF
    doc = fitz.open(input_pdf)

    # Selecionar a página (por exemplo, a primeira página)
    page = doc[0]

    rect = fitz.Rect(36, 290, 400, 150)

    # Inserir o texto na área definida pelo retângulo (rect)
    point = rect.tl  # Pega o canto superior esquerdo do retângulo
    page.insert_text(point, texto, fontsize=9, color=(0, 0, 0), overlay=True, rotate=90)

    # Salvar o novo PDF com o texto adicionado
    doc.save(output_pdf)
    # print(f"\nTexto adicionado e PDF salvo como {output_pdf}")

    return output_pdf


def extrair_adicionar_todas_as_paginas(pdf_origem, pdf_destino, i ):
    # Abrir o PDF de origem

    # print(f"Extrair adicinar todas paginas {pdf_origem}, {pdf_destino}")


    configuracao = carregar_configuracao()
    arquivos_delete = configuracao["config_imprir_os"]["arquivos_deletedos"]

    output_pdf = f"{configuracao['caminho_download']}\\caema_bot\\arquivo_temp_salvos{i}.pdf"
    antigo_pdf = f"{configuracao['caminho_download']}\\caema_bot\\arquivo_temp_salvos{i - 1}.pdf"
    

    with open(pdf_origem, "rb") as file_origem:
        reader_origem = PdfReader(file_origem)
        
       # 'Criar um novo PDF para o destino'
        
        writer_destino = PdfWriter()

        #  Abrir o PDF de destino {pdf_destino}
        with open(pdf_destino, "rb") as file_destino:
            reader_destino = PdfReader(file_destino)
            
            #  Adicionar todas as páginas do PDF de destino ao novo PDF
            for i in range(len(reader_destino.pages)):
                writer_destino.add_page(reader_destino.pages[i])

        # Adicionar todas as páginas do PDF de origem ao novo PDF{pdf_origem}
        for i in range(len(reader_origem.pages)):
            writer_destino.add_page(reader_origem.pages[i])

        
        with open(output_pdf, "wb") as output_pdf_file:
            writer_destino.write(output_pdf_file)
            


        arquivos_delete.append(pdf_origem)
        arquivos_delete.append(pdf_destino)
        arquivos_delete.append(antigo_pdf)

        configuracao["config_imprir_os"]["arquivos_deletedos"] = arquivos_delete


        salvar_configuracao(configuracao)
        time.sleep(2)

        return output_pdf
