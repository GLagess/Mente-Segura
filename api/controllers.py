from flask import request, jsonify
from flask_restful import Resource
from IA.chatbot import chat_with_llama

# Variáveis de memória para protótipo
conversation_history = []
vault_content = []
vault_embeddings = []

class ChatbotResource(Resource):
    def post(self):
        """
        Enviar mensagem para a IA e receber resposta
        ---
        parameters:
          - name: pergunta
            in: body
            required: true
            schema:
              type: object
              properties:
                pergunta:
                  type: string
        responses:
          200:
            description: Resposta da IA
        """
        data = request.get_json()
        pergunta = data.get("pergunta")

        if not pergunta:
            return jsonify({"erro": "A pergunta não pode estar vazia!"})

        # Chama a função da IA
        resposta = chat_with_llama(pergunta, vault_embeddings, vault_content, conversation_history)
        return jsonify({"resposta": resposta})
