from PyQt5.QtWidgets import QMessageBox
from src.modelo.dao.ClienteDaoJDBC import ClienteDaoJDBC
from src.modelo.vo.ClienteInicioVO import ClienteInicioVO
from src.vista.Ui.InterfazClienteUnificada import interfaz_cliente_inicio

class ControladorPrincipal:

    def __init__(self, vista, modelo):

        self.vista = vista
        self.modelo = modelo

    def abrirIniciarSesion(self):

        self.vista.botonEntrar.clicked.connect(
            self.iniciarSesion
        )

        self.vista.show()


    def iniciarSesion(self):

        usuario = self.vista.txtUsuario.text()
        password = self.vista.txtPassword.text()

        if usuario == "" or password == "":

            QMessageBox.warning(
                self.vista,
                "Error",
                "Completa todos los campos"
            )

            return

        rol = self.modelo.validarLogin(
            usuario,
            password
        )

        if rol:

            QMessageBox.information(
                self.vista,
                "Correcto",
                f"Bienvenido {usuario}\nRol: {rol}"
            )

        else:

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