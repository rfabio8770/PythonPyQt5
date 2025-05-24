import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import mysql.connector


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("gui.ui", self)
        self.btnCrearDB.clicked.connect(self.crearDB)
        self.btnEliminarDB.clicked.connect(self.eliminarDB)
        self.btnMostrarDB.clicked.connect(self.mostrarDB)

    def showMessage(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.exec_()

    def crearDB(self):
        # crear la conexion a la base de datos
        con = mysql.connector.connect(host="localhost", user="root", password="1234")

        # crear el cursor
        cursor = con.cursor()
        consulta = "CREATE DATABASE IF NOT EXISTS db_prueba"
        cursor.execute(consulta)

        con.close()

        self.showMessage("Base de Datos Creada", "La base de datos 'db_prueba' ha sido creada exitosamente.")   
    
    def eliminarDB(self):
        # crear la conexion a la base de datos
        con = mysql.connector.connect(host="localhost", user="root", password="1234")

        # crear el cursor
        cursor = con.cursor()
        consulta = "DROP DATABASE IF EXISTS db_prueba"
        cursor.execute(consulta)

        con.close()

        self.showMessage("Base de Datos Eliminada", "La base de datos 'db_prueba' ha sido eliminada exitosamente.")
    
    def mostrarDB(self):
        # crear la conexion a la base de datos
        con = mysql.connector.connect(host="localhost", user="root", password="1234")

        # crear el cursor
        cursor = con.cursor()
        consulta = "SHOW DATABASES"
        cursor.execute(consulta)

        databases = cursor.fetchall()
        


        con.close()

        # desplegar la lista de bases de datos del servidor en la tabla
        n_databases = len(databases)
        self.tablaBD.setRowCount(n_databases)
        fila = 0
        for x in databases:
            nombre_db = x[0]
            self.tablaBD.setItem(fila, 0, QTableWidgetItem(nombre_db))
            fila = fila + 1



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())