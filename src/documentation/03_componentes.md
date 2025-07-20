# Componentes principales

## 1. main.py
Punto de entrada. Inicializa la aplicación, la ventana principal y gestiona el cambio de idioma y navegación entre pantallas.

## 2. auth/login_form.py y auth/register_form.py
- **login_form.py**: Formulario de inicio de sesión. Verifica usuario/contraseña contra la base de datos y emite señal de login exitoso.
- **register_form.py**: Permite registrar nuevos usuarios, solicita correo, envía token de confirmación y valida el registro antes de guardar el usuario.

## 3. data/email_utils.py
Módulo para el envío de correos SMTP (Mailtrap) con el token de confirmación de registro.

## 4. dashboard/dashboard.py
Pantalla principal tras el login. Permite navegar entre los CRUDs de profesores, clases y alumnos. Incluye un dashboard visual con estadísticas.

## 5. dashboard/teachers_crud.py, classes_crud.py, students_crud.py
CRUDs para gestionar profesores, clases y alumnos. Usan la clase DBStorage para interactuar con la base de datos.

## 6. data/storage.py
Contiene la clase DBStorage, que abstrae todas las operaciones con SQLite3 (crear tablas, CRUD, relaciones, usuarios, confirmación de registro).

## 7. data/translator.py
Carga los archivos de idioma y permite traducción dinámica de la interfaz.

## 8. data/auth_manager.py
Genera y verifica tokens JWT para la sesión del usuario.

## 9. resources/
- **lang/**: Archivos de idioma (es.json, en.json).
- **images/**: Imágenes usadas en la interfaz.
- **styles.qss**: Estilos visuales para la app.

Cada componente está documentado en el código y en este instructivo para facilitar su comprensión y extensión.
