import tkinter as tk
from main_controller import verificar_assinatura_pdf


def verificar_assinatura_view(root):
    """
    Função para criar a interface gráfica para verificar a assinatura de um PDF.
    :param root: Instância da janela principal do Tkinter.
    :return: None
    """
    botao_verficar = tk.Button(root, text="Verificar Assinatura", command=verificar_assinatura_pdf)
    botao_verficar.pack(pady=20)
    return botao_verficar