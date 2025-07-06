# cliente_wifi.py
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class ClienteVoto(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Votación vía ESP32")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.label = QLabel("Ingrese su ID de votante:")
        layout.addWidget(self.label)

        self.input_id = QLineEdit()
        layout.addWidget(self.input_id)

        self.boton = QPushButton("Verificar con ESP32")
        self.boton.clicked.connect(self.verificar)
        layout.addWidget(self.boton)

        self.setLayout(layout)

    def verificar(self):
        id_votante = self.input_id.text().strip()
        if not id_votante:
            QMessageBox.warning(self, "Error", "Debe ingresar un ID.")
            return

        try:
            # Dirección IP del ESP32 en tu red
            url = f"http://192.168.100.14/autorizar?id={id_votante}"
            r = requests.get(url, timeout=5)

            if r.status_code == 200 and r.text.strip() == "AUTORIZADO":
                QMessageBox.information(self, "Autorizado", "Puede votar ahora.")
                self.lanzar_votacion()
            else:
                QMessageBox.critical(self, "Denegado", "No está autorizado para votar.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al conectar con el ESP32:\n{e}")

    def lanzar_votacion(self):
        QMessageBox.information(self, "Votación", "Aquí se puede iniciar la pantalla de votación")
        # Aquí mostrarías tu pantalla de votación real

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ClienteVoto()
    ventana.show()
    sys.exit(app.exec_())
