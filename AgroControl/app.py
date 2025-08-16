import sys
import csv
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QTableWidget, QTableWidgetItem, 
                             QDialog, QFormLayout, QLineEdit, QDateEdit, QComboBox,
                             QTextEdit, QMessageBox, QHeaderView, QLabel, QDoubleSpinBox,
                             QSpinBox, QFrame)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QIcon

class RegistroDialog(QDialog):
    """Dialog para crear/editar registros de producción agrícola"""
    
    def __init__(self, parent=None, registro=None):
        super().__init__(parent)
        self.registro = registro
        self.es_edicion = registro is not None
        self.setup_ui()
        
        if self.es_edicion:
            self.cargar_datos()
    
    def setup_ui(self):
        self.setWindowTitle("Editar Registro" if self.es_edicion else "Nuevo Registro")
        self.setFixedSize(400, 600)
        
        layout = QFormLayout()
        
        # Campos del formulario
        self.fecha_siembra = QDateEdit()
        self.fecha_siembra.setDate(QDate.currentDate())
        self.fecha_siembra.setCalendarPopup(True)
        
        self.fecha_cosecha = QDateEdit()
        self.fecha_cosecha.setDate(QDate.currentDate())
        self.fecha_cosecha.setCalendarPopup(True)
        
        self.cultivo = QLineEdit()
        self.variedad = QLineEdit()
        
        self.superficie = QDoubleSpinBox()
        self.superficie.setDecimals(2)
        self.superficie.setMinimum(0.01)
        self.superficie.setMaximum(999.99)
        self.superficie.setSuffix(" ha")
        
        self.cantidad = QSpinBox()
        self.cantidad.setMinimum(0)
        self.cantidad.setMaximum(999999)
        self.cantidad.setSuffix(" kg")
        
        self.precio_venta = QSpinBox()
        self.precio_venta.setMinimum(1)
        self.precio_venta.setMaximum(999999)
        self.precio_venta.setSuffix(" $/kg")
        
        self.costo_produccion = QSpinBox()
        self.costo_produccion.setMinimum(0)
        self.costo_produccion.setMaximum(999999999)
        self.costo_produccion.setSuffix(" $")
        
        self.estado = QComboBox()
        self.estado.addItems(["En proceso", "Vendido", "En almacén"])
        
        self.observaciones = QTextEdit()
        self.observaciones.setMaximumHeight(80)
        
        # Agregar campos al layout
        layout.addRow("Fecha de Siembra:", self.fecha_siembra)
        layout.addRow("Fecha de Cosecha:", self.fecha_cosecha)
        layout.addRow("Cultivo:", self.cultivo)
        layout.addRow("Variedad:", self.variedad)
        layout.addRow("Superficie:", self.superficie)
        layout.addRow("Cantidad Producida:", self.cantidad)
        layout.addRow("Precio de Venta:", self.precio_venta)
        layout.addRow("Costo de Producción:", self.costo_produccion)
        layout.addRow("Estado:", self.estado)
        layout.addRow("Observaciones:", self.observaciones)
        
        # Botones
        button_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_cancelar = QPushButton("Cancelar")
        
        button_layout.addWidget(self.btn_guardar)
        button_layout.addWidget(self.btn_cancelar)
        
        layout.addRow(button_layout)
        
        self.setLayout(layout)
        
        # Conectar señales
        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_cancelar.clicked.connect(self.reject)
    
    def cargar_datos(self):
        """Cargar datos existentes en el formulario"""
        if not self.registro:
            return
            
        self.fecha_siembra.setDate(QDate.fromString(self.registro[1], "yyyy-MM-dd"))
        self.fecha_cosecha.setDate(QDate.fromString(self.registro[2], "yyyy-MM-dd"))
        self.cultivo.setText(self.registro[3])
        self.variedad.setText(self.registro[4])
        self.superficie.setValue(float(self.registro[5]))
        self.cantidad.setValue(int(self.registro[6]))
        self.precio_venta.setValue(int(self.registro[7]))
        self.costo_produccion.setValue(int(self.registro[8]))
        self.estado.setCurrentText(self.registro[10])
        self.observaciones.setText(self.registro[11])
    
    def guardar(self):
        """Validar y guardar los datos"""
        if not self.validar_datos():
            return
        
        self.accept()
    
    def validar_datos(self):
        """Validar los datos del formulario"""
        if not self.cultivo.text().strip():
            QMessageBox.warning(self, "Error", "El campo 'Cultivo' es obligatorio")
            return False
        
        if not self.variedad.text().strip():
            QMessageBox.warning(self, "Error", "El campo 'Variedad' es obligatorio")
            return False
        
        fecha_siembra = self.fecha_siembra.date().toPyDate()
        fecha_cosecha = self.fecha_cosecha.date().toPyDate()
        
        if fecha_cosecha <= fecha_siembra:
            QMessageBox.warning(self, "Error", "La fecha de cosecha debe ser posterior a la fecha de siembra")
            return False
        
        return True
    
    def obtener_datos(self):
        """Obtener los datos del formulario"""
        ganancia_neta = (self.cantidad.value() * self.precio_venta.value()) - self.costo_produccion.value()
        
        return [
            self.fecha_siembra.date().toString("yyyy-MM-dd"),
            self.fecha_cosecha.date().toString("yyyy-MM-dd"),
            self.cultivo.text().strip(),
            self.variedad.text().strip(),
            str(self.superficie.value()),
            str(self.cantidad.value()),
            str(self.precio_venta.value()),
            str(self.costo_produccion.value()),
            str(ganancia_neta),
            self.observaciones.toPlainText().strip(),
            self.estado.currentText()
        ]

class ProduccionAgricolaApp(QMainWindow):
    """Aplicación principal para gestión de producción agrícola"""
    
    def __init__(self):
        super().__init__()
        self.archivo_csv = "produccion_agricola.csv"
        self.datos = []
        self.setup_ui()
        self.cargar_datos()
    
    def setup_ui(self):
        self.setWindowTitle("Sistema de Gestión de Producción Agrícola")
        self.setGeometry(100, 100, 1200, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel("Sistema de Gestión de Producción Agrícola")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("QLabel { color: #2E7D32; margin: 10px; }")
        layout.addWidget(titulo)
        
        # Frame para botones
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        
        # Botones de acción
        self.btn_nuevo = QPushButton("Nuevo Registro")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_actualizar = QPushButton("Actualizar Tabla")
        
        # Estilo de botones
        button_style = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        """
        
        for btn in [self.btn_nuevo, self.btn_editar, self.btn_eliminar, self.btn_actualizar]:
            btn.setStyleSheet(button_style)
        
        button_layout.addWidget(self.btn_nuevo)
        button_layout.addWidget(self.btn_editar)
        button_layout.addWidget(self.btn_eliminar)
        button_layout.addWidget(self.btn_actualizar)
        button_layout.addStretch()
        
        layout.addWidget(button_frame)
        
        # Tabla de datos
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(12)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "F. Siembra", "F. Cosecha", "Cultivo", "Variedad",
            "Superficie (ha)", "Cantidad (kg)", "Precio $/kg", "Costo Prod.",
            "Ganancia", "Observaciones", "Estado"
        ])
        
        # Configurar tabla
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.tabla)
        
        # Label de información
        self.label_info = QLabel("Registros cargados: 0")
        self.label_info.setStyleSheet("QLabel { color: #666; margin: 5px; }")
        layout.addWidget(self.label_info)
        
        central_widget.setLayout(layout)
        
        # Conectar señales
        self.btn_nuevo.clicked.connect(self.nuevo_registro)
        self.btn_editar.clicked.connect(self.editar_registro)
        self.btn_eliminar.clicked.connect(self.eliminar_registro)
        self.btn_actualizar.clicked.connect(self.cargar_datos)
    
    def crear_archivo_csv(self):
        """Crear archivo CSV con headers si no existe"""
        if not os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'id', 'fecha_siembra', 'fecha_cosecha', 'cultivo', 'variedad',
                    'superficie_hectareas', 'cantidad_producida_kg', 'precio_venta_kg',
                    'costo_produccion', 'ganancia_neta', 'observaciones', 'estado'
                ])
    
    def cargar_datos(self):
        """Cargar datos desde el archivo CSV"""
        self.crear_archivo_csv()
        self.datos = []
        
        try:
            with open(self.archivo_csv, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Saltar header
                for row in reader:
                    if len(row) >= 12:  # Verificar que tenga todos los campos
                        self.datos.append(row)
        except FileNotFoundError:
            pass
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {str(e)}")
        
        self.actualizar_tabla()
    
    def actualizar_tabla(self):
        """Actualizar la tabla con los datos cargados"""
        self.tabla.setRowCount(len(self.datos))
        
        for i, fila in enumerate(self.datos):
            for j, valor in enumerate(fila):
                item = QTableWidgetItem(str(valor))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.tabla.setItem(i, j, item)
        
        self.label_info.setText(f"Registros cargados: {len(self.datos)}")
    
    def guardar_datos(self):
        """Guardar todos los datos al archivo CSV"""
        try:
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Escribir header
                writer.writerow([
                    'id', 'fecha_siembra', 'fecha_cosecha', 'cultivo', 'variedad',
                    'superficie_hectareas', 'cantidad_producida_kg', 'precio_venta_kg',
                    'costo_produccion', 'ganancia_neta', 'observaciones', 'estado'
                ])
                # Escribir datos
                writer.writerows(self.datos)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar datos: {str(e)}")
    
    def obtener_nuevo_id(self):
        """Obtener el siguiente ID disponible"""
        if not self.datos:
            return 1
        return max(int(fila[0]) for fila in self.datos) + 1
    
    def nuevo_registro(self):
        """Crear un nuevo registro"""
        dialog = RegistroDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            nuevo_id = self.obtener_nuevo_id()
            datos_registro = dialog.obtener_datos()
            registro_completo = [str(nuevo_id)] + datos_registro
            
            self.datos.append(registro_completo)
            self.guardar_datos()
            self.actualizar_tabla()
            
            QMessageBox.information(self, "Éxito", "Registro creado correctamente")
    
    def editar_registro(self):
        """Editar el registro seleccionado"""
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un registro para editar")
            return
        
        registro_actual = self.datos[fila_seleccionada]
        dialog = RegistroDialog(self, registro_actual)
        
        if dialog.exec_() == QDialog.Accepted:
            datos_actualizados = dialog.obtener_datos()
            # Mantener el ID original
            registro_actualizado = [registro_actual[0]] + datos_actualizados
            
            self.datos[fila_seleccionada] = registro_actualizado
            self.guardar_datos()
            self.actualizar_tabla()
            
            QMessageBox.information(self, "Éxito", "Registro actualizado correctamente")
    
    def eliminar_registro(self):
        """Eliminar el registro seleccionado"""
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un registro para eliminar")
            return
        
        registro = self.datos[fila_seleccionada]
        respuesta = QMessageBox.question(
            self, "Confirmar Eliminación",
            f"¿Está seguro de eliminar el registro del cultivo '{registro[3]}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            del self.datos[fila_seleccionada]
            self.guardar_datos()
            self.actualizar_tabla()
            
            QMessageBox.information(self, "Éxito", "Registro eliminado correctamente")

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Producción Agrícola")
    
    ventana = ProduccionAgricolaApp()
    ventana.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()