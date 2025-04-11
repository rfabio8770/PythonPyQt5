import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi

class Ejemplo1Window(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('ejemplo1.ui',self)
        self.setWindowTitle('Primer ejemplo GUI en PyQt5')
        self.btnMsg.clicked.connect(self.showMessage)
    
    def showMessage(self):
        msgBox= QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle('Python GUI')
        msgBox.setText('Bienvenido a la programación GUI')
        msgBox.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Ejemplo1Window()
    form.show()
    sys.exit(app.exec_())