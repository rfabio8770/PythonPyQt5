import sys
import csv
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTableWidget, QTableWidgetItem, 
                             QPushButton, QDialog, QFormLayout, QLineEdit, 
                             QComboBox, QDateEdit, QTextEdit, QSpinBox,
                             QMessageBox, QHeaderView, QLabel, QGroupBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

class TaskManager:
    def __init__(self, csv_file='tareas_proyectos.csv'):
        self.csv_file = csv_file
        self.fieldnames = ['id', 'proyecto', 'tarea', 'descripcion', 'estado', 
                          'prioridad', 'fecha_inicio', 'fecha_fin', 'asignado_a', 
                          'estimacion_horas', 'horas_trabajadas', 'categoria']
        self.create_csv_if_not_exists()
    
    def create_csv_if_not_exists(self):
        """Crea el archivo CSV con headers si no existe"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
    
    def get_next_id(self):
        """Obtiene el siguiente ID disponible"""
        tasks = self.read_tasks()
        if not tasks:
            return 1
        return max(int(task['id']) for task in tasks) + 1
    
    def read_tasks(self):
        """Lee todas las tareas del archivo CSV"""
        tasks = []
        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                tasks = list(reader)
        except FileNotFoundError:
            pass
        return tasks
    
    def write_tasks(self, tasks):
        """Escribe todas las tareas al archivo CSV"""
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(tasks)
    
    def create_task(self, task_data):
        """Crea una nueva tarea"""
        task_data['id'] = str(self.get_next_id())
        tasks = self.read_tasks()
        tasks.append(task_data)
        self.write_tasks(tasks)
        return True
    
    def update_task(self, task_id, task_data):
        """Actualiza una tarea existente"""
        tasks = self.read_tasks()
        for i, task in enumerate(tasks):
            if task['id'] == str(task_id):
                task_data['id'] = str(task_id)
                tasks[i] = task_data
                self.write_tasks(tasks)
                return True
        return False
    
    def delete_task(self, task_id):
        """Elimina una tarea"""
        tasks = self.read_tasks()
        tasks = [task for task in tasks if task['id'] != str(task_id)]
        self.write_tasks(tasks)
        return True

class TaskDialog(QDialog):
    def __init__(self, parent=None, task_data=None):
        super().__init__(parent)
        self.task_data = task_data
        self.init_ui()
        if task_data:
            self.populate_fields()
    
    def init_ui(self):
        self.setWindowTitle('Nueva Tarea' if not self.task_data else 'Editar Tarea')
        self.setModal(True)
        self.resize(500, 600)
        
        layout = QVBoxLayout()
        
        # Formulario
        form_layout = QFormLayout()
        
        self.proyecto_edit = QLineEdit()
        self.tarea_edit = QLineEdit()
        self.descripcion_edit = QTextEdit()
        self.descripcion_edit.setMaximumHeight(100)
        
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(['Pendiente', 'En Progreso', 'Completado', 'Cancelado'])
        
        self.prioridad_combo = QComboBox()
        self.prioridad_combo.addItems(['Baja', 'Media', 'Alta', 'Crítica'])
        
        self.fecha_inicio_edit = QDateEdit()
        self.fecha_inicio_edit.setDate(QDate.currentDate())
        self.fecha_inicio_edit.setCalendarPopup(True)
        
        self.fecha_fin_edit = QDateEdit()
        self.fecha_fin_edit.setDate(QDate.currentDate().addDays(7))
        self.fecha_fin_edit.setCalendarPopup(True)
        
        self.asignado_edit = QLineEdit()
        
        self.estimacion_spin = QSpinBox()
        self.estimacion_spin.setRange(0, 1000)
        self.estimacion_spin.setSuffix(' horas')
        
        self.horas_trabajadas_spin = QSpinBox()
        self.horas_trabajadas_spin.setRange(0, 1000)
        self.horas_trabajadas_spin.setSuffix(' horas')
        
        self.categoria_combo = QComboBox()
        self.categoria_combo.addItems(['Frontend', 'Backend', 'Testing', 'DevOps', 
                                      'Diseño', 'Análisis', 'Documentación'])
        
        # Agregar campos al formulario
        form_layout.addRow('Proyecto:', self.proyecto_edit)
        form_layout.addRow('Tarea:', self.tarea_edit)
        form_layout.addRow('Descripción:', self.descripcion_edit)
        form_layout.addRow('Estado:', self.estado_combo)
        form_layout.addRow('Prioridad:', self.prioridad_combo)
        form_layout.addRow('Fecha Inicio:', self.fecha_inicio_edit)
        form_layout.addRow('Fecha Fin:', self.fecha_fin_edit)
        form_layout.addRow('Asignado a:', self.asignado_edit)
        form_layout.addRow('Estimación:', self.estimacion_spin)
        form_layout.addRow('Horas Trabajadas:', self.horas_trabajadas_spin)
        form_layout.addRow('Categoría:', self.categoria_combo)
        
        layout.addLayout(form_layout)
        
        # Botones
        button_layout = QHBoxLayout()
        self.save_button = QPushButton('Guardar')
        self.cancel_button = QPushButton('Cancelar')
        
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def populate_fields(self):
        """Llena los campos con los datos de la tarea"""
        if not self.task_data:
            return
        
        self.proyecto_edit.setText(self.task_data.get('proyecto', ''))
        self.tarea_edit.setText(self.task_data.get('tarea', ''))
        self.descripcion_edit.setPlainText(self.task_data.get('descripcion', ''))
        
        estado = self.task_data.get('estado', 'Pendiente')
        index = self.estado_combo.findText(estado)
        if index >= 0:
            self.estado_combo.setCurrentIndex(index)
        
        prioridad = self.task_data.get('prioridad', 'Media')
        index = self.prioridad_combo.findText(prioridad)
        if index >= 0:
            self.prioridad_combo.setCurrentIndex(index)
        
        try:
            fecha_inicio = datetime.strptime(self.task_data.get('fecha_inicio', ''), '%Y-%m-%d')
            self.fecha_inicio_edit.setDate(QDate(fecha_inicio.year, fecha_inicio.month, fecha_inicio.day))
        except:
            pass
        
        try:
            fecha_fin = datetime.strptime(self.task_data.get('fecha_fin', ''), '%Y-%m-%d')
            self.fecha_fin_edit.setDate(QDate(fecha_fin.year, fecha_fin.month, fecha_fin.day))
        except:
            pass
        
        self.asignado_edit.setText(self.task_data.get('asignado_a', ''))
        self.estimacion_spin.setValue(int(self.task_data.get('estimacion_horas', 0)))
        self.horas_trabajadas_spin.setValue(int(self.task_data.get('horas_trabajadas', 0)))
        
        categoria = self.task_data.get('categoria', 'Frontend')
        index = self.categoria_combo.findText(categoria)
        if index >= 0:
            self.categoria_combo.setCurrentIndex(index)
    
    def get_task_data(self):
        """Obtiene los datos del formulario"""
        return {
            'proyecto': self.proyecto_edit.text(),
            'tarea': self.tarea_edit.text(),
            'descripcion': self.descripcion_edit.toPlainText(),
            'estado': self.estado_combo.currentText(),
            'prioridad': self.prioridad_combo.currentText(),
            'fecha_inicio': self.fecha_inicio_edit.date().toString('yyyy-MM-dd'),
            'fecha_fin': self.fecha_fin_edit.date().toString('yyyy-MM-dd'),
            'asignado_a': self.asignado_edit.text(),
            'estimacion_horas': str(self.estimacion_spin.value()),
            'horas_trabajadas': str(self.horas_trabajadas_spin.value()),
            'categoria': self.categoria_combo.currentText()
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()
        self.init_ui()
        self.load_tasks()
    
    def init_ui(self):
        self.setWindowTitle('Gestor de Tareas de Proyectos Informáticos')
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Título
        title_label = QLabel('Gestor de Tareas de Proyectos Informáticos')
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.new_button = QPushButton('Nueva Tarea')
        self.edit_button = QPushButton('Editar Tarea')
        self.delete_button = QPushButton('Eliminar Tarea')
        self.refresh_button = QPushButton('Actualizar')
        
        self.new_button.clicked.connect(self.new_task)
        self.edit_button.clicked.connect(self.edit_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.refresh_button.clicked.connect(self.load_tasks)
        
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Tabla de tareas
        self.table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.table)
        
        # Estadísticas
        stats_group = QGroupBox('Estadísticas')
        stats_layout = QHBoxLayout()
        
        self.total_label = QLabel('Total: 0')
        self.pendientes_label = QLabel('Pendientes: 0')
        self.progreso_label = QLabel('En Progreso: 0')
        self.completadas_label = QLabel('Completadas: 0')
        
        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.pendientes_label)
        stats_layout.addWidget(self.progreso_label)
        stats_layout.addWidget(self.completadas_label)
        stats_layout.addStretch()
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        central_widget.setLayout(layout)
    
    def setup_table(self):
        """Configura la tabla de tareas"""
        headers = ['ID', 'Proyecto', 'Tarea', 'Descripción', 'Estado', 'Prioridad', 
                  'Fecha Inicio', 'Fecha Fin', 'Asignado', 'Est. Horas', 'Hrs. Trabajadas', 'Categoría']
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Configurar el header para que se ajuste
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # Permitir selección de filas completas
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Conectar doble clic para editar
        self.table.doubleClicked.connect(self.edit_task)
    
    def load_tasks(self):
        """Carga las tareas en la tabla"""
        tasks = self.task_manager.read_tasks()
        
        self.table.setRowCount(len(tasks))
        
        for row, task in enumerate(tasks):
            self.table.setItem(row, 0, QTableWidgetItem(task.get('id', '')))
            self.table.setItem(row, 1, QTableWidgetItem(task.get('proyecto', '')))
            self.table.setItem(row, 2, QTableWidgetItem(task.get('tarea', '')))
            self.table.setItem(row, 3, QTableWidgetItem(task.get('descripcion', '')))
            self.table.setItem(row, 4, QTableWidgetItem(task.get('estado', '')))
            self.table.setItem(row, 5, QTableWidgetItem(task.get('prioridad', '')))
            self.table.setItem(row, 6, QTableWidgetItem(task.get('fecha_inicio', '')))
            self.table.setItem(row, 7, QTableWidgetItem(task.get('fecha_fin', '')))
            self.table.setItem(row, 8, QTableWidgetItem(task.get('asignado_a', '')))
            self.table.setItem(row, 9, QTableWidgetItem(task.get('estimacion_horas', '')))
            self.table.setItem(row, 10, QTableWidgetItem(task.get('horas_trabajadas', '')))
            self.table.setItem(row, 11, QTableWidgetItem(task.get('categoria', '')))
        
        self.update_statistics(tasks)
    
    def update_statistics(self, tasks):
        """Actualiza las estadísticas"""
        total = len(tasks)
        pendientes = len([t for t in tasks if t.get('estado') == 'Pendiente'])
        progreso = len([t for t in tasks if t.get('estado') == 'En Progreso'])
        completadas = len([t for t in tasks if t.get('estado') == 'Completado'])
        
        self.total_label.setText(f'Total: {total}')
        self.pendientes_label.setText(f'Pendientes: {pendientes}')
        self.progreso_label.setText(f'En Progreso: {progreso}')
        self.completadas_label.setText(f'Completadas: {completadas}')
    
    def new_task(self):
        """Crea una nueva tarea"""
        dialog = TaskDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            if self.task_manager.create_task(task_data):
                QMessageBox.information(self, 'Éxito', 'Tarea creada correctamente')
                self.load_tasks()
            else:
                QMessageBox.critical(self, 'Error', 'Error al crear la tarea')
    
    def edit_task(self):
        """Edita la tarea seleccionada"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Advertencia', 'Seleccione una tarea para editar')
            return
        
        task_id = self.table.item(current_row, 0).text()
        tasks = self.task_manager.read_tasks()
        task_data = next((task for task in tasks if task['id'] == task_id), None)
        
        if task_data:
            dialog = TaskDialog(self, task_data)
            if dialog.exec_() == QDialog.Accepted:
                updated_data = dialog.get_task_data()
                if self.task_manager.update_task(task_id, updated_data):
                    QMessageBox.information(self, 'Éxito', 'Tarea actualizada correctamente')
                    self.load_tasks()
                else:
                    QMessageBox.critical(self, 'Error', 'Error al actualizar la tarea')
    
    def delete_task(self):
        """Elimina la tarea seleccionada"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Advertencia', 'Seleccione una tarea para eliminar')
            return
        
        task_id = self.table.item(current_row, 0).text()
        tarea_nombre = self.table.item(current_row, 2).text()
        
        reply = QMessageBox.question(self, 'Confirmar eliminación', 
                                   f'¿Está seguro de que desea eliminar la tarea "{tarea_nombre}"?',
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.task_manager.delete_task(task_id):
                QMessageBox.information(self, 'Éxito', 'Tarea eliminada correctamente')
                self.load_tasks()
            else:
                QMessageBox.critical(self, 'Error', 'Error al eliminar la tarea')

def main():
    app = QApplication(sys.argv)
    
    # Configurar estilo
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()