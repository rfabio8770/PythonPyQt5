import sys
import csv
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QTableWidget, QTableWidgetItem, 
                             QLineEdit, QComboBox, QDateEdit, QLabel, QMessageBox,
                             QHeaderView, QGroupBox, QFormLayout, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont


class FinanzasPersonales(QMainWindow):
    def __init__(self):
        super().__init__()
        self.archivo_csv = "transacciones.csv"
        self.init_ui()
        self.cargar_datos()
        
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("Gestión de Finanzas Personales")
        self.setGeometry(100, 100, 1000, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Título
        titulo = QLabel("💰 Gestión de Finanzas Personales")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titulo)
        
        # Crear formulario de entrada
        self.crear_formulario(main_layout)
        
        # Crear botones de acción
        self.crear_botones(main_layout)
        
        # Crear tabla
        self.crear_tabla(main_layout)
        
        # Crear resumen financiero
        self.crear_resumen(main_layout)
        
    def crear_formulario(self, layout):
        """Crea el formulario para agregar/editar transacciones"""
        form_group = QGroupBox("Datos de la Transacción")
        form_layout = QFormLayout()
        
        # Campos del formulario
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setDate(QDate.currentDate())
        self.fecha_edit.setCalendarPopup(True)
        
        self.descripcion_edit = QLineEdit()
        self.descripcion_edit.setPlaceholderText("Ej: Pago de electricidad")
        
        self.categoria_combo = QComboBox()
        self.categoria_combo.addItems([
            "Servicios", "Alimentación", "Transporte", "Entretenimiento",
            "Salud", "Educación", "Ingresos", "Otros"
        ])
        self.categoria_combo.setEditable(True)
        
        self.monto_spin = QDoubleSpinBox()
        self.monto_spin.setRange(-999999.99, 999999.99)
        self.monto_spin.setDecimals(2)
        self.monto_spin.setSuffix(" Gs")
        
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Gasto", "Ingreso"])
        self.tipo_combo.currentTextChanged.connect(self.actualizar_signo_monto)
        
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Pagado", "No Pagado"])
        
        # Agregar campos al formulario
        form_layout.addRow("Fecha:", self.fecha_edit)
        form_layout.addRow("Descripción:", self.descripcion_edit)
        form_layout.addRow("Categoría:", self.categoria_combo)
        form_layout.addRow("Monto:", self.monto_spin)
        form_layout.addRow("Tipo:", self.tipo_combo)
        form_layout.addRow("Estado:", self.estado_combo)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
    def crear_botones(self, layout):
        """Crea los botones de acción CRUD"""
        buttons_layout = QHBoxLayout()
        
        self.btn_agregar = QPushButton("➕ Agregar")
        self.btn_agregar.clicked.connect(self.agregar_transaccion)
        
        self.btn_actualizar = QPushButton("✏️ Actualizar")
        self.btn_actualizar.clicked.connect(self.actualizar_transaccion)
        self.btn_actualizar.setEnabled(False)
        
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_transaccion)
        self.btn_eliminar.setEnabled(False)
        
        self.btn_limpiar = QPushButton("🔄 Limpiar")
        self.btn_limpiar.clicked.connect(self.limpiar_formulario)
        
        buttons_layout.addWidget(self.btn_agregar)
        buttons_layout.addWidget(self.btn_actualizar)
        buttons_layout.addWidget(self.btn_eliminar)
        buttons_layout.addWidget(self.btn_limpiar)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
    def crear_tabla(self, layout):
        """Crea la tabla para mostrar las transacciones"""
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Fecha", "Descripción", "Categoría", "Monto", "Tipo", "Estado"
        ])
        
        # Configurar el ancho de las columnas
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Fecha
        header.setSectionResizeMode(2, QHeaderView.Stretch)           # Descripción
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Categoría
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Monto
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Tipo
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Estado
        
        # Conectar selección de fila
        self.tabla.itemSelectionChanged.connect(self.seleccionar_fila)
        
        layout.addWidget(self.tabla)
        
    def crear_resumen(self, layout):
        """Crea el resumen financiero"""
        resumen_group = QGroupBox("Resumen Financiero")
        resumen_layout = QHBoxLayout()
        
        self.lbl_ingresos = QLabel("Ingresos: 0 Gs")
        self.lbl_gastos = QLabel("Gastos: 0 Gs")
        self.lbl_balance = QLabel("Balance: 0 Gs")
        self.lbl_pendientes = QLabel("Pagos Pendientes: 0 Gs")
        
        # Estilo para las etiquetas
        for lbl in [self.lbl_ingresos, self.lbl_gastos, self.lbl_balance, self.lbl_pendientes]:
            lbl.setFont(QFont("Arial", 10, QFont.Bold))
            
        resumen_layout.addWidget(self.lbl_ingresos)
        resumen_layout.addWidget(self.lbl_gastos)
        resumen_layout.addWidget(self.lbl_balance)
        resumen_layout.addWidget(self.lbl_pendientes)
        
        resumen_group.setLayout(resumen_layout)
        layout.addWidget(resumen_group)
        
    def actualizar_signo_monto(self):
        """Actualiza el signo del monto según el tipo de transacción"""
        if self.tipo_combo.currentText() == "Gasto":
            if self.monto_spin.value() > 0:
                self.monto_spin.setValue(-abs(self.monto_spin.value()))
        else:  # Ingreso
            if self.monto_spin.value() < 0:
                self.monto_spin.setValue(abs(self.monto_spin.value()))
                
    def inicializar_csv(self):
        """Crea el archivo CSV si no existe"""
        if not os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'fecha', 'descripcion', 'categoria', 'monto', 'tipo_transaccion', 'estado_pago'])
                
    def obtener_nuevo_id(self):
        """Obtiene el siguiente ID disponible"""
        try:
            with open(self.archivo_csv, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Saltar header
                ids = [int(row[0]) for row in reader if row]
                return max(ids) + 1 if ids else 1
        except (FileNotFoundError, ValueError):
            return 1
            
    def agregar_transaccion(self):
        """Agrega una nueva transacción (CREATE)"""
        if not self.validar_formulario():
            return
            
        self.inicializar_csv()
        
        nueva_transaccion = [
            self.obtener_nuevo_id(),
            self.fecha_edit.date().toString("yyyy-MM-dd"),
            self.descripcion_edit.text().strip(),
            self.categoria_combo.currentText(),
            self.monto_spin.value(),
            self.tipo_combo.currentText(),
            self.estado_combo.currentText()
        ]
        
        try:
            with open(self.archivo_csv, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(nueva_transaccion)
                
            self.cargar_datos()
            self.limpiar_formulario()
            QMessageBox.information(self, "Éxito", "Transacción agregada correctamente")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar transacción: {str(e)}")
            
    def cargar_datos(self):
        """Carga los datos del CSV a la tabla (READ)"""
        self.inicializar_csv()
        
        try:
            with open(self.archivo_csv, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                datos = list(reader)
                
            if len(datos) <= 1:  # Solo header o archivo vacío
                self.tabla.setRowCount(0)
                self.actualizar_resumen()
                return
                
            # Remover header
            datos = datos[1:]
            self.tabla.setRowCount(len(datos))
            
            for i, fila in enumerate(datos):
                for j, valor in enumerate(fila):
                    if j == 4:  # Columna monto
                        valor = f"{float(valor):,.2f} Gs"
                    item = QTableWidgetItem(str(valor))
                    self.tabla.setItem(i, j, item)
                    
            self.actualizar_resumen()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {str(e)}")
            
    def seleccionar_fila(self):
        """Maneja la selección de una fila en la tabla"""
        fila_actual = self.tabla.currentRow()
        
        if fila_actual >= 0:
            # Habilitar botones de actualizar y eliminar
            self.btn_actualizar.setEnabled(True)
            self.btn_eliminar.setEnabled(True)
            
            # Cargar datos en el formulario
            self.fecha_edit.setDate(QDate.fromString(self.tabla.item(fila_actual, 1).text(), "yyyy-MM-dd"))
            self.descripcion_edit.setText(self.tabla.item(fila_actual, 2).text())
            self.categoria_combo.setCurrentText(self.tabla.item(fila_actual, 3).text())
            
            # Convertir monto de vuelta a número
            monto_texto = self.tabla.item(fila_actual, 4).text().replace(" Gs", "").replace(",", "")
            self.monto_spin.setValue(float(monto_texto))
            
            self.tipo_combo.setCurrentText(self.tabla.item(fila_actual, 5).text())
            self.estado_combo.setCurrentText(self.tabla.item(fila_actual, 6).text())
        else:
            self.btn_actualizar.setEnabled(False)
            self.btn_eliminar.setEnabled(False)
            
    def actualizar_transaccion(self):
        """Actualiza la transacción seleccionada (UPDATE)"""
        fila_actual = self.tabla.currentRow()
        if fila_actual < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione una transacción para actualizar")
            return
            
        if not self.validar_formulario():
            return
            
        id_transaccion = self.tabla.item(fila_actual, 0).text()
        
        try:
            # Leer todas las transacciones
            with open(self.archivo_csv, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                datos = list(reader)
                
            # Actualizar la transacción específica
            for i, fila in enumerate(datos[1:], 1):  # Saltar header
                if fila[0] == id_transaccion:
                    datos[i] = [
                        id_transaccion,
                        self.fecha_edit.date().toString("yyyy-MM-dd"),
                        self.descripcion_edit.text().strip(),
                        self.categoria_combo.currentText(),
                        self.monto_spin.value(),
                        self.tipo_combo.currentText(),
                        self.estado_combo.currentText()
                    ]
                    break
                    
            # Escribir datos actualizados
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(datos)
                
            self.cargar_datos()
            self.limpiar_formulario()
            QMessageBox.information(self, "Éxito", "Transacción actualizada correctamente")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar transacción: {str(e)}")
            
    def eliminar_transaccion(self):
        """Elimina la transacción seleccionada (DELETE)"""
        fila_actual = self.tabla.currentRow()
        if fila_actual < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione una transacción para eliminar")
            return
            
        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self, "Confirmar eliminación",
            "¿Está seguro que desea eliminar esta transacción?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta != QMessageBox.Yes:
            return
            
        id_transaccion = self.tabla.item(fila_actual, 0).text()
        
        try:
            # Leer todas las transacciones
            with open(self.archivo_csv, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                datos = list(reader)
                
            # Filtrar la transacción a eliminar
            datos_filtrados = [datos[0]]  # Mantener header
            for fila in datos[1:]:
                if fila[0] != id_transaccion:
                    datos_filtrados.append(fila)
                    
            # Escribir datos filtrados
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(datos_filtrados)
                
            self.cargar_datos()
            self.limpiar_formulario()
            QMessageBox.information(self, "Éxito", "Transacción eliminada correctamente")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar transacción: {str(e)}")
            
    def validar_formulario(self):
        """Valida los datos del formulario"""
        if not self.descripcion_edit.text().strip():
            QMessageBox.warning(self, "Error de validación", "La descripción es obligatoria")
            return False
            
        if self.monto_spin.value() == 0:
            QMessageBox.warning(self, "Error de validación", "El monto no puede ser cero")
            return False
            
        return True
        
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.fecha_edit.setDate(QDate.currentDate())
        self.descripcion_edit.clear()
        self.categoria_combo.setCurrentIndex(0)
        self.monto_spin.setValue(0)
        self.tipo_combo.setCurrentIndex(0)
        self.estado_combo.setCurrentIndex(0)
        
        # Deshabilitar botones de actualizar y eliminar
        self.btn_actualizar.setEnabled(False)
        self.btn_eliminar.setEnabled(False)
        
        # Limpiar selección de tabla
        self.tabla.clearSelection()
        
    def actualizar_resumen(self):
        """Actualiza el resumen financiero"""
        try:
            with open(self.archivo_csv, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                datos = list(reader)
                
            if len(datos) <= 1:
                return
                
            ingresos = 0
            gastos = 0
            pendientes = 0
            
            for fila in datos[1:]:  # Saltar header
                if len(fila) >= 7:
                    monto = float(fila[4])
                    estado = fila[6]
                    
                    if monto > 0:
                        ingresos += monto
                    else:
                        gastos += abs(monto)
                        if estado == "No Pagado":
                            pendientes += abs(monto)
                            
            balance = ingresos - gastos
            
            self.lbl_ingresos.setText(f"Ingresos: {ingresos:,.2f} Gs")
            self.lbl_gastos.setText(f"Gastos: {gastos:,.2f} Gs")
            self.lbl_balance.setText(f"Balance: {balance:,.2f} Gs")
            self.lbl_pendientes.setText(f"Pagos Pendientes: {pendientes:,.2f} Gs")
            
            # Cambiar color del balance
            if balance >= 0:
                self.lbl_balance.setStyleSheet("color: green;")
            else:
                self.lbl_balance.setStyleSheet("color: red;")
                
        except Exception as e:
            print(f"Error al actualizar resumen: {e}")


def main():
    """Función principal para ejecutar la aplicación"""
    app = QApplication(sys.argv)
    ventana = FinanzasPersonales()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()