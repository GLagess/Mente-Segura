Mente Segura - Assistente de Apoio Emocional com IA

📌 Sobre o Projeto

O Mente Segura é um chatbot assistido por IA que processa documentos PDF, extrai informações relevantes e utiliza um banco de dados vetorial baseado em FAISS para realizar buscas eficientes e fornecer respostas mais precisas. O sistema tem como objetivo oferecer suporte empático aos usuários, incentivando a conversa e oferecendo estratégias de acolhimento emocional.

🚀 Funcionalidades

✅ Processamento de PDFs: Extrai e organiza o conteúdo de documentos. ✅ Armazenamento de embeddings: Utiliza FAISS para armazenar e recuperar embeddings de texto. ✅ Busca rápida e eficiente: Encontra trechos mais relevantes nos documentos processados. ✅ Chatbot responsivo: Mantém um histórico de conversas e gera respostas personalizadas. ✅ Integração com Telegram: Permite interações diretas via bot no Telegram.

🔧 Tecnologias Utilizadas

Python 3.11

Flask

FAISS

Ollama

PyPDF2

Telebot

PostgreSQL

📂 Estrutura do Projeto

Mente_segura-ia/ │── api/ # Código da API Flask │ ├── api.py # Definição das rotas │ ├── controllers.py # Controladores da API │ ├── models.py # Modelos do banco de dados │ ├── routes.py # Definição das rotas │ ├── init.py # Pacote Python │ │── bot/ # Código do bot Telegram │ ├── main.py # Inicialização do bot │ ├── .env # Variáveis de ambiente │ ├── requirements.txt # Dependências do bot │ │── IA_mentesegura/ # Código da IA │ ├── chatbot.py # Lógica de resposta do chatbot │ ├── embeddings.py # Geração e armazenamento de embeddings no FAISS │ ├── leitor_pdf.py # Extração de texto de PDFs │ ├── main.py # Processamento inicial e teste do chatbot │ ├── init.py # Pacote Python │ │── data/ # Pasta de armazenamento de PDFs │ │── venv/ # Ambiente virtual │── run.py # Arquivo de execução principal │── requirements.txt # Dependências do projeto │── .gitignore # Arquivos ignorados pelo Git

🛠️ Instalação e Configuração

1️⃣ Clone o repositório

git clone https://github.com/seu-usuario/Mente_Segura-IA.git cd Mente_Segura-IA

2️⃣ Crie e ative um ambiente virtual

python -m venv venv

source venv/bin/activate # Linux/macOS

venv\Scripts\activate # Windows

3️⃣ Instale as dependências

pip install -r requirements.txt

4️⃣ Configurar Variáveis de Ambiente

Crie um arquivo .env dentro das pastas bot/ e api/ com as seguintes informações:

BOT_TOKEN=seu_token_do_telegram IA_API_URL=http://127.0.0.1:5000/api/chatbot DB_HOST=localhost DB_NAME=mente_segura DB_USER=usuario DB_PASSWORD=senha

5️⃣ Executar a API

python api/api.py

A API estará disponível em: http://127.0.0.1:5000/apidocs

6️⃣ Executar o Bot do Telegram

python bot/main.py

7️⃣ Processar os PDFs e Indexar os Embeddings

python IA_mentesegura/main.py

📌 Como Funciona?

1️⃣ O usuário interage com o chatbot via Telegram ou API. 2️⃣ A IA verifica o histórico da conversa e os trechos mais relevantes no FAISS. 3️⃣ Com base nesses dados, a IA gera uma resposta personalizada utilizando Ollama. 4️⃣ A resposta é enviada ao usuário, incentivando a continuidade da conversa.

📝 Contribuições

Se quiser contribuir com melhorias, sinta-se à vontade para abrir um Pull Request ou reportar problemas via Issues!

📩 Contato: gabriellages210711@gmail.com / matheusmendesbmf@outlook.com

🔗 LinkedIn: https://www.linkedin.com/in/gabriel-lages-a31638226/ ; https://www.linkedin.com/in/matheusmendesdev/