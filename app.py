from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from config import Config

# Configuração do Flask e Swagger
app = Flask(__name__)
app.config.from_object(Config)

# Inicializando o SQLAlchemy
db = SQLAlchemy(app)

# Definição do Modelo de Dados
class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=False)
    nota_segundo_semestre = db.Column(db.Float, nullable=False)
    professor = db.Column(db.String(255), nullable=False)
    sala = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return "Servidor Flask está funcionando!"

# Bloco de inicialização do banco de dados
with app.app_context():
    db.create_all()

# Rotas
@app.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.json
    aluno = Aluno(
        nome=data['nome'],
        idade=data['idade'],
        nota_primeiro_semestre=data['nota_primeiro_semestre'],
        nota_segundo_semestre=data['nota_segundo_semestre'],
        professor=data['professor'],
        sala=data['sala']
    )
    db.session.add(aluno)
    db.session.commit()
    return jsonify({'message': 'Aluno criado com sucesso!'}), 201

@app.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    return jsonify([{
        'id': aluno.id,
        'nome': aluno.nome,
        'idade': aluno.idade,
        'nota_primeiro_semestre': aluno.nota_primeiro_semestre,
        'nota_segundo_semestre': aluno.nota_segundo_semestre,
        'professor': aluno.professor,
        'sala': aluno.sala
    } for aluno in alunos])

@app.route('/alunos/<int:id>', methods=['GET'])
def get_aluno(id):
    aluno = Aluno.query.get(id)
    if aluno:
        return jsonify({
            'id': aluno.id,
            'nome': aluno.nome,
            'idade': aluno.idade,
            'nota_primeiro_semestre': aluno.nota_primeiro_semestre,
            'nota_segundo_semestre': aluno.nota_segundo_semestre,
            'professor': aluno.professor,
            'sala': aluno.sala
        })
    return jsonify({'message': 'Aluno não encontrado'}), 404

@app.route('/alunos/<int:id>', methods=['PUT'])
def update_aluno(id):
    data = request.json
    aluno = Aluno.query.get(id)
    if aluno:
        aluno.nome = data['nome']
        aluno.idade = data['idade']
        aluno.nota_primeiro_semestre = data['nota_primeiro_semestre']
        aluno.nota_segundo_semestre = data['nota_segundo_semestre']
        aluno.professor = data['professor']
        aluno.sala = data['sala']
        db.session.commit()
        return jsonify({'message': 'Aluno atualizado com sucesso!'})
    return jsonify({'message': 'Aluno não encontrado'}), 404

@app.route('/alunos/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    aluno = Aluno.query.get(id)
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno deletado com sucesso!'})
    return jsonify({'message': 'Aluno não encontrado'}), 404

# Configuração do Swagger UI
SWAGGER_URL = '/apidocs'
API_URL = '/static/apispec_1.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "API de Alunos"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)