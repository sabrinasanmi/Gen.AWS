from app import db

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float)
    nota_segundo_semestre = db.Column(db.Float)
    professor = db.Column(db.String(100))
    sala = db.Column(db.String(50))

    def __init__(self, nome, idade, nota_primeiro_semestre, nota_segundo_semestre, professor, sala):
        self.nome = nome
        self.idade = idade
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.professor = professor
        self.sala = sala