from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMenuBar, QAction, QHBoxLayout
from data.translator import Translator
from .teachers_crud import TeachersCRUD
from .classes_crud import ClassesCRUD
from .students_crud import StudentsCRUD
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Dashboard(QWidget):
    def __init__(self, parent=None, translator=None):
        super().__init__(parent)
        self.translator = translator or Translator("es")
        self.init_ui()

    def init_ui(self):
        self.menu_bar = QMenuBar(self)
        # Elimina menús previos para evitar superposición
        self.menu_bar.clear()
        # Crea el menú de idioma correctamente
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

        self.dashboard_widget = QWidget()
        self.dashboard_layout = QVBoxLayout(self.dashboard_widget)
        self.dashboard_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.dashboard_layout.addWidget(self.dashboard_canvas)

        self.show_dashboard()

        self.action_dashboard = QAction(self.translator.t("dashboard_title"), self)
        self.menu_bar.addAction(self.action_dashboard)
        self.action_dashboard.triggered.connect(self.show_dashboard)

    def show_dashboard(self):
        self.clear_content()
        self.update_dashboard_charts()
        self.content_layout.addWidget(self.title)
        self.content_layout.addWidget(self.dashboard_widget)

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

    def update_dashboard_charts(self):
        from data.storage import DBStorage
        db = DBStorage()
        classes = db.get_classes()
        students = db.get_students()
        # 1. Porcentaje de alumnos por clase
        class_names = [c['name'] for c in classes]
        class_counts = []
        total_students = len(students)
        for c in classes:
            count = 0
            for s in students:
                student_classes = db.get_student_classes(s['id'])
                if any(sc['id'] == c['id'] for sc in student_classes):
                    count += 1
            class_counts.append(count)
        # 2. Clases con profesor asignado
        prof_labels = [self.translator.t('with_teacher'), self.translator.t('without_teacher')]
        with_prof = sum(1 for c in classes if c['teacher'])
        without_prof = len(classes) - with_prof
        prof_counts = [with_prof, without_prof]
        # Graficar
        fig = self.dashboard_canvas.figure
        fig.clear()
        ax1 = fig.add_subplot(121)
        if class_names:
            ax1.pie(class_counts, labels=class_names, autopct=lambda p: f'{p:.0f}%\n({int(p*total_students/100)})' if total_students else '0', startangle=90)
            ax1.set_title(self.translator.t('students_per_class'))
        else:
            ax1.text(0.5, 0.5, self.translator.t('no_classes'), ha='center', va='center')
        ax2 = fig.add_subplot(122)
        ax2.bar(prof_labels, prof_counts, color=['#1976d2', '#b0bec5'])
        ax2.set_title(self.translator.t('classes_with_teacher'))
        for i, v in enumerate(prof_counts):
            ax2.text(i, v + 0.1, str(v), ha='center')
        fig.tight_layout()
        self.dashboard_canvas.draw()

    def set_language(self, lang):
        self.translator.load_language(lang)
        self.lang_menu.setTitle(self.translator.t("language"))
        self.title.setText(self.translator.t("dashboard_title"))
        self.classes_btn.setText(self.translator.t("classes"))
        self.students_btn.setText(self.translator.t("students"))
        self.teachers_btn.setText(self.translator.t("teachers"))
        self.logout_btn.setText(self.translator.t("logout"))
        self.action_dashboard.setText(self.translator.t("dashboard_title"))
        self.update_dashboard_charts()
        # Propagar idioma a los CRUDs
        self.teachers_crud.set_language(lang)
        self.classes_crud.set_language(lang)
        self.students_crud.set_language(lang)
