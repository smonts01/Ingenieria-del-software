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
        # La vista conecta su propio botón — solo le asignamos el controlador
        self.vista.set_controlador(self)
        self.vista.show()

    def iniciarSesion(self):
        # El controlador lee los datos a través de getters de la vista
        usuario  = self.vista.get_usuario()
        password = self.vista.get_contrasena()

        if not usuario or not password:
            self.vista.mostrar_error("Completa usuario y contraseña")
            return

        datos_usuario = self.modelo.iniciar_sesion(usuario, password)

        if not datos_usuario:
            self.vista.mostrar_error("Usuario o contraseña incorrectos")
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
            self.vista.mostrar_error(f"Rol desconocido: {rol}")
            self.vista.show()