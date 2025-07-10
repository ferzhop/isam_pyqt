import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'isam.db')

class DBStorage:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()
    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            teacher_id INTEGER,
            FOREIGN KEY(teacher_id) REFERENCES teachers(id)
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS student_classes (
            student_id INTEGER,
            class_id INTEGER,
            PRIMARY KEY(student_id, class_id),
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(class_id) REFERENCES classes(id)
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')
        self.conn.commit()
    # --- TEACHERS ---
    def get_teachers(self):
        c = self.conn.cursor()
        c.execute('SELECT id, name, subject FROM teachers')
        return [{'id': row[0], 'name': row[1], 'subject': row[2]} for row in c.fetchall()]
    def add_teacher(self, name, subject):
        c = self.conn.cursor()
        c.execute('INSERT INTO teachers (name, subject) VALUES (?, ?)', (name, subject))
        self.conn.commit()
    def update_teacher(self, id, name, subject):
        c = self.conn.cursor()
        c.execute('UPDATE teachers SET name=?, subject=? WHERE id=?', (name, subject, id))
        self.conn.commit()
    def delete_teacher(self, id):
        c = self.conn.cursor()
        c.execute('DELETE FROM teachers WHERE id=?', (id,))
        self.conn.commit()
    # --- CLASSES ---
    def get_classes(self):
        c = self.conn.cursor()
        c.execute('''SELECT classes.id, classes.name, teachers.name FROM classes LEFT JOIN teachers ON classes.teacher_id = teachers.id''')
        return [{'id': row[0], 'name': row[1], 'teacher': row[2] or ''} for row in c.fetchall()]
    def add_class(self, name, teacher_id):
        c = self.conn.cursor()
        c.execute('INSERT INTO classes (name, teacher_id) VALUES (?, ?)', (name, teacher_id))
        self.conn.commit()
    def update_class(self, id, name, teacher_id):
        c = self.conn.cursor()
        c.execute('UPDATE classes SET name=?, teacher_id=? WHERE id=?', (name, teacher_id, id))
        self.conn.commit()
    def delete_class(self, id):
        c = self.conn.cursor()
        c.execute('DELETE FROM classes WHERE id=?', (id,))
        self.conn.commit()
    # --- STUDENTS ---
    def get_students(self):
        c = self.conn.cursor()
        c.execute('SELECT id, name, age FROM students')
        return [{'id': row[0], 'name': row[1], 'age': row[2]} for row in c.fetchall()]
    def add_student(self, name, age):
        c = self.conn.cursor()
        c.execute('INSERT INTO students (name, age) VALUES (?, ?)', (name, age))
        student_id = c.lastrowid
        self.conn.commit()
        return student_id
    def update_student(self, id, name, age):
        c = self.conn.cursor()
        c.execute('UPDATE students SET name=?, age=? WHERE id=?', (name, age, id))
        self.conn.commit()
    def delete_student(self, id):
        c = self.conn.cursor()
        c.execute('DELETE FROM students WHERE id=?', (id,))
        c.execute('DELETE FROM student_classes WHERE student_id=?', (id,))
        self.conn.commit()
    # --- STUDENT_CLASSES ---
    def get_student_classes(self, student_id):
        c = self.conn.cursor()
        c.execute('''SELECT classes.id, classes.name FROM student_classes JOIN classes ON student_classes.class_id = classes.id WHERE student_classes.student_id=?''', (student_id,))
        return [{'id': row[0], 'name': row[1]} for row in c.fetchall()]
    def set_student_classes(self, student_id, class_ids):
        c = self.conn.cursor()
        c.execute('DELETE FROM student_classes WHERE student_id=?', (student_id,))
        for class_id in class_ids:
            c.execute('INSERT INTO student_classes (student_id, class_id) VALUES (?, ?)', (student_id, class_id))
        self.conn.commit()
    # --- USERS ---
    def create_admin_user(self):
        import hashlib
        c = self.conn.cursor()
        # Crea la tabla de usuarios si no existe
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')
        # Verifica si el usuario admin ya existe
        c.execute('SELECT * FROM users WHERE username=?', ("ISAM",))
        if not c.fetchone():
            # Guardar contraseña codificada (sha256)
            password_hash = hashlib.sha256("Am3l1a".encode()).hexdigest()
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ("ISAM", password_hash))
            self.conn.commit()
    def verify_user(self, username, password):
        import hashlib
        c = self.conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password_hash))
        return c.fetchone() is not None
