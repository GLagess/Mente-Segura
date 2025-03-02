from flask import Flask
from flasgger import Swagger
from api.routes import api_bp  # Importa as rotas definidas

app = Flask(__name__)
swagger = Swagger(app)  # Inicializa a documentação Swagger

# Registra as rotas da API
app.register_blueprint(api_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
