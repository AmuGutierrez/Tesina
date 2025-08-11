# Sistema de Inscripciones - Escuela PROA

Sistema web para la gestión de inscripciones de estudiantes en la Escuela PROA Río Tercero, desarrollado con Flask, MySQL y HTML/CSS.

## 🚀 Características

- **Página de inicio** con información de la escuela
- **Sistema de login** para acceder al formulario de inscripción
- **Formulario de inscripción** completo con datos del estudiante y tutor
- **Base de datos MySQL** para almacenar las inscripciones
- **Panel de administración** para ver todas las inscripciones
- **Diseño responsivo** con estilos CSS unificados

## 📋 Requisitos Previos

- Python 3.8 o superior
- MySQL Server
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd Tesina
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
```

### 3. Activar el entorno virtual
**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar MySQL (XAMPP)

1. **Iniciar XAMPP:**
   - Abrir XAMPP Control Panel
   - Iniciar Apache y MySQL
   - Verificar que ambos servicios estén corriendo (luz verde)

2. **Crear la base de datos:**
   - Abrir phpMyAdmin: `http://localhost/phpmyadmin`
   - Crear nueva base de datos: `inscripciones_proa`
   - Importar el archivo `basedatos/crear_tablas.sql` o ejecutar el script manualmente

3. **Configurar las credenciales en `Main.py` (ya configurado para XAMPP):**
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inscripciones_proa'
```

### 6. Ejecutar la aplicación
```bash
python Main.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📁 Estructura del Proyecto

```
Tesina/
├── Main.py                 # Aplicación principal Flask
├── requirements.txt        # Dependencias de Python
├── README.md              # Este archivo
├── Static/
│   ├── styles.css         # Estilos CSS unificados
│   └── scripts.js         # JavaScript (vacío)
├── Templates/
│   ├── Index.html         # Página de inicio
│   ├── Login.html         # Página de login
│   └── Inscripcion.html   # Formulario de inscripción
└── basedatos/             # Archivos de base de datos
```

## 🗄️ Base de Datos

El sistema utiliza las siguientes tablas (crear manualmente con el script SQL):

### Tabla `estudiantes`
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
- `nombre` (VARCHAR(100))
- `apellido` (VARCHAR(100))
- `edad` (INT)
- `dni` (VARCHAR(20), UNIQUE)
- `secundario_cursado` (VARCHAR(200))
- `repitente` (VARCHAR(100))
- `domicilio` (VARCHAR(200))
- `anio_cursado` (VARCHAR(100))
- `fecha_inscripcion` (DATETIME)

### Tabla `tutores`
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
- `estudiante_id` (INT, FOREIGN KEY)
- `nombre` (VARCHAR(200))
- `email` (VARCHAR(100))
- `dni` (VARCHAR(20))
- `telefono` (VARCHAR(20))

## 🔐 Credenciales de Acceso

**Usuario:** `proa`  
**Contraseña:** `1234`

## 🎨 Estilos CSS

Los estilos están unificados en `Static/styles.css` e incluyen:
- Estilos para formularios
- Estilos para la página de inicio
- Estilos para el login
- Estilos para mensajes flash
- Diseño responsivo

## 🚀 Rutas de la Aplicación

- `/` - Página de inicio
- `/login` - Página de login
- `/inscripcion` - Formulario de inscripción
- `/logout` - Cerrar sesión
- `/admin` - Panel de administración

## 🔧 Configuración de Desarrollo

Para desarrollo, la aplicación se ejecuta en modo debug:
- Host: `0.0.0.0`
- Puerto: `5000`
- Debug: `True`

## 📝 Notas Importantes

1. **Seguridad**: Cambia la `secret_key` en `Main.py` por una clave segura
2. **XAMPP**: Asegúrate de que XAMPP esté corriendo y MySQL esté activo
3. **Base de datos**: Crea las tablas usando el script `basedatos/crear_tablas.sql`
4. **Puertos**: Verifica que el puerto 5000 esté disponible
5. **Dependencias**: Instala `mysqlclient` según tu sistema operativo

## 🐛 Solución de Problemas

### Error de conexión a MySQL
- Verifica que XAMPP esté corriendo y MySQL esté activo
- Confirma que la base de datos `inscripciones_proa` existe
- Ejecuta el script `basedatos/crear_tablas.sql` en phpMyAdmin

### Error de dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Error de puerto ocupado
Cambia el puerto en `Main.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📞 Soporte

Para soporte técnico, contacta al equipo de desarrollo.

---

**Desarrollado para la Escuela PROA Río Tercero** 🎓
