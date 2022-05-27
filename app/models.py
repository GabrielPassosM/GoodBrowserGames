from email.policy import default
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db, login


class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), index=True, )
    categoria = db.Column(db.String(64), index=True)
    url_jogo = db.Column(db.String, index=True)
    url_video = db.Column(db.String, index=True)
    url_imagem = db.Column(db.String, index=True)
    descricao = db.Column(db.String, index=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    senha_hash = db.Column(db.String(128))
    nome_completo = db.Column(db.String(120), index=True)
    data_de_nascimento = db.Column(db.Date, index=True, default=datetime.utcnow)
    estado = db.Column(db.String(64), index=True)
    pais = db.Column(db.String(64), index=True)

    def set_password(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)


class Avaliacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estrelas = db.Column(db.Float, index=True)
    texto = db.Column(db.String(255))
    qnt_util = db.Column(db.Integer, index=True, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    jogo_id = db.Column(db.Integer, db.ForeignKey('jogo.id'))


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True, unique=True)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))