from weakref import ref
from flask import Flask, render_template, request, flash, redirect, session, jsonify, g
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'joaopedro'
app.config['DATABASE'] = 'usuarios.db'

#Metelancia De Dados(CUIDADO!)
def get_db():
     if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory=sqlite3.Row
     return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def create_table():
    db = get_db()
    db.execute('''
         CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            tema TEXT DEFAULT '#3b5998',
            img_perfil TEXT DEFAULT '/static/imagens/user.png',
            img_capa TEXT DEFAULT '/static/imagens/fundo.jpg',
            email TEXT NOT NULL
        );

''')
    ''
    db.commit()

with app.app_context():
    create_table()



@app.route("/")
def login():
    return render_template('login.html')


@app.route("/acesso", methods=['POST'] )
def acesso():
    nome = request.form.get('email')
    senha = request.form.get('senha')


    db = get_db()
    usuario = db.execute('SELECT * FROM usuario WHERE(nome = ? OR email = ?) AND senha = ?', (nome,nome,senha)).fetchone() 


    if usuario:
        session['id'] = usuario ['id']
        return redirect('/home')
    else:
        flash('nome e/ou senha invalidos , tente novamente!!')

        return redirect('/')
    
@app.route("/cadastro")
def cadastro():
     return render_template('cadastro.html')

@app.route("/cadastrando" , methods=['POST'])
def cadastrando():
    nome = request.form.get('nome') 
    senha = request.form.get('senha') 
    email = request.form.get('email') 
    tema = '#3b5998'
    img_capa = '/static/imagens/Fundo.png'
    img_perfil = '/static/imagens/user.png'

    db = get_db()
    cursor = db.execute(''' 
            INSERT INTO usuario (nome, senha, tema, img_perfil, img_capa, email) VALUES (?, ?, ?, ?, ?, ?)
''', (nome, senha, tema, img_perfil, img_capa, email))
    
    db.commit()

    flash(f'seja bem vindo, {nome}!!')
    session['id'] = cursor.lastrowid
    return redirect('/home')


@app.route("/esqueci")
def esqueci():
     return render_template('esqueci.html')



@app.route('/home')
def home():
    if 'id' in session:
        id_usuario = session ['id']
        db = get_db()
        usuario = db.execute('SELECT * FROM usuario WHERE id = ?', (id_usuario,)).fetchone()
        nome = usuario ['nome']
        if usuario:
            nome = usuario ['nome']
            tema = usuario ['tema']
            img_capa = usuario ['img_capa']
            img_perfil = usuario ['img_perfil']
            return render_template('home.html', nome=nome, tema=tema, img_capa=img_capa, img_perfil=img_perfil )
        else:
            flash ('usuario não encontrado...')
            return redirect ('/')
        
    else:

        return redirect ('/')




if __name__ in '__main__':
        app.run(debug=True)