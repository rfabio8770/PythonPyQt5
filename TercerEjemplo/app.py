import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
import mysql.connector as mysql_connector
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class Ejemplo1Window(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('promedio.ui',self)
        self.setWindowTitle('Primer ejemplo GUI en PyQt5')
        self.btnCalcular.clicked.connect(self.calcularPromedio)
        self.conexion = mysql_connector.connect(user='root', password='1234', host='localhost', database='escuela')
        self.cargarDatos()
        self.tblViewDatos.selectionModel().selectionChanged.connect(self.cargarDatosSeleccionados)

    def cargarDatos(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM tblalumnos")
        alumnos = cursor.fetchall()
        # crear modelo
        self.modelo = QStandardItemModel()
        self.modelo.setHorizontalHeaderLabels(['ID', 'Nombre', 'Puntaje 1', 'Puntaje 2', 'Puntaje 3', 'Puntaje 4'])
        for alumno in alumnos:
            items = [QStandardItem(str(col)) for col in alumno]
            self.modelo.appendRow(items)
        self.tblViewDatos.setModel(self.modelo)        
        cursor.close()
    

    def cargarDatosSeleccionados(self):
        fila = self.tblViewDatos.currentIndex().row()
        self.txtPromedio.setText('')
        if fila == -1:
            msgBox= QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle('Promedio de puntajes')
            msgBox.setText('Se debe seleccionar un registro')
            msgBox.exec()
            return
        if fila >= 0:
            id = self.modelo.item(fila,0).text()
            nombre = self.modelo.item(fila,1).text()
            nota1 = self.modelo.item(fila,2).text()
            nota2 = self.modelo.item(fila,3).text()
            nota3 = self.modelo.item(fila,4).text()
            nota4 = self.modelo.item(fila,5).text()
            # self.txtId.setText(id)
            self.txtNombre.setText(nombre)
            self.txtPuntaje1.setText(nota1)
            self.txtPuntaje2.setText(nota2)
            self.txtPuntaje3.setText(nota3)
            self.txtPuntaje4.setText(nota4)

    def calcularPromedio(self):
        nota1 = float(self.txtPuntaje1.text())
        nota2 = float(self.txtPuntaje2.text())
        nota3 = float(self.txtPuntaje3.text())
        nota4 = float(self.txtPuntaje4.text())
        promedio = (nota1 + nota2 + nota3 + nota4) // 4
        self.txtPromedio.setText(str(promedio))

           
    def showMessage(self):
        msgBox= QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle('Python GUI')
        msgBox.setText('Calcular promedio')
        msgBox.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Ejemplo1Window()
    form.show()
    sys.exit(app.exec_())
