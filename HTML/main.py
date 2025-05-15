from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask_socketio import SocketIO, send
import phonenumbers
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'joaopedro'
app.config['DATABASE'] = 'usuarios.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

socketio = SocketIO(app)


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Banco de dados
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db:
        db.close()

def create_table():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tema TEXT DEFAULT '#3b5998',
            img_perfil TEXT DEFAULT '/static/imagens/icon2.png',
            img_capa TEXT DEFAULT '/static/imagens/fundo.jpg',
            email TEXT NOT NULL UNIQUE,
            celular TEXT UNIQUE
        );
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            mensagem TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuario (id)
        );
    ''')
    db.commit()

with app.app_context():
    create_table()

# Validação de celular
def celular_valido(numero, pais='BR'):
    try:
        parsed = phonenumbers.parse(numero, pais)
        return phonenumbers.is_valid_number(parsed) and phonenumbers.number_type(parsed) == phonenumbers.PhoneNumberType.MOBILE
    except:
        return False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Rotas
@app.route("/")
def login():
    return render_template('login.html')

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/acesso", methods=['POST'])
def acesso():
    nome = request.form.get('email')
    senha = request.form.get('senha')

    db = get_db()
    usuario = db.execute('SELECT * FROM usuario WHERE nome = ? OR email = ?', (nome, nome)).fetchone()

    if usuario and check_password_hash(usuario['senha'], senha):
        session['id'] = usuario['id']
        return redirect('/home')
    else:
        flash('Nome de usuário ou senha incorretos, tente novamente!!')
        return redirect('/')

@app.route("/cadastrando", methods=['POST'])
def cadastrando():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    email = request.form.get('email')
    celular = request.form.get('celular')

    tema = '#3b5998'
    img_capa = '/static/imagens/Fundo.png'
    img_perfil = '/static/imagens/user.png'

    if not celular_valido(celular):
        flash('Número de celular inválido. Use o formato com DDD, ex: (11) 91234-5678.')
        return redirect('/cadastro')

    parsed = phonenumbers.parse(celular, 'BR')
    celular_formatado = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)

    db = get_db()
    existente = db.execute('SELECT * FROM usuario WHERE email = ? OR celular = ? OR nome = ?', (email, celular_formatado, nome)).fetchone()
    if existente:
        if existente['email'] == email:
            flash('Este e-mail já está em uso.')
        elif existente['celular'] == celular_formatado:
            flash('Este número de celular já está em uso.')
        elif existente['nome'] == nome:
            flash('Este nome de usuario já está em uso.')
        return redirect('/cadastro')

    senha_hash = generate_password_hash(senha)

    cursor = db.execute('''
        INSERT INTO usuario (nome, senha, tema, img_perfil, img_capa, email, celular)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, senha_hash, tema, img_perfil, img_capa, email, celular_formatado))
    db.commit()

    flash(f'Seja bem-vindo, {nome}!!')
    session['id'] = cursor.lastrowid
    return redirect('/home')

@app.route("/home")
def home():
    if 'id' in session:
        db = get_db()
        usuario = db.execute('SELECT * FROM usuario WHERE id = ?', (session['id'],)).fetchone()
        if usuario:
            return render_template('home.html',
                                   nome=usuario['nome'],
                                   tema=usuario['tema'],
                                   img_capa=usuario['img_capa'],
                                   img_perfil=usuario['img_perfil'])
        else:
            flash('Usuário não encontrado...')
    return redirect('/')

@app.route("/perfil")
def perfil():
    if 'id' in session:
        db = get_db()
        usuario = db.execute('SELECT * FROM usuario WHERE id = ?', (session['id'],)).fetchone()
        if usuario:
            return render_template('perfil.html',
                                   nome=usuario['nome'],
                                   email=usuario['email'],
                                   img_perfil=usuario['img_perfil'],
                                   celular=usuario['celular'])
        else:
            flash("Usuário não encontrado.")
            return redirect('/')
    flash("Você precisa estar logado.")
    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'foto_perfil' not in request.files:
        flash('Nenhuma imagem foi enviada.')
        return redirect('/perfil')

    file = request.files['foto_perfil']

    if file.filename == '' or not allowed_file(file.filename):
        flash('Nome de arquivo inválido ou tipo não permitido.')
        return redirect('/perfil')

    filename = secure_filename(f"perfil_{session['id']}_{file.filename}")
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(caminho)

    db = get_db()
    db.execute('UPDATE usuario SET img_perfil = ? WHERE id = ?', (f'/static/uploads/{filename}', session['id']))
    db.commit()

    flash('Foto de perfil atualizada com sucesso!')
    return redirect('/perfil')

@app.route("/fotos")
def fotos():
    return render_template('fotos.html')

@app.route("/chat")
def chat():
    if 'id' in session:
        db = get_db()
        usuario = db.execute('SELECT * FROM usuario WHERE id = ?', (session['id'],)).fetchone()
        mensagens = db.execute('''
            SELECT m.mensagem, u.nome, m.timestamp 
            FROM mensagens m 
            JOIN usuario u ON m.usuario_id = u.id 
            ORDER BY m.timestamp ASC
        ''').fetchall()
        return render_template("chat.html", nome_usuario=usuario['nome'], mensagens=mensagens)
    return redirect('/')

@socketio.on('message')
def handle_message(msg):
    print(f'Mensagem recebida: {msg}')
    usuario_id = session.get('id')

    if usuario_id:
        msg_text = msg['text']
        db = get_db()
        db.execute('INSERT INTO mensagens (usuario_id, mensagem) VALUES (?, ?)', (usuario_id, msg_text))
        db.commit()
        usuario = db.execute('SELECT nome FROM usuario WHERE id = ?', (usuario_id,)).fetchone()
        send(f'{usuario["nome"]}: {msg_text}', broadcast=True)
    else:
        print("Usuário não autenticado para enviar mensagem.")

@app.route("/configuracoes")
def configuracoes():
    return render_template('configuracoes.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/esquecer", methods=["GET", "POST"])
def esquecer():
    if request.method == "POST":
        email = request.form.get('email')
        flash('Se o email estiver cadastrado, enviaremos as instruções para alterar a senha.')
        return redirect(url_for('esquecer'))
    return render_template('esquecer.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
