from flask import request, jsonify
from flask_restful import Resource

class ChatbotResource(Resource):
    def get(self):
        """
        Endpoint para testar a API
        ---
        responses:
          200:
            description: API está rodando corretamente.
        """
        return jsonify({"message": "API do chatbot está rodando!"})

    def post(self):
        """
        Enviar mensagem para o chatbot
        ---
        parameters:
          - name: message
            in: body
            type: string
            required: true
            description: Mensagem do usuário para o chatbot
        responses:
          200:
            description: Resposta do chatbot
        """
        data = request.get_json()
        user_message = data.get("message", "")

        # Simulação de resposta do chatbot (IA será integrada depois)
        chatbot_response = f"Você disse: {user_message}"

        return jsonify({"user_message": user_message, "chatbot_response": chatbot_response})
