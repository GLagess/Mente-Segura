import os
import torch
from leitor_pdf import extract_text_from_pdf
from IA_mentesegura.embeddings import generate_embeddings, save_text_to_vault
from chatbot import chat_with_llama

def load_vault(file_path="vault.txt"):
    """Carrega o conteúdo do vault e gera embeddings sem incluir linhas vazias."""
    if not os.path.exists(file_path):
        return [], torch.tensor([])

    with open(file_path, "r", encoding="utf-8") as file:
        vault_content = [line.strip() for line in file.readlines() if line.strip()]  # Remove linhas vazias

    embeddings = []
    for text in vault_content:
        embedding = generate_embeddings(text)
        if embedding.numel() > 0:  # Verifica se o tensor não está vazio
            embeddings.append(embedding)

    if not embeddings:  # Se não houver embeddings válidos, retorna um tensor vazio
        return vault_content, torch.tensor([])

    vault_embeddings = torch.stack(embeddings)
    return vault_content, vault_embeddings


if __name__ == "__main__":
    print("📄 Processando PDFs na pasta 'data/'...")

    for file in os.listdir("data"):
        if file.endswith(".pdf"):
            pdf_path = os.path.join("data", file)
            print(f"📖 Extraindo texto de: {file}...")

            pdf_text_chunks = extract_text_from_pdf(pdf_path)  # Retorna uma lista de chunks
            save_text_to_vault(pdf_text_chunks)  # Salva cada chunk no vault.txt

            print(f"✅ {file} processado com {len(pdf_text_chunks)} chunks.")

    print("📂 Carregando documentos para consulta...")
    vault_content, vault_embeddings = load_vault()

    conversation_history = []  # Armazena o histórico de conversa

    print("💬 Chatbot iniciado! Digite sua pergunta ou 'sair' para encerrar.")
    while True:
        user_input = input("\nDigite sua pergunta: ")
        if user_input.lower() == "sair":
            print("👋 Encerrando chatbot. Até logo!")
            break

        response = chat_with_llama(user_input, vault_embeddings, vault_content, conversation_history)
        print("\n🤖 Resposta:", response)

