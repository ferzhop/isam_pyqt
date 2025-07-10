from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMenuBar, QAction, QHBoxLayout
from data.translator import Translator
from .teachers_crud import TeachersCRUD
from .classes_crud import ClassesCRUD
from .students_crud import StudentsCRUD

class Dashboard(QWidget):
    def __init__(self, parent=None, translator=None):
        super().__init__(parent)
        self.translator = translator or Translator("es")
        self.init_ui()

    def init_ui(self):
        # Menú de idioma solo en la barra superior
        self.menu_bar = QMenuBar(self)
        self.lang_menu = self.menu_bar.addMenu(self.translator.t("language"))
        self.action_es = QAction("Español", self)
        self.action_en = QAction("English", self)
        self.lang_menu.addAction(self.action_es)
        self.lang_menu.addAction(self.action_en)
        self.action_es.triggered.connect(lambda: self.set_language("es"))
        self.action_en.triggered.connect(lambda: self.set_language("en"))

        self.title = QLabel(self.translator.t("dashboard_title"))
        self.classes_btn = QPushButton(self.translator.t("classes"))
        self.students_btn = QPushButton(self.translator.t("students"))
        self.teachers_btn = QPushButton(self.translator.t("teachers"))
        self.logout_btn = QPushButton(self.translator.t("logout"))

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.classes_btn)
        nav_layout.addWidget(self.students_btn)
        nav_layout.addWidget(self.teachers_btn)
        nav_layout.addStretch(1)

        self.teachers_crud = TeachersCRUD(self, translator=self.translator)
        self.classes_crud = ClassesCRUD(self, teachers_ref=self.teachers_crud, translator=self.translator)
        self.students_crud = StudentsCRUD(self, classes_ref=self.classes_crud, translator=self.translator)
        self.classes_btn.clicked.connect(self.show_classes)
        self.students_btn.clicked.connect(self.show_students)
        self.teachers_btn.clicked.connect(self.show_teachers)

        self.content_layout = QVBoxLayout()
        self.content_layout.addWidget(self.title)

        layout = QVBoxLayout()
        layout.setMenuBar(self.menu_bar)
        layout.addLayout(nav_layout)
        layout.addLayout(self.content_layout)
        layout.addWidget(self.logout_btn)
        self.setLayout(layout)
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_content()
        self.content_layout.addWidget(self.title)

    def show_classes(self):
        self.clear_content()
        self.content_layout.addWidget(self.classes_crud)

    def show_students(self):
        self.clear_content()
        self.content_layout.addWidget(self.students_crud)

    def show_teachers(self):
        self.clear_content()
        self.content_layout.addWidget(self.teachers_crud)

    def clear_content(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                self.content_layout.removeWidget(widget)
                widget.setParent(None)

    def set_language(self, lang):
        self.translator.load_language(lang)
        self.lang_menu.setTitle(self.translator.t("language"))
        self.title.setText(self.translator.t("dashboard_title"))
        self.classes_btn.setText(self.translator.t("classes"))
        self.students_btn.setText(self.translator.t("students"))
        self.teachers_btn.setText(self.translator.t("teachers"))
        self.logout_btn.setText(self.translator.t("logout"))
        # Propagar idioma a los CRUDs
        self.teachers_crud.set_language(lang)
        self.classes_crud.set_language(lang)
        self.students_crud.set_language(lang)
