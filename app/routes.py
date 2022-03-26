from flask import render_template, flash, redirect
from flask.helpers import url_for
from werkzeug.exceptions import MethodNotAllowed
from app import app
from app.forms import CadastroJogoForm


@app.route("/")
@app.route("/index")
def index():
    jogos = [
        {
            "nome": "Teste",
            "categoria": "RPG",
            "url_jogo": "www.teste.com",
            "url_video": "www.yotube.com"
        },
        {
            "nome": "Teste 2",
            "categoria": "RPG",
            "url_jogo": "www.teste.com",
            "url_video": "www.yotube.com"
        }
    ]
    return render_template("index.html", jogos=jogos)


@app.route("/cadastrar-jogo", methods=["GET", "POST"])
def cadastrar_jogo():
    form = CadastroJogoForm()
    if form.validate_on_submit():
        flash(f"Jogo {form.nome.data} cadastrado!")
        return redirect(url_for("cadastrar_jogo"))
    return render_template("cadastro_jogo.html", form=form)
