from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flasgger import Swagger
from menteIA.chatbot import chat_with_llama  # Importando a função da IA

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

# Simulando um banco de memória para manter o contexto da conversa
conversation_history = []
vault_content = []  # Aqui devem estar os chunks de texto extraídos
vault_embeddings = []  # Aqui devem estar os embeddings extraídos


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

        resposta = chat_with_llama(pergunta, vault_embeddings, vault_content, conversation_history)

        return jsonify({"resposta": resposta})


# Adicionando o endpoint da IA na API
api.add_resource(ChatbotResource, "/api/chatbot")

if __name__ == "__main__":
    app.run(debug=True)
