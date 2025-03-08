import os
import database
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BASE_DIR = "conversas_pdfs/"

def gerar_pdf_conversa(conversa_id, usuario_id, usuario_nome):
    """Gera um PDF contendo todas as mensagens de uma conversa e salva no banco."""
    mensagens = database.obter_mensagens(conversa_id)

    if not mensagens:
        print("Nenhuma mensagem encontrada para gerar PDF.")
        return None

    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    caminho_pdf = os.path.join(BASE_DIR, f"conversa_{conversa_id}.pdf")

    pdf = canvas.Canvas(caminho_pdf, pagesize=letter)
    y = 750  # Define a posição inicial no PDF

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, y, f"Conversa de {usuario_nome}")
    y -= 30

    pdf.setFont("Helvetica", 12)

    for autor, texto, timestamp in mensagens:
        # Caso não tenha 'timestamp' na tabela, remova ou adapte a formatação de data
        horario = timestamp.strftime("%H:%M") if timestamp else "??:??"
        if y < 50:  # Evita que o texto fique cortado no rodapé
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = 750

        pdf.drawString(100, y, f"[{horario}] {autor}: {texto}")
        y -= 20  # Ajusta o espaçamento entre linhas

    pdf.save()

    # Salvar no banco de dados (histórico-conversa)
    if database.salvar_pdf_conversa(usuario_id, caminho_pdf):
        print(f"PDF da conversa {conversa_id} salvo com sucesso no banco.")
    else:
        print(f"Erro ao salvar o PDF da conversa {conversa_id} no banco.")

    return caminho_pdf
