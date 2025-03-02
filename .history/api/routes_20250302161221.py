from flask import Blueprint
from flask_restful import Api
from api.controllers import ChatbotResource

# Criando um Blueprint para organizar as rotas
api_bp = Blueprint("api", __name__)
api = Api(api_bp)

# Adicionando os endpoints
api.add_resource(ChatbotResource, "/chatbot")  # Rota para interagir com o chatbot
