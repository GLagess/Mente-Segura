# 🧠 Mente Segura – Assistente de Apoio Emocional com IA

Mente Segura é um **chatbot inteligente** que processa documentos PDF, extrai informações relevantes e utiliza um banco vetorial com **FAISS** para realizar buscas eficientes e fornecer **respostas personalizadas e empáticas**.  
O objetivo é oferecer um **suporte emocional acolhedor**, incentivando a conversa e fornecendo estratégias de bem-estar ao usuário.

---

## 🚀 Funcionalidades

- 📄 **Processamento de PDFs**: Extrai e organiza o conteúdo de documentos.
- 🧠 **Armazenamento de embeddings**: Utiliza FAISS para salvar e consultar vetores semânticos.
- ⚡ **Busca eficiente**: Recupera trechos relevantes com alta performance.
- 💬 **Chatbot responsivo**: Gera respostas personalizadas com histórico de conversa.
- 📲 **Integração com Telegram**: Permite interações via bot de forma prática.

---

## 🧰 Tecnologias Utilizadas

- Python 3.11  
- Flask  
- FAISS  
- Ollama  
- PyPDF2  
- Telebot (pyTelegramBotAPI)  
- PostgreSQL

---

## 📂 Estrutura do Projeto

```
Mente_segura-ia/
├── api/                # Código da API Flask
│   ├── api.py
│   ├── controllers.py
│   ├── models.py
│   ├── routes.py
│   └── __init__.py
│
├── bot/                # Bot do Telegram
│   ├── main.py
│   ├── .env
│   └── requirements.txt
│
├── IA_mentesegura/     # Lógica da Inteligência Artificial
│   ├── chatbot.py
│   ├── embeddings.py
│   ├── leitor_pdf.py
│   ├── main.py
│   └── __init__.py
│
├── data/               # PDFs processados
├── venv/               # Ambiente virtual
├── run.py              # Execução principal
├── requirements.txt    # Dependências do projeto
└── .gitignore          # Arquivos ignorados pelo Git
```

---

## ⚙️ Instalação e Configuração

### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/seu-usuario/Mente_Segura-IA.git
cd Mente_Segura-IA
```

### 2️⃣ Crie e Ative um Ambiente Virtual

```bash
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3️⃣ Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure as Variáveis de Ambiente

Crie um arquivo `.env` dentro das pastas `bot/` e `api/` com:

```
BOT_TOKEN=seu_token_do_telegram
IA_API_URL=http://127.0.0.1:5000/api/chatbot
DB_HOST=localhost
DB_NAME=mente_segura
DB_USER=usuario
DB_PASSWORD=senha
```

### 5️⃣ Execute a API

```bash
python api/api.py
```

A API estará disponível em: [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

### 6️⃣ Execute o Bot do Telegram

```bash
python bot/main.py
```

### 7️⃣ Indexe os Embeddings

```bash
python IA_mentesegura/main.py
```

---

## 💡 Como Funciona?

1. O usuário interage via Telegram ou API.
2. A IA consulta o histórico e os documentos no FAISS.
3. Com base nisso, gera uma resposta personalizada usando o **Ollama**.
4. A resposta é enviada, estimulando a continuidade da conversa.

---

## 🤝 Contribuições

Contribuições são muito bem-vindas!  
Abra uma **Pull Request** com melhorias ou relate problemas em **Issues**.

---

## 📬 Contato

- ✉️ gabriellages210711@gmail.com  
- ✉️ matheusmendesbmf@outlook.com  
- 🔗 [Gabriel Lages – LinkedIn](https://www.linkedin.com/in/gabriel-lages-a31638226/)  
- 🔗 [Matheus Mendes – LinkedIn](https://www.linkedin.com/in/matheusmendesdev/)
