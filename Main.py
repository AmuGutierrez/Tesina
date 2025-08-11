from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import os
from datetime import datetime

app = Flask(__name__)

# Configuración de la aplicación
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto por una clave segura

# Configuración de MySQL (XAMPP)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inscripciones_proa'

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
        
        # Validación simple (puedes mejorar esto con la base de datos)
        if usuario == "proa" and contraseña == "1234":
            session['logged_in'] = True
            session['usuario'] = usuario
            flash('¡Bienvenido al sistema de inscripciones!', 'success')
            return redirect(url_for('inscripcion'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('Login.html')

@app.route('/inscripcion', methods=['GET', 'POST'])
def inscripcion():
    """Página de inscripción"""
    if not session.get('logged_in'):
        flash('Debes iniciar sesión para acceder a esta página', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Obtener datos del formulario
        datos_estudiante = {
            'nombre': request.form.get('nombre'),
            'apellido': request.form.get('apellido'),
            'edad': request.form.get('edad'),
            'dni': request.form.get('dni'),
            'secundario': request.form.get('secundario'),
            'repitente': request.form.get('repitente'),
            'domicilio': request.form.get('domicilio'),
            'anio': request.form.get('anio')
        }
        
        datos_tutor = {
            'nombre': request.form.get('tutor-nombre'),
            'email': request.form.get('tutor-email'),
            'dni': request.form.get('tutor-dni'),
            'telefono': request.form.get('tutor-telefono')
        }
        
        try:
            # Guardar en la base de datos
            cur = mysql.connection.cursor()
            
            # Insertar datos del estudiante
            cur.execute("""
                INSERT INTO estudiantes (nombre, apellido, edad, dni, secundario_cursado, 
                repitente, domicilio, anio_cursado, fecha_inscripcion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                datos_estudiante['nombre'], datos_estudiante['apellido'], 
                datos_estudiante['edad'], datos_estudiante['dni'],
                datos_estudiante['secundario'], datos_estudiante['repitente'],
                datos_estudiante['domicilio'], datos_estudiante['anio'],
                datetime.now()
            ))
            
            estudiante_id = cur.lastrowid
            
            # Insertar datos del tutor
            cur.execute("""
                INSERT INTO tutores (estudiante_id, nombre, email, dni, telefono)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                estudiante_id, datos_tutor['nombre'], datos_tutor['email'],
                datos_tutor['dni'], datos_tutor['telefono']
            ))
            
            mysql.connection.commit()
            cur.close()
            
            flash('¡Inscripción realizada con éxito!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error al procesar la inscripción: {str(e)}', 'error')
            mysql.connection.rollback()
    
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
            FROM estudiantes e
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

# Manejo de errores
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Verificar conexión a MySQL al iniciar la aplicación
    with app.app_context():
        if verificar_conexion():
            print("🚀 Iniciando aplicación Flask...")
            # Ejecutar la aplicación en modo desarrollo
            app.run(debug=True, host='0.0.0.0', port=5000)
                else:
            print("❌ No se pudo iniciar la aplicación debido a problemas de conexión")