import os
import psycopg2
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Obter a URL do banco de dados
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def obter_conexao():
    """Cria e retorna uma conexão com o banco de dados."""
    try:
        return psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def executar_query(query, parametros=None):
    """
    Função genérica para executar queries.
    Retorna todos os registros em caso de SELECT, ou None em caso de erro ou INSERT/UPDATE.
    """
    conn = obter_conexao()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, parametros or ())
            if query.strip().lower().startswith("select"):
                resultado = cursor.fetchall()
                conn.commit()
                return resultado
            conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return None


def verificar_cadastro(telegram_id):
    """Verifica se o ID do Telegram está cadastrado e retorna o nome do usuário."""
    query = "SELECT nome FROM usuarios WHERE telegram = %s"
    resultado = executar_query(query, (telegram_id,))
    if resultado:
        return resultado[0][0]  # Retorna o nome do usuário cadastrado
    return None


def obter_usuario_id_por_telegram(telegram_id):
    """Retorna o user_id da tabela usuarios, dado o telegram_id."""
    query = "SELECT user_id FROM usuarios WHERE telegram = %s"
    resultado = executar_query(query, (telegram_id,))
    if resultado:
        return resultado[0][0]
    return None


def criar_usuario(user_id, nome, email):
    """Cria um novo usuário no banco de dados (exemplo)."""
    query = """
        INSERT INTO usuarios (user_id, nome, email)
        VALUES (%s, %s, %s)
        RETURNING user_id
    """
    resultado = executar_query(query, (user_id, nome, email))
    if resultado:
        return resultado[0][0]
    return None


def criar_conversa(usuario_id):
    """Cria uma nova conversa no banco de dados (relacionada ao usuário)."""
    query = "INSERT INTO conversas (usuario_id) VALUES (%s) RETURNING conversa_id"
    resultado = executar_query(query, (usuario_id,))
    if resultado:
        return resultado[0][0]
    return None


def salvar_mensagem(conversa_id, origem, mensagem):
    """Salva as mensagens trocadas na conversa."""
    query = """
        INSERT INTO mensagens (conversa_id, origem, mensagem)
        VALUES (%s, %s, %s)
    """
    executar_query(query, (conversa_id, origem, mensagem))


def obter_ultima_conversa(usuario_id):
    """Retorna a última conversa do usuário (conversa_id), ou None se não existir."""
    query = """
        SELECT conversa_id
        FROM conversas
        WHERE usuario_id = %s
        ORDER BY conversa_id DESC
        LIMIT 1
    """
    resultado = executar_query(query, (usuario_id,))
    if resultado:
        return resultado[0][0]
    return None


def obter_mensagens(conversa_id):
    """
    Retorna (origem, mensagem, timestamp) para cada mensagem da conversa, em ordem cronológica.
    ATENÇÃO: certifique-se de que a tabela 'mensagens' tenha a coluna 'timestamp'
    ou ajuste o ORDER BY conforme sua estrutura (ex: ORDER BY mensagem_id).
    """
    query = """
        SELECT origem, mensagem, timestamp
        FROM mensagens
        WHERE conversa_id = %s
        ORDER BY timestamp ASC
    """
    resultado = executar_query(query, (conversa_id,))
    return resultado if resultado else []


def salvar_pdf_conversa(usuario_id, pdf_path):
    """
    Salva o arquivo PDF da conversa na tabela "histórico-conversa".
    A tabela possui colunas:
        - id (integer, NOT NULL)
        - nome (character varying(255), NOT NULL)
        - cpf (character varying(11), NOT NULL)
        - unidade (character varying(255), NOT NULL)
        - pdf (bytea, NOT NULL)
    """
    # 1) Obter nome do usuário (caso precise armazenar na coluna 'nome')
    query_user = "SELECT nome FROM usuarios WHERE user_id = %s"
    user_data = executar_query(query_user, (usuario_id,))
    if not user_data:
        print("Usuário não encontrado na tabela 'usuarios'.")
        return False

    user_name = user_data[0][0]

    # Exemplo de valores para 'cpf' e 'unidade' (se não tiver no 'usuarios'):
    cpf_fake = "00000000000"
    unidade_fake = "UNIDADE_PADRAO"

    # 2) Lê o PDF em binário
    try:
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo PDF: {e}")
        return False

    # 3) Salvar no banco
    query_insert = """
        INSERT INTO "histórico-conversa" (id, nome, cpf, unidade, pdf)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        conn = obter_conexao()
        if not conn:
            return False

        with conn.cursor() as cursor:
            # Aqui, 'id' será o próprio usuario_id, assumindo que
            # user_id cabe na coluna 'id' da tabela "histórico-conversa"
            cursor.execute(query_insert, (usuario_id, user_name, cpf_fake, unidade_fake, psycopg2.Binary(pdf_data)))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao salvar PDF no banco: {e}")
        return False
