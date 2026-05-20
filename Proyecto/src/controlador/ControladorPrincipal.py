from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
import os
import datetime

from src.controlador.ControladorAdministrador import ControladorAdministrador


class ControladorPrincipal:

    def __init__(self, vista_login, modelo):
        self.vista_login = vista_login
        self.modelo = modelo
        self.usuario_actual = None
        self.ventana_actual = None

        self.ruta_ui = os.path.join(os.path.dirname(__file__), "..", "vista", "Ui")

    def abrirIniciarSesion(self):
        self.vista_login.show()

    def iniciar_sesion(self, username, password):
        usuario = self.modelo.iniciar_sesion(username, password)

        if usuario is None:
            QMessageBox.warning(
                self.vista_login,
                "Error",
                "Usuario o contraseña incorrectos"
            )
        else:
            self.usuario_actual = usuario
            self.abrir_panel_por_rol(usuario["rol"])

    def abrir_panel_por_rol(self, rol):
        if rol == "cliente":
            archivo_ui = "interfaz_cliente_inicio.ui"
        elif rol == "entrenador":
            archivo_ui = "interfaz_entrenador.ui"
        elif rol == "recepcionista":
            archivo_ui = "interfaz_recepcionista.ui"
        elif rol == "administrador":
            archivo_ui = "interfaz_admin_inicio.ui"
        elif rol == "contable":
            archivo_ui = "interfaz_contable.ui"
        else:
            QMessageBox.warning(self.vista_login, "Error", "Rol no válido")
            return

        ruta = os.path.join(self.ruta_ui, archivo_ui)

        self.ventana_actual = uic.loadUi(ruta)
        self.ventana_actual.show()
        self.vista_login.close()