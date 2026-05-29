import os
from src.vista.componentes import MensajeView

from src.controlador.ControladorAdministrador import ControladorAdministrador
from src.controlador.ControladorCliente import ControladorCliente
from src.controlador.ControladorEntrenador import ControladorEntrenador
from src.controlador.ControladorContable import ControladorContable
from src.controlador.ControladorRecepcionista import ControladorRecepcionista


class ControladorPrincipal:

    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo
        self.ruta_ui = os.path.join("src", "vista", "Ui")

    def abrirIniciarSesion(self):
        self.vista.botonEntrar.clicked.connect(self.iniciarSesion)
        self.vista.show()

    def iniciarSesion(self):
        usuario = self.vista.txtUsuario.text().strip()
        password = self.vista.txtPassword.text().strip()

        if not usuario or not password:
            MensajeView.warning(self.vista, "Error", "Completa usuario y contraseña")
            return

        datos_usuario = self.modelo.iniciar_sesion(usuario, password)

        if not datos_usuario:
            MensajeView.warning(self.vista, "Error", "Usuario o contraseña incorrectos")
            return

        rol = datos_usuario["rol"]
        self.vista.hide()

        controladores = {
            "administrador": ControladorAdministrador,
            "cliente":       ControladorCliente,
            "entrenador":    ControladorEntrenador,
            "contable":      ControladorContable,
            "recepcionista": ControladorRecepcionista,
        }

        ClaseControlador = controladores.get(rol)
        if ClaseControlador:
            ctrl = ClaseControlador(self.modelo, datos_usuario, self.ruta_ui, self.vista)
            ctrl.abrir()
        else:
            MensajeView.warning(self.vista, "Error", f"Rol desconocido: {rol}")
            self.vista.showMaximized()
            self.vista.show()
