from app import db


class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), index=True, unique=True)
    categoria = db.Column(db.String(64), index=True)
    url_jogo = db.Column(db.String, index=True, unique=True)
    url_video = db.Column(db.String, index=True, unique=True)
    url_imagem = db.Column(db.String, index=True, unique=True)
    descricao = db.Column(db.String, index=True, unique=True)
    
    def __repr__(self) -> str:
        return f"<Jogo {self.nome}>"
