from flask import render_template, flash, redirect, request
from flask.helpers import url_for
from app import app, db
from app.forms import CadastroJogoForm
from app.models import Jogo


@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    jogos = Jogo.query.all()
    return render_template("index.html", jogos=jogos)


@app.route("/cadastrar-jogo", methods=["GET", "POST"])
def cadastrar_jogo():
    form = CadastroJogoForm()
    if request.method == "POST":
        nome = form.nome.data
        categoria = form.categoria.data
        url_jogo = form.url_jogo.data
        url_video = form.url_video.data
        url_imagem = form.url_imagem.data
        descricao = form.descricao.data

        jogo = Jogo(
            nome=nome,
            categoria=categoria,
            url_jogo=url_jogo,
            url_video=url_video,
            url_imagem=url_imagem,
            descricao=descricao
        )
        db.session.add(jogo)
        db.session.commit()
        flash(f"Jogo {nome} cadastrado!")
        return redirect(url_for("index"))
    return render_template("cadastro_jogo.html", form=form)
