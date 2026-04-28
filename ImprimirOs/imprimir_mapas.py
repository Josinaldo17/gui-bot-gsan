from Padrao.config import carregar_configuracao, salvar_configuracao
from Padrao.manipular_pdf import copiar_pdf, deletar_arquivo
from ImprimirOs.manipular_pdf_lista import extrair_adicionar_todas_as_paginas
import re
from PyPDF2 import PdfReader, PdfWriter
import fitz  # PyMuPDF
import os



# ---------------------------------------------------
# Localiza e copia o mapa correto (com base em loc, setor, rota)
# ---------------------------------------------------
def pegar_mapa(localidade, setor, rota, pasta_base, output_pdf):
    for pasta_loc in os.listdir(pasta_base):
        try:

            if str(localidade) in pasta_loc:
                caminho_loc = os.path.join(pasta_base, pasta_loc)
                for pasta_setor in os.listdir(caminho_loc):
                    if str(setor) in pasta_setor:
                        caminho_setor = os.path.join(caminho_loc, pasta_setor)
                        for arquivo in os.listdir(caminho_setor):
                            if arquivo.lower().endswith(".pdf"):
                                # Pega só o nome do arquivo (sem caminho nem extensão)
                                nome_arquivo = os.path.splitext(os.path.basename(arquivo))[0]
                                
                                # Extrai o primeiro número encontrado no nome
                                match = re.search(r'(\d+)', nome_arquivo)
                                if match:
                                    rota_arquivo = int(match.group(1))  # transforma em número
                                    
                                    if rota_arquivo == int(rota):
                                        pdf_origem = os.path.join(caminho_setor, arquivo)
                                        copiar_pdf(pdf_origem, output_pdf)
                                        print(f"Mapa encontrado e copiado: {pdf_origem}")
                                        return output_pdf
        except:

            return None

    print(f"Nenhum mapa encontrado para Loc {localidade}, Setor {setor}, Rota {rota}")
    return None


# ---------------------------------------------------
# Junta todos os mapas dos dados informados
# ---------------------------------------------------
def juntas_map(dados, pasta_base, arquivo_final):

    configuracao = carregar_configuracao()
    



    contador = 0
    todas_os_mapas = None

    for dado in dados:
        contador += 1
        novo_pdf_mapa = pegar_mapa(dado["localidade"], dado["setor"], dado["rota"], pasta_base,
                                   f"{configuracao['caminho_download']}\\caema_bot\\mapas{contador}.pdf")
        if novo_pdf_mapa is None:
            continue

        if todas_os_mapas is None:
            todas_os_mapas = novo_pdf_mapa
        else:
            todas_os_mapas = extrair_adicionar_todas_as_paginas(novo_pdf_mapa, todas_os_mapas, contador)

    # Copia o PDF final para o destino final
    if todas_os_mapas:
        copiar_pdf(todas_os_mapas, arquivo_final)
        print(f"\n✅ Todos os mapas foram unidos em: {arquivo_final}")
        configuracao = carregar_configuracao()
        arquivos_delete = configuracao["config_imprir_os"]["arquivos_deletedos"]


        # Deleta os temporários
        for arq in arquivos_delete:
            deletar_arquivo(arq)


# ---------------------------------------------------
# Executar a função principal
# ---------------------------------------------------
# if __name__ == "__main__":

#     juntas_map([
#         {"nome": "nome", "os": "435345", "matricula": "4353535", "inscricao": "345", "localidade": 122, "setor": 107, "rota": 6},
#         {"nome": "nome", "os": "435345", "matricula": "4353535", "inscricao": "345", "localidade": 122, "setor": 107, "rota": 7},
#         {"nome": "nome", "os": "435345", "matricula": "4353535", "inscricao": "345", "localidade": 122, "setor": 107, "rota": 8},
#         {"nome": "nome", "os": "435345", "matricula": "4353535", "inscricao": "345", "localidade": 111, "setor": 104, "rota": 8},
#     ], r"Z:\JOSINALDO VS CODE\MAPAS", r"C:\Users\equipehidro\Downloads\mapas_juntos.pdf")
