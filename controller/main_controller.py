import fitz
import uuid
import os

from tkinter import filedialog, messagebox
from controller.gerar_assinatura_controller import assinar_documentos_pdfa


def selecionar_pdf():
    """Função para selecionar um arquivo PDF."""
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo PDF", filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if caminho_arquivo:
        transform_to_pdfa(caminho_arquivo)
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

    uuid_filename = uuid.uuid4()
    doc.save(f"./input/{uuid_filename}", garbage=4, deflate=True, clean=True)
    print("PDF/A convertido e salvo em ./input")

    assinar_documentos_pdfa(f"./input/{uuid_filename}")
    doc.close()
