import os

import psycopg2
import requests
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


TOKEN = os.getenv("BOT_TOKEN")
IA_API_URL = os.getenv("IA_API_URL")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

bot = telebot.TeleBot(TOKEN)

# Comentando as funções de banco de dados
# def conectar_bd():
#     return psycopg2.connect(
#         host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
#     )


# def init_db():
#     conn = conectar_bd()
#     cursor = conn.cursor()
#     cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS mensagens (
#             id SERIAL PRIMARY KEY,
#             user_id BIGINT NOT NULL,
#             mensagem TEXT NOT NULL,
#             resposta TEXT DEFAULT NULL,
#             status VARCHAR(20) DEFAULT 'pendente'
#         )
#     """
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()


# init_db()


@bot.message_handler(commands=["start"])
def start(msg: telebot.types.Message):
    resposta = (
        "Bem-vindo ao Mente Segura!\n\n"
        "Como podemos te ajudar hoje?\n"
        "- Selecione uma opção abaixo:"
    )

    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(
        "💬 Quero conversar com IA", callback_data="conversar_ia"
    )
    btn2 = InlineKeyboardButton("⚙ PLATAFORMA", callback_data="plataforma")
    btn3 = InlineKeyboardButton("🔝 EMERGÊNCIA", callback_data="emergencia")
    btn4 = InlineKeyboardButton("🔗 DATALINK", callback_data="datalink")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    bot.send_message(msg.chat.id, resposta, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "conversar_ia":
        bot.send_message(
            call.message.chat.id,
            "Você iniciou uma conversa com a IA! Pergunte o que quiser.",
        )
    elif call.data == "plataforma":
        bot.send_message(
            call.message.chat.id,
            "Você selecionou PLATAFORMA. Aqui estão os detalhes...",
        )
    elif call.data == "emergencia":
        bot.send_message(
            call.message.chat.id,
            "📞 *Se precisar conversar, o CVV está disponível 24h!*\n\n"
            "💬 *Chat:* [www.cvv.org.br](https://www.cvv.org.br) \n"
            "📞 *Telefone:* 188 (ligação gratuita)\n"
            "📧 *E-mail:* atendimento@cvv.org.br\n\n"
            "O CVV oferece apoio emocional e prevenção ao suicídio com sigilo e anonimato.",
        )
    elif call.data == "datalink":
        bot.send_message(
            call.message.chat.id, "Você selecionou DATALINK. Aqui estão os detalhes..."
        )
    else:
        bot.send_message(call.message.chat.id, "Opção inválida.")


@bot.message_handler(func=lambda message: True)
def receber_pergunta(message):
    user_id = message.chat.id
    pergunta = message.text

    # Comentar a parte de salvar a pergunta no banco (como você não está usando o banco por enquanto)
    # conn = conectar_bd()
    # cursor = conn.cursor()
    # cursor.execute(
    #     "INSERT INTO mensagens (user_id, mensagem, status) VALUES (%s, %s, 'pendente')",
    #     (user_id, pergunta),
    # )
    # conn.commit()
    # cursor.close()
    # conn.close()

    bot.send_message(user_id, "Sua pergunta foi recebida e será avaliada.")

    processar_perguntas()


def processar_perguntas():
    # Comentar a parte de acessar o banco de dados
    # conn = conectar_bd()
    # cursor = conn.cursor()

    # cursor.execute(
    #     "SELECT id, user_id, mensagem FROM mensagens WHERE status = 'pendente'"
    # )
    # perguntas = cursor.fetchall()

    # for pergunta in perguntas:
    #     pergunta_id, user_id, texto = pergunta

    #     resposta_ia = consultar_ia(texto)

    #     cursor.execute(
    #         "UPDATE mensagens SET resposta = %s, status = 'respondido' WHERE id = %s",
    #         (resposta_ia, pergunta_id),
    #     )
    #     conn.commit()

    #     bot.send_message(user_id, f"🤖 Resposta da IA:\n{resposta_ia}")

    # cursor.close()
    # conn.close()

    pergunta = "Exemplo de pergunta da IA"
    user_id = 123456  # Usando um ID de exemplo
    resposta_ia = consultar_ia(pergunta)
    bot.send_message(user_id, f"🤖 Resposta da IA:\n{resposta_ia}")


def consultar_ia(pergunta):
    try:
        response = requests.post(IA_API_URL, json={"pergunta": pergunta})

        if response.status_code == 200:
            return response.json().get("resposta", "Não obtive resposta da IA.")
        else:
            return f"Erro ao consultar IA: {response.status_code}"

    except Exception as e:
        return f"Erro ao acessar a IA: {str(e)}"


bot.infinity_polling()