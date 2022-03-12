from flask import render_template, request, redirect, session
from _app.models.usuario import Usuario
from _app import app
from flask import flash

from  flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/dashboard")
def result():
    if 'idUsuario' in session:
        data = {"id": int(session['idUsuario'])}
    else:
        return redirect('/')

    usuario = Usuario.get_usuario(data)
    return render_template('dashboard.html', usuario = usuario)

@app.route('/create_usuario', methods=["POST"])
def usuarioNew():
    if not Usuario.validate_user(request.form):
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pwd
    }

    email = Usuario.search_email(data)
    if not Usuario.is_exists_email(email):
        return redirect('/')

    Usuario.save(data)
    idUsuario = Usuario.search_id(data)
    session['idUsuario'] = idUsuario
    return redirect('/dashboard')

@app.route('/ingresar_usuario', methods=["POST"])
def usuarioShow():
    if not Usuario.validate_user_login(request.form):
        return redirect('/')

    data = {"email": request.form["email"]}
    email = Usuario.search_email(data)

    if not Usuario.exists_email(email):
        return redirect('/')
    else:
        password = Usuario.search_password(data)
        if not bcrypt.check_password_hash(password,request.form["password"]):
            flash("Wrong Password", 'login')
            return redirect('/')

    idUsuario = Usuario.search_id(data)
    session['idUsuario'] = idUsuario
    return redirect('/dashboard')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')