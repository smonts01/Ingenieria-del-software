"""
Vista de registro de nuevo usuario del administrador (interfaz_admin_usuarios_nuevo_usuario.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class VistaAdminNuevoUsuario(QMainWindow):
    """Vista del formulario para crear un nuevo usuario."""

    ROLES = ["Cliente", "Entrenador", "Contable", "Recepcionista", "Administrador"]

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_admin_usuarios_nuevo_usuario.ui", self)
        self._configurar_ui()

    def _configurar_ui(self):
        self.cmbRolUsuario.addItems(self.ROLES)

    # --- Getters del formulario ---
    def get_nombre(self) -> str:
        return self.findChild(type(self), "txtNombre").text().strip() \
            if hasattr(self, "txtNombre") else ""

    def get_datos_personales(self) -> dict:
        """Devuelve un dict con todos los campos del formulario de datos personales."""
        campos = {}
        for nombre_widget in ["txtNombre", "txtDni", "txtEmail", "txtTelefono",
                               "txtDireccion", "txtFechaNacimiento"]:
            widget = self.findChild(type(self.cmbRolUsuario), nombre_widget) \
                if hasattr(self, nombre_widget) else None
            # Búsqueda genérica por nombre
            from PyQt5.QtWidgets import QLineEdit
            w = self.findChild(QLineEdit, nombre_widget)
            if w:
                campos[nombre_widget.replace("txt", "").lower()] = w.text().strip()
        return campos

    def get_datos_acceso(self) -> dict:
        from PyQt5.QtWidgets import QLineEdit
        password_w = self.findChild(QLineEdit, "txtPassword")
        confirmar_w = self.findChild(QLineEdit, "txtConfirmar")
        return {
            "password": password_w.text() if password_w else "",
            "confirmar": confirmar_w.text() if confirmar_w else "",
        }

    def get_rol(self) -> str:
        return self.cmbRolUsuario.currentText()

    # --- Feedback ---
    def mostrar_error(self, mensaje: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error de validación", mensaje)

    def mostrar_exito(self, mensaje: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Usuario creado", mensaje)

    def limpiar_formulario(self):
        from PyQt5.QtWidgets import QLineEdit
        for widget in self.findChildren(QLineEdit):
            widget.clear()
        self.cmbRolUsuario.setCurrentIndex(0)

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.btnRegistrarUsuario.clicked.connect(ctrl.registrar_usuario)
        self.btnCancelar.clicked.connect(ctrl.cancelar)
        # Navegación
        self.btnInicio.clicked.connect(ctrl.ir_inicio)
        self.btnUsuarios.clicked.connect(ctrl.ir_usuarios)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnInscripciones.clicked.connect(ctrl.ir_inscripciones)
        self.btnPagos.clicked.connect(ctrl.ir_pagos)
        self.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
        self.btnConfiguracion.clicked.connect(ctrl.ir_configuracion)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
