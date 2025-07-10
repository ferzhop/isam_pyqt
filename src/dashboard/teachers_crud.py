from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QLabel, QLineEdit, QFormLayout, QComboBox, QMenuBar, QAction)
from PyQt5.QtCore import Qt
from data.storage import SimpleStorage
from data.translator import Translator
import os

class TeachersCRUD(QWidget):
    def __init__(self, parent=None, translator=None):
        super().__init__(parent)
        self.translator = translator or Translator("es")
        self.storage = SimpleStorage(os.path.join(os.path.dirname(__file__), '../data/teachers.txt'))
        self.teachers = self.storage.load()
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout()
        self.add_btn = QPushButton(self.translator.t("add_teacher"))
        self.add_btn.clicked.connect(self.add_teacher)
        layout.addWidget(self.add_btn)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels([
            self.translator.t("teacher_name"),
            self.translator.t("teacher_subject"),
            self.translator.t("action")
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.refresh_table()
    def refresh_table(self):
        self.teachers = self.storage.load()
        self.table.setRowCount(0)
        for idx, t in enumerate(self.teachers):
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(t["name"]))
            self.table.setItem(idx, 1, QTableWidgetItem(t["subject"]))
            edit_btn = QPushButton(self.translator.t("edit"))
            delete_btn = QPushButton(self.translator.t("delete"))
            edit_btn.clicked.connect(lambda _, i=idx: self.edit_teacher(i))
            delete_btn.clicked.connect(lambda _, i=idx: self.delete_teacher(i))
            container = QWidget()
            hlayout = QHBoxLayout(container)
            hlayout.addWidget(edit_btn)
            hlayout.addWidget(delete_btn)
            hlayout.setContentsMargins(0,0,0,0)
            hlayout.setSpacing(4)
            self.table.setCellWidget(idx, 2, container)
    def add_teacher(self):
        dialog = TeacherFormDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            self.teachers.append(data)
            self.storage.save(self.teachers)
            self.refresh_table()
    def edit_teacher(self, idx):
        dialog = TeacherFormDialog(self, self.teachers[idx])
        if dialog.exec_():
            self.teachers[idx] = dialog.get_data()
            self.storage.save(self.teachers)
            self.refresh_table()
    def delete_teacher(self, idx):
        confirm = QMessageBox.question(self, "Eliminar", "¿Eliminar este profesor?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.teachers.pop(idx)
            self.storage.save(self.teachers)
            self.refresh_table()
    def set_language(self, lang):
        self.translator.load_language(lang)
        self.add_btn.setText(self.translator.t("add_teacher"))
        self.table.setHorizontalHeaderLabels([
            self.translator.t("teacher_name"),
            self.translator.t("teacher_subject"),
            self.translator.t("action")
        ])
        self.refresh_table()

class TeacherFormDialog(QDialog):
    def __init__(self, parent=None, teacher_data=None):
        super().__init__(parent)
        self.translator = getattr(parent, 'translator', None)
        self.setWindowTitle(self.tr_text("register_teacher", "Registrar/Editar Profesor"))
        self.teacher_data = teacher_data
        self.name_input = QLineEdit()
        self.subject_input = QLineEdit()
        form = QFormLayout()
        form.addRow(self.tr_text("teacher_name", "Nombre del profesor"), self.name_input)
        form.addRow(self.tr_text("teacher_subject", "Especialidad"), self.subject_input)
        self.save_btn = QPushButton(self.tr_text("save", "Guardar"))
        self.save_btn.clicked.connect(self.accept)
        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)
        if teacher_data:
            self.name_input.setText(teacher_data["name"])
            self.subject_input.setText(teacher_data["subject"])
    def tr_text(self, key, default):
        if self.translator:
            return self.translator.t(key)
        return default
    def get_data(self):
        return {"name": self.name_input.text(), "subject": self.subject_input.text()}
