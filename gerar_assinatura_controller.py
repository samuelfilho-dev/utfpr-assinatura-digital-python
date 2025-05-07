from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import fitz

from tkinter import messagebox
from qr_code_generator import gerar_qr_code


from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

import io
import os
import uuid
import base64

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

    # Cria um hash SHA-256 do conteúdo do PDF/A
    # Cria um hash SHA-256 do conteúdo do PDF/A
    hash_pdfa = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hash_pdfa.update(conteudo_pdfa)
    hash_pdfa = hash_pdfa.finalize()

    # Assina o hash usando a chave privada e curva elíptica ECDSA
    assinatura = chave_privada.sign(hash_pdfa, ec.ECDSA(hashes.SHA256()))

    qrcode = gerar_qr_code(chave_publica_pem, assinatura, hash_pdfa)

    return criar_pdf_com_assinatura(documento_pdfa, qrcode)


def criar_pdf_com_assinatura(documento_pdfa, qr_code):
    doc = fitz.open(documento_pdfa)

    # Save QR code to a temporary buffer
    qr_buffer = io.BytesIO()
    qr_code.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    # Add the hash text and QR code to the bottom of each page
    for page_num in range(len(doc)):
        page = doc[page_num]

        # Get page dimensions
        page_width = page.rect.width
        page_height = page.rect.height

        # Calculate position for text (bottom of page)
        text_x = 50  # Some margin from left
        text_y = page_height - 20  # Some margin from bottom

        # Insert the hash text
        page.insert_text(
            (text_x, text_y),
            "Documento Assinado Digitalmente",
            fontsize=8,
            color=(0, 0, 0),
        )

        # Add QR code to the bottom right of the page
        qr_rect = fitz.Rect(
            page_width - 90,  # Position from right
            page_height - 90,  # Position from bottom
            page_width - 10,  # Right margin
            page_height - 10,  # Bottom margin
        )

        # Insert the QR code image
        page.insert_image(qr_rect, stream=qr_buffer.getvalue())

    # Save the modified document with a new filename
    output_path = (
        os.path.dirname(os.path.abspath(__file__))
        + "/output/"
        + str(FILENAME)
        + "_assinado.pdf"
    )
    doc.save(output_path)
    doc.close()

    # Return the path to the signed document
    return output_path
