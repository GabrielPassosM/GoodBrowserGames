from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField, DateField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import User


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

    categoria = SelectField("Categoria", choices=opcoes_de_categorias)
    submit = SubmitField("Buscar")