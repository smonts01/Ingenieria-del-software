import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem


class ControladorRecepcionista:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None

    def abrir(self):
        self.abrir_pantalla("interfaz_recepcionista.ui")

    def abrir_pantalla(self, archivo):
        if self.ventana:
            self.ventana.close()

        ruta = os.path.join(self.ruta_ui, archivo)
        self.ventana = uic.loadUi(ruta)
        self.conectar_botones()
        self.cargar_datos()
        self.ventana.show()

    def conectar_botones(self):
        v = self.ventana

        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(self.cerrar_sesion)

        if hasattr(v, "btnInicio"):
            v.btnInicio.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista.ui"))

        if hasattr(v, "btnClases"):
            v.btnClases.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_clientes.ui"))

        if hasattr(v, "btnInscripciones"):
            v.btnInscripciones.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_registrar_usuario.ui"))

        if hasattr(v, "btnPagos"):
            v.btnPagos.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_control_de_acceso.ui"))

        if hasattr(v, "btnOcupacion"):
            v.btnOcupacion.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_perfil.ui"))

        if hasattr(v, "btnInicio_4"):
            v.btnInicio_4.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_registrar_usuario.ui"))

        if hasattr(v, "btnInicio_5"):
            v.btnInicio_5.clicked.connect(self.cargar_datos)

        if hasattr(v, "btnInicio_2"):
            v.btnInicio_2.clicked.connect(lambda: self.registrar_acceso("entrada"))

        if hasattr(v, "btnInicio_3"):
            v.btnInicio_3.clicked.connect(lambda: self.registrar_acceso("salida"))

    def cargar_datos(self):
        v = self.ventana

        if hasattr(v, "tablaProximasClases"):
            datos = self.modelo.listar_clases()
            self.rellenar_tabla(v.tablaProximasClases, datos)

        if hasattr(v, "tablaProximasClases_2"):
            datos = self.modelo.pagos_pendientes()
            self.rellenar_tabla(v.tablaProximasClases_2, datos)

        if hasattr(v, "tableWidget"):
            if "control" in v.windowTitle().lower():
                datos = self.modelo.listar_accesos()
            else:
                datos = self.modelo.listar_clientes()
            self.rellenar_tabla(v.tableWidget, datos)

    def registrar_acceso(self, tipo):
        v = self.ventana

        try:
            id_usuario = int(v.lineEdit.text())
            self.modelo.registrar_acceso(id_usuario, tipo)
            QMessageBox.information(v, "Correcto", "Acceso registrado")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def registrar_usuario_recepcionista(self):
        v = self.ventana

        try:
            dni = v.lineEdit.text()
            nombre = v.lineEdit_3.text()
            telefono = v.lineEdit_4.text()
            email = v.lineEdit_5.text()
            direccion = v.lineEdit_2.text()
            fecha = v.lineEdit_6.text()
            usuario = v.lineEdit_7.text()
            password = v.lineEdit_8.text()

            id_rol = 1

            self.modelo.registrar_usuario(
                dni, nombre, telefono, email,
                usuario, password, id_rol,
                direccion, fecha
            )

            QMessageBox.information(v, "Correcto", "Usuario registrado")

        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def rellenar_tabla(self, tabla, datos):
        tabla.setRowCount(len(datos))
        if datos:
            tabla.setColumnCount(len(datos[0]))

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))

    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()