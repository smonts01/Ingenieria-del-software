from datetime import datetime

from src.modelo.VO.Registro_accesoVO import RegistroAccesoVO

from src.modelo.dao.ClienteConsultasDaoJDBC import ClienteConsultasDaoJDBC
from src.modelo.dao.RegistroAccesoDaoJDBC import RegistroAccesoDaoJDBC
from src.modelo.dao.RegistroAccesoConsultasDaoJDBC import RegistroAccesoConsultasDaoJDBC
from src.modelo.dao.UsuarioConsultasDaoJDBC import UsuarioConsultasDaoJDBC
from src.modelo.dao.ClaseConsultasDaoJDBC import ClaseConsultasDaoJDBC


class LogicaRecepcionista:
    """Reglas de negocio de recepción y control de acceso."""

    def __init__(self):
        self._cliente_consultas_dao = ClienteConsultasDaoJDBC()
        self._acceso_dao = RegistroAccesoDaoJDBC()
        self._acceso_consultas_dao = RegistroAccesoConsultasDaoJDBC()
        self._usuario_consultas_dao = UsuarioConsultasDaoJDBC()
        self._clase_consultas_dao = ClaseConsultasDaoJDBC()

    # ── INICIO RECEPCIONISTA ────────────────────────────────────────

    def recepcion_entradas_hoy(self):
        return self._acceso_consultas_dao.recepcion_entradas_hoy()

    def recepcion_nuevos_usuarios_hoy(self):
        return self._usuario_consultas_dao.recepcion_nuevos_usuarios_hoy()

    def recepcion_clases_hoy(self):
        return self._clase_consultas_dao.recepcion_clases_hoy()

    def recepcion_ultimos_registros_acceso(self):
        return self._acceso_consultas_dao.recepcion_ultimos_registros_acceso()

    # ── CONTROL DE ACCESO ───────────────────────────────────────────

    def buscar_cliente_acceso_por_dni_o_id(self, texto):
        if not texto:
            raise ValueError("Introduce un DNI o ID de cliente")

        return self._cliente_consultas_dao.buscar_cliente_acceso_por_dni_o_id(texto)

    def ultimo_acceso_cliente(self, id_usuario):
        if not id_usuario:
            raise ValueError("Debe indicarse el cliente")

        return self._acceso_consultas_dao.ultimo_acceso_cliente(id_usuario)

    def listar_ultimos_accesos_control(self):
        return self._acceso_consultas_dao.listar_ultimos_accesos_control()

    def registrar_acceso(self, id_usuario, tipo_acceso):
        if not id_usuario:
            raise ValueError("Debe indicarse el cliente")

        if tipo_acceso not in ("entrada", "salida"):
            raise ValueError("El tipo de acceso debe ser entrada o salida")

        acceso_vo = RegistroAccesoVO(
            None,
            id_usuario,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tipo_acceso
        )

        return self._acceso_dao.insert(acceso_vo)

    def listar_accesos(self):
        accesos = self._acceso_dao.select()

        return accesos

    def registrar_acceso_cliente_control(self, id_usuario, tipo_acceso):
        if not id_usuario:
            raise ValueError("Debe seleccionarse un cliente")

        if tipo_acceso not in ("entrada", "salida"):
            raise ValueError("Tipo de acceso no válido")

        ultimo = self._acceso_consultas_dao.ultimo_acceso_cliente(id_usuario)

        if tipo_acceso == "salida" and not ultimo:
            raise ValueError("No se puede registrar una salida sin una entrada previa")

        if ultimo:
            ultimo_tipo = str(ultimo[-1]).lower()

            if tipo_acceso == "entrada" and ultimo_tipo == "entrada":
                raise ValueError("Este cliente ya tiene una entrada registrada")

            if tipo_acceso == "salida" and ultimo_tipo == "salida":
                raise ValueError("Este cliente ya tiene una salida registrada")

        acceso_vo = RegistroAccesoVO(
            None,
            id_usuario,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tipo_acceso
        )

        return self._acceso_dao.insert(acceso_vo)