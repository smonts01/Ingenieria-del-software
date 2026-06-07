"""
Vista de la pantalla de login (interfaz_grafica.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi


class VistaLogin(QDialog):
    """Vista del formulario de inicio de sesión."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_grafica.ui", self)
        self.controlador = None
        self._configurar_ui()

    def _configurar_ui(self):
        """Configuración inicial de la interfaz."""
        self.txtContrasea.setEchoMode(self.txtContrasea.Password)
        self.txtContrasea_2.setEchoMode(self.txtContrasea_2.Password)
        self.btnOjo.setCheckable(True)
        self.btnOjo.toggled.connect(self._toggle_password)

    def _toggle_password(self, visible: bool):
        modo = self.txtContrasea.Normal if visible else self.txtContrasea.Password
        self.txtContrasea.setEchoMode(modo)
        self.txtContrasea_2.setEchoMode(modo)

    def set_controlador(self, ctrl):
        """Asigna el controlador y conecta el botón de login."""
        self.controlador = ctrl
        self.botonEntrar.clicked.connect(self._on_entrar)

    def _on_entrar(self):
        """La vista captura el onclick y delega al controlador."""
        self.controlador.iniciarSesion()

    # --- Getters para el controlador ---
    def get_usuario(self) -> str:
        return self.txtUsuario.text().strip()

    def get_contrasena(self) -> str:
        return self.txtContrasea.text()

    # --- Métodos de feedback ---
    def mostrar_error(self, mensaje: str):
        QMessageBox.critical(self, "Error de acceso", mensaje)

    def limpiar_campos(self):
        self.txtUsuario.clear()
        self.txtContrasea.clear()
        self.txtContrasea_2.clear()
        self.txtUsuario.setFocus()