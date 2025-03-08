from flask import Blueprint
from flask_restful import Api
from api.controllers import ChatbotResource

api_bp = Blueprint("api", __name__)  # Blueprint para agrupar rotas
api = Api(api_bp)

# Rota para interagir com o chatbot (GET e POST)
api.add_resource(ChatbotResource, "/chatbot")
