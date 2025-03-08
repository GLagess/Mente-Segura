import ollama
import torch
import numpy as np
import faiss
import os

VAULT_FILE = "vault.txt"
FAISS_INDEX_PATH = "faiss_index.bin"

def generate_embeddings(text):
    """Gera embeddings usando o modelo Ollama (mxbai-embed-large)."""
    response = ollama.embeddings(model="mxbai-embed-large", prompt=text)
    # Retorna como array float32 (FAISS trabalha melhor com float32)
    return np.array(response["embedding"], dtype="float32")

def save_text_to_vault(text_chunks, file_path=VAULT_FILE):
    """Salva os chunks de texto no arquivo vault.txt"""
    with open(file_path, "a", encoding="utf-8") as file:
        for chunk in text_chunks:
            file.write(chunk + "\n\n")  # Adiciona um espaço entre os chunks

def create_faiss_index():
    """Cria um índice FAISS a partir do vault.txt e salva em disco."""
    if not os.path.exists(VAULT_FILE):
        print(f"Arquivo {VAULT_FILE} não encontrado. Certifique-se de ter gerado o vault primeiro.")
        return None, []

    # Lê os chunks do vault
    with open(VAULT_FILE, "r", encoding="utf-8") as f:
        text_chunks = [line.strip() for line in f.readlines() if line.strip()]

    # Gera embeddings para cada chunk
    all_embeddings = []
    for chunk in text_chunks:
        emb = generate_embeddings(chunk)
        # Normaliza cada embedding para usar com IndexFlatIP (cosseno)
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb = emb / norm
        all_embeddings.append(emb)

    all_embeddings = np.array(all_embeddings, dtype="float32")

    # Cria o índice FAISS (usando produto interno - IP)
    d = all_embeddings.shape[1]  # Dimensão do embedding
    index = faiss.IndexFlatIP(d)
    index.add(all_embeddings)

    # Salva em disco
    faiss.write_index(index, FAISS_INDEX_PATH)
    print(f"✅ Índice FAISS criado e salvo em {FAISS_INDEX_PATH}")

    return index, text_chunks

def load_faiss_index():
    """Carrega o índice FAISS e os chunks do vault. Se não existir, cria."""
    if os.path.exists(FAISS_INDEX_PATH):
        print(f"✅ Carregando índice FAISS de {FAISS_INDEX_PATH}...")
        index = faiss.read_index(FAISS_INDEX_PATH)
        # Precisamos dos chunks também (na mesma ordem)
        with open(VAULT_FILE, "r", encoding="utf-8") as f:
            text_chunks = [line.strip() for line in f.readlines() if line.strip()]
        return index, text_chunks
    else:
        print("⚠️ Índice FAISS não encontrado. Criando um novo...")
        return create_faiss_index()
