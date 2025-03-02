import os
import requests
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Carregar variáveis de ambiente
load_dotenv()

# Definir tokens e URL da API
TOKEN = os.getenv("BOT_TOKEN")  # Token do seu bot no Telegram
IA_API_URL = "http://127.0.0.1:5000/api/chatbot"  # URL do endpoint da API Flask

# Inicializa o bot
bot = telebot.TeleBot(TOKEN)

# Função para consultar a IA via API Flask
def consultar_ia(pergunta):
    try:
        headers = {"Content-Type": "application/json"}
        data = {"pergunta": pergunta}
        response = requests.post(IA_API_URL, json=data, headers=headers)

        if response.status_code == 200:
            return response.json().get("resposta", "Não obtive resposta da IA.")
        else:
            return f"Erro ao consultar IA: {response.status_code} - {response.text}"  # Exibe erro completo

    except Exception as e:
        return f"Erro ao acessar a IA: {str(e)}"



# Comando /start - Enviar menu interativo
@bot.message_handler(commands=["start"])
def start(msg: telebot.types.Message):
    resposta = (
        "Bem-vindo ao Mente Segura!\n\n"
        "Como podemos te ajudar hoje?\n"
        "- Selecione uma opção abaixo:"
    )

    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("💬 Conversar com a IA", callback_data="conversar_ia")
    btn2 = InlineKeyboardButton("⚙ Plataforma", callback_data="plataforma")
    btn3 = InlineKeyboardButton("🔝 Emergência", callback_data="emergencia")
    btn4 = InlineKeyboardButton("🔗 DataLink", callback_data="datalink")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    bot.send_message(msg.chat.id, resposta, reply_markup=markup)


# Respostas para os botões do menu interativo
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "conversar_ia":
        bot.send_message(
            call.message.chat.id, "Você iniciou uma conversa com a IA! Pergunte o que quiser."
        )
    elif call.data == "plataforma":
        bot.send_message(call.message.chat.id, "Você selecionou PLATAFORMA. Aqui estão os detalhes...")
    elif call.data == "emergencia":
        bot.send_message(
            call.message.chat.id,
            "📞 *Se precisar conversar, o CVV está disponível 24h!*\n\n"
            "💬 *Chat:* [www.cvv.org.br](https://www.cvv.org.br) \n"
            "📞 *Telefone:* 188 (ligação gratuita)\n"
            "📧 *E-mail:* atendimento@cvv.org.br\n\n"
            "O CVV oferece apoio emocional e prevenção ao suicídio com sigilo e anonimato.",
            parse_mode="Markdown"
        )
    elif call.data == "datalink":
        bot.send_message(call.message.chat.id, "Você selecionou DATALINK. Aqui estão os detalhes...")
    else:
        bot.send_message(call.message.chat.id, "Opção inválida.")


# Quando o usuário mandar uma mensagem, a IA responde
@bot.message_handler(func=lambda message: True)
def receber_pergunta(message):
    user_id = message.chat.id
    pergunta = message.text

    bot.send_message(user_id, "🤖 Processando sua pergunta...")

    resposta_ia = consultar_ia(pergunta)  # Envia a pergunta para a API Flask
    bot.send_message(user_id, f"🤖 Resposta da IA:\n{resposta_ia}")


# Inicia o bot do Telegram
bot.polling()
