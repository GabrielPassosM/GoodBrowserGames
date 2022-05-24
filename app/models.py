from datetime import datetime
from app import db


class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), index=True, )
    categoria = db.Column(db.String(64), index=True)
    url_jogo = db.Column(db.String, index=True)
    url_video = db.Column(db.String, index=True)
    url_imagem = db.Column(db.String, index=True)
    descricao = db.Column(db.String, index=True)
    
    def __repr__(self) -> str:
        return f"<Jogo {self.nome}>"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    senha_hash = db.Column(db.String(128))
    nome_completo = db.Column(db.String(120), index=True)
    data_de_nascimento = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    estado = db.Column(db.String(64), index=True)
    pais = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Avaliacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estrelas = db.Column(db.Float, index=True)
    texto = db.Column(db.String(255))
    qnt_util = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    jogo_id = db.Column(db.Integer, db.ForeignKey('jogo.id'))
