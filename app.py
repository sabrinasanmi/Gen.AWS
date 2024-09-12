from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import os
from config import Config  # Adicione esta linha para importar a configuração

# Configuração do Flask e Swagger
app = Flask(__name__)
app.config.from_object(Config)  # Atualize esta linha para usar a configuração do config.py
Swagger(app)

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

# Rotas
@app.route('/alunos', methods=['POST'])
def create_aluno():
    """
    Criar um novo aluno
    ---
    parameters:
      - name: aluno
        in: body
        required: true
        schema:
          id: Aluno
          required:
            - nome
            - idade
            - nota_primeiro_semestre
            - nota_segundo_semestre
            - professor
            - sala
          properties:
            nome:
              type: string
              description: Nome do aluno
            idade:
              type: integer
              description: Idade do aluno
            nota_primeiro_semestre:
              type: number
              format: float
              description: Nota do primeiro semestre
            nota_segundo_semestre:
              type: number
              format: float
              description: Nota do segundo semestre
            professor:
              type: string
              description: Nome do professor
            sala:
              type: string
              description: Número da sala
    responses:
      201:
        description: Aluno criado com sucesso
    """
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
    """
    Listar todos os alunos
    ---
    responses:
      200:
        description: Lista de alunos
        schema:
          type: array
          items:
            $ref: '#/definitions/Aluno'
    """
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
    """
    Obter um aluno por ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do aluno
    responses:
      200:
        description: Detalhes do aluno
        schema:
          $ref: '#/definitions/Aluno'
      404:
        description: Aluno não encontrado
    """
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
    """
    Atualizar um aluno por ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do aluno
      - name: aluno
        in: body
        required: true
        schema:
          id: Aluno
          required:
            - nome
            - idade
            - nota_primeiro_semestre
            - nota_segundo_semestre
            - professor
            - sala
          properties:
            nome:
              type: string
              description: Nome do aluno
            idade:
              type: integer
              description: Idade do aluno
            nota_primeiro_semestre:
              type: number
              format: float
              description: Nota do primeiro semestre
            nota_segundo_semestre:
              type: number
              format: float
              description: Nota do segundo semestre
            professor:
              type: string
              description: Nome do professor
            sala:
              type: string
              description: Número da sala
    responses:
      200:
        description: Aluno atualizado com sucesso
      404:
        description: Aluno não encontrado
    """
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
    """
    Deletar um aluno por ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do aluno
    responses:
      200:
        description: Aluno deletado com sucesso
      404:
        description: Aluno não encontrado
    """
    aluno = Aluno.query.get(id)
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno deletado com sucesso!'})
    return jsonify({'message': 'Aluno não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)