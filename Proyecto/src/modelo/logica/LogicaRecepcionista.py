from datetime import datetime

from src.modelo.VO.Registro_accesoVO import RegistroAccesoVO
from src.modelo.dao.ClienteConsultasDaoJDBC import ClienteConsultasDaoJDBC
from src.modelo.dao.RegistroAccesoDaoJDBC import RegistroAccesoDaoJDBC
from src.modelo.dao.RegistroAccesoConsultasDaoJDBC import RegistroAccesoConsultasDaoJDBC
from src.modelo.dao.UsuarioConsultasDaoJDBC import UsuarioConsultasDaoJDBC
from src.modelo.dao.ClaseConsultasDaoJDBC import ClaseConsultasDaoJDBC


class LogicaRecepcionista:
    """Lógica de negocio para la recepción y el control de acceso al gimnasio.
    Gestiona el panel de inicio de la recepcionista (entradas del día,
    clases programadas, últimos registros) y las operaciones de control
    de acceso (buscar clientes, registrar entradas y salidas).
    """

    def __init__(self):
        self._cliente_consultas_dao  = ClienteConsultasDaoJDBC()
        self._acceso_dao             = RegistroAccesoDaoJDBC()
        self._acceso_consultas_dao   = RegistroAccesoConsultasDaoJDBC()
        self._usuario_consultas_dao  = UsuarioConsultasDaoJDBC()
        self._clase_consultas_dao    = ClaseConsultasDaoJDBC()

    # Panel del inicio

    def recepcion_entradas_hoy(self):
        """Devuelve el número de entradas registradas hoy en el gimnasio."""
        return self._acceso_consultas_dao.recepcion_entradas_hoy()

    def recepcion_nuevos_usuarios_hoy(self):
        """Devuelve el número de nuevos usuarios registrados hoy."""
        return self._usuario_consultas_dao.recepcion_nuevos_usuarios_hoy()

    def recepcion_clases_hoy(self):
        """Devuelve el número de clases programadas para el día actual."""
        return self._clase_consultas_dao.recepcion_clases_hoy()

    def recepcion_ultimos_registros_acceso(self):
        """Devuelve los últimos registros de acceso (entradas y salidas)
        para mostrarlos en la tabla del panel de inicio."""
        return self._acceso_consultas_dao.recepcion_ultimos_registros_acceso()

    # Control de acceso es decir entradas y salidas del gimnasio

    def buscar_cliente_acceso_por_dni_o_id(self, texto):
        """Busca un cliente por DNI o por ID de usuario para identificarlo
        en el control de acceso.
        Lanza ValueError si el texto de búsqueda está vacío."""
        if not texto:
            raise ValueError("Introduce un DNI o ID de cliente")
        return self._cliente_consultas_dao.buscar_cliente_acceso_por_dni_o_id(texto)

    def ultimo_acceso_cliente(self, id_usuario):
        """Devuelve el último registro de acceso del cliente indicado,
        o None si no tiene ninguno.
        Lanza ValueError si no se indica el cliente."""
        if not id_usuario:
            raise ValueError("Debe indicarse el cliente")
        return self._acceso_consultas_dao.ultimo_acceso_cliente(id_usuario)

    def listar_ultimos_accesos_control(self):
        """Devuelve los últimos registros de acceso para la tabla
        de control de acceso de la recepcionista."""
        return self._acceso_consultas_dao.listar_ultimos_accesos_control()


    def listar_accesos(self):
        """Devuelve todos los registros de acceso como lista de RegistroAccesoVO."""
        return self._acceso_dao.select()

    def registrar_acceso_cliente_control(self, id_usuario, tipo_acceso):
        """Registra una entrada o salida con validación de secuencia.

        Reglas de negocio:
        - No se puede registrar una salida sin una entrada previa.
        - No se puede registrar dos entradas consecutivas.
        - No se puede registrar dos salidas consecutivas.

        Lanza ValueError si se incumple alguna regla o si los parámetros
        son inválidos.
        """
        if not id_usuario:
            raise ValueError("Debe seleccionarse un cliente")
        if tipo_acceso not in ("entrada", "salida"):
            raise ValueError("Tipo de acceso no válido")

        # Obtener el último acceso del cliente para validar la secuencia
        ultimo = self._acceso_consultas_dao.ultimo_acceso_cliente(id_usuario)

        # No se puede salir sin haber entrado antes
        if tipo_acceso == "salida" and not ultimo:
            raise ValueError("No se puede registrar una salida sin una entrada previa")

        if ultimo:
            ultimo_tipo = str(ultimo[-1]).lower()
            # No se permiten dos entradas o dos salidas consecutivas
            if tipo_acceso == "entrada" and ultimo_tipo == "entrada":
                raise ValueError("Este cliente ya tiene una entrada registrada")
            if tipo_acceso == "salida" and ultimo_tipo == "salida":
                raise ValueError("Este cliente ya tiene una salida registrada")

        # Crear el VO con la fecha y hora actuales y registrarlo
        acceso_vo = RegistroAccesoVO(
            None,
            id_usuario,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tipo_acceso
        )
        return self._acceso_dao.insert(acceso_vo)