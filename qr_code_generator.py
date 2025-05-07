import qrcode
import json
import datetime

def gerar_qr_code(chave_publica, assinatura, pdf_hash):
    """
    Função para gerar um QR Code com os dados da chave pública e outras informações.
    :param chave_publica: A chave pública a ser incluída no QR Code.
    :param assinatura: A assinatura digital a ser incluída no QR Code.
    :return: Imagem do QR Code gerado.
    """
    qr_data = {
        "version": "1.0",
        "institution": "Universidade Federal Tecnológica do Paraná",
        "algorithm": "ECDSA-SHA256-SECP256R1",
        "course": "PPGCA - Programa de Pós-Graduação em Computação Aplicada",
        "signature": assinatura.hex(),
        "public_key": chave_publica,
        "document_hash": pdf_hash.hex(),
        "timestamp": datetime.datetime.now().isoformat(),
    }

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(json.dumps(qr_data))

    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img
