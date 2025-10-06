from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import os
from datetime import datetime

app = Flask(__name__)

# Configuración de la aplicación
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto por una clave segura

# Configuración de MySQL (XAMPP)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin123'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_DB'] = 'inscripciones'

# Inicializar MySQL
mysql = MySQL(app)

# Rutas de la aplicación

@app.route('/')
def index():
    """Página de inicio"""
    return render_template('Index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        try:
            cur = mysql.connection.cursor()
            # Buscar usuario por mail
            cur.execute("""
                SELECT id, nombre, apellido, mail, password
                FROM usuarios
                WHERE mail = %s
            """, (usuario,))
            user = cur.fetchone()
            cur.close()

            if user and check_password_hash(user[4], contraseña):
                session['logged_in'] = True
                session['usuario'] = user[3]
                session['nombre'] = user[1]
                session['apellido'] = user[2]
                flash('¡Bienvenido al sistema de inscripciones!', 'success')
                return redirect(url_for('inscripcion'))
            else:
                flash('Usuario o contraseña incorrectos', 'error')
        except Exception as e:
            flash(f'Error al iniciar sesión: {str(e)}', 'error')
    
    return render_template('Login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registro de usuarios"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        mail = request.form.get('mail')
        password = request.form.get('password')

        try:
            cur = mysql.connection.cursor()
            # Crear tabla usuarios si no existe
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    apellido VARCHAR(100) NOT NULL,
                    mail VARCHAR(120) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)

            # Verificar si el mail ya existe
            cur.execute("SELECT id FROM usuarios WHERE mail = %s", (mail,))
            existente = cur.fetchone()
            if existente:
                cur.close()
                flash('El correo ya está registrado', 'error')
                return redirect(url_for('registro'))

            hash_pwd = generate_password_hash(password)

            # Insertar nuevo usuario
            cur.execute("""
                INSERT INTO usuarios (nombre, apellido, mail, password)
                VALUES (%s, %s, %s, %s)
            """, (nombre, apellido, mail, hash_pwd))
            mysql.connection.commit()
            cur.close()

            flash('Registro exitoso. Ya podés iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al registrar: {str(e)}', 'error')

    return render_template('Registro.html')

@app.route('/inscripcion', methods=['GET', 'POST'])
def inscripcion():
    """Página de inscripción"""
    if not session.get('logged_in'):
        flash('Debes iniciar sesión para acceder a esta página', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        datos_estudiante = {
            'nombre': request.form.get('nombre'),
            'apellido': request.form.get('apellido'),
            'edad': request.form.get('edad'),
            'dni': request.form.get('dni'),
            'secundario_cursado': request.form.get('secundario_cursado'),
            'repitente': request.form.get('repitente'),
            'domicilio': request.form.get('domicilio'),
            'anio_cursado': request.form.get('anio_cursado')
        }
        datos_tutor = {
            'nombre': request.form.get('tutor-nombre'),
            'email': request.form.get('tutor-email'),
            'dni': request.form.get('tutor-dni'),
            'telefono': request.form.get('tutor-telefono')
        }
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT IDAlum FROM alumno WHERE dni = %s", (datos_estudiante['dni'],))
            existe = cur.fetchone()
            if existe:
                flash('Ya existe una inscripción con ese DNI.', 'error')
                return render_template('Inscripcion.html')
            
            cur.execute("""
                INSERT INTO alumno (nombre, apellido, edad, dni, domicilio)
                VALUES ( %s, %s, %s, %s, %s)
            """, (
                datos_estudiante['nombre'],
                datos_estudiante['apellido'],
                datos_estudiante['edad'],
                datos_estudiante['dni'],
                datos_estudiante['domicilio'],
            ))
            estudiante_id = cur.lastrowid
            cur.execute("""
                INSERT INTO tutores (estudiante_id, nombre, email, dni, telefono)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                estudiante_id,
                datos_tutor['nombre'],
                datos_tutor['email'],
                datos_tutor['dni'],
                datos_tutor['telefono']
            ))
            tutor_id = cur.lastrowid

            # Insertar inscripción
            cur.execute("""
                INSERT INTO inscripciones (IDAlum, IdTutor, Escuela_procedente, Curso_ingresante, Repitente, Observaciones, fecha_inscripcion)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                estudiante_id,
                tutor_id,
                request.form.get('escuela_procedente'),
                request.form.get('curso_ingresante'),
                request.form.get('repitente'),
                request.form.get('observaciones'),
                datetime.now()  # Guarda la fecha y hora actual
            ))
            mysql.connection.commit()
            cur.close()
            # Redirigir al template de finalización
            return render_template('Finalizacion.html')
        except Exception as e:
            flash(f'Error al procesar la inscripción: {str(e)}', 'error')
    
    return render_template('Inscripcion.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    """Panel de administración (solo para desarrollo)"""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT e.*, t.nombre as tutor_nombre, t.email as tutor_email, t.telefono
            FROM alumno e
            LEFT JOIN tutores t ON e.id = t.estudiante_id
            ORDER BY e.fecha_inscripcion DESC
        """)
        inscripciones = cur.fetchall()
        cur.close()
        
        return render_template('admin.html', inscripciones=inscripciones)
    except Exception as e:
        flash(f'Error al cargar las inscripciones: {str(e)}', 'error')
        return render_template('admin.html', inscripciones=[])

# Función para verificar conexión a MySQL
def verificar_conexion():
    """Verificar que la conexión a MySQL esté funcionando"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        print("✅ Conexión a MySQL exitosa")
        return True
    except Exception as e:
        print(f"❌ Error de conexión a MySQL: {str(e)}")
        print("💡 Asegúrate de que XAMPP esté corriendo y MySQL esté activo")
        return False
