import fitz
import uuid
import os
import shutil
import gc
import redis

from tkinter import filedialog, messagebox
from gerar_assinatura_controller import assinar_documentos_pdfa

FILENAME = uuid.uuid4()
PATH = os.path.dirname(os.path.abspath(__file__)) + "/input/" + str(FILENAME) + ".pdf"


def selecionar_pdf():
    """Função para selecionar um arquivo PDF."""
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo PDF", filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if caminho_arquivo:
        shutil.copy(caminho_arquivo, PATH)
        transform_to_pdfa(PATH)
    else:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado.")


def transform_to_pdfa(caminho_arquivo):
    """
    Função para converter um arquivo PDF em PDF/A.
    :param caminho_arquivo: Caminho para o arquivo PDF a ser convertido.
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

    try:
        gc.disable()
        doc.save(PATH, incremental=True, encryption=0)
        print("PDF/A convertido e salvo em:", PATH)
        assinar_documentos_pdfa(PATH)
    except Exception as e:
        print("Erro ao salvar o PDF/A:", e)
        messagebox.showerror("Erro", "Falha ao converter o PDF para PDF/A.")
        doc.close()
    finally:
        gc.enable()
        doc.close()

def verificar_assinatura_pdf():
    """
    Função para verificar a assinatura digital de um arquivo PDF.
    :return: None
    """
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo PDF", filetypes=[("Arquivos PDF", "*.pdf")]
    )
    
    if not caminho_arquivo:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
        
    name_file_with_ass_name = os.path.basename(caminho_arquivo).split(".")[0]
    file_name = name_file_with_ass_name.split('_')[0]

    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    hash_value = redis_client.get(file_name)
    print(f'hash_value {hash_value}')
    
    if hash_value:
        messagebox.showinfo("Sucesso", "Assinatura verificada com sucesso.")
    else:
        messagebox.showerror("Erro", "Assinatura não encontrada.")
        