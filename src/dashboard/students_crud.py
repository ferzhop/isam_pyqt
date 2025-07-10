from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QLabel, QLineEdit, QFormLayout, QComboBox, QListWidget, QListWidgetItem, QAbstractItemView)
from PyQt5.QtCore import Qt
from data.storage import DBStorage
from data.translator import Translator
import os

class StudentsCRUD(QWidget):
    def __init__(self, parent=None, classes_ref=None, translator=None):
        super().__init__(parent)
        self.translator = translator or Translator("es")
        self.db = DBStorage()
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout()
        self.add_btn = QPushButton(self.translator.t("add_student"))
        self.add_btn.clicked.connect(self.add_student)
        layout.addWidget(self.add_btn)
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels([
            self.translator.t("student_name"),
            self.translator.t("student_age"),
            self.translator.t("student_classes"),
            self.translator.t("action")
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.refresh_table()
    def refresh_table(self):
        students = self.db.get_students()
        classes = self.db.get_classes()
        self.table.setRowCount(0)
        for idx, s in enumerate(students):
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(s["name"]))
            self.table.setItem(idx, 1, QTableWidgetItem(str(s["age"])))
            # Obtener nombres de clases asociadas
            student_classes = self.db.get_student_classes(s["id"])
            class_names = [c["name"] for c in student_classes]
            self.table.setItem(idx, 2, QTableWidgetItem(", ".join(class_names)))
            edit_btn = QPushButton(self.translator.t("edit"))
            delete_btn = QPushButton(self.translator.t("delete"))
            edit_btn.clicked.connect(lambda _, i=s["id"]: self.edit_student(i))
            delete_btn.clicked.connect(lambda _, i=s["id"]: self.delete_student(i))
            container = QWidget()
            hlayout = QHBoxLayout(container)
            hlayout.addWidget(edit_btn)
            hlayout.addWidget(delete_btn)
            hlayout.setContentsMargins(0,0,0,0)
            hlayout.setSpacing(4)
            self.table.setCellWidget(idx, 3, container)
    def add_student(self):
        classes = self.db.get_classes()
        dialog = StudentFormDialog(self, classes, None)
        if dialog.exec_():
            data = dialog.get_data()
            student_id = self.db.add_student(data["name"], data["age"])
            # Guardar relación alumno-clase
            class_ids = [c["id"] for c in classes if c["name"] in data["classes"]]
            self.db.set_student_classes(student_id, class_ids)
            self.refresh_table()
    def edit_student(self, student_id):
        students = self.db.get_students()
        student = next((s for s in students if s["id"] == student_id), None)
        if not student:
            return
        classes = self.db.get_classes()
        # Obtener clases asociadas
        student_classes = self.db.get_student_classes(student_id)
        class_names = [c["name"] for c in student_classes]
        student_data = {"name": student["name"], "age": student["age"], "classes": class_names}
        dialog = StudentFormDialog(self, classes, student_data)
        if dialog.exec_():
            data = dialog.get_data()
            self.db.update_student(student_id, data["name"], data["age"])
            class_ids = [c["id"] for c in classes if c["name"] in data["classes"]]
            self.db.set_student_classes(student_id, class_ids)
            self.refresh_table()
    def delete_student(self, student_id):
        confirm = QMessageBox.question(self, self.translator.t("delete"), self.translator.t("delete")+"?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.db.delete_student(student_id)
            self.refresh_table()
    def set_language(self, lang):
        self.translator.load_language(lang)
        self.add_btn.setText(self.translator.t("add_student"))
        self.table.setHorizontalHeaderLabels([
            self.translator.t("student_name"),
            self.translator.t("student_age"),
            self.translator.t("student_classes"),
            self.translator.t("action")
        ])
        self.refresh_table()

class StudentFormDialog(QDialog):
    def __init__(self, parent=None, classes=None, student_data=None):
        super().__init__(parent)
        self.translator = getattr(parent, 'translator', None)
        self.setWindowTitle(self.tr_text("register_student", "Registrar/Editar Alumno"))
        self.student_data = student_data
        self.classes = classes or []
        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.classes_list = QListWidget()
        self.classes_list.setSelectionMode(QAbstractItemView.MultiSelection)
        for c in self.classes:
            item = QListWidgetItem(c["name"])
            self.classes_list.addItem(item)
        form = QFormLayout()
        form.addRow(self.tr_text("student_name", "Nombre del alumno"), self.name_input)
        form.addRow(self.tr_text("student_age", "Edad"), self.age_input)
        form.addRow(self.tr_text("student_classes", "Clases"), self.classes_list)
        self.save_btn = QPushButton(self.tr_text("save", "Guardar"))
        self.save_btn.clicked.connect(self.accept)
        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)
        if student_data:
            self.name_input.setText(student_data["name"])
            self.age_input.setText(str(student_data["age"]))
            for i in range(self.classes_list.count()):
                if self.classes_list.item(i).text() in student_data["classes"]:
                    self.classes_list.item(i).setSelected(True)
    def tr_text(self, key, default):
        if self.translator:
            return self.translator.t(key)
        return default
    def get_data(self):
        selected_classes = [item.text() for item in self.classes_list.selectedItems()]
        return {"name": self.name_input.text(), "age": int(self.age_input.text()), "classes": selected_classes}
