from flask import Flask, render_template, request, redirect, session
import psycopg2
import bcrypt

app = Flask(__name__)
app.secret_key = 'chave_super_secreta'

# Conexão com o PostgreSQL
def conectar_bd():
    return psycopg2.connect(
        host="localhost",
        database="notton_db",
        user="postgres",
        password="1234"
    )

# Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        hash_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        conn = conectar_bd()
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, hash_senha))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/login')
    return render_template('register.html')

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = conectar_bd()
        cur = conn.cursor()
        cur.execute("SELECT senha FROM usuarios WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and bcrypt.checkpw(senha.encode('utf-8'), user[0].encode('utf-8')):
            session['user'] = email
            return redirect('/')
        else:
            return "Login ou senha incorretos"

    return render_template('login.html')

# Página inicial após login
@app.route('/')
def index():
    if 'user' in session:
        return f'Bem-vindo, {session["user"]}!'
    return redirect('/login')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
