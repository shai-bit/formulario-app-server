from sqlalchemy import text
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:boguetos@10.0.0.4/usuarios'
app.config['SECRET_KEY'] = '2002'
db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    contraseña = db.Column(db.String(120), nullable=False)


@app.route('/')
def index():
    return send_from_directory('/var/www/html/formulario-app-server/src', 'index.html')

@app.route('/home')
def home():
    return send_from_directory('/var/www/html/formulario-app-server/src', 'home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']

        # Preparar la consulta SQL. Utiliza parámetros con nombre para evitar la inyección de SQL.
        query = text("SELECT * FROM usuarios WHERE nombre_usuario = :username AND contraseña = crypt(:password, contraseña)")

        # Obtener una conexión a través del motor
        connection = db.engine.connect()

        try:
            # Ejecutar la consulta con los parámetros del usuario
            # Los parámetros se pasan como un diccionario
            result = connection.execute(query, {"username": usuario, "password": contraseña}).fetchone()

            if result:
                # Inicio de sesión exitoso
                return redirect(url_for('home'))  # redirige a la página de inicio
            else:
                # Inicio de sesión fallido, redirigir de nuevo al login con un mensaje de error
                flash('Usuario o contraseña incorrectos', 'error')  # muestra un mensaje de error
                return redirect(url_for('index'))

        finally:
            # Asegúrate de cerrar la conexión
            connection.close()

    # Si el método no es POST (es decir, el usuario está solicitando la página de inicio de sesión), simplemente muestra la página de inicio de sesión
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
