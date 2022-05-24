from flask import render_template, flash, redirect, request
from flask.helpers import url_for
from app import app, db
from app.forms import CadastroJogoForm, FiltrarPorNomeForm, FiltrarPorCategoriaForm, LoginForm
from app.models import Jogo


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    jogos = Jogo.query.all()
    form_nome = FiltrarPorNomeForm()
    form_cat = FiltrarPorCategoriaForm()
    if request.method == "POST":
        nome = form_nome.nome.data
        categoria = form_cat.categoria.data
        if nome:
            jogos_filtrados = Jogo.query.filter_by(nome=nome)
        elif categoria:
            jogos_filtrados = Jogo.query.filter_by(categoria=categoria)
        
        if jogos_filtrados:
            jogos = jogos_filtrados

    return render_template("index.html", form_nome=form_nome, form_cat=form_cat, jogos=jogos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login feito por usuário {}'.format(form.username.data))
        return redirect('/index')
    return render_template('login.html', title='Entrar', form=form)


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
        flash(f"Jogo {nome} cadastrado com sucesso!")
        return redirect(url_for("index"))
    return render_template("cadastro_jogo.html", form=form)


@app.route("/delete-jogo/<id>")
def delete_jogo(id):
    jogo = Jogo.query.filter_by(id=id).first_or_404()
    nome = jogo.nome
    db.session.delete(jogo)
    db.session.commit()
    flash(f"Jogo {nome} deletado com sucesso!")
    return redirect(url_for("index"))


@app.route("/editar-jogo/<id>", methods=["GET", "POST"])
def editar_jogo(id):
    jogo = Jogo.query.filter_by(id=id).first_or_404()
    nome = jogo.nome
    form = CadastroJogoForm()
    if request.method == "POST":
        jogo.categoria = form.categoria.data
        jogo.url_jogo = form.url_jogo.data
        jogo.url_video = form.url_video.data
        jogo.url_imagem = form.url_imagem.data
        jogo.descricao = form.descricao.data
        
        db.session.add(jogo)
        db.session.commit()
        flash(f"Jogo {nome} editado com sucesso!")
        return redirect(url_for("index"))

    return render_template("edicao_jogo.html", form=form, nome_jogo=jogo.nome)
