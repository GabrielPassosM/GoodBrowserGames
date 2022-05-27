from sre_constants import CATEGORY_DIGIT
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField, DateField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Categoria, User


class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')


class RegistrationForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    nome_completo = StringField('Nome completo', validators=[DataRequired()])
    data_de_nascimento = DateField('Data de nascimento', validators=[DataRequired()])
    pais = StringField('País', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    senha2 = PasswordField(
        'Repita a senha', validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Nome de usuário já existente')


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

    categorias = list(Categoria.query.all())

    if categorias:
        for cat in categorias:
            opcoes_de_categorias.append((cat.nome, cat.nome.capitalize()))

    nome = StringField("Nome do jogo", validators=[DataRequired()])
    categoria = SelectField("Categoria", choices=opcoes_de_categorias, validators=[DataRequired()])
    url_jogo = StringField("URL do jogo", validators=[DataRequired()])
    url_video = StringField("URL vídeo demonstrativo")
    descricao = StringField("Descrição", validators=[DataRequired()])
    url_imagem = StringField("URL de imagem ilustrativa", validators=[DataRequired()])
    submit = SubmitField("Salvar")


class FiltrarPorNomeForm(FlaskForm):
    nome = StringField("Nome do jogo")
    submit = SubmitField("Buscar")


class FiltrarPorCategoriaForm(FlaskForm):
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

    categorias = list(Categoria.query.all())

    if categorias:
        for cat in categorias:
            opcoes_de_categorias.append((cat.nome, cat.nome.capitalize()))

    categoria = SelectField("Categoria", choices=opcoes_de_categorias)
    submit = SubmitField("Buscar")


class CriarCategoria(FlaskForm):
    nome = StringField("Nome da categoria", validators=[DataRequired()])
    submit = SubmitField("Salvar")

    def validate_categoria(self, nome):
        cat = Categoria.query.filter_by(nome=nome.data.lower()).first()
        if cat is not None:
            raise ValidationError('Categoria já existente!')


class FazerAvaliacao(FlaskForm):
    opcoes_de_estrelas = [
        (1, "1"), 
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    ]

    estrelas = SelectField("Estrelas", choices=opcoes_de_estrelas, validators=[DataRequired()])
    texto = StringField("Texto:", validators=[DataRequired()])
    submit = SubmitField("Salvar")
