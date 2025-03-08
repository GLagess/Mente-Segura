import os

# Definir a variável de ambiente para permitir múltiplas instâncias do OpenMP
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import faiss
import numpy as np
import torch
import ollama

# Imports do seu projeto
from extrator_pdf import process_pdfs
from embeddings import create_faiss_index, load_faiss_index
from chatbot import chat_with_llama

def main():
    # (Opcional) Processa PDFs e gera vault.txt
    # process_pdfs(pdf_folder="data", output_file="vault.txt")

    # Cria ou carrega o índice FAISS
    faiss_index, vault_content = load_faiss_index()

    conversation_history = []
    print("🔮 IA carregada! Faça uma pergunta ou digite 'sair' para encerrar.")

    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Encerrando...")
            break

        resposta = chat_with_llama(
            query=user_input,
            faiss_index=faiss_index,
            vault_content=vault_content,
            conversation_history=conversation_history
        )
        print("IA:", resposta, "\n")

if __name__ == "__main__":
    main()
