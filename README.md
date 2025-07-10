# ISAM School Management System

Esta es una aplicación de escritorio desarrollada en Python con PyQt5 para la gestión escolar de ISAM (escuela de computación e inglés). Incluye:

- Inicio de sesión seguro (usuario: ISAM, contraseña: Am3l1a)
- Registro de usuarios
- Dashboard con registro de clases y alumnos
- Soporte multi-idioma (español/inglés)
- Selección de idioma desde menú de hamburguesa
- Autenticación y sesión con JWT

## Requisitos
- Python 3.8+
- PyQt5
- PyJWT

## Instalación
1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta la aplicación:
   ```bash
   python src/main.py
   ```

## Modo desarrollo (hot reload)
Para desarrollo, ejecuta:
```bash
python run_dev.py
```
La app se reiniciará automáticamente al guardar cambios en archivos `.py` o `.json` dentro de `src/`.

## Estructura del proyecto
- `src/` Código fuente principal
- `src/auth/` Formularios de login y registro
- `src/dashboard/` Dashboard, clases y alumnos
- `src/data/` Persistencia y JWT
- `src/resources/` Imágenes y archivos de idioma

## Notas
- Los archivos de idioma están en `src/resources/lang/`.
- Cambia el idioma desde el menú de hamburguesa en la app.
