# Flujo de la Aplicación

A continuación se describe el flujo principal de la aplicación desde el inicio hasta la gestión de datos y el registro de usuarios.

## Diagrama de flujo principal

![Diagrama flujo principal](diagramas/Diagram_Mermaid_Flujo_Principal.png)

```mermaid
sequenceDiagram
    participant Usuario
    participant MainApp
    participant RegisterForm
    participant EmailUtils
    participant Dashboard
    participant DBStorage

    Usuario->>MainApp: Ejecuta la app
    MainApp->>RegisterForm: Solicita registro
    RegisterForm->>DBStorage: Verifica unicidad de email
    RegisterForm->>EmailUtils: Envía correo con token
    Usuario->>RegisterForm: Ingresa token recibido
    RegisterForm->>DBStorage: Guarda usuario confirmado
    MainApp->>Dashboard: Muestra dashboard
    Usuario->>Dashboard: Navega entre CRUDs
    Dashboard->>DBStorage: Consulta/actualiza datos
    DBStorage-->>Dashboard: Devuelve datos
```

## Funcionalidades y pantallas principales

- **Login:** Pantalla de acceso al sistema.
  ![Login](pantallas/Login.png)

- **Registro de usuario:** Permite crear una cuenta, solicita usuario, contraseña y correo electrónico.
  ![Registro](pantallas/Register.png)

- **Correo de confirmación:** El usuario recibe un correo con un código de confirmación para activar su cuenta.
  ![Correo de confirmación](pantallas/Confirmation_email.png)

- **Pantalla de confirmación:** El usuario ingresa el código recibido para activar su cuenta.
  ![Confirmación de código](pantallas/Confirmation_code_registration.png)

- **Notificación de activación:** Mensaje visual tras enviar el correo de activación.
  ![Notificación de activación](pantallas/Email_notification_for_activation_sent.png)

- **Dashboard:** Vista principal tras el login, con acceso a los CRUDs y visualización de estadísticas.
  ![Dashboard](pantallas/Dashboard.png)

- **Gestión de profesores, alumnos y clases:** CRUDs para cada entidad.
  - Profesores: ![Profesores](pantallas/Teachers.png)
  - Alumnos: ![Alumnos](pantallas/Students.png)
  - Clases: ![Clases](pantallas/Classes.png)

- **Edición y registro de entidades:** Formularios para agregar o editar profesores, alumnos y clases.
  - Registrar/Editar Profesor: ![Registrar/Editar Profesor](pantallas/Register-Edit-Teachers.png)
  - Registrar/Editar Alumno: ![Registrar/Editar Alumno](pantallas/Register-Edit-Students.png)
  - Registrar/Editar Clase: ![Registrar/Editar Clase](pantallas/Register-Edit-Classes.png)

- **Cambio de idioma:** Permite alternar entre español e inglés desde el menú.
  ![Cambio de idioma](pantallas/Language.png)

- **Notificación de eliminación:** Mensaje visual al eliminar registros en los CRUDs.
  ![Notificación de eliminación](pantallas/Confirmation_of_record_deletion_in_cruds.png)

Cada pantalla está diseñada para ser intuitiva y guiar al usuario en el flujo de registro, confirmación y gestión escolar.
