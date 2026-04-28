from Padrao.config import carregar_configuracao, salvar_configuracao
import os
import re
import fitz  
import pdfplumber





def extrair_dados(texto):
    dados = {}
    configuracao = carregar_configuracao()
    data_os = configuracao["config_imprir_os"]["data_os"]


    match_os = re.search(r"Nº:\s*(\d+)", texto)
    if match_os:
        dados["os"] = match_os.group(1)

    match_inscricao = re.search(r"Inscrição:\s*([\d\.\-]+)", texto)
    if match_inscricao:
        dados["inscricao"] = match_inscricao.group(1)

    match_matricula = re.search(r"Matrícula:\s*(\d+)", texto)
    if match_matricula:
        dados["matricula"] = match_matricula.group(1)

    match_localidade_rota = re.search(r"Localidade/Rota/Sequencial Rota:\s*(\d+)/(\d+)/(\d+)", texto)
    if match_localidade_rota:
        dados["localidade"] = match_localidade_rota.group(1)
        dados["rota"] = match_localidade_rota.group(2)
        dados["sequencial_rota"] = match_localidade_rota.group(3)


    return dados

# Função para ler o PDF e extrair os dados
def ler_pdf_extrair_dados(pdf_path):
    nomes_pr_inserir = []
    configuracao = carregar_configuracao()
    dados = configuracao["config_imprir_os"]["dados"]

    with pdfplumber.open(pdf_path) as pdf:
        for i, pagina in enumerate(pdf.pages):
            texto = pagina.extract_text()

            if texto:
                dados_pdf = extrair_dados(texto)
                if dados_pdf:

                    
                    # Verificar se existe um dado igual no array 'dados'
                    for i, item in enumerate(dados):
                        
                        # Verifique se o item corresponde à OS e inscrição
                        if item['os'] == dados_pdf.get('os') :# and item['inscricao'] == dados_pdf.get('inscricao')
                            nome = item['nome']
                            nomes_pr_inserir.append({"nome": nome, "pagina": i })


    return nomes_pr_inserir
                            


# Função para inserir o nome no PDF
def inserir_nome_no_pdf(input_pdf, nomes, dia):

    configuracao = carregar_configuracao()

    doc = fitz.open(input_pdf)

    # Iterar sobre a lista de nomes e páginas
    for item in nomes:
        nome = item['nome']
        pagina_idx = item['pagina']
        
        # Selecionar a página baseada no índice
        page = doc[pagina_idx]

        # Definir as coordenadas da caixa de texto (x0, y0, x1, y1) - ajuste conforme necessário
        rect = fitz.Rect(36, 230, 400, 150)  # Caixa de texto nas coordenadas (36, 230) até (400, 150)

        # Ponto inicial para inserção do texto (canto superior esquerdo)
        point = rect.tl  # .tl retorna o canto superior esquerdo (x, y)

        # Inserir o nome na página com rotação 0 (sem rotação, na horizontal)
        page.insert_text(point, nome, fontsize=10, color=(0, 0, 0), overlay=True, rotate=90)

        print(f"Nome '{nome}' inserido na página {pagina_idx + 1}")

        # Salvar o novo PDF com os nomes inseridos

    nome_arquivo = f"Os_{dia}.pdf"
    
    doc.save(f"{configuracao['caminho_download']}\\{nome_arquivo}")

    print(f"PDF salvo como {nome_arquivo}")

    salvar_configuracao(configuracao) 


