# ISAM School Management System

Esta es una aplicación de escritorio desarrollada en Python con PyQt5 para la gestión escolar de ISAM (escuela de computación e inglés). Incluye:

- Inicio de sesión seguro (usuario: ISAM, contraseña: Am3l1a)
- Registro de usuarios con confirmación por correo electrónico (SMTP, Mailtrap)
- Validación de correo y token de confirmación con expiración de 24 horas
- Dashboard con registro de profesores, clases y alumnos
- Soporte multi-idioma (español/inglés)
- Selección de idioma desde menú de hamburguesa
- Autenticación y sesión con JWT
- Persistencia de datos en base de datos SQLite3 (no se usan archivos txt)
- Dashboard visual con estadísticas usando matplotlib

## Usuario y contraseña por defecto
- **Usuario:** ISAM
- **Contraseña:** Am3l1a

## Requisitos
- Python 3.8+
- PyQt5
- PyJWT
- matplotlib

## Instalación
1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   pip install matplotlib
   ```
2. Ejecuta la aplicación:
   ```bash
   python src/main.py
   ```
   O, si necesitas especificar la ruta de Python (por ejemplo, en Windows):
   ```bash
   C:\Python\Python39\python.exe src/main.py
   ```

## Configuración de correo SMTP (Mailtrap)
La app utiliza Mailtrap para enviar correos de confirmación de registro. Puedes cambiar las credenciales en `src/data/email_utils.py`:

```
SMTP_HOST = 'sandbox.smtp.mailtrap.io'
SMTP_PORT = 587
SMTP_USER = 'TU_USUARIO_MAILTRAP'
SMTP_PASS = 'TU_PASSWORD_MAILTRAP'
FROM_EMAIL = 'noreply@isam.com'
```

## Modo desarrollo (hot reload)
Para desarrollo, ejecuta:
```bash
python run_dev.py
```
O, si necesitas especificar la ruta de Python:
```bash
C:\Python\Python39\python.exe run_dev.py
```
La app se reiniciará automáticamente al guardar cambios en archivos `.py` o `.json` dentro de `src/`.

## Estructura del proyecto
- `src/` Código fuente principal
- `src/auth/` Formularios de login y registro (con confirmación por email)
- `src/dashboard/` Dashboard, profesores, clases y alumnos
- `src/data/` Persistencia (SQLite3), JWT y envío de correos
- `src/resources/` Imágenes y archivos de idioma
- `src/documentation/` Documentación y diagramas

## Notas
- Los archivos de idioma están en `src/resources/lang/`.
- Cambia el idioma desde el menú de hamburguesa en la app.
- Todos los datos (profesores, clases, alumnos y sus relaciones) se almacenan en la base de datos SQLite (`src/data/isam.db`).
- Ya no se utilizan archivos txt ni SimpleStorage para la gestión de datos.
- El dashboard visual requiere tener instalada la librería matplotlib.
- El registro de usuarios requiere acceso a internet para el envío de correos de confirmación.
