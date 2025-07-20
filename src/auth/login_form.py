from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from data.translator import Translator
from data.auth_manager import AuthManager
import os

class LoginForm(QWidget):
    login_successful = pyqtSignal(str)

    def __init__(self, parent=None, translator=None):
        super().__init__(parent)
        self.translator = translator or Translator("es")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.translator.t("login_title"))
        self.user_label = QLabel(self.translator.t("username"))
        self.user_input = QLineEdit()
        self.pass_label = QLabel(self.translator.t("password"))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.login_btn = QPushButton(self.translator.t("login"))
        self.login_btn.clicked.connect(self.handle_login)
        self.user_input.returnPressed.connect(self.handle_login)
        self.pass_input.returnPressed.connect(self.handle_login)

        # Logo ISAM
        self.logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "..", "resources", "images", "Logo_ISAM.png")
        pixmap = QPixmap(logo_path)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setFixedHeight(120)
        self.logo_label.setScaledContents(True)

        # Link a registro
        self.register_label = QLabel(f'<a href="#">{self.translator.t("register")}</a>')
        self.register_label.setStyleSheet('color: #1976d2; text-align: center;')
        self.register_label.setTextFormat(Qt.RichText)
        self.register_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.register_label.setOpenExternalLinks(False)
        self.register_label.linkActivated.connect(self.go_to_register)

        # Centrar el formulario
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.logo_label)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.user_label)
        form_layout.addWidget(self.user_input)
        form_layout.addWidget(self.pass_label)
        form_layout.addWidget(self.pass_input)
        form_layout.addWidget(self.login_btn)
        form_layout.addWidget(self.register_label)
        form_layout.setAlignment(self.logo_label, Qt.AlignHCenter)
        form_layout.setAlignment(self.login_btn, Qt.AlignHCenter)
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(60, 40, 60, 40)

        container = QWidget()
        container.setLayout(form_layout)

        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addWidget(container, alignment=Qt.AlignCenter)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

    def handle_login(self):
        from data.storage import DBStorage
        username = self.user_input.text()
        password = self.pass_input.text()
        db = DBStorage()
        db.create_admin_user()  # Asegura que el admin exista
        if db.verify_user(username, password):
            token = AuthManager.generate_token(username)
            self.login_successful.emit(token)
        else:
            QMessageBox.warning(self, self.translator.t("login_title"), "Usuario o contraseña incorrectos.")

    def set_language(self, lang):
        self.translator.load_language(lang)
        self.setWindowTitle(self.translator.t("login_title"))
        self.user_label.setText(self.translator.t("username"))
        self.pass_label.setText(self.translator.t("password"))
        self.login_btn.setText(self.translator.t("login"))

    def go_to_register(self):
        if self.parent() and hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'stacked_widget'):
            self.parent().parent().stacked_widget.setCurrentIndex(1)
        elif self.parent() and hasattr(self.parent(), 'stacked_widget'):
            self.parent().stacked_widget.setCurrentIndex(1)
