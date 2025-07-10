from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
import sys
from auth.login_form import LoginForm
from auth.register_form import RegisterForm
from dashboard.dashboard import Dashboard
from data.translator import Translator

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ISAM School Management System")
        self.setGeometry(100, 100, 800, 600)
        self.translator = Translator("es")

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.login_form = LoginForm(self, self.translator)
        self.register_form = RegisterForm(self, self.translator)
        self.dashboard = Dashboard(self, self.translator)

        self.stacked_widget.addWidget(self.login_form)
        self.stacked_widget.addWidget(self.register_form)
        self.stacked_widget.addWidget(self.dashboard)

        self.login_form.login_successful.connect(self.show_dashboard)
        self.dashboard.logout_btn.clicked.connect(self.show_login)
        self.login_form.login_btn.clicked.connect(self.check_register)
        self.dashboard.action_es.triggered.connect(lambda: self.set_language("es"))
        self.dashboard.action_en.triggered.connect(lambda: self.set_language("en"))

    def show_dashboard(self, token=None):
        self.stacked_widget.setCurrentWidget(self.dashboard)

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_form)

    def check_register(self):
        if self.login_form.user_input.text() == "" and self.login_form.pass_input.text() == "":
            self.stacked_widget.setCurrentWidget(self.register_form)

    def set_language(self, lang):
        self.translator.load_language(lang)
        self.login_form.set_language(lang)
        self.register_form.set_language(lang)
        self.dashboard.set_language(lang)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Cargar y aplicar estilos QSS globales
    import os
    qss_path = os.path.join(os.path.dirname(__file__), "resources", "styles.qss")
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"No se pudo cargar el archivo de estilos: {e}")
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
