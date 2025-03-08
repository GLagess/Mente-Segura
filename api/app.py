from flask import Flask
from flasgger import Swagger
from api.routes import api_bp  # Importa o Blueprint com as rotas

app = Flask(__name__)
swagger = Swagger(app)  # Inicializa o Swagger

# Registra o Blueprint com prefixo /api
app.register_blueprint(api_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
