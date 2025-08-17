import sys
import csv
import os
from datetime import datetime, date
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QListWidget, QListWidgetItem, QPushButton,
                             QLineEdit, QTextEdit, QComboBox, QLabel, QMessageBox,
                             QDateTimeEdit, QCheckBox, QSplitter, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont

class AgendaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.archivo_csv = "agenda.csv"
        self.datos = []
        self.elemento_seleccionado = None
        
        # Crear archivo CSV si no existe
        self.crear_archivo_si_no_existe()
        
        # Configurar interfaz
        self.configurar_ventana()
        self.crear_interfaz()
        self.cargar_datos()
        
    def crear_archivo_si_no_existe(self):
        """Crea el archivo CSV con encabezados si no existe"""
        if not os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(['id', 'tipo', 'titulo', 'contenido', 'fecha_creacion', 
                                 'fecha_recordatorio', 'completado'])
                
    def configurar_ventana(self):
        """Configura la ventana principal"""
        self.setWindowTitle("Mi Agenda Personal - Notas y Recordatorios")
        self.setGeometry(100, 100, 900, 600)
        self.setMinimumSize(700, 500)
        
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Layout principal horizontal
        layout_principal = QHBoxLayout(widget_central)
        
        # Crear splitter para redimensionar
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo - Lista y controles
        panel_izquierdo = self.crear_panel_izquierdo()
        splitter.addWidget(panel_izquierdo)
        
        # Panel derecho - Formulario
        panel_derecho = self.crear_panel_derecho()
        splitter.addWidget(panel_derecho)
        
        # Configurar tamaños del splitter
        splitter.setSizes([400, 500])
        layout_principal.addWidget(splitter)
        
    def crear_panel_izquierdo(self):
        """Crea el panel con la lista y botones de control"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Título
        titulo = QLabel("📝 Lista de Elementos")
        titulo.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(titulo)
        
        # Filtros
        grupo_filtros = QGroupBox("Filtros")
        layout_filtros = QHBoxLayout(grupo_filtros)
        
        self.combo_filtro_tipo = QComboBox()
        self.combo_filtro_tipo.addItems(["Todos", "Notas", "Recordatorios"])
        self.combo_filtro_tipo.currentTextChanged.connect(self.aplicar_filtros)
        
        self.combo_filtro_estado = QComboBox()
        self.combo_filtro_estado.addItems(["Todos", "Pendientes", "Completados"])
        self.combo_filtro_estado.currentTextChanged.connect(self.aplicar_filtros)
        
        layout_filtros.addWidget(QLabel("Tipo:"))
        layout_filtros.addWidget(self.combo_filtro_tipo)
        layout_filtros.addWidget(QLabel("Estado:"))
        layout_filtros.addWidget(self.combo_filtro_estado)
        
        layout.addWidget(grupo_filtros)
        
        # Lista de elementos
        self.lista_elementos = QListWidget()
        self.lista_elementos.itemClicked.connect(self.seleccionar_elemento)
        layout.addWidget(self.lista_elementos)
        
        # Botones de control
        layout_botones = QHBoxLayout()
        
        btn_nuevo = QPushButton("➕ Nuevo")
        btn_nuevo.clicked.connect(self.nuevo_elemento)
        
        btn_eliminar = QPushButton("🗑️ Eliminar")
        btn_eliminar.clicked.connect(self.eliminar_elemento)
        
        btn_completar = QPushButton("✅ Completar")
        btn_completar.clicked.connect(self.marcar_completado)
        
        layout_botones.addWidget(btn_nuevo)
        layout_botones.addWidget(btn_eliminar)
        layout_botones.addWidget(btn_completar)
        
        layout.addLayout(layout_botones)
        
        return widget
        
    def crear_panel_derecho(self):
        """Crea el panel con el formulario de edición"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Título del formulario
        self.titulo_formulario = QLabel("📄 Nuevo Elemento")
        self.titulo_formulario.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(self.titulo_formulario)
        
        # Formulario
        grupo_form = QGroupBox()
        form_layout = QFormLayout(grupo_form)
        
        # Campos del formulario
        self.campo_titulo = QLineEdit()
        self.campo_titulo.setPlaceholderText("Escribe el título...")
        
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["nota", "recordatorio"])
        self.combo_tipo.currentTextChanged.connect(self.cambiar_tipo)
        
        self.campo_contenido = QTextEdit()
        self.campo_contenido.setPlaceholderText("Escribe el contenido...")
        self.campo_contenido.setMaximumHeight(150)
        
        self.campo_fecha_recordatorio = QDateTimeEdit()
        self.campo_fecha_recordatorio.setDateTime(QDateTime.currentDateTime())
        self.campo_fecha_recordatorio.setDisplayFormat("dd/MM/yyyy hh:mm")
        
        self.check_completado = QCheckBox("Marcado como completado")
        
        # Agregar campos al formulario
        form_layout.addRow("Título:", self.campo_titulo)
        form_layout.addRow("Tipo:", self.combo_tipo)
        form_layout.addRow("Contenido:", self.campo_contenido)
        form_layout.addRow("Fecha recordatorio:", self.campo_fecha_recordatorio)
        form_layout.addRow("Estado:", self.check_completado)
        
        layout.addWidget(grupo_form)
        
        # Botones del formulario
        layout_botones_form = QHBoxLayout()
        
        self.btn_guardar = QPushButton("💾 Guardar")
        self.btn_guardar.clicked.connect(self.guardar_elemento)
        
        self.btn_cancelar = QPushButton("❌ Cancelar")
        self.btn_cancelar.clicked.connect(self.cancelar_edicion)
        
        layout_botones_form.addWidget(self.btn_guardar)
        layout_botones_form.addWidget(self.btn_cancelar)
        
        layout.addLayout(layout_botones_form)
        
        # Espacio flexible
        layout.addStretch()
        
        # Inicialmente ocultar fecha de recordatorio
        self.cambiar_tipo()
        
        return widget
        
    def cambiar_tipo(self):
        """Muestra/oculta el campo de fecha según el tipo seleccionado"""
        es_recordatorio = self.combo_tipo.currentText() == "recordatorio"
        self.campo_fecha_recordatorio.setVisible(es_recordatorio)
        
    def cargar_datos(self):
        """Carga todos los datos del archivo CSV"""
        self.datos = []
        try:
            with open(self.archivo_csv, 'r', newline='', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    self.datos.append(fila)
        except FileNotFoundError:
            QMessageBox.warning(self, "Advertencia", "Archivo no encontrado. Se creará uno nuevo.")
            
        self.actualizar_lista()
        
    def actualizar_lista(self):
        """Actualiza la lista visual con los datos cargados"""
        self.lista_elementos.clear()
        
        for elemento in self.datos:
            # Crear texto para mostrar en la lista
            icono = "📝" if elemento['tipo'] == "nota" else "⏰"
            estado = "✅" if elemento['completado'] == "verdadero" else "⭕"
            
            texto = f"{icono} {estado} {elemento['titulo']}"
            
            # Añadir información adicional
            fecha_creacion = elemento['fecha_creacion'][:10] if elemento['fecha_creacion'] else ""
            if fecha_creacion:
                texto += f" ({fecha_creacion})"
                
            item = QListWidgetItem(texto)
            item.setData(Qt.UserRole, elemento['id'])
            self.lista_elementos.addItem(item)
            
    def aplicar_filtros(self):
        """Aplica filtros a la lista"""
        tipo_filtro = self.combo_filtro_tipo.currentText()
        estado_filtro = self.combo_filtro_estado.currentText()
        
        self.lista_elementos.clear()
        
        for elemento in self.datos:
            # Filtrar por tipo
            if tipo_filtro == "Notas" and elemento['tipo'] != "nota":
                continue
            if tipo_filtro == "Recordatorios" and elemento['tipo'] != "recordatorio":
                continue
                
            # Filtrar por estado
            if estado_filtro == "Pendientes" and elemento['completado'] == "verdadero":
                continue
            if estado_filtro == "Completados" and elemento['completado'] == "falso":
                continue
                
            # Añadir elemento que pasa los filtros
            icono = "📝" if elemento['tipo'] == "nota" else "⏰"
            estado = "✅" if elemento['completado'] == "verdadero" else "⭕"
            
            texto = f"{icono} {estado} {elemento['titulo']}"
            fecha_creacion = elemento['fecha_creacion'][:10] if elemento['fecha_creacion'] else ""
            if fecha_creacion:
                texto += f" ({fecha_creacion})"
                
            item = QListWidgetItem(texto)
            item.setData(Qt.UserRole, elemento['id'])
            self.lista_elementos.addItem(item)
            
    def seleccionar_elemento(self, item):
        """Carga los datos del elemento seleccionado en el formulario"""
        elemento_id = item.data(Qt.UserRole)
        
        # Buscar el elemento por ID
        for elemento in self.datos:
            if elemento['id'] == elemento_id:
                self.elemento_seleccionado = elemento
                self.cargar_elemento_en_formulario(elemento)
                break
                
    def cargar_elemento_en_formulario(self, elemento):
        """Carga los datos de un elemento en el formulario"""
        self.titulo_formulario.setText(f"✏️ Editando: {elemento['titulo']}")
        
        self.campo_titulo.setText(elemento['titulo'])
        self.combo_tipo.setCurrentText(elemento['tipo'])
        self.campo_contenido.setPlainText(elemento['contenido'])
        
        # Cargar fecha de recordatorio si existe
        if elemento['fecha_recordatorio']:
            fecha = QDateTime.fromString(elemento['fecha_recordatorio'], "yyyy-MM-dd hh:mm")
            self.campo_fecha_recordatorio.setDateTime(fecha)
            
        self.check_completado.setChecked(elemento['completado'] == "verdadero")
        self.cambiar_tipo()
        
    def nuevo_elemento(self):
        """Prepara el formulario para crear un nuevo elemento"""
        self.elemento_seleccionado = None
        self.limpiar_formulario()
        self.titulo_formulario.setText("📄 Nuevo Elemento")
        
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.campo_titulo.clear()
        self.combo_tipo.setCurrentText("nota")
        self.campo_contenido.clear()
        self.campo_fecha_recordatorio.setDateTime(QDateTime.currentDateTime())
        self.check_completado.setChecked(False)
        self.cambiar_tipo()
        
    def guardar_elemento(self):
        """Guarda o actualiza un elemento"""
        # Validar campos obligatorios
        if not self.campo_titulo.text().strip():
            QMessageBox.warning(self, "Error", "El título no puede estar vacío")
            return
            
        if not self.campo_contenido.toPlainText().strip():
            QMessageBox.warning(self, "Error", "El contenido no puede estar vacío")
            return
            
        # Preparar datos
        titulo = self.campo_titulo.text().strip()
        tipo = self.combo_tipo.currentText()
        contenido = self.campo_contenido.toPlainText().strip()
        completado = "verdadero" if self.check_completado.isChecked() else "falso"
        
        fecha_recordatorio = ""
        if tipo == "recordatorio":
            fecha_recordatorio = self.campo_fecha_recordatorio.dateTime().toString("yyyy-MM-dd hh:mm")
            
        if self.elemento_seleccionado:
            # Actualizar elemento existente
            self.actualizar_elemento(titulo, tipo, contenido, fecha_recordatorio, completado)
        else:
            # Crear nuevo elemento
            self.crear_elemento(titulo, tipo, contenido, fecha_recordatorio, completado)
            
    def crear_elemento(self, titulo, tipo, contenido, fecha_recordatorio, completado):
        """Crea un nuevo elemento y lo guarda en el CSV"""
        # Obtener nuevo ID
        nuevo_id = self.obtener_nuevo_id()
        fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Crear nueva fila
        nueva_fila = [nuevo_id, tipo, titulo, contenido, fecha_creacion, fecha_recordatorio, completado]
        
        # Guardar en CSV
        try:
            with open(self.archivo_csv, 'a', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(nueva_fila)
                
            QMessageBox.information(self, "Éxito", "Elemento creado correctamente")
            self.cargar_datos()
            self.limpiar_formulario()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
            
    def actualizar_elemento(self, titulo, tipo, contenido, fecha_recordatorio, completado):
        """Actualiza un elemento existente"""
        if not self.elemento_seleccionado:
            return
            
        # Actualizar datos en memoria
        for elemento in self.datos:
            if elemento['id'] == self.elemento_seleccionado['id']:
                elemento['titulo'] = titulo
                elemento['tipo'] = tipo
                elemento['contenido'] = contenido
                elemento['fecha_recordatorio'] = fecha_recordatorio
                elemento['completado'] = completado
                break
                
        # Reescribir archivo completo
        self.guardar_todos_los_datos()
        
    def eliminar_elemento(self):
        """Elimina el elemento seleccionado"""
        item_actual = self.lista_elementos.currentItem()
        if not item_actual:
            QMessageBox.warning(self, "Advertencia", "Selecciona un elemento para eliminar")
            return
            
        respuesta = QMessageBox.question(self, "Confirmar eliminación", 
                                       "¿Estás seguro de eliminar este elemento?",
                                       QMessageBox.Yes | QMessageBox.No)
        
        if respuesta == QMessageBox.Yes:
            elemento_id = item_actual.data(Qt.UserRole)
            
            # Eliminar de la lista en memoria
            self.datos = [elem for elem in self.datos if elem['id'] != elemento_id]
            
            # Guardar cambios
            self.guardar_todos_los_datos()
            self.limpiar_formulario()
            self.titulo_formulario.setText("📄 Nuevo Elemento")
            
    def marcar_completado(self):
        """Marca/desmarca un elemento como completado"""
        item_actual = self.lista_elementos.currentItem()
        if not item_actual:
            QMessageBox.warning(self, "Advertencia", "Selecciona un elemento")
            return
            
        elemento_id = item_actual.data(Qt.UserRole)
        
        # Cambiar estado
        for elemento in self.datos:
            if elemento['id'] == elemento_id:
                elemento['completado'] = "verdadero" if elemento['completado'] == "falso" else "falso"
                break
                
        self.guardar_todos_los_datos()
        
        # Si el elemento está cargado en el formulario, actualizar checkbox
        if self.elemento_seleccionado and self.elemento_seleccionado['id'] == elemento_id:
            self.check_completado.setChecked(elemento['completado'] == "verdadero")
            
    def cancelar_edicion(self):
        """Cancela la edición y limpia el formulario"""
        self.limpiar_formulario()
        self.titulo_formulario.setText("📄 Nuevo Elemento")
        self.elemento_seleccionado = None
        
    def obtener_nuevo_id(self):
        """Obtiene el siguiente ID disponible"""
        if not self.datos:
            return "1"
            
        ids_existentes = [int(elem['id']) for elem in self.datos]
        return str(max(ids_existentes) + 1)
        
    def guardar_todos_los_datos(self):
        """Reescribe todo el archivo CSV con los datos actuales"""
        try:
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                # Escribir encabezados
                escritor.writerow(['id', 'tipo', 'titulo', 'contenido', 'fecha_creacion', 
                                 'fecha_recordatorio', 'completado'])
                
                # Escribir datos
                for elemento in self.datos:
                    escritor.writerow([
                        elemento['id'], elemento['tipo'], elemento['titulo'],
                        elemento['contenido'], elemento['fecha_creacion'],
                        elemento['fecha_recordatorio'], elemento['completado']
                    ])
                    
            QMessageBox.information(self, "Éxito", "Datos guardados correctamente")
            self.cargar_datos()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")

# Función principal
def main():
    app = QApplication(sys.argv)
    
    # Configurar estilo de la aplicación
    app.setStyle('Fusion')  # Estilo más moderno
    
    ventana = AgendaApp()
    ventana.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()