from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox)
from data.translator import Translator

class RegisterForm(QWidget):
    def __init__(self, parent=None, translator=None):
        super().__init__(parent)
        self.translator = translator or Translator("es")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.translator.t("register"))
        self.user_label = QLabel(self.translator.t("username"))
        self.user_input = QLineEdit()
        self.pass_label = QLabel(self.translator.t("password"))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.register_btn = QPushButton(self.translator.t("register"))
        self.register_btn.clicked.connect(self.handle_register)

        layout = QVBoxLayout()
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.register_btn)
        self.setLayout(layout)

    def handle_register(self):
        # Aquí deberías guardar el usuario en una base de datos o archivo
        QMessageBox.information(self, self.translator.t("register"), "Usuario registrado (demo)")

    def set_language(self, lang):
        self.translator.load_language(lang)
        self.setWindowTitle(self.translator.t("register"))
        self.user_label.setText(self.translator.t("username"))
        self.pass_label.setText(self.translator.t("password"))
        self.register_btn.setText(self.translator.t("register"))
