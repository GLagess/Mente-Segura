import ollama
import torch

def generate_embeddings(text):
    """Gera embeddings usando o modelo Ollama."""
    response = ollama.embeddings(model="mxbai-embed-large", prompt=text)
    return torch.tensor(response["embedding"])

def save_text_to_vault(text_chunks, file_path="vault.txt"):
    """Salva os chunks de texto no arquivo vault.txt"""
    with open(file_path, "a", encoding="utf-8") as file:
        for chunk in text_chunks:
            file.write(chunk + "\n\n")  # Adiciona um espaço entre os chunks

