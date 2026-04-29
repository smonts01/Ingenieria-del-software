from PyQt5.QtWidgets import QMessageBox
from src.controlador.ControladorCliente import ControladorCliente
from src.controlador.ControladorRecepcionista import ControladorRecepcionista
from src.controlador.ControladorEntrenador import ControladorEntrenador
from src.controlador.ControladorAdministrador import ControladorAdministrador
from src.controlador.ControladorContable import ControladorContable


class ControladorPrincipal:
    """
    Controlador raíz. Gestiona el login y delega al controlador
    de rol correspondiente una vez autenticado el usuario.
    """

    def __init__(self, ventana, modelo):
        self.ventana = ventana
        self.modelo = modelo
        self.usuario_actual = None

    # ------------------------------------------------------------------
    # UC1 · Iniciar sesión
    # ------------------------------------------------------------------
    def abrirIniciarSesion(self):
        self.ventana.pushButton.clicked.connect(self.iniciarSesion)
        self.ventana.show()

    def iniciarSesion(self):
        username = self.ventana.txtUsuario.text().strip()
        password = self.ventana.txtContrasea.text().strip()

        if not username or not password:
            QMessageBox.warning(
                self.ventana, "Error", "Debes completar usuario y contraseña."
            )
            return

        resultado = self.modelo.autenticar_usuario(username, password)

        if resultado is None:
            QMessageBox.critical(
                self.ventana,
                "Acceso denegado",
                "Usuario o contraseña incorrectos.",
            )
            return

        self.usuario_actual = resultado          # dict con id, nombre, rol, etc.
        rol = resultado["nombre_rol"]

        self.ventana.hide()
        self._abrir_panel_por_rol(rol)

    def _abrir_panel_por_rol(self, rol):
        controladores = {
            "cliente":        ControladorCliente,
            "recepcionista":  ControladorRecepcionista,
            "entrenador":     ControladorEntrenador,
            "administrador":  ControladorAdministrador,
            "contable":       ControladorContable,
        }
        cls = controladores.get(rol)
        if cls is None:
            QMessageBox.critical(
                self.ventana, "Error", f"Rol '{rol}' no reconocido."
            )
            return
        ctrl = cls(self.modelo, self.usuario_actual, self)
        ctrl.abrir()

    def cerrar_sesion(self):
        """Llamado por cualquier controlador hijo para volver al login."""
        self.usuario_actual = None
        self.ventana.txtUsuario.clear()
        self.ventana.txtContrasea.clear()
        self.ventana.show()
