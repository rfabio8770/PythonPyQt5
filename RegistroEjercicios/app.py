import sys
import csv
import os
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# ========================================
# 🧮 FUNCIONES PARA MANEJAR EL CSV
# ========================================

def crear_csv_si_no_existe():
    """Crea el archivo CSV con headers si no existe"""
    if not os.path.exists('ejercicios.csv'):
        with open('ejercicios.csv', 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['id', 'fecha', 'usuario', 'ejercicio', 'tipo', 
                           'minutos', 'intensidad', 'peso', 'calorias', 'notas'])
        print("✅ Archivo CSV creado!")

def calcular_calorias(tipo_ejercicio, minutos, intensidad, peso):
    """Calcula las calorías quemadas (¡matemáticas simples!)"""
    # Calorías base por minuto según tipo de ejercicio
    calorias_por_minuto = {
        'Cardio': 8,
        'Fuerza': 6,
        'Flexibilidad': 3,
        'HIIT': 12,
        'Natación': 10,
        'Ciclismo': 7
    }
    
    # Multiplicador según intensidad
    multiplicador_intensidad = {
        'Baja': 0.8,
        'Media': 1.0,
        'Alta': 1.3
    }
    
    calorias_base = calorias_por_minuto.get(tipo_ejercicio, 6)
    multiplicador = multiplicador_intensidad.get(intensidad, 1.0)
    
    # Fórmula simple: base * minutos * intensidad * (peso/70)
    # 70 es un peso promedio de referencia
    total = calorias_base * minutos * multiplicador * (peso / 70)
    return round(total)

def obtener_nuevo_id():
    """Obtiene el siguiente ID disponible"""
    try:
        with open('ejercicios.csv', 'r', encoding='utf-8') as archivo:
            reader = csv.reader(archivo)
            next(reader)  # Saltar header
            ids = []
            for fila in reader:
                if fila:  # Si la fila no está vacía
                    ids.append(int(fila[0]))
            
            return max(ids) + 1 if ids else 1
    except:
        return 1

def guardar_ejercicio(datos):
    """Guarda un nuevo ejercicio en el CSV"""
    try:
        # Calcular calorías automáticamente
        calorias = calcular_calorias(
            datos['tipo'], 
            datos['minutos'], 
            datos['intensidad'], 
            datos['peso']
        )
        
        with open('ejercicios.csv', 'a', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow([
                obtener_nuevo_id(),
                datos['fecha'],
                datos['usuario'],
                datos['ejercicio'],
                datos['tipo'],
                datos['minutos'],
                datos['intensidad'],
                datos['peso'],
                calorias,
                datos['notas']
            ])
        return True
    except Exception as e:
        print(f"❌ Error al guardar: {e}")
        return False

def leer_ejercicios():
    """Lee todos los ejercicios del CSV"""
    ejercicios = []
    try:
        with open('ejercicios.csv', 'r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                ejercicios.append(fila)
    except:
        pass
    return ejercicios

def eliminar_ejercicio(id_ejercicio):
    """Elimina un ejercicio por su ID"""
    ejercicios = leer_ejercicios()
    # Filtrar todos excepto el que queremos eliminar
    ejercicios_filtrados = [e for e in ejercicios if e['id'] != str(id_ejercicio)]
    
    # Reescribir el archivo
    try:
        with open('ejercicios.csv', 'w', newline='', encoding='utf-8') as archivo:
            if ejercicios_filtrados:
                writer = csv.DictWriter(archivo, fieldnames=ejercicios_filtrados[0].keys())
                writer.writeheader()
                writer.writerows(ejercicios_filtrados)
            else:
                # Si no hay ejercicios, crear headers vacíos
                writer = csv.writer(archivo)
                writer.writerow(['id', 'fecha', 'usuario', 'ejercicio', 'tipo', 
                               'minutos', 'intensidad', 'peso', 'calorias', 'notas'])
        return True
    except Exception as e:
        print(f"❌ Error al eliminar: {e}")
        return False

# ========================================
# 🎨 VENTANA PARA AGREGAR EJERCICIOS
# ========================================

class VentanaAgregarEjercicio(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("🏋️ Agregar Nuevo Ejercicio")
        self.setFixedSize(400, 450)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Título bonito
        titulo = QLabel("✨ Registra tu ejercicio")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setStyleSheet("color: #2E86C1; margin: 10px;")
        layout.addWidget(titulo)
        
        # Formulario
        form_layout = QFormLayout()
        
        # Campo Usuario
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Tu nombre...")
        form_layout.addRow("👤 Usuario:", self.usuario_input)
        
        # Campo Ejercicio
        self.ejercicio_input = QLineEdit()
        self.ejercicio_input.setPlaceholderText("Ej: Correr, Flexiones, Sentadillas...")
        form_layout.addRow("🏃 Ejercicio:", self.ejercicio_input)
        
        # Tipo de ejercicio
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(['Cardio', 'Fuerza', 'Flexibilidad', 'HIIT', 'Natación', 'Ciclismo'])
        form_layout.addRow("📋 Tipo:", self.tipo_combo)
        
        # Duración
        self.minutos_spin = QSpinBox()
        self.minutos_spin.setRange(1, 300)
        self.minutos_spin.setValue(30)
        self.minutos_spin.setSuffix(" min")
        form_layout.addRow("⏱️ Duración:", self.minutos_spin)
        
        # Intensidad
        self.intensidad_combo = QComboBox()
        self.intensidad_combo.addItems(['Baja', 'Media', 'Alta'])
        self.intensidad_combo.setCurrentText('Media')
        form_layout.addRow("🔥 Intensidad:", self.intensidad_combo)
        
        # Peso
        self.peso_spin = QDoubleSpinBox()
        self.peso_spin.setRange(30.0, 200.0)
        self.peso_spin.setValue(70.0)
        self.peso_spin.setSuffix(" kg")
        form_layout.addRow("⚖️ Tu peso:", self.peso_spin)
        
        # Notas
        self.notas_input = QTextEdit()
        self.notas_input.setMaximumHeight(60)
        self.notas_input.setPlaceholderText("Algo que quieras recordar...")
        form_layout.addRow("📝 Notas:", self.notas_input)
        
        layout.addLayout(form_layout)
        
        # Botones
        botones_layout = QHBoxLayout()
        
        btn_guardar = QPushButton("💾 Guardar")
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ECC71;
            }
        """)
        btn_guardar.clicked.connect(self.guardar_ejercicio)
        
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        btn_cancelar.clicked.connect(self.reject)
        
        botones_layout.addWidget(btn_guardar)
        botones_layout.addWidget(btn_cancelar)
        layout.addLayout(botones_layout)
        
        self.setLayout(layout)
    
    def guardar_ejercicio(self):
        # Validar que los campos importantes no estén vacíos
        if not self.usuario_input.text().strip():
            QMessageBox.warning(self, "❌ Error", "¡Necesitas escribir tu nombre!")
            return
        
        if not self.ejercicio_input.text().strip():
            QMessageBox.warning(self, "❌ Error", "¡Necesitas escribir qué ejercicio hiciste!")
            return
        
        # Crear diccionario con los datos
        datos = {
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'usuario': self.usuario_input.text().strip(),
            'ejercicio': self.ejercicio_input.text().strip(),
            'tipo': self.tipo_combo.currentText(),
            'minutos': self.minutos_spin.value(),
            'intensidad': self.intensidad_combo.currentText(),
            'peso': self.peso_spin.value(),
            'notas': self.notas_input.toPlainText().strip()
        }
        
        # Guardar
        if guardar_ejercicio(datos):
            QMessageBox.information(self, "🎉 ¡Éxito!", "¡Ejercicio guardado correctamente!")
            self.accept()
        else:
            QMessageBox.critical(self, "❌ Error", "No se pudo guardar el ejercicio")

# ========================================
# 🖥️ VENTANA PRINCIPAL
# ========================================

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cargar_ejercicios()
    
    def init_ui(self):
        self.setWindowTitle("🏋️ Mi Registro de Ejercicios")
        self.setGeometry(100, 100, 1000, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Título súper llamativo
        titulo = QLabel("🏋️ MI GIMNASIO DIGITAL")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Arial", 18, QFont.Bold))
        titulo.setStyleSheet("""
            QLabel {
                color: #8E44AD;
                background-color: #F8F9FA;
                padding: 15px;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        layout.addWidget(titulo)
        
        # Barra de botones
        botones_layout = QHBoxLayout()
        
        btn_agregar = QPushButton("➕ Agregar Ejercicio")
        btn_agregar.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        btn_agregar.clicked.connect(self.abrir_ventana_agregar)
        
        btn_actualizar = QPushButton("🔄 Actualizar")
        btn_actualizar.setStyleSheet("""
            QPushButton {
                background-color: #F39C12;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E67E22;
            }
        """)
        btn_actualizar.clicked.connect(self.cargar_ejercicios)
        
        btn_eliminar = QPushButton("🗑️ Eliminar Seleccionado")
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        btn_eliminar.clicked.connect(self.eliminar_ejercicio)
        
        botones_layout.addWidget(btn_agregar)
        botones_layout.addWidget(btn_actualizar)
        botones_layout.addWidget(btn_eliminar)
        botones_layout.addStretch()  # Esto empuja los botones a la izquierda
        
        layout.addLayout(botones_layout)
        
        # Tabla de ejercicios
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(10)
        headers = ['ID', 'Fecha', '👤 Usuario', '🏃 Ejercicio', '📋 Tipo', 
                  '⏱️ Min', '🔥 Intensidad', '⚖️ Peso', '🔥 Calorías', '📝 Notas']
        self.tabla.setHorizontalHeaderLabels(headers)
        
        # Estilo de la tabla
        self.tabla.setStyleSheet("""
            QTableWidget {
                gridline-color: #BDC3C7;
                background-color: white;
                alternate-background-color: #F8F9FA;
            }
            QHeaderView::section {
                background-color: #34495E;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla)
        
        # Estadísticas en la parte inferior
        self.stats_label = QLabel("📊 Cargando estadísticas...")
        self.stats_label.setStyleSheet("""
            QLabel {
                background-color: #2C3E50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.stats_label)
        
        central_widget.setLayout(layout)
    
    def abrir_ventana_agregar(self):
        ventana_agregar = VentanaAgregarEjercicio()
        if ventana_agregar.exec_() == QDialog.Accepted:
            self.cargar_ejercicios()  # Recargar la tabla
    
    def cargar_ejercicios(self):
        ejercicios = leer_ejercicios()
        
        self.tabla.setRowCount(len(ejercicios))
        
        total_calorias = 0
        total_minutos = 0
        
        for row, ejercicio in enumerate(ejercicios):
            self.tabla.setItem(row, 0, QTableWidgetItem(ejercicio['id']))
            self.tabla.setItem(row, 1, QTableWidgetItem(ejercicio['fecha']))
            self.tabla.setItem(row, 2, QTableWidgetItem(ejercicio['usuario']))
            self.tabla.setItem(row, 3, QTableWidgetItem(ejercicio['ejercicio']))
            self.tabla.setItem(row, 4, QTableWidgetItem(ejercicio['tipo']))
            self.tabla.setItem(row, 5, QTableWidgetItem(ejercicio['minutos']))
            self.tabla.setItem(row, 6, QTableWidgetItem(ejercicio['intensidad']))
            self.tabla.setItem(row, 7, QTableWidgetItem(ejercicio['peso']))
            self.tabla.setItem(row, 8, QTableWidgetItem(ejercicio['calorias']))
            self.tabla.setItem(row, 9, QTableWidgetItem(ejercicio['notas']))
            
            # Sumar para estadísticas
            try:
                total_calorias += int(ejercicio['calorias'])
                total_minutos += int(ejercicio['minutos'])
            except:
                pass
        
        # Actualizar estadísticas
        if ejercicios:
            self.stats_label.setText(
                f"📊 Total: {len(ejercicios)} ejercicios | "
                f"🔥 {total_calorias} calorías quemadas | "
                f"⏱️ {total_minutos} minutos entrenados | "
                f"💪 ¡Sigue así!"
            )
        else:
            self.stats_label.setText("📊 No hay ejercicios registrados. ¡Agrega tu primer ejercicio! 💪")
        
        # Ajustar columnas automáticamente
        self.tabla.resizeColumnsToContents()
    
    def eliminar_ejercicio(self):
        fila_actual = self.tabla.currentRow()
        
        if fila_actual == -1:
            QMessageBox.warning(self, "⚠️ Aviso", "¡Selecciona un ejercicio de la tabla!")
            return
        
        # Obtener el ID del ejercicio seleccionado
        id_ejercicio = int(self.tabla.item(fila_actual, 0).text())
        ejercicio_nombre = self.tabla.item(fila_actual, 3).text()
        
        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self, 
            "❓ Confirmar", 
            f"¿Seguro que quieres eliminar '{ejercicio_nombre}'?\n\n¡No se puede deshacer!",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            if eliminar_ejercicio(id_ejercicio):
                QMessageBox.information(self, "🎉 ¡Listo!", "Ejercicio eliminado correctamente")
                self.cargar_ejercicios()  # Recargar tabla
            else:
                QMessageBox.critical(self, "❌ Error", "No se pudo eliminar el ejercicio")

# ========================================
# 🚀 FUNCIÓN PRINCIPAL
# ========================================

def main():
    # Crear la aplicación
    app = QApplication(sys.argv)
    
    # Crear el archivo CSV si no existe
    crear_csv_si_no_existe()
    
    # Crear y mostrar la ventana principal
    ventana = VentanaPrincipal()
    ventana.show()
    
    print("🚀 ¡Aplicación iniciada! Registro de ejercicios listo para usar.")
    
    # Ejecutar la aplicación
    sys.exit(app.exec_())

# ========================================
# ✨ AQUÍ EMPIEZA TODO
# ========================================

if __name__ == "__main__":
    main()