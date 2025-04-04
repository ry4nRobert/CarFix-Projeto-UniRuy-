from flask import Flask, render_template, request, flash, redirect, session, jsonify











app = Flask(__name__)
app.config['SECRET_KEY'] = 'joaopedro'


@app.route("/")
def login():
    return render_template('teste.html')


@app.route("/acesso", methods=['POST'] )
def acesso():
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    if email == 'joaobatatinha123@gmail.com' and senha == '123':
        return render_template('home.html')
    else:
        flash('Email e/ou senha inválidos, tente novamente!')
        return redirect('/')
    
    
    print(email)
    print(senha)
    
    return redirect('/')














if __name__ in '__main__':
        app.run(debug=True)