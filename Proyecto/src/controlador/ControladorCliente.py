import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem


class ControladorCliente:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None

    def abrir(self):
        self.abrir_pantalla("interfaz_cliente_inicio.ui")

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
            v.btnInicio.clicked.connect(lambda: self.abrir_pantalla("interfaz_cliente_inicio.ui"))

        if hasattr(v, "btnClases"):
            v.btnClases.clicked.connect(lambda: self.abrir_pantalla("interfaz_cliente_clases_todas.ui"))

        if hasattr(v, "btnEstadisticas"):
            v.btnEstadisticas.clicked.connect(lambda: self.abrir_pantalla("interfaz_cliente_estadisticas.ui"))

        if hasattr(v, "btnPerfil"):
            v.btnPerfil.clicked.connect(lambda: self.abrir_pantalla("interfaz_cliente_perfil.ui"))

        if hasattr(v, "btnInformacion"):
            v.btnInformacion.clicked.connect(lambda: self.abrir_pantalla("interfaz_cliente_informacion.ui"))

        if hasattr(v, "btnReservar1"):
            v.btnReservar1.clicked.connect(lambda: self.reservar_clase(1))

        if hasattr(v, "btnReservar2"):
            v.btnReservar2.clicked.connect(lambda: self.reservar_clase(2))

        if hasattr(v, "btnReservar3"):
            v.btnReservar3.clicked.connect(lambda: self.reservar_clase(3))

        if hasattr(v, "btnReservar4"):
            v.btnReservar4.clicked.connect(lambda: self.reservar_clase(4))

    def cargar_datos(self):
        v = self.ventana

        if hasattr(v, "tablaProximasClases"):
            datos = self.modelo.clases_inscritas_cliente(self.usuario["id_usuario"])
            self.rellenar_tabla(v.tablaProximasClases, datos)

        if hasattr(v, "txtNombre"):
            perfil = self.modelo.perfil_usuario(self.usuario["id_usuario"])
            if perfil:
                v.txtNombre.setText(str(perfil[2]))
                v.txtTelefono.setText(str(perfil[3]))
                v.txtEmail.setText(str(perfil[4]))
                v.txtDireccion.setText(str(perfil[7]))

    def reservar_clase(self, id_clase):
        try:
            self.modelo.inscribirse_clase(self.usuario["id_usuario"], id_clase)
            QMessageBox.information(self.ventana, "Correcto", "Clase reservada")
        except Exception as e:
            QMessageBox.warning(self.ventana, "Error", str(e))

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