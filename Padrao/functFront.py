import os
from tkinter import filedialog, messagebox
import openpyxl

class Arquivo_excel_check:
    def __init__(self):
        self.caminho_arquivo = ""

    def selecionar_arquivo_exel(self, label_destino):
        caminho = filedialog.askopenfilename(title="Selecione um arquivo")
        if not caminho.endswith(".xlsx"):
            label_destino.config(text="Nenhum arquivo válido selecionado.")
            messagebox.showerror("Erro", "Por favor, selecione um arquivo Excel com a extensão '.xlsx'.")
            return False, None
        else:
            _, arquivo = os.path.split(caminho)
            label_destino.config(text=arquivo)
            self.caminho_arquivo = caminho
            return True, caminho

    def verificar_colunas_no_excel(self, caminho_arquivo, colunas_necessarias):
        try:
            workbook = openpyxl.load_workbook(caminho_arquivo, read_only=True)
            sheet = workbook.active
            cabecalho = [cell.value for cell in sheet[1]]
            workbook.close()
            
            if all(col in cabecalho for col in colunas_necessarias):
                return True
            else:
                colunas_str = "', '".join(colunas_necessarias)
                messagebox.showerror("Erro", f"O arquivo Excel não contém as colunas necessárias: '{colunas_str}'.")
                return False

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar ler o arquivo Excel: {e}")
            return False


class Padroes_Front:
    def __init__(self):
        self.caminho_arquivo = ""

    def selecionar_arquivo(self):
        self.caminho = filedialog.askopenfilename(title="Selecione um arquivo")
        _, arquivo = os.path.split(self.caminho)
        return self.caminho , arquivo
    
    def selecionar_pasta(self):
        # Abre o diálogo de seleção de pasta
        self.caminho_pasta = filedialog.askdirectory(title="Selecione uma pasta")
        
        # Verifica se o usuário escolheu uma pasta
        if self.caminho_pasta:
            return self.caminho_pasta
        else:
            return False

