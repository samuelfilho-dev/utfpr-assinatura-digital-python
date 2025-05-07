import tkinter as tk
from main_controller import selecionar_pdf


def criar_assinatura_view(root):
    """
    Função para criar a view de assinatura digital.
    :param root: Instância da janela principal do Tkinter.
    :return: None
    """
    botao_upload = tk.Button(root, text="Selecionar PDF", command=selecionar_pdf)
    botao_upload.pack(pady=20)
    return botao_upload