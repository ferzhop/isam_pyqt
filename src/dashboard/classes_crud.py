from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QLabel, QLineEdit, QFormLayout, QComboBox)
from PyQt5.QtCore import Qt
from data.storage import SimpleStorage
from data.translator import Translator
import os

class ClassesCRUD(QWidget):
    def __init__(self, parent=None, teachers_ref=None, translator=None):
        super().__init__(parent)
        self.translator = translator or Translator("es")
        self.storage = SimpleStorage(os.path.join(os.path.dirname(__file__), '../data/classes.txt'))
        self.classes = self.storage.load()
        self.teachers_ref = teachers_ref  # Referencia a lista de profesores
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout()
        self.add_btn = QPushButton(self.translator.t("add_class"))
        self.add_btn.clicked.connect(self.add_class)
        layout.addWidget(self.add_btn)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels([
            self.translator.t("class_name"),
            self.translator.t("class_teacher"),
            self.translator.t("action")
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.refresh_table()
    def refresh_table(self):
        self.classes = self.storage.load()
        self.table.setRowCount(0)
        for idx, c in enumerate(self.classes):
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(c["name"]))
            self.table.setItem(idx, 1, QTableWidgetItem(c["teacher"]))
            edit_btn = QPushButton(self.translator.t("edit"))
            delete_btn = QPushButton(self.translator.t("delete"))
            edit_btn.clicked.connect(lambda _, i=idx: self.edit_class(i))
            delete_btn.clicked.connect(lambda _, i=idx: self.delete_class(i))
            container = QWidget()
            hlayout = QHBoxLayout(container)
            hlayout.addWidget(edit_btn)
            hlayout.addWidget(delete_btn)
            hlayout.setContentsMargins(0,0,0,0)
            hlayout.setSpacing(4)
            self.table.setCellWidget(idx, 2, container)
    def add_class(self):
        dialog = ClassFormDialog(self, self.teachers_ref, None)
        if dialog.exec_():
            data = dialog.get_data()
            self.classes.append(data)
            self.storage.save(self.classes)
            self.refresh_table()
    def edit_class(self, idx):
        dialog = ClassFormDialog(self, self.teachers_ref, self.classes[idx])
        if dialog.exec_():
            self.classes[idx] = dialog.get_data()
            self.storage.save(self.classes)
            self.refresh_table()
    def delete_class(self, idx):
        confirm = QMessageBox.question(self, "Eliminar", "¿Eliminar esta clase?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.classes.pop(idx)
            self.storage.save(self.classes)
            self.refresh_table()
    def set_language(self, lang):
        self.translator.load_language(lang)
        self.add_btn.setText(self.translator.t("add_class"))
        self.table.setHorizontalHeaderLabels([
            self.translator.t("class_name"),
            self.translator.t("class_teacher"),
            self.translator.t("action")
        ])
        self.refresh_table()

class ClassFormDialog(QDialog):
    def __init__(self, parent=None, teachers_ref=None, class_data=None):
        super().__init__(parent)
        self.translator = getattr(parent, 'translator', None)
        self.setWindowTitle(self.tr_text("register_class", "Registrar/Editar Clase"))
        self.class_data = class_data
        self.teachers_ref = teachers_ref
        self.name_input = QLineEdit()
        self.teacher_combo = QComboBox()
        if teachers_ref:
            self.teacher_combo.addItems([t["name"] for t in teachers_ref.teachers])
        form = QFormLayout()
        form.addRow(self.tr_text("class_name", "Nombre de la clase"), self.name_input)
        form.addRow(self.tr_text("class_teacher", "Profesor"), self.teacher_combo)
        self.save_btn = QPushButton(self.tr_text("save", "Guardar"))
        self.save_btn.clicked.connect(self.accept)
        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)
        if class_data:
            self.name_input.setText(class_data["name"])
            idx = self.teacher_combo.findText(class_data["teacher"])
            if idx >= 0:
                self.teacher_combo.setCurrentIndex(idx)
    def tr_text(self, key, default):
        if self.translator:
            return self.translator.t(key)
        return default
    def get_data(self):
        return {"name": self.name_input.text(), "teacher": self.teacher_combo.currentText()}
