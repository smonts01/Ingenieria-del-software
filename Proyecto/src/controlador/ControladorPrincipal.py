<<<<<<< Updated upstream
from PyQt5.QtWidgets import QMessageBox
from src.modelo.dao.ClienteDaoJDBC import ClienteDaoJDBC
from src.modelo.vo.ClienteInicioVO import ClienteInicioVO
from src.vista.Ui.InterfazClienteUnificada import interfaz_cliente_inicio
=======
import os
from PyQt5.QtWidgets import QMessageBox

from src.controlador.ControladorAdministrador import ControladorAdministrador
from src.controlador.ControladorCliente import ControladorCliente
from src.controlador.ControladorEntrenador import ControladorEntrenador
from src.controlador.ControladorContable import ControladorContable
from src.controlador.ControladorRecepcionista import ControladorRecepcionista

>>>>>>> Stashed changes

class ControladorPrincipal:

    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo
        # Ruta base a los ficheros .ui (relativa al directorio de trabajo = raíz del proyecto)
        self.ruta_ui = os.path.join("src", "vista", "Ui")

    def abrirIniciarSesion(self):
        self.vista.pushButton.clicked.connect(self.iniciarSesion)
        self.vista.show()

    def iniciarSesion(self):
        usuario = self.vista.txtUsuario.text().strip()
        password = self.vista.txtContrasea.text().strip()

        if not usuario or not password:
            QMessageBox.warning(self.vista, "Error", "Completa usuario y contraseña")
            return

        datos_usuario = self.modelo.iniciar_sesion(usuario, password)

        if not datos_usuario:
            QMessageBox.warning(self.vista, "Error", "Usuario o contraseña incorrectos")
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
<<<<<<< Updated upstream

            QMessageBox.warning(
                self.vista,
                "Error",
                "Usuario o contraseña incorrectos"
            )
        from src.modelo.dao.ClienteDaoJDBC import ClienteDaoJDBC
from src.modelo.vo.ClienteInicioVO import ClienteInicioVO
# Ajusta la ruta al módulo real de tu vista
from src.vista.InterfazClienteUnificada import InterfazClienteUnificada


# Apertura de la interfaz del cliente 

def abrirInterfazCliente(self, id_cliente: int) -> None:
    """
    Carga todos los datos necesarios para la interfaz unificada del
    cliente y la abre con ellos ya inicializados.

    Flujo:
        1. Solicita al DAO todos los datos del cliente (ClienteInicioVO).
        2. Valida que el cliente exista.
        3. Instancia la vista y la inicializa pasándole el VO.
        4. Muestra la ventana.

    Parámetros:
        id_cliente  ID del usuario autenticado (clave en clientes).
    """
    # 1. Obtener datos del modelo 
    dao = ClienteDaoJDBC()
    vo: ClienteInicioVO | None = dao.selectInicioCliente(id_cliente)

    if vo is None:
        # El cliente no existe o ocurrió un error en el DAO.
        # Aquí puedes mostrar un QMessageBox o redirigir al login.
        print(f"[ControladorPrincipal] No se encontraron datos para "
                f"el cliente con id={id_cliente}.")
        return

    # 2. Instanciar y cargar la vista 
    self.ventana_cliente = InterfazClienteUnificada(
        controlador=self,
        vo=vo
    )

    # 3. Mostrar 
    self.ventana_cliente.show()
=======
            QMessageBox.warning(self.vista, "Error", f"Rol desconocido: {rol}")
            self.vista.show()
>>>>>>> Stashed changes
