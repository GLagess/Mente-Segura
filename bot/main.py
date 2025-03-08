import os
import requests
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import database
from gerar_pdf import gerar_pdf_conversa

load_dotenv()

# Configuração do bot e APIs
TOKEN = os.getenv("BOT_TOKEN")
IA_API_URL = os.getenv("IA_API_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WHISPER_API_URL = os.getenv("WHISPER_API_URL")

bot = telebot.TeleBot(TOKEN)


def consultar_ia(pergunta):
    """Envia a pergunta para a API de IA e retorna a resposta."""
    if not IA_API_URL:
        return "Erro: URL da API IA não configurada."

    try:
        response = requests.post(IA_API_URL, json={"pergunta": pergunta})
        if response.status_code == 200:
            return response.json().get("resposta", "Não obtive resposta da IA.")
        else:
            return f"Erro ao consultar IA: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Erro ao acessar a IA: {str(e)}"


@bot.message_handler(commands=["start"])
def start(msg: telebot.types.Message):
    """Mensagem inicial e verificação de acesso."""
    telegram_id = str(msg.chat.id)  # ID do Telegram do usuário
    usuario_nome = database.verificar_cadastro(telegram_id)

    if usuario_nome:
        # Usuário está cadastrado
        resposta = (
            f"Bem-vindo, {usuario_nome}! 🎉\n\n"
            "Como podemos te ajudar hoje?\n"
            "- Selecione uma opção abaixo:"
        )

        markup = InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton("💬 Conversar com a IA", callback_data="conversar_ia")
        btn2 = InlineKeyboardButton("🌐 Plataforma", callback_data="web")
        btn3 = InlineKeyboardButton("❓ Quem somos", callback_data="quem_somos")

        markup.add(btn1, btn2, btn3)
        bot.send_message(msg.chat.id, resposta, reply_markup=markup)
    else:
        # Usuário não cadastrado: mostra botão para verificar novamente
        markup = InlineKeyboardMarkup(row_width=1)
        btn_verificar = InlineKeyboardButton(
            "Verificar cadastro novamente",
            callback_data="verificar_acesso"
        )
        markup.add(btn_verificar)

        bot.send_message(
            msg.chat.id,
            f"🔒 Acesso restrito! Seu ID do Telegram *{telegram_id}* não está cadastrado.\n\n"
            "Caso deseje solicitar acesso, utilize seu ID e acesse o link abaixo:\n\n"
            "🔑 [Solicitar Acesso](http://servidorprivadoigor.online/formulariomendes/)",
            parse_mode="Markdown",
            reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Gerencia cliques nos botões do menu."""
    # Se o callback for para verificar o cadastro novamente, chamamos 'start' novamente
    if call.data == "verificar_acesso":
        start(call.message)
        return

    # Caso contrário, seguimos com as opções de menu
    respostas = {
        "conversar_ia": "Você iniciou uma conversa com a IA! Pergunte o que quiser.",
        "web": "Você selecionou PLATAFORMA. Aqui estão os detalhes...",
        "quem_somos": (
            "📞 Se precisar conversar, o CVV está disponível 24h!\n\n"
            "💬 Chat: [www.cvv.org.br](https://www.cvv.org.br)\n"
            "📞 Telefone: 188 (ligação gratuita)\n"
            "📧 E-mail: atendimento@cvv.org.br\n\n"
            "O CVV oferece apoio emocional e prevenção ao suicídio com sigilo e anonimato."
        ),
    }

    resposta = respostas.get(call.data, "Opção inválida.")
    bot.send_message(call.message.chat.id, resposta, parse_mode="Markdown")


@bot.message_handler(content_types=["text"])
def receber_pergunta(message):
    """Recebe perguntas de texto do usuário e consulta a IA."""
    user_id = message.chat.id
    pergunta = message.text.strip()

    try:
        # Cria (ou recupera) o usuário no banco
        usuario_id = database.criar_usuario(user_id, "Usuário Desconhecido", None)
        # Cria uma nova conversa
        conversa_id = database.criar_conversa(usuario_id)
        # Salva a mensagem do usuário
        database.salvar_mensagem(conversa_id, "Usuário", pergunta)

        # Chama a IA
        resposta_ia = consultar_ia(pergunta)
        # Salva a resposta da IA
        database.salvar_mensagem(conversa_id, "Bot", resposta_ia)

        bot.send_message(user_id, f"🤖 Resposta da IA:\n{resposta_ia}")
    except Exception as e:
        bot.send_message(user_id, f"Erro ao processar sua mensagem: {e}")


@bot.message_handler(content_types=["voice"])
def receber_audio(message):
    """Recebe mensagens de áudio e transcreve via Whisper."""
    try:
        file_info = bot.get_file(message.voice.file_id)
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

        response = requests.get(file_url)
        if response.status_code != 200:
            raise Exception("Erro ao baixar o áudio.")

        audio_path = "audio.ogg"
        with open(audio_path, "wb") as f:
            f.write(response.content)

        # Enviar para Whisper API
        with open(audio_path, "rb") as f:
            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
            files = {"file": f}
            data = {"model": "whisper-1"}
            response = requests.post(
                WHISPER_API_URL, headers=headers, files=files, data=data
            )

        if response.status_code == 200:
            texto = response.json().get("text", "Não foi possível converter o áudio.")
            bot.send_message(message.chat.id, f"🎙 Transcrição: {texto}")

            # Conversa
            usuario_id = database.criar_usuario(message.chat.id, "Usuário Desconhecido", None)
            conversa_id = database.criar_conversa(usuario_id)
            database.salvar_mensagem(conversa_id, "Usuário", texto)

            # IA
            resposta_ia = consultar_ia(texto)
            database.salvar_mensagem(conversa_id, "Bot", resposta_ia)

            bot.send_message(message.chat.id, f"🤖 Resposta da IA:\n{resposta_ia}")
        else:
            bot.send_message(message.chat.id, "Erro ao processar o áudio.")

    except Exception as e:
        bot.send_message(message.chat.id, f"Erro: {str(e)}")


@bot.message_handler(commands=["gerar_pdf"])
def gerar_pdf_command(msg: telebot.types.Message):
    """
    Comando que gera um PDF da última conversa do usuário
    e salva na tabela "histórico-conversa".
    """
    telegram_id = str(msg.chat.id)
    usuario_nome = database.verificar_cadastro(telegram_id)

    if not usuario_nome:
        bot.send_message(msg.chat.id, "🔒 Você não está cadastrado no sistema.")
        return

    # Obter user_id real (coluna user_id em usuarios)
    usuario_id = database.obter_usuario_id_por_telegram(telegram_id)
    if not usuario_id:
        bot.send_message(msg.chat.id, "⚠️ Não foi possível encontrar seu 'user_id' no banco.")
        return

    # Obter a última conversa associada a este usuario_id
    conversa_id = database.obter_ultima_conversa(usuario_id)
    if not conversa_id:
        bot.send_message(msg.chat.id, "⚠️ Nenhuma conversa encontrada para gerar PDF.")
        return

    # Gera o PDF e salva no banco
    pdf_path = gerar_pdf_conversa(conversa_id, usuario_id, usuario_nome)
    if pdf_path:
        bot.send_message(msg.chat.id, "✅ PDF gerado e salvo com sucesso no banco!")
    else:
        bot.send_message(msg.chat.id, "⚠️ Ocorreu um erro ao gerar o PDF da conversa.")


# Inicia o bot
bot.infinity_polling()
