import serial
from PyQt5.QtCore import QTimer, Qt 
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import sys
from PyQt5.uic import loadUi 

class SerialApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('gui.ui', self)
        self.btnConectar.clicked.connect(self.connect_serial)
        self.btnSalir.clicked.connect(self.close)
        self.serial = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)

    def connect_serial(self):
        if self.serial.is_open:
            self.timer.start(1000)  # Update every second
        
    def update_labels(self):
        if self.serial.is_open:
            try:
                line = self.serial.readline().decode('utf-8').strip()
                if line:
                    data = line.split('#')
                    if len(data) == 3:
                        self.lblX.setText(f'{data[0]} cm')
                        self.lblY.setText(f'{data[1]} cm')
                        self.lblZ.setText(f'{data[2]} cm')
            except Exception as e:
                print(f"Error reading from serial: {e}")    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SerialApp()
    window.show()
    sys.exit(app.exec_())