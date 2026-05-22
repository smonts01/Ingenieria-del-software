"""
Vista de configuración del administrador (interfaz_admin_configuracion.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class VistaAdminConfiguracion(QMainWindow):
    """Vista de configuración del perfil del administrador."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_admin_configuracion.ui", self)

    # --- Getters / Setters ---
    def get_nombre(self) -> str:
        return self.txtNombreAdmin.text().strip()

    def get_email(self) -> str:
        return self.txtEmailAdmin.text().strip()

    def set_nombre(self, nombre: str):
        self.txtNombreAdmin.setText(nombre)
        self.lblNombre.setText(nombre)

    def set_email(self, email: str):
        self.txtEmailAdmin.setText(email)
        self.lblEmail.setText(email)

    # --- Feedback ---
    def mostrar_error(self, mensaje: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", mensaje)

    def mostrar_exito(self, mensaje: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Guardado", mensaje)

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.btnGuardar.clicked.connect(ctrl.guardar)
        # Navegación
        self.btnInicio.clicked.connect(ctrl.ir_inicio)
        self.btnUsuarios.clicked.connect(ctrl.ir_usuarios)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnInscripciones.clicked.connect(ctrl.ir_inscripciones)
        self.btnPagos.clicked.connect(ctrl.ir_pagos)
        self.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
