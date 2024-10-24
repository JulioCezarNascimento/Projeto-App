from flask import Flask, render_template, redirect, url_for, flash
from forms import LoginForm, RegisterForm
from models import db, User
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
Bootstrap(app)

# Inicializar o banco de dados (para criar as tabelas)
with app.app_context():
    db.create_all()

# Rota para o login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            flash(f'Logged in successfully as {form.username.data}', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

# Rota para o cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists!', 'danger')
        else:
            # Criar um novo usuário e salvar no banco de dados
            new_user = User(username=form.username.data, age=form.age.data)
            new_user.set_password(form.password.data)  # Armazena o hash da senha
            db.session.add(new_user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Rota para a página inicial
@app.route('/')
def home():
    return 'Home Page'

if __name__ == '__main__':
    app.run(debug=True)
