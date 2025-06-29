import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import mysql.connector


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("gui.ui", self)
        self.btnInsertar.clicked.connect(self.insertaAlumno)
        self.btnBorrar.clicked.connect(self.eliminarAlumno)
        self.btnModificar.clicked.connect(self.modificar)
        self.btnBuscar.clicked.connect(self.buscar)
        self.btnCerrar.clicked.connect(self.cerrar)
        self.connectar_baseDatos()
        self.mostrarAlumnos()

    def connectar_baseDatos(self):
        try:
            self.con = mysql.connector.connect(host="localhost", user="root", password="1234", database="escuela")
            self.cursor = self.con.cursor()
            self.showMessage("Conexión Exitosa", "Conexión a la base de datos establecida correctamente.")
        except mysql.connector.Error as err:
            self.showMessage("Error de Conexión", f"Error al conectar a la base de datos: {err}")

    def insertaAlumno(self):
    # obtener los valores de los campos de texto
        nombre = self.txtNombre.text()
        nota1 = self.txtPuntaje1.text()
        nota2 = self.txtPuntaje2.text()
        nota3 = self.txtPuntaje3.text()
        nota4 = self.txtPuntaje4.text()
        if not nombre or not nota1 or not nota2 or not nota3 or not nota4:
            self.showMessage("Error", "Todos los campos deben ser completados.")
            return
        try:
            # insertar los datos en la tabla alumnos
            consulta = "INSERT INTO tblalumnos (nombre, nota1, nota2, nota3, nota4) VALUES (%s, %s, %s, %s, %s)"
            valores = (nombre, nota1, nota2, nota3, nota4)
            self.cursor.execute(consulta, valores)
            self.con.commit()
            self.showMessage("Éxito", "Alumno insertado correctamente.")
            self.mostrarAlumnos()  # actualizar la tabla de alumnos
            self.limpiarCampos()  # limpiar los campos de texto
        except mysql.connector.Error as err:
            self.showMessage("Error de Conexión", f"Error al conectar a la base de datos: {err}")

    def limpiarCampos(self):
        # limpiar los campos de texto
        self.txtNombre.clear()
        self.txtPuntaje1.clear()
        self.txtPuntaje2.clear()
        self.txtPuntaje3.clear()
        self.txtPuntaje4.clear()

    def showMessage(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.exec_()

    def buscar(self):
        # obtener el nombre del alumno a buscar
        nombre = self.txtNombre.text()
        if not nombre:
            self.showMessage("Error", "El campo de nombre debe ser completado.")
            return

        try:
            # buscar el alumno en la tabla alumnos
            consulta = "SELECT * FROM tblalumnos WHERE nombre = %s"
            valores = (nombre,)
            self.cursor.execute(consulta, valores)
            alumno = self.cursor.fetchone()
            if alumno:
                # mostrar los datos del alumno en los campos de texto
                self.txtPuntaje1.setText(str(alumno[2]))
                self.txtPuntaje2.setText(str(alumno[3]))
                self.txtPuntaje3.setText(str(alumno[4]))
                self.txtPuntaje4.setText(str(alumno[5]))
            else:
                self.showMessage("Error", "No se encontró un alumno con ese nombre.")
        except mysql.connector.Error as err:
            self.showMessage("Error de Conexión", f"Error al conectar a la base de datos: {err}")
    
    def modificar(self):
        # obtener el nombre del alumno a modificar
        nombre = self.txtNombre.text()
        if not nombre:
            self.showMessage("Error", "El campo de nombre debe ser completado.")
            return

        # obtener las nuevas notas
        nota1 = self.txtPuntaje1.text()
        nota2 = self.txtPuntaje2.text()
        nota3 = self.txtPuntaje3.text()
        nota4 = self.txtPuntaje4.text()
        
        if not nota1 or not nota2 or not nota3 or not nota4:
            self.showMessage("Error", "Todos los campos deben ser completados.")
            return

        try:
            # actualizar los datos del alumno en la tabla alumnos
            consulta = "UPDATE tblalumnos SET nota1 = %s, nota2 = %s, nota3 = %s, nota4 = %s WHERE nombre = %s"
            valores = (nota1, nota2, nota3, nota4, nombre)
            self.cursor.execute(consulta, valores)
            self.con.commit()
            if self.cursor.rowcount > 0:
                self.showMessage("Éxito", "Alumno modificado correctamente.")
                self.mostrarAlumnos()  # actualizar la tabla de alumnos
                self.limpiarCampos()  # limpiar los campos de texto
            else:
                self.showMessage("Error", "No se encontró un alumno con ese nombre.")
        except mysql.connector.Error as err:
            self.showMessage("Error de Conexión", f"Error al conectar a la base de datos: {err}")

    def eliminarAlumno(self):
        # obtener el nombre del alumno a eliminar
        nombre = self.txtNombre.text()
        if not nombre:
            self.showMessage("Error", "El campo de nombre debe ser completado.")
            return

        try:
            # eliminar el alumno de la tabla alumnos
            consulta = "DELETE FROM tblalumnos WHERE nombre = %s"
            valores = (nombre,)
            self.cursor.execute(consulta, valores)
            self.con.commit()
            if self.cursor.rowcount > 0:
                self.showMessage("Éxito", "Alumno eliminado correctamente.")
                self.mostrarAlumnos()
                self.limpiarCampos()  # limpiar los campos de texto
            else:
                self.showMessage("Error", "No se encontró un alumno con ese nombre.")
        except mysql.connector.Error as err:
            self.showMessage("Error de Conexión", f"Error al conectar a la base de datos: {err}")
    
    def cerrar(self):
        # cerrar la conexión a la base de datos
        if self.con.is_connected():
            self.cursor.close()
            self.con.close()
            self.showMessage("Conexión Cerrada", "La conexión a la base de datos ha sido cerrada.")
    
    def mostrarAlumnos(self):
        consulta = "SELECT nombre, nota1, nota2, nota3, nota4 FROM tblalumnos"
        try:
            self.cursor.execute(consulta)
            alumnos = self.cursor.fetchall()
            n_alumnos = len(alumnos)
            self.tablaAlumnos.setColumnCount(5)  # nombre, nota1, nota2, nota3, nota4
            self.tablaAlumnos.setRowCount(n_alumnos)
            fila = 0
            for alumno in alumnos:
                self.tablaAlumnos.setItem(fila, 0, QTableWidgetItem(str(alumno[0]))) # nombre
                self.tablaAlumnos.setItem(fila, 1, QTableWidgetItem(str(alumno[1])))  # nota1
                self.tablaAlumnos.setItem(fila, 2, QTableWidgetItem(str(alumno[2])))  # nota2
                self.tablaAlumnos.setItem(fila, 3, QTableWidgetItem(str(alumno[3])))  # nota3
                self.tablaAlumnos.setItem(fila, 4, QTableWidgetItem(str(alumno[4])))  # nota4
                fila += 1
        except mysql.connector.Error as err:
            self.showMessage("Error de Consulta", f"Error al consultar los alumnos: {err}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())