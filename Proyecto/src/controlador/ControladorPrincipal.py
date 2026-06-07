import os
# MensajeView pertenece a la capa Vista, y esta dentro de Componentes.py, lo hicimos para asi no importar PyQt5
# Se usa para mostrar mensajes visuales sin meter QMessageBox directamente en el controlador.
from src.vista.componentes import MensajeView

# Importamos los controladores de cada perfil.
# El ControladorPrincipal decide qué controlador abrir según el rol del usuario.
from src.controlador.ControladorAdministrador import ControladorAdministrador
from src.controlador.ControladorCliente import ControladorCliente
from src.controlador.ControladorEntrenador import ControladorEntrenador
from src.controlador.ControladorContable import ControladorContable
from src.controlador.ControladorRecepcionista import ControladorRecepcionista


class ControladorPrincipal:

    """
    Lo que hace el controlador principal es:
    - Recibe la vista de login y el modelo general.
    - Pide al modelo que valide el inicio de sesión.
    - Según el rol del usuario, abre el controlador correspondiente.
    """

    def __init__(self, vista, modelo):
        # Vista de login.
        self.vista = vista

        # Desde aquí se accede a la lógica de autenticación, usuarios, pagos, etc.
        self.modelo = modelo

        # Ruta donde están los archivos .ui de las interfaces.
        self.ruta_ui = os.path.join("src", "vista", "Ui")

    def abrirIniciarSesion(self):
        # Muestra pantalla de login
        self.vista.set_controlador(self)
        self.vista.show()

    def iniciarSesion(self):
        """
        Cuando se pulsa a boton para entrar, despues de iniciar sesión
        Flujo:
        Vista -> ControladorPrincipal -> Modelo/Logica -> DAO -> BD
        """

        # El controlador lee los datos usando getters de la vista.
        # Así no toca widgets internos
        usuario = self.vista.get_usuario()
        password = self.vista.get_contrasena()

        # Validación básica de interfaz.
        # No se llama al modelo si faltan datos obligatorios.
        if not usuario or not password:
            self.vista.mostrar_error("Completa usuario y contraseña")
            return

        # El controlador delega la autenticación en el modelo.
        datos_usuario = self.modelo.iniciar_sesion(usuario, password)

        # Si el modelo no devuelve usuario es porque algo estaba mal en las credenciales.
        if not datos_usuario:
            self.vista.mostrar_error("Usuario o contraseña incorrectos")
            return

        # El modelo devuelve los datos del usuario autenticado y  su rol.
        rol = datos_usuario["rol"]

        # Ocultamos la vista de login antes de abrir el panel correspondiente -> para evitar eliminar
        self.vista.hide()

        # Diccionario que relaciona cada rol con su controlador.
        controladores = {
            "administrador": ControladorAdministrador,
            "cliente": ControladorCliente,
            "entrenador": ControladorEntrenador,
            "contable": ControladorContable,
            "recepcionista": ControladorRecepcionista,
        }

        # Seleccionamos la clase controladora según el rol.
        ClaseControlador = controladores.get(rol)

        if ClaseControlador:
            # Se crea el controlador del perfil correspondiente.
            # Se le pasa el modelo, el usuario autenticado, la ruta de las vistas y el login.
            ctrl = ClaseControlador(
                self.modelo,
                datos_usuario,
                self.ruta_ui,
                self.vista
            )

            # Abrimos la pantalla inicial de ese perfil.
            ctrl.abrir()

        else:
            # Si el rol no existe, se informa al usuario y se vuelve al login.
            self.vista.mostrar_error(f"Rol desconocido: {rol}")
            self.vista.show()