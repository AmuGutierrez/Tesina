from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from datetime import datetime
import os

app = Flask(__name__)

# Configuración
app.secret_key = 'tu_clave_secreta_muy_segura_2025'

# Configuración MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin123'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_DB'] = 'inscripciones'

mysql = MySQL(app)

# ==========================================
# RUTAS PÚBLICAS
# ==========================================

@app.route('/')
def index():
    """Página de inicio"""
    return render_template('Index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contraseña = request.form.get('contraseña')

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT id, nombre, apellido, mail, password
                FROM usuarios
                WHERE mail = %s
            """, (usuario,))
            user = cur.fetchone()
            cur.close()

            if user and check_password_hash(user[4], contraseña):
                session['logged_in'] = True
                session['usuario_id'] = user[0]
                session['usuario'] = user[3]
                session['nombre'] = user[1]
                session['apellido'] = user[2]

                # Verificar si es administrador
                if user[3].lower() == 'admin123@gmail.com':
                    session['is_admin'] = True
                    flash('Bienvenido administrador', 'success')
                    return redirect(url_for('admin'))
                else:
                    session['is_admin'] = False
                    flash(f'Bienvenido/a {user[1]}', 'success')
                    return redirect(url_for('opciones'))
            else:
                flash('Usuario o contraseña incorrectos', 'error')
        except Exception as e:
            flash(f'Error al iniciar sesión: {str(e)}', 'error')
    
    return render_template('Login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registro de nuevos tutores"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        mail = request.form.get('mail')
        password = request.form.get('password')
        dni = request.form.get('dni')
        telefono = request.form.get('telefono')
        domicilio = request.form.get('domicilio')

        try:
            cur = mysql.connection.cursor()
            
            # Verificar si el mail ya existe
            cur.execute("SELECT id FROM usuarios WHERE mail = %s", (mail,))
            if cur.fetchone():
                cur.close()
                flash('El correo ya está registrado', 'error')
                return redirect(url_for('registro'))

            hash_pwd = generate_password_hash(password)

            # Insertar nuevo usuario
            cur.execute("""
                INSERT INTO usuarios (nombre, apellido, mail, password, dni, telefono, domicilio)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre, apellido, mail, hash_pwd, dni, telefono, domicilio))
            mysql.connection.commit()
            cur.close()

            flash('Registro exitoso. Ya podés iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al registrar: {str(e)}', 'error')

    return render_template('Registro.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

# ==========================================
# RUTAS DE USUARIO (TUTOR)
# ==========================================

@app.route('/opciones')
def opciones():
    """Panel de opciones para tutores"""
    if not session.get('logged_in'):
        flash('Debes iniciar sesión', 'error')
        return redirect(url_for('login'))

    try:
        cur = mysql.connection.cursor()
        # Obtener todos los alumnos del tutor actual
        cur.execute("""
            SELECT IDAlum, nombre, apellido, dni, curso_ingresante
            FROM alumno
            WHERE id_tutor = %s
            ORDER BY fecha_inscripcion DESC
        """, (session.get('usuario_id'),))
        alumnos = cur.fetchall()
        cur.close()

        return render_template('opciones.html', alumnos=alumnos)

    except Exception as e:
        flash(f'Error al cargar opciones: {str(e)}', 'error')
        return render_template('opciones.html', alumnos=[])

@app.route('/inscripcion', methods=['GET', 'POST'])
def inscripcion():
    """Formulario de inscripción de alumno"""
    if not session.get('logged_in'):
        flash('Debes iniciar sesión para acceder a esta página', 'error')
        return redirect(url_for('login'))
    
    # Obtener datos del tutor para pre-llenar el formulario
    usuario = None
    if request.method == 'GET':
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT nombre, apellido, mail, dni, telefono
                FROM usuarios WHERE id = %s
            """, (session.get('usuario_id'),))
            usuario_data = cur.fetchone()
            cur.close()
            if usuario_data:
                usuario = {
                    'nombre': f"{usuario_data[0]} {usuario_data[1]}",
                    'email': usuario_data[2],
                    'dni': usuario_data[3],
                    'telefono': usuario_data[4]
                }
        except Exception as e:
            print(f"Error al cargar datos del tutor: {str(e)}")
    
    if request.method == 'POST':
        # Datos del estudiante
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        edad = request.form.get('edad')
        dni = request.form.get('dni')
        domicilio = request.form.get('domicilio')
        escuela_procedente = request.form.get('escuela_procedente')
        curso_ingresante = request.form.get('curso_ingresante')
        repitente = request.form.get('repitente')
        anio_cursado = request.form.get('anio_cursado')
        observaciones = request.form.get('observaciones')

        try:
            cur = mysql.connection.cursor()
            
            # Verificar si el DNI ya existe
            cur.execute("SELECT IDAlum FROM alumno WHERE dni = %s", (dni,))
            if cur.fetchone():
                cur.close()
                flash('Ya existe una inscripción con ese DNI.', 'error')
                return render_template('Inscripcion.html', usuario=usuario)
            
            # Insertar alumno vinculado al tutor actual
            cur.execute("""
                INSERT INTO alumno (
                    nombre, apellido, edad, dni, domicilio, 
                    escuela_procedente, curso_ingresante, repitente, 
                    anio_cursado, id_tutor
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                nombre, apellido, edad, dni, domicilio,
                escuela_procedente, curso_ingresante, repitente,
                anio_cursado, session.get('usuario_id')
            ))
            alumno_id = cur.lastrowid

            # Crear relación en tabla tutores
            cur.execute("""
                INSERT INTO tutores (id_usuario, id_alumno)
                VALUES (%s, %s)
            """, (session.get('usuario_id'), alumno_id))

            # Registrar inscripción
            cur.execute("""
                INSERT INTO inscripciones (
                    IDAlum, IdTutor, fecha_inscripcion, 
                    estado, observaciones
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                alumno_id, 
                session.get('usuario_id'),
                datetime.now(),
                'En espera',
                observaciones
            ))

            mysql.connection.commit()
            cur.close()
            
            flash('Inscripción registrada exitosamente', 'success')
            return render_template('Finalizacion.html')
            
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al procesar la inscripción: {str(e)}', 'error')
    
    return render_template('Inscripcion.html', usuario=usuario)

@app.route('/estado_inscripcion/<int:id>')
def estado_inscripcion(id):
    """Ver estado de inscripción de un alumno"""
    if not session.get('logged_in'):
        flash('Debes iniciar sesión', 'error')
        return redirect(url_for('login'))

    try:
        cur = mysql.connection.cursor()
        
        # Verificar que el alumno pertenece al tutor actual
        cur.execute("""
            SELECT a.*, i.estado, i.observaciones, i.fecha_inscripcion
            FROM alumno a
            LEFT JOIN inscripciones i ON a.IDAlum = i.IDAlum
            WHERE a.IDAlum = %s AND a.id_tutor = %s
        """, (id, session.get('usuario_id')))
        
        alumno = cur.fetchone()
        cur.close()

        if not alumno:
            flash('Alumno no encontrado o no tienes permiso para verlo', 'error')
            return redirect(url_for('opciones'))

        # Convertir a diccionario para el template
        alumno_dict = {
            'IDAlum': alumno[0],
            'nombre': alumno[1],
            'apellido': alumno[2],
            'edad': alumno[3],
            'dni': alumno[4],
            'domicilio': alumno[5],
            'escuela_procedente': alumno[6],
            'curso_ingresante': alumno[7],
            'repitente': alumno[8],
            'anio_cursado': alumno[9],
            'estado': alumno[12] if len(alumno) > 12 and alumno[12] else 'En espera',
            'observaciones': alumno[13] if len(alumno) > 13 else '',
            'fecha_inscripcion': alumno[14] if len(alumno) > 14 else alumno[11]
        }

        return render_template('estado_inscripcion.html', alumno=alumno_dict)
        
    except Exception as e:
        flash(f'Error al cargar la ficha: {str(e)}', 'error')
        return redirect(url_for('opciones'))

@app.route('/editar_inscripcion/<int:id>', methods=['POST'])
def editar_inscripcion(id):
    """Editar datos de inscripción del alumno"""
    if not session.get('logged_in'):
        flash('Debes iniciar sesión', 'error')
        return redirect(url_for('login'))

    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    edad = request.form.get('edad')
    dni = request.form.get('dni')
    domicilio = request.form.get('domicilio')
    escuela_procedente = request.form.get('escuela_procedente')
    curso_ingresante = request.form.get('curso_ingresante')
    repitente = request.form.get('repitente')
    anio_cursado = request.form.get('anio_cursado')

    try:
        cur = mysql.connection.cursor()
        
        # Verificar que el alumno pertenece al tutor
        cur.execute("""
            SELECT IDAlum FROM alumno 
            WHERE IDAlum = %s AND id_tutor = %s
        """, (id, session.get('usuario_id')))
        
        if not cur.fetchone():
            cur.close()
            flash('No tienes permiso para editar este alumno', 'error')
            return redirect(url_for('opciones'))
        
        # Actualizar datos
        cur.execute("""
            UPDATE alumno
            SET nombre = %s, apellido = %s, edad = %s, dni = %s,
                domicilio = %s, escuela_procedente = %s, 
                curso_ingresante = %s, repitente = %s, anio_cursado = %s
            WHERE IDAlum = %s
        """, (nombre, apellido, edad, dni, domicilio, 
              escuela_procedente, curso_ingresante, repitente, 
              anio_cursado, id))
        
        mysql.connection.commit()
        cur.close()
        
        flash('Datos actualizados correctamente', 'success')
        return redirect(url_for('estado_inscripcion', id=id))
        
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al guardar: {str(e)}', 'error')
        return redirect(url_for('estado_inscripcion', id=id))

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    """Ver y editar perfil del tutor"""
    if not session.get('logged_in'):
        flash('Debes iniciar sesión', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        dni = request.form.get('dni')
        telefono = request.form.get('telefono')
        domicilio = request.form.get('domicilio')

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE usuarios
                SET nombre = %s, apellido = %s, dni = %s, 
                    telefono = %s, domicilio = %s
                WHERE id = %s
            """, (nombre, apellido, dni, telefono, domicilio, 
                  session.get('usuario_id')))
            mysql.connection.commit()
            cur.close()

            # Actualizar sesión
            session['nombre'] = nombre
            session['apellido'] = apellido
            
            flash('Perfil actualizado correctamente', 'success')
            return redirect(url_for('perfil'))
            
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al actualizar: {str(e)}', 'error')

    # Obtener datos del usuario
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT nombre, apellido, mail, dni, telefono, domicilio
            FROM usuarios WHERE id = %s
        """, (session.get('usuario_id'),))
        usuario = cur.fetchone()
        cur.close()

        if not usuario:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('opciones'))

        usuario_dict = {
            'nombre': usuario[0] or '',
            'apellido': usuario[1] or '',
            'mail': usuario[2] or '',
            'dni': usuario[3] or '',
            'telefono': usuario[4] or '',
            'domicilio': usuario[5] or ''
        }

        return render_template('perfil.html', usuario=usuario_dict)
        
    except Exception as e:
        print(f"Error en perfil: {str(e)}")  # Para debugging
        flash(f'Error al cargar perfil: {str(e)}', 'error')
        return redirect(url_for('opciones'))

# ==========================================
# RUTAS DE ADMINISTRADOR
# ==========================================

@app.route('/admin')
def admin():
    """Panel de administración"""
    if not session.get('logged_in') or not session.get('is_admin'):
        flash('Acceso denegado', 'error')
        return redirect(url_for('login'))
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                i.IDInscripcion,
                a.IDAlum,
                a.nombre AS alumno_nombre,
                a.apellido AS alumno_apellido,
                a.dni AS alumno_dni,
                a.curso_ingresante,
                u.nombre AS tutor_nombre,
                u.mail AS tutor_email,
                u.telefono AS tutor_telefono,
                i.estado,
                i.fecha_inscripcion
            FROM inscripciones i
            JOIN alumno a ON i.IDAlum = a.IDAlum
            JOIN usuarios u ON i.IdTutor = u.id
            ORDER BY i.fecha_inscripcion DESC
        """)
        inscripciones = cur.fetchall()
        cur.close()
        
        return render_template('admin.html', inscripciones=inscripciones)
    except Exception as e:
        flash(f'Error al cargar inscripciones: {str(e)}', 'error')
        return render_template('admin.html', inscripciones=[])

@app.route('/admin/cambiar_estado/<int:id>', methods=['POST'])
def cambiar_estado(id):
    """Cambiar estado de una inscripción"""
    if not session.get('is_admin'):
        flash('Acceso denegado', 'error')
        return redirect(url_for('login'))

    nuevo_estado = request.form.get('estado')
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE inscripciones 
            SET estado = %s 
            WHERE IDInscripcion = %s
        """, (nuevo_estado, id))
        mysql.connection.commit()
        cur.close()
        
        flash('Estado actualizado correctamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al actualizar estado: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/ficha/<int:id_alumno>')
def admin_ficha_completa(id_alumno):
    """Obtener ficha completa de un alumno para el administrador"""
    if not session.get('is_admin'):
        return {'success': False, 'error': 'Acceso denegado'}, 403
    
    try:
        from flask import jsonify
        cur = mysql.connection.cursor()
        
        # Obtener datos del alumno
        cur.execute("""
            SELECT IDAlum, nombre, apellido, edad, dni, domicilio,
                   escuela_procedente, curso_ingresante, repitente, anio_cursado
            FROM alumno
            WHERE IDAlum = %s
        """, (id_alumno,))
        alumno_data = cur.fetchone()
        
        if not alumno_data:
            cur.close()
            return jsonify({'success': False, 'error': 'Alumno no encontrado'}), 404
        
        # Obtener datos de la inscripción
        cur.execute("""
            SELECT IDInscripcion, estado, observaciones, fecha_inscripcion
            FROM inscripciones
            WHERE IDAlum = %s
        """, (id_alumno,))
        inscripcion_data = cur.fetchone()
        
        # Obtener datos del tutor
        cur.execute("""
            SELECT u.nombre, u.apellido, u.dni, u.mail, u.telefono, u.domicilio
            FROM usuarios u
            JOIN alumno a ON a.id_tutor = u.id
            WHERE a.IDAlum = %s
        """, (id_alumno,))
        tutor_data = cur.fetchone()
        
        cur.close()
        
        # Construir respuesta JSON
        response = {
            'success': True,
            'alumno': {
                'id': alumno_data[0],
                'nombre': alumno_data[1],
                'apellido': alumno_data[2],
                'edad': alumno_data[3],
                'dni': alumno_data[4],
                'domicilio': alumno_data[5],
                'escuela_procedente': alumno_data[6],
                'curso_ingresante': alumno_data[7],
                'repitente': alumno_data[8],
                'anio_cursado': alumno_data[9]
            },
            'inscripcion': {
                'id': inscripcion_data[0] if inscripcion_data else None,
                'estado': inscripcion_data[1] if inscripcion_data else 'Sin estado',
                'observaciones': inscripcion_data[2] if inscripcion_data else '',
                'fecha': inscripcion_data[3].strftime('%d/%m/%Y %H:%M') if inscripcion_data and inscripcion_data[3] else 'N/A'
            },
            'tutor': {
                'nombre': tutor_data[0] if tutor_data else '',
                'apellido': tutor_data[1] if tutor_data else '',
                'dni': tutor_data[2] if tutor_data else '',
                'email': tutor_data[3] if tutor_data else '',
                'telefono': tutor_data[4] if tutor_data else '',
                'domicilio': tutor_data[5] if tutor_data else ''
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==========================================
# UTILIDADES
# ==========================================

def verificar_conexion():
    """Verificar conexión a MySQL"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        print("✅ Conexión a MySQL exitosa")
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def verificar_templates():
    """Verificar que existan todos los templates necesarios"""
    templates_necesarios = [
        'Index.html',
        'Login.html', 
        'Registro.html',
        'Inscripcion.html',
        'Finalizacion.html',
        'opciones.html',
        'estado_inscripcion.html',
        'perfil.html',
        'admin.html'
    ]
    
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    faltantes = []
    
    for template in templates_necesarios:
        ruta = os.path.join(templates_dir, template)
        if not os.path.exists(ruta):
            faltantes.append(template)
    
    if faltantes:
        print(f"⚠️  ADVERTENCIA: Faltan los siguientes templates:")
        for t in faltantes:
            print(f"   - {t}")
        return False
    else:
        print("✅ Todos los templates están presentes")
        return True

# ==========================================
# INICIAR APLICACIÓN
# ==========================================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Iniciando Sistema de Inscripciones PROA")
    print("="*50 + "\n")
    
    if verificar_conexion():
        verificar_templates()
        print("\n✅ Aplicación lista en: http://localhost:5000")
        print("="*50 + "\n")
        app.run(debug=True, port=5000)
    else:
        print("\n❌ No se pudo conectar a MySQL.")
        print("💡 Verifica que XAMPP esté corriendo y MySQL activo en puerto 3307")
        print("="*50 + "\n")
