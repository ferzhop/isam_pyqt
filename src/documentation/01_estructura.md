# Estructura del Proyecto

La aplicación está organizada en carpetas según su función. Esto facilita el mantenimiento y la escalabilidad.

![Diagrama Estructura Proyecto](diagramas/Diagram_Mermaid_Estructura_Del_Proyecto.png)

```mermaid
graph TD
    SRC[src/]
    SRC --> AUTH[auth/]
    SRC --> DASH[dashboard/]
    SRC --> DATA[data/]
    SRC --> RES[resources/]
    SRC --> DOC[documentation/]
    AUTH --> LOGIN[login_form.py]
    AUTH --> REGISTER[register_form.py]
    DASH --> DASHBOARD[dashboard.py]
    DASH --> TEACHERS[teachers_crud.py]
    DASH --> CLASSES[classes_crud.py]
    DASH --> STUDENTS[students_crud.py]
    DATA --> STORAGE[storage.py]
    DATA --> TRANSLATOR[translator.py]
    DATA --> AUTHMAN[auth_manager.py]
    DATA --> EMAIL[email_utils.py]
    RES --> LANG[lang/]
    RES --> IMAGES[images/]
    RES --> STYLES[styles.qss]
```

- **auth/**: Login y registro de usuarios (con confirmación por email).
- **dashboard/**: Pantalla principal y gestión de entidades.
- **data/**: Persistencia (SQLite3), traducción, autenticación y envío de correos.
- **resources/**: Archivos de idioma, imágenes y estilos.
- **documentation/**: Instructivos y diagramas.

Cada módulo tiene responsabilidades claras y se comunica con los demás mediante clases y métodos bien definidos.
