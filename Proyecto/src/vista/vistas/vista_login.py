"""
Vista de la pantalla de login (interfaz_grafica.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox


class VistaLogin(QDialog):
    """Vista del formulario de inicio de sesión."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_grafica.ui", self)
        self._configurar_ui()

    def _configurar_ui(self):
        """Configuración inicial de la interfaz."""
        self.txtContrasea.setEchoMode(self.txtContrasea.Password)
        self.txtContrasea_2.setEchoMode(self.txtContrasea_2.Password)
        # Botón ojo: alternar visibilidad de contraseña
        self.btnOjo.setCheckable(True)
        self.btnOjo.toggled.connect(self._toggle_password)

    def _toggle_password(self, visible: bool):
        modo = self.txtContrasea.Normal if visible else self.txtContrasea.Password
        self.txtContrasea.setEchoMode(modo)
        self.txtContrasea_2.setEchoMode(modo)

    # --- Getters para el controlador ---
    def get_usuario(self) -> str:
        return self.txtUsuario.text().strip()

    def get_contrasena(self) -> str:
        return self.txtContrasea.text()

    # --- Métodos de feedback al usuario ---
    def mostrar_error(self, mensaje: str):
        
        QMessageBox.critical(self, "Error de acceso", mensaje)

    def limpiar_campos(self):
        self.txtUsuario.clear()
        self.txtContrasea.clear()
        self.txtContrasea_2.clear()
        self.txtUsuario.setFocus()
