import PyPDF2
import os

def extract_text_from_pdf(pdf_path, chunk_size=800):
    """Lê um PDF e divide o texto em partes menores (chunks)."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    
    # Divide o texto em chunks menores
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    
    return chunks

def process_pdfs(pdf_folder="data", output_file="vault.txt"):
    """Processa todos os PDFs na pasta e salva o conteúdo no vault.txt"""
    if not os.path.exists(pdf_folder):
        print(f"A pasta {pdf_folder} não existe.")
        return

    with open(output_file, "w", encoding="utf-8") as vault_file:
        for pdf_file in os.listdir(pdf_folder):
            if pdf_file.endswith(".pdf"):
                pdf_path = os.path.join(pdf_folder, pdf_file)
                print(f"📄 Processando: {pdf_file}")
                
                chunks = extract_text_from_pdf(pdf_path)
                for chunk in chunks:
                    vault_file.write(chunk + "\n\n")  # Adiciona uma linha extra para separar os textos
                
                print(f"✅ {pdf_file} processado com {len(chunks)} chunks.")

if __name__ == "__main__":
    process_pdfs()
