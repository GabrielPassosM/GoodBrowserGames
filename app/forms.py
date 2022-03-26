from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class CadastroJogoForm(FlaskForm):
    opcoes_de_categorias = [
        ("strategy", "Strategy"), 
        ("shooter", "Shooter"),
        ("puzzle", "Puzzle"),
        ("arcade", "Arcade"),
        ("rpg", "RPG"),
        ("sports", "Sports"),
        ("action", "Action"),
        ("adventure", "Adventure"),
    ]

    nome = StringField("Nome do jogo", validators=[DataRequired()])
    categoria = SelectField("Categoria", choices=opcoes_de_categorias, validators=[DataRequired()])
    url_jogo = StringField("URL do jogo", validators=[DataRequired()])
    url_video = StringField("URL vídeo demonstrativo")
    descricao = StringField("Descrição", validators=[DataRequired()])
    url_imagem = StringField("URL de imagem ilustrativa", validators=[DataRequired()])
    submit = SubmitField("Cadastrar")