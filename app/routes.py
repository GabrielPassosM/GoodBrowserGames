from flask import render_template, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask.helpers import url_for
from app import app, db
from app.forms import CadastroJogoForm, CriarCategoria, FazerAvaliacao, FiltrarPorNomeForm, FiltrarPorCategoriaForm, LoginForm, RegistrationForm
from app.models import Avaliacao, Categoria, Jogo, JogoAvaliado, User, VotoUtil
import operator


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


@app.route("/listar-categorias", methods=["GET", "POST"])
def listar_categorias():
    categorias_base = [
        "Strategy", 
        "Shooter",
        "Puzzle",
        "Arcade",
        "RPG",
        "Sports",
        "Action",
        "Adventure",
    ]

    categorias = list(Categoria.query.all())

    return render_template("lista_categorias.html", categorias=categorias, padroes=categorias_base)



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
        return redirect(url_for("listar_categorias"))
    return render_template("criar_categoria.html", form=form)


@app.route("/editar-categoria/<id>", methods=["GET", "POST"])
def editar_categoria(id):
    categoria = Categoria.query.filter_by(id=id).first_or_404()
    nome_antigo = categoria.nome
    form = CriarCategoria()
    if request.method == "POST":
        novo_nome = form.nome.data
        categoria.nome = novo_nome
        db.session.add(categoria)

        jogos_dessa_cat = list(Jogo.query.filter_by(categoria=nome_antigo))
        if jogos_dessa_cat:
            for jogo in jogos_dessa_cat:
                jogo.categoria = novo_nome
                db.session.add(jogo)
        
        db.session.commit()
        flash(f"Categoria {nome_antigo} editada para {novo_nome} com sucesso!")
        return redirect(url_for("listar_categorias"))

    return render_template("edicao_categoria.html", form=form, nome_antigo=nome_antigo)


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


@app.route("/listar-avaliacoes/<id>", methods=["GET", "POST"])
def listar_avaliacoes(id):
    avaliacoes = list(Avaliacao.query.filter_by(jogo_id=id))
    jogo = Jogo.query.filter_by(id=id).first()

    ids_avaliacoes_uteis_usuario = None
    if avaliacoes:
        avaliacoes_ids = [a.id for a in avaliacoes]
        user_id_expression = VotoUtil.user_id.in_([current_user.id])
        in_expression = VotoUtil.avaliacao_id.in_(avaliacoes_ids)
        votos_util_usuario = list(VotoUtil.query.filter(user_id_expression, in_expression))
        ids_avaliacoes_uteis_usuario = [v.avaliacao_id for v in votos_util_usuario]
    
    avaliacao_pelo_usuario = Avaliacao.query.filter_by(jogo_id=id, user_id=current_user.id).first()
    if avaliacao_pelo_usuario:
        avaliacao_feita = avaliacao_pelo_usuario
    else:
        avaliacao_feita = None

    return render_template("lista_avaliacoes.html", avaliacoes=avaliacoes, jogo=jogo, avaliacao_feita=avaliacao_feita, avals_uteis_ids=ids_avaliacoes_uteis_usuario)


@app.route("/fazer-avaliacao/<jogo_id>", methods=["GET", "POST"])
def fazer_avaliacao(jogo_id):
    form = FazerAvaliacao()
    jogo = Jogo.query.filter_by(id=jogo_id).first()
    if request.method == "POST":
        texto = form.texto.data
        estrelas = form.estrelas.data
        user_id = current_user.id

        avaliacao = Avaliacao(
            texto=texto,
            estrelas=estrelas,
            user_id=user_id,
            jogo_id=jogo_id
        )

        jogo_avaliado = JogoAvaliado(
            user_id=user_id,
            jogo_id=jogo_id
        )

        db.session.add(avaliacao)
        db.session.add(jogo_avaliado)
        db.session.commit()
        flash(f"Avaliação feita com sucesso!")
        return redirect(url_for("listar_avaliacoes", id=jogo_id))
    return render_template("fazer_avaliacao.html", form=form, jogo=jogo)


@app.route("/editar-avaliacao/<id>/", methods=["GET", "POST"])
def editar_avaliacao(id):
    avaliacao = Avaliacao.query.filter_by(id=id).first_or_404()
    jogo = Jogo.query.filter_by(id=avaliacao.jogo_id).first()
    form = FazerAvaliacao()
    if request.method == "POST":
        avaliacao.estrelas = form.estrelas.data
        avaliacao.texto = form.texto.data
        
        db.session.add(avaliacao)
        db.session.commit()
        flash(f"Avaliação editada com sucesso!")
        return redirect(url_for("listar_avaliacoes", id=jogo.id))

    return render_template("edicao_avaliacao.html", form=form, nome_jogo=jogo.nome)


@app.route("/achar-util/<aval_id>/<page>", methods=["GET", "POST"])
def achar_util(aval_id, page):
    avaliacao = Avaliacao.query.filter_by(id=aval_id).first()
    avaliacao.qnt_util += 1

    util = VotoUtil(
        user_id=current_user.id,
        avaliacao_id=aval_id
    )

    db.session.add(avaliacao)
    db.session.add(util)
    db.session.commit()
    if page == "1":
        return redirect(url_for("listar_avaliacoes", id=avaliacao.jogo_id))
    else:
        return redirect(url_for("avaliacoes_mais_uteis"))


@app.route("/tirar-util/<aval_id>/<page>", methods=["GET", "POST"])
def tirar_util(aval_id, page):
    avaliacao = Avaliacao.query.filter_by(id=aval_id).first()
    avaliacao.qnt_util -= 1

    util = VotoUtil.query.filter_by(avaliacao_id=aval_id, user_id=current_user.id).first()

    db.session.add(avaliacao)
    db.session.delete(util)
    db.session.commit()
    
    if page == "1":
        return redirect(url_for("listar_avaliacoes", id=avaliacao.jogo_id))
    else:
        return redirect(url_for("avaliacoes_mais_uteis"))


@app.route("/avaliacoes-mais-uteis", methods=["GET", "POST"])
def avaliacoes_mais_uteis():
    avaliacoes = list(Avaliacao.query.order_by(Avaliacao.qnt_util.desc()))

    avals_e_jogos = {}
    ids_avaliacoes_uteis_usuario = None
    if avaliacoes:
        avaliacoes_ids = [a.id for a in avaliacoes]
        user_id_expression = VotoUtil.user_id.in_([current_user.id])
        in_expression = VotoUtil.avaliacao_id.in_(avaliacoes_ids)
        votos_util_usuario = list(VotoUtil.query.filter(user_id_expression, in_expression))
        ids_avaliacoes_uteis_usuario = [v.avaliacao_id for v in votos_util_usuario]

        for aval in avaliacoes:
            jogo = Jogo.query.filter_by(id=aval.jogo_id).first()
            avals_e_jogos[aval] = jogo.nome


    return render_template("avaliacoes_mais_uteis.html", avals_e_jogos=avals_e_jogos, avals_uteis_ids=ids_avaliacoes_uteis_usuario)


@app.route("/recomendacoes", methods=["GET", "POST"])
def recomendacoes():
    jogos_avaliados = list(JogoAvaliado.query.filter_by(user_id=current_user.id))
    ids_jogos_avaliados = [j.jogo_id for j in jogos_avaliados]

    jogos_recomendados = []
    categorias_avaliadas = {}
    if jogos_avaliados:
        # try:
        for jogo_avaliado in jogos_avaliados:
            jogo = Jogo.query.filter_by(id=jogo_avaliado.jogo_id).first()
            cat = jogo.categoria
            qnt_avaliacoes = categorias_avaliadas.get(cat, None)
            if qnt_avaliacoes:
                qnt_avaliacoes += 1
                categorias_avaliadas[cat] = qnt_avaliacoes
            else:
                categorias_avaliadas[cat] = 1
        
        categoria_preferida = max(categorias_avaliadas.items(), key=operator.itemgetter(1))[0]
        todos_jogos_cat_preferida = list(Jogo.query.filter_by(categoria=categoria_preferida))
        for jogo in todos_jogos_cat_preferida:
            if jogo.id not in ids_jogos_avaliados:
                jogos_recomendados.append(jogo)
        # except:
            # pass
    
    return render_template("recomendacoes.html", jogos_recomendados=jogos_recomendados)
