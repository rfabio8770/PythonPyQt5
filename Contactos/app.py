import sys
import csv
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QTableWidget, QTableWidgetItem, 
                           QPushButton, QLineEdit, QLabel, QMessageBox, 
                           QDialog, QFormLayout, QHeaderView)
from PyQt5.QtCore import Qt

class ContactManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.csv_file = "contactos.csv"
        self.contacts = []
        self.init_ui()
        self.load_contacts()
        self.display_contacts()
    
    def init_ui(self):
        """Inicializar la interfaz de usuario"""
        self.setWindowTitle("Gestor de Contactos")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Título
        title = QLabel("📞 MI AGENDA DE CONTACTOS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title)
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("🔍 Buscar:"))
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Escribe nombre, apellido, teléfono o email...")
        self.search_box.textChanged.connect(self.search_contacts)
        search_layout.addWidget(self.search_box)
        main_layout.addLayout(search_layout)
        
        # Tabla de contactos
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Teléfono", "Email", "Dirección"])
        
        # Hacer que las columnas se ajusten al contenido
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        main_layout.addWidget(self.table)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("➕ Agregar Contacto")
        self.add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        self.add_btn.clicked.connect(self.add_contact)
        
        self.edit_btn = QPushButton("✏️ Editar Contacto")
        self.edit_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        self.edit_btn.clicked.connect(self.edit_contact)
        
        self.delete_btn = QPushButton("🗑️ Eliminar Contacto")
        self.delete_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        self.delete_btn.clicked.connect(self.delete_contact)
        
        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 8px;")
        self.refresh_btn.clicked.connect(self.refresh_table)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.refresh_btn)
        
        main_layout.addLayout(button_layout)
    
    def create_csv_if_not_exists(self):
        """Crear archivo CSV si no existe"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "nombre", "apellido", "telefono", "email", "direccion"])
                print("Archivo CSV creado exitosamente!")
    
    def load_contacts(self):
        """Cargar contactos desde el archivo CSV"""
        self.create_csv_if_not_exists()
        self.contacts = []
        
        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.contacts.append(row)
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No se pudo encontrar el archivo de contactos")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar contactos: {str(e)}")
    
    def save_contacts(self):
        """Guardar contactos en el archivo CSV"""
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                if self.contacts:
                    fieldnames = ["id", "nombre", "apellido", "telefono", "email", "direccion"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.contacts)
                else:
                    writer = csv.writer(file)
                    writer.writerow(["id", "nombre", "apellido", "telefono", "email", "direccion"])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar contactos: {str(e)}")
    
    def display_contacts(self, contacts_to_show=None):
        """Mostrar contactos en la tabla"""
        if contacts_to_show is None:
            contacts_to_show = self.contacts
            
        self.table.setRowCount(len(contacts_to_show))
        
        for row, contact in enumerate(contacts_to_show):
            self.table.setItem(row, 0, QTableWidgetItem(str(contact["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(contact["nombre"]))
            self.table.setItem(row, 2, QTableWidgetItem(contact["apellido"]))
            self.table.setItem(row, 3, QTableWidgetItem(contact["telefono"]))
            self.table.setItem(row, 4, QTableWidgetItem(contact["email"]))
            self.table.setItem(row, 5, QTableWidgetItem(contact["direccion"]))
    
    def get_next_id(self):
        """Obtener el siguiente ID disponible"""
        if not self.contacts:
            return 1
        return max(int(contact["id"]) for contact in self.contacts) + 1
    
    def add_contact(self):
        """Agregar un nuevo contacto"""
        dialog = ContactDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            contact_data = dialog.get_data()
            contact_data["id"] = str(self.get_next_id())
            self.contacts.append(contact_data)
            self.save_contacts()
            self.display_contacts()
            QMessageBox.information(self, "Éxito", "Contacto agregado correctamente!")
    
    def edit_contact(self):
        """Editar contacto seleccionado"""
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona un contacto para editar")
            return
        
        # Obtener el ID del contacto seleccionado
        contact_id = self.table.item(current_row, 0).text()
        contact_to_edit = None
        contact_index = -1
        
        for i, contact in enumerate(self.contacts):
            if contact["id"] == contact_id:
                contact_to_edit = contact
                contact_index = i
                break
        
        if contact_to_edit:
            dialog = ContactDialog(self, contact_to_edit)
            if dialog.exec_() == QDialog.Accepted:
                updated_data = dialog.get_data()
                updated_data["id"] = contact_id  # Mantener el mismo ID
                self.contacts[contact_index] = updated_data
                self.save_contacts()
                self.display_contacts()
                QMessageBox.information(self, "Éxito", "Contacto actualizado correctamente!")
    
    def delete_contact(self):
        """Eliminar contacto seleccionado"""
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona un contacto para eliminar")
            return
        
        # Confirmar eliminación
        reply = QMessageBox.question(self, "Confirmar", "¿Estás seguro de que quieres eliminar este contacto?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            contact_id = self.table.item(current_row, 0).text()
            self.contacts = [c for c in self.contacts if c["id"] != contact_id]
            self.save_contacts()
            self.display_contacts()
            QMessageBox.information(self, "Éxito", "Contacto eliminado correctamente!")
    
    def search_contacts(self):
        """Buscar contactos según el texto ingresado"""
        search_text = self.search_box.text().lower()
        
        if not search_text:
            self.display_contacts()
            return
        
        filtered_contacts = []
        for contact in self.contacts:
            # Buscar en todos los campos
            if (search_text in contact["nombre"].lower() or 
                search_text in contact["apellido"].lower() or 
                search_text in contact["telefono"].lower() or 
                search_text in contact["email"].lower() or 
                search_text in contact["direccion"].lower()):
                filtered_contacts.append(contact)
        
        self.display_contacts(filtered_contacts)
    
    def refresh_table(self):
        """Actualizar la tabla de contactos"""
        self.load_contacts()
        self.display_contacts()
        self.search_box.clear()
        QMessageBox.information(self, "Actualizado", "Lista de contactos actualizada!")

class ContactDialog(QDialog):
    def __init__(self, parent=None, contact_data=None):
        super().__init__(parent)
        self.contact_data = contact_data
        self.init_ui()
        
        if contact_data:
            self.populate_fields()
    
    def init_ui(self):
        """Inicializar interfaz del diálogo"""
        self.setWindowTitle("Agregar/Editar Contacto" if not self.contact_data else "Editar Contacto")
        self.setFixedSize(400, 300)
        
        layout = QFormLayout()
        
        # Campos del formulario
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Ej: Juan")
        
        self.lastname_edit = QLineEdit()
        self.lastname_edit.setPlaceholderText("Ej: Pérez")
        
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("Ej: 555-0123")
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Ej: juan@email.com")
        
        self.address_edit = QLineEdit()
        self.address_edit.setPlaceholderText("Ej: Calle Principal 123")
        
        # Agregar campos al layout
        layout.addRow("Nombre:", self.name_edit)
        layout.addRow("Apellido:", self.lastname_edit)
        layout.addRow("Teléfono:", self.phone_edit)
        layout.addRow("Email:", self.email_edit)
        layout.addRow("Dirección:", self.address_edit)
        
        # Botones
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Guardar")
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        save_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addRow(button_layout)
        self.setLayout(layout)
    
    def populate_fields(self):
        """Llenar los campos con datos del contacto a editar"""
        self.name_edit.setText(self.contact_data["nombre"])
        self.lastname_edit.setText(self.contact_data["apellido"])
        self.phone_edit.setText(self.contact_data["telefono"])
        self.email_edit.setText(self.contact_data["email"])
        self.address_edit.setText(self.contact_data["direccion"])
    
    def get_data(self):
        """Obtener datos del formulario"""
        return {
            "nombre": self.name_edit.text().strip(),
            "apellido": self.lastname_edit.text().strip(),
            "telefono": self.phone_edit.text().strip(),
            "email": self.email_edit.text().strip(),
            "direccion": self.address_edit.text().strip()
        }
    
    def accept(self):
        """Validar y aceptar los datos"""
        data = self.get_data()
        
        # Validaciones básicas
        if not data["nombre"]:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return
        
        if not data["apellido"]:
            QMessageBox.warning(self, "Error", "El apellido es obligatorio")
            return
        
        if not data["telefono"]:
            QMessageBox.warning(self, "Error", "El teléfono es obligatorio")
            return
        
        super().accept()

def main():
    """Función principal"""
    app = QApplication(sys.argv)
    
    # Configurar estilo de la aplicación
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f0f0f0;
        }
        QTableWidget {
            background-color: white;
            alternate-background-color: #f9f9f9;
            selection-background-color: #3daee9;
            gridline-color: #d0d0d0;
        }
        QLineEdit {
            padding: 5px;
            border: 2px solid #ddd;
            border-radius: 4px;
        }
        QLineEdit:focus {
            border-color: #3daee9;
        }
    """)
    
    window = ContactManager()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()