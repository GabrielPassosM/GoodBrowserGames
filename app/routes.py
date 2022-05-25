from flask import render_template, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask.helpers import url_for
from app import app, db
from app.forms import CadastroJogoForm, CriarCategoria, FiltrarPorNomeForm, FiltrarPorCategoriaForm, LoginForm, RegistrationForm
from app.models import Categoria, Jogo, User


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.senha.data):
            flash('Usuário ou senha inválido!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Login feito por usuário {}'.format(form.username.data))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Entrar', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            nome_completo=form.nome_completo.data,
            data_de_nascimento=form.data_de_nascimento.data,
            pais=form.pais.data,
            estado=form.estado.data
        )
        user.set_password(form.senha.data)
        db.session.add(user)
        db.session.commit()
        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('login'))
    return render_template('cadastre_se.html', title='Cadastre-se', form=form)


@app.route("/criar-categoria", methods=["GET", "POST"])
def criar_categoria():
    form = CriarCategoria()
    if request.method == "POST":
        nome = form.nome.data.lower()

        categoria = Categoria(
            nome=nome
        )
        db.session.add(categoria)
        db.session.commit()
        flash(f"Categoria {nome} cadastrada com sucesso!")
        return redirect(url_for("index"))
    return render_template("criar_categoria.html", form=form)


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
