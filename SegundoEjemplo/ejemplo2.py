import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox
)

class StudentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Notas de Estudiantes")
        self.resize(600, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Widgets de entrada
        form_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del alumno")
        self.note_inputs = [QLineEdit() for _ in range(4)]
        for i, note_input in enumerate(self.note_inputs):
            note_input.setPlaceholderText(f"Nota {i + 1}")

        self.add_button = QPushButton("Agregar")
        self.add_button.clicked.connect(self.add_student)

        form_layout.addWidget(self.name_input)
        for note_input in self.note_inputs:
            form_layout.addWidget(note_input)
        form_layout.addWidget(self.add_button)

        # Tabla de estudiantes
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Nombre", "Nota 1", "Nota 2", "Nota 3", "Nota 4"])

        # Botones de archivo
        file_buttons_layout = QHBoxLayout()
        self.open_button = QPushButton("Abrir CSV")
        self.open_button.clicked.connect(self.open_csv)
        self.save_button = QPushButton("Guardar CSV")
        self.save_button.clicked.connect(self.save_csv)
        self.new_button = QPushButton("Nuevo CSV")
        self.new_button.clicked.connect(self.new_csv)

        file_buttons_layout.addWidget(self.open_button)
        file_buttons_layout.addWidget(self.save_button)
        file_buttons_layout.addWidget(self.new_button)

        # Agregar widgets al layout principal
        layout.addLayout(form_layout)
        layout.addWidget(self.table)
        layout.addLayout(file_buttons_layout)

        # Configurar el widget central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_student(self):
        name = self.name_input.text()
        notes = [note_input.text() for note_input in self.note_inputs]

        if not name or any(not note.isdigit() for note in notes):
            QMessageBox.warning(self, "Error", "Por favor, ingrese un nombre y cuatro notas válidas (números).")
            return

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(name))
        for i, note in enumerate(notes):
            self.table.setItem(row_position, i + 1, QTableWidgetItem(note))

        self.name_input.clear()
        for note_input in self.note_inputs:
            note_input.clear()

    def open_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Abrir archivo CSV", "", "Archivos CSV (*.csv)")
        if path:
            with open(path, "r", newline='', encoding="utf-8") as file:
                reader = csv.reader(file)
                self.table.setRowCount(0)  # Limpiar tabla
                for row_data in reader:
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)
                    for column, data in enumerate(row_data):
                        self.table.setItem(row_position, column, QTableWidgetItem(data))

    def save_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo CSV", "", "Archivos CSV (*.csv)")
        if path:
            with open(path, "w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                for row in range(self.table.rowCount()):
                    row_data = [self.table.item(row, column).text() if self.table.item(row, column) else "" for column in range(self.table.columnCount())]
                    writer.writerow(row_data)

    def new_csv(self):
        self.table.setRowCount(0)
        QMessageBox.information(self, "Nuevo CSV", "Se ha creado un nuevo archivo CSV.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentApp()
    window.show()
    sys.exit(app.exec_())