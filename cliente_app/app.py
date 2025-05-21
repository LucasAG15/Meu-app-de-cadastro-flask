from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_esta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# configuraçao do usuario

USERNAME = 'Lucas_Alves_Gon'
PASSWORD_HASH = generate_password_hash('Meus!Clientes')

# Modelo do cliente, essa é a classe que constroi a tabela


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    servico = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    manutencao = db.Column(db.Boolean, default=False)


# banco de dados
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def entrar():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
            session['logged_in'] = True
            return redirect(url_for('principal'))
        else:
            flash('Usuário ou senha incorretos!', 'error')

    return render_template('login.html')


@app.route('/principal', methods=['GET', 'POST'])
def principal():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        servico = request.form['servico']
        valor = float(request.form['valor'])
        manutencao = True if request.form.get('manutencao') == 'on' else False

        novo_cliente = Cliente(nome=nome, servico=servico,
                               valor=valor, manutencao=manutencao)
        db.session.add(novo_cliente)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!', 'success')

    clientes = Cliente.query.all()
    return render_template('principal.html', clientes=clientes)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('principal.html.'))


if __name__ == '__main__':
    app.run(debug=True)
