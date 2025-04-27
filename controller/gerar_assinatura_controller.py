from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from tkinter import messagebox
from controller.qr_code_generator import gerar_qr_code

from PyPDF2 import PdfReader, PdfWriter

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

import io
import os
import uuid

chave_privada = ec.generate_private_key(ec.SECP256R1())
chave_publica = chave_privada.public_key()


FILENAME = uuid.uuid4()

# Serializando a chave privada
chave_privada_pem = chave_privada.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

chave_publica_pem = chave_publica.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
).decode("utf-8")


def assinar_documentos_pdfa(documento_pdfa):
    """
    Função para assinar um documento PDF/A com uma assinatura digital.
    A assinatura é gerada a partir do hash SHA-256 do conteúdo do PDF/A.
    Um QR Code é gerado com a chave pública e a assinatura, e é adicionado ao PDF.
    :param documento_pdfa: Caminho do arquivo PDF/A a ser assinado.
    :return: None
    """

    # Verifica se o arquivo PDF/A foi fornecido
    if not documento_pdfa:
        messagebox.showerror("Erro", "Nenhum documento PDF/A fornecido.")
        return None

    # Verifica se o arquivo PDF/A existe
    with open(documento_pdfa, "rb") as f:
        conteudo_pdfa = f.read()

    # Calcula o hash SHA-256 do conteúdo do PDF/A
    cal = hashes.Hash(hashes.SHA256(), backend=default_backend())
    cal.update(conteudo_pdfa)
    pdf_hash = cal.finalize()

    # Assina o hash do PDF/A com a chave privada
    assinatura = chave_privada.sign(
        pdf_hash,
        ec.ECDSA(hashes.SHA256()),
    )
    
    print(f"Assinatura: {assinatura.hex()}")

    # Gera o QR Code com a chave pública, assinatura e hash do PDF/A
    qr_img = gerar_qr_code(chave_publica_pem, assinatura, pdf_hash)

    qr_bytes = io.BytesIO()
    qr_img.save(qr_bytes, format="PNG")
    qr_bytes.seek(0)

    leitor = PdfReader(documento_pdfa)
    escritor = PdfWriter()

    for pagina in leitor.pages:
        escritor.add_page(pagina)

    # Cria um novo PDF com o QR Code
    packet = io.BytesIO()
    can = canvas.Canvas(packet)

    img = ImageReader(qr_bytes)
    can.drawImage(
        img, 100, 100, width=100, height=100
    )  # Ajuste a posição e o tamanho conforme necessário

    can.setFont("Helvetica", 8)
    can.drawString(100, 80, "Assinatura Digital")

    can.save()

    packet.seek(0)
    qr_pdf = PdfReader(packet)

    # Mescla o QR Code na primeira página do PDF
    primeira_pagina = escritor.pages[0]
    primeira_pagina.merge_page(qr_pdf.pages[0])

    # Salva o PDF assinado
    caminho_pdf_assinado = os.path.dirname(os.path.abspath(__file__)) + "/output/" + str(FILENAME) + "_assinado.pdf"

    os.makedirs(os.path.dirname(caminho_pdf_assinado), exist_ok=True)

    with open(caminho_pdf_assinado, "wb") as f:
        escritor.write(f)

    print(f"PDF assinado salvo em: {caminho_pdf_assinado}")

    messagebox.showinfo("Sucesso", f"PDF assinado salvo em: {caminho_pdf_assinado}")
