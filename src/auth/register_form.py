from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
from data.translator import Translator
import re
import secrets
import time
from data.email_utils import send_confirmation_email

class RegisterForm(QWidget):
    def __init__(self, parent=None, translator=None):
        super().__init__(parent)
        self.translator = translator or Translator("es")
        self.init_ui()
        self.pending_token = None
        self.pending_email = None
        self.pending_username = None
        self.pending_password = None
        self.token_expiry = None

    def init_ui(self):
        self.setWindowTitle(self.translator.t("register"))
        self.user_label = QLabel(self.translator.t("username"))
        self.user_input = QLineEdit()
        self.pass_label = QLabel(self.translator.t("password"))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.email_label = QLabel(self.translator.t("email") if hasattr(self.translator, 't') else "Correo electrónico")
        self.email_input = QLineEdit()
        self.register_btn = QPushButton(self.translator.t("register"))
        self.register_btn.clicked.connect(self.handle_register)
        self.back_btn = QPushButton(self.translator.t("logout"))
        self.back_btn.setText(self.translator.t("back") if hasattr(self.translator, 't') and self.translator.t("back") != "back" else "Volver")
        self.back_btn.setStyleSheet('background-color: #b0bec5; color: #222;')
        self.back_btn.clicked.connect(self.go_to_login)
        self.confirm_label = QLabel(self.translator.t("confirm_token") if hasattr(self.translator, 't') else "Código de confirmación")
        self.confirm_input = QLineEdit()
        self.confirm_btn = QPushButton(self.translator.t("confirm") if hasattr(self.translator, 't') else "Confirmar")
        self.confirm_btn.clicked.connect(self.handle_confirm)
        self.confirm_label.hide()
        self.confirm_input.hide()
        self.confirm_btn.hide()
        # Logo ISAM
        from PyQt5.QtGui import QPixmap
        import os
        self.logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "..", "resources", "images", "Logo_ISAM.png")
        pixmap = QPixmap(logo_path)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setFixedHeight(120)
        self.logo_label.setScaledContents(True)
        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addSpacing(10)
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.register_btn)
        layout.addWidget(self.confirm_label)
        layout.addWidget(self.confirm_input)
        layout.addWidget(self.confirm_btn)
        layout.addWidget(self.back_btn)
        layout.setAlignment(self.logo_label, Qt.AlignHCenter)
        layout.setAlignment(self.register_btn, Qt.AlignHCenter)
        layout.setAlignment(self.confirm_btn, Qt.AlignHCenter)
        layout.setAlignment(self.back_btn, Qt.AlignHCenter)
        layout.setSpacing(12)
        layout.setContentsMargins(60, 40, 60, 40)
        self.setLayout(layout)

    def handle_register(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()
        email = self.email_input.text().strip()
        if not username or not password or not email:
            QMessageBox.warning(self, self.translator.t("register"), "Todos los campos son obligatorios.")
            return
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            QMessageBox.warning(self, self.translator.t("register"), "Correo electrónico inválido.")
            return
        # Verificar si el correo ya está registrado
        from data.storage import DBStorage
        db = DBStorage()
        db.ensure_users_table()
        c = db.conn.cursor()
        c.execute('SELECT * FROM users WHERE email=?', (email,))
        if c.fetchone():
            QMessageBox.warning(self, self.translator.t("register"), f"El correo {email} ya está registrado.")
            return
        # Generar token y guardar temporalmente
        token = secrets.token_hex(4)
        expiry = int(time.time()) + 24*3600
        self.pending_token = token
        self.pending_email = email
        self.pending_username = username
        self.pending_password = password
        self.token_expiry = expiry
        try:
            send_confirmation_email(email, username, token)
            QMessageBox.information(self, self.translator.t("register"), f"Se ha enviado un correo de confirmación a {email}. Ingresa el código recibido para activar tu cuenta.")
            self.confirm_label.show()
            self.confirm_input.show()
            self.confirm_btn.show()
        except Exception as e:
            QMessageBox.critical(self, self.translator.t("register"), f"Error al enviar correo: {e}")

    def handle_confirm(self):
        token = self.confirm_input.text().strip()
        if not token:
            QMessageBox.warning(self, self.translator.t("confirm"), "Ingresa el código de confirmación.")
            return
        if token != self.pending_token:
            QMessageBox.warning(self, self.translator.t("confirm"), "Código incorrecto.")
            return
        if int(time.time()) > self.token_expiry:
            QMessageBox.warning(self, self.translator.t("confirm"), "El código ha expirado. Regístrate de nuevo.")
            return
        # Guardar usuario en la base de datos
        from data.storage import DBStorage
        import hashlib
        db = DBStorage()
        password_hash = hashlib.sha256(self.pending_password.encode()).hexdigest()
        c = db.conn.cursor()
        c.execute('''INSERT INTO users (username, password, email, is_confirmed) VALUES (?, ?, ?, 1)''', (self.pending_username, password_hash, self.pending_email))
        db.conn.commit()
        QMessageBox.information(self, self.translator.t("register"), "Usuario registrado y confirmado. Ya puedes iniciar sesión.")
        self.go_to_login()

    def go_to_login(self):
        self.confirm_label.hide()
        self.confirm_input.hide()
        self.confirm_btn.hide()
        if self.parent() and hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'stacked_widget'):
            self.parent().parent().stacked_widget.setCurrentIndex(0)
        elif self.parent() and hasattr(self.parent(), 'stacked_widget'):
            self.parent().stacked_widget.setCurrentIndex(0)

    def set_language(self, lang):
        self.translator.load_language(lang)
        self.setWindowTitle(self.translator.t("register"))
        self.user_label.setText(self.translator.t("username"))
        self.pass_label.setText(self.translator.t("password"))
        self.register_btn.setText(self.translator.t("register"))
        self.email_label.setText(self.translator.t("email") if hasattr(self.translator, 't') else "Correo electrónico")
        self.confirm_label.setText(self.translator.t("confirm_token") if hasattr(self.translator, 't') else "Código de confirmación")
        self.confirm_btn.setText(self.translator.t("confirm") if hasattr(self.translator, 't') else "Confirmar")
