from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify, abort
from dao import JogoDao, UsuarioDao
from models import Jogo, Usuario
import pymysql
import json


app = Flask(__name__)
app.secret_key = 'Fabio' #essa linha é necessária para se trabalhar com Sessao
#configuracoes para a conexao com o banco

db = pymysql.connect(user='root', passwd='mysql', host='127.0.0.1', port=3306)
jogo_dao = JogoDao(db)

usuario_dao = UsuarioDao(db)

#jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
#jogo2 = Jogo('Pokemon Gold', 'RPG', 'GBA')
#lista = [jogo1, jogo2]


@app.route('/')
@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo="U'Follower Web", jogos=lista)

@app.route('/novo')
def novo():
#url_for linka para o recurso apenas informando o nome da funcao
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return  redirect(url_for('login', proxima = url_for('novo')))#novo é o caminho a seguir depois que eu fizer o login
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])#observar que essa lista tem uma virgula no final
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    #lista.append(jogo)#adicionando o jogo na lista
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = request.form['usuario']
            flash('Bem-Vindo {}!'.format(usuario.nome))
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário ou senha incorretos.')
        return redirect(url_for('login'))



@app.route('/editar/<int:id>')
def editar(id):
#url_for linka para o recurso apenas informando o nome da funcao
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return  redirect(url_for('login', proxima = url_for('editar')))#novo é o caminho a seguir depois que eu fizer o login
    jogo = jogo_dao.busca_por_id(id)
    return render_template('editar.html', titulo='Editar Jogo', jogo=jogo)


@app.route('/atualizar', methods=['POST',])#observar que essa lista tem uma virgula no final
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request. form['console']
    jogo = Jogo(nome, categoria, console, id=request.form['id'])
    #lista.append(jogo)#adicionando o jogo na lista
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))


@app.route('/logout')
def logout(id):
    session['usuario_logado']=None
    flash('Usuário deslogado.')
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    jogo = jogo_dao.busca_por_id(id)
    jogo_nome = jogo.nome
    jogo_dao.deletar(id)
    flash('O jogo {} foi deletado com sucesso!'.format(jogo_nome))
    return redirect(url_for('index'))



tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})




app.run(debug=True)#debug=True é um mode de dev onde não precisa ficar dando reload a toda hora
