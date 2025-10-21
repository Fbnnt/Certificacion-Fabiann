# 🎬 CinePedia - Sistema de Gestión de Películas

Una aplicación web moderna para gestionar películas con sistema de usuarios, comentarios y diseño estilo Netflix.

## 📋 Características

- ✅ **Sistema de usuarios** con registro y autenticación segura
- ✅ **Gestión de películas** (crear, editar, eliminar, ver)
- ✅ **Sistema de comentarios** en películas
- ✅ **Diseño responsivo** estilo Netflix
- ✅ **Base de datos MySQL** con relaciones
- ✅ **Validaciones** de formularios
- ✅ **Sesiones** y control de acceso

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask 3.1.2
- **Base de datos**: MySQL
- **Frontend**: HTML5, CSS3 (estilo Netflix)
- **Autenticación**: Werkzeug (bcrypt)
- **ORM**: PyMySQL

## 📁 Estructura del Proyecto

```
Certificacion-Fabiann/
├── base/                          # Aplicación principal
│   ├── __init__.py               # Configuración Flask
│   ├── config/
│   │   └── mysqlconnection.py    # Conexión a BD
│   ├── controllers/              # Controladores (rutas)
│   │   ├── usuarios.py          # Auth (login/registro)
│   │   └── peliculas.py         # CRUD películas
│   ├── models/                   # Modelos de datos
│   │   ├── usuario.py           # Modelo usuario
│   │   ├── pelicula.py          # Modelo película
│   │   └── comentario.py        # Modelo comentario
│   ├── templates/               # Plantillas HTML
│   │   ├── index.html          # Login/Registro
│   │   ├── dashboard.html      # Lista películas
│   │   ├── nueva.html          # Crear película
│   │   ├── editar.html         # Editar película
│   │   └── ver.html            # Ver película
│   └── static/css/
│       └── style.css           # Estilos Netflix
├── server.py                    # Servidor principal
├── setup_db.py                 # Configurar BD
├── scripts.sql                 # Scripts SQL
├── requirements.txt            # Dependencias
└── README.md                   # Este archivo
```

## 🚀 Instalación y Configuración

### 1. Prerrequisitos

- **Python 3.8+**
- **MySQL 5.7+** o **MySQL 8.0+**
- **Git** (opcional)

### 2. Clonar el Proyecto

```bash
git clone <url-del-repositorio>
cd Certificacion-Fabiann
```

### 3. Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar Base de Datos

#### Opción A: Script Automático
```bash
python setup_db.py
```

#### Opción B: Manual
1. Abrir MySQL Workbench o cliente MySQL
2. Ejecutar el contenido de `scripts.sql`
3. Verificar que se creó la base de datos `cine_db`

### 6. Variables de Entorno (Opcional)

Crear archivo `.env` en la raíz del proyecto:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña
MYSQL_DB=cine_db
MYSQL_PORT=3306
```

### 7. Ejecutar la Aplicación

```bash
python server.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📖 Guía de Uso

### 1. Registro de Usuario
- Ir a `http://localhost:5000`
- Completar formulario de registro
- Iniciar sesión con las credenciales

### 2. Gestión de Películas
- **Ver películas**: Dashboard principal
- **Crear película**: Botón "Nueva Peli"
- **Editar película**: Solo el autor puede editar
- **Eliminar película**: Solo el autor puede eliminar
- **Ver detalles**: Click en "Ver Detalles"

### 3. Sistema de Comentarios
- Comentar en películas de otros usuarios
- No se puede comentar en propias películas
- Eliminar comentarios propios

## 🔧 Configuración Avanzada

### Base de Datos

La aplicación usa MySQL con las siguientes tablas:

- **usuarios**: Datos de usuarios con contraseñas encriptadas
- **peliculas**: Información de películas con relación a usuarios
- **comentarios**: Comentarios con relación a usuarios y películas

### Seguridad

- Contraseñas encriptadas con bcrypt
- Validación de formularios
- Control de sesiones
- Protección CSRF (Flask por defecto)

### Personalización

#### Cambiar Tema
Editar `base/static/css/style.css` - Variables CSS en `:root`

#### Agregar Campos
1. Modificar `scripts.sql` para agregar columnas
2. Actualizar modelos en `base/models/`
3. Modificar templates HTML
4. Actualizar controladores

## 🐛 Solución de Problemas

### Error de Conexión a MySQL
```bash
# Verificar que MySQL esté ejecutándose
# Windows
net start mysql

# Linux/Mac
sudo systemctl start mysql
```

### Error de Dependencias
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

### Error de Base de Datos
```bash
# Recrear base de datos
python setup_db.py
```

### Puerto en Uso
```bash
# Cambiar puerto en server.py
app.run(debug=True, port=5001)
```

## 📝 API Endpoints

### Autenticación
- `GET /` - Página de login/registro
- `POST /registro` - Registrar usuario
- `POST /login` - Iniciar sesión
- `GET /logout` - Cerrar sesión

### Películas
- `GET /cine` - Listar películas
- `GET /cine/nueva` - Formulario nueva película
- `POST /cine/nueva` - Crear película
- `GET /cine/<id>` - Ver película
- `GET /cine/editar/<id>` - Formulario editar
- `POST /cine/editar/<id>` - Actualizar película
- `POST /cine/<id>/eliminar` - Eliminar película

### Comentarios
- `POST /cine/<id>/comentarios` - Crear comentario
- `POST /cine/<id>/comentarios/<comentario_id>/eliminar` - Eliminar comentario

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Autores

- **Fabiann** - Desarrollo inicial

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisar la sección de solución de problemas
2. Verificar que todas las dependencias estén instaladas
3. Comprobar la configuración de MySQL
4. Crear un issue en el repositorio

---

**¡Disfruta gestionando tus películas favoritas! 🍿**
