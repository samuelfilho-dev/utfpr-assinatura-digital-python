import fitz
import uuid
import os
import shutil

from tkinter import filedialog, messagebox
from controller.gerar_assinatura_controller import assinar_documentos_pdfa

FILENAME = uuid.uuid4()
PATH = os.path.dirname(os.path.abspath(__file__)) + "/input/" + str(FILENAME) + ".pdf"


def selecionar_pdf():
    """Função para selecionar um arquivo PDF."""
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo PDF", filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if caminho_arquivo:

        print("Arquivo selecionado:", caminho_arquivo)
        print("Caminho do arquivo:", PATH)

        shutil.copy(caminho_arquivo, PATH)
        transform_to_pdfa(PATH)
    else:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado.")


def transform_to_pdfa(caminho_arquivo):
    """
    Função para transformar um arquivo PDF em PDF/A.
    Esta função adiciona metadados e salva o arquivo em um local temporário.
    O arquivo PDF/A é uma versão do PDF que atende a requisitos específicos de arquivamento a longo prazo.
    :param caminho_arquivo: Caminho do arquivo PDF a ser convertido.
    :return: None
    """
    doc = fitz.open(caminho_arquivo)

    doc.set_metadata(
        {
            "title": f"{uuid.uuid4()}",
            "author": "Author Name",
            "subject": "Convertido para PDF/A",
            "keywords": "PDF/A, exemplo",
            "creator": "Creator Name",
            "producer": "Producer Name",
            "creationDate": "D:20231010120000+00'00'",
        }
    )

    doc.save(PATH, garbage=4, deflate=True, clean=True, incremental=True)
    print("PDF/A convertido e salvo em:", PATH)
    assinar_documentos_pdfa(PATH)
    doc.close()
