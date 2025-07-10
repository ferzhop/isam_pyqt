from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QLabel, QLineEdit, QFormLayout, QComboBox, QListWidget, QListWidgetItem, QAbstractItemView)
from PyQt5.QtCore import Qt
from data.storage import SimpleStorage
from data.translator import Translator
import os

class StudentsCRUD(QWidget):
    def __init__(self, parent=None, classes_ref=None, translator=None):
        super().__init__(parent)
        self.translator = translator or Translator("es")
        self.storage = SimpleStorage(os.path.join(os.path.dirname(__file__), '../data/students.txt'))
        self.students = self.storage.load()
        self.classes_ref = classes_ref
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
        self.students = self.storage.load()
        self.table.setRowCount(0)
        for idx, s in enumerate(self.students):
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(s["name"]))
            self.table.setItem(idx, 1, QTableWidgetItem(str(s["age"])))
            self.table.setItem(idx, 2, QTableWidgetItem(", ".join(s["classes"])))
            edit_btn = QPushButton(self.translator.t("edit"))
            delete_btn = QPushButton(self.translator.t("delete"))
            edit_btn.clicked.connect(lambda _, i=idx: self.edit_student(i))
            delete_btn.clicked.connect(lambda _, i=idx: self.delete_student(i))
            container = QWidget()
            hlayout = QHBoxLayout(container)
            hlayout.addWidget(edit_btn)
            hlayout.addWidget(delete_btn)
            hlayout.setContentsMargins(0,0,0,0)
            hlayout.setSpacing(4)
            self.table.setCellWidget(idx, 3, container)
    def add_student(self):
        dialog = StudentFormDialog(self, self.classes_ref, None)
        if dialog.exec_():
            data = dialog.get_data()
            self.students.append(data)
            self.storage.save(self.students)
            self.refresh_table()
    def edit_student(self, idx):
        dialog = StudentFormDialog(self, self.classes_ref, self.students[idx])
        if dialog.exec_():
            self.students[idx] = dialog.get_data()
            self.storage.save(self.students)
            self.refresh_table()
    def delete_student(self, idx):
        confirm = QMessageBox.question(self, "Eliminar", "¿Eliminar este alumno?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.students.pop(idx)
            self.storage.save(self.students)
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
    def __init__(self, parent=None, classes_ref=None, student_data=None):
        super().__init__(parent)
        self.translator = getattr(parent, 'translator', None)
        self.setWindowTitle(self.tr_text("register_student", "Registrar/Editar Alumno"))
        self.student_data = student_data
        self.classes_ref = classes_ref
        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.classes_list = QListWidget()
        self.classes_list.setSelectionMode(QAbstractItemView.MultiSelection)
        if classes_ref:
            for c in classes_ref.classes:
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
