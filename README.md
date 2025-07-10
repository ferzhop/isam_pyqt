# ISAM School Management System

Esta es una aplicación de escritorio desarrollada en Python con PyQt5 para la gestión escolar de ISAM (escuela de computación e inglés). Incluye:

- Inicio de sesión seguro (usuario: ISAM, contraseña: Am3l1a)
- Registro de usuarios
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
- `src/auth/` Formularios de login y registro
- `src/dashboard/` Dashboard, profesores, clases y alumnos
- `src/data/` Persistencia (SQLite3) y JWT
- `src/resources/` Imágenes y archivos de idioma

## Notas
- Los archivos de idioma están en `src/resources/lang/`.
- Cambia el idioma desde el menú de hamburguesa en la app.
- Todos los datos (profesores, clases, alumnos y sus relaciones) se almacenan en la base de datos SQLite (`src/data/isam.db`).
- Ya no se utilizan archivos txt ni SimpleStorage para la gestión de datos.
- El dashboard visual requiere tener instalada la librería matplotlib.
