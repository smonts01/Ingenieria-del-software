import hashlib
from datetime import datetime

from src.modelo.VO.UsuarioVO import UsuarioVO
from src.modelo.VO.ClientesVO import ClientesVO
from src.modelo.VO.MenorVO import MenorVO
from src.modelo.VO.AdultoVO import AdultoVO
from src.modelo.VO.InscripcionVO import InscripcionVO

from src.modelo.dao.UsuarioDaoJDBC import UsuarioDaoJDBC
from src.modelo.dao.ClienteDaoJDBC import ClienteDaoJDBC
from src.modelo.dao.ClienteConsultasDaoJDBC import ClienteConsultasDaoJDBC
from src.modelo.dao.MenorDaoJDBC import MenorDaoJDBC
from src.modelo.dao.AdultoDaoJDBC import AdultoDaoJDBC
from src.modelo.dao.InscripcionDaoJDBC import InscripcionDaoJDBC
from src.modelo.dao.InscripcionConsultasDaoJDBC import InscripcionConsultasDaoJDBC
from src.modelo.dao.ClaseConsultasDaoJDBC import ClaseConsultasDaoJDBC
from src.modelo.dao.ClienteTarifaDaoJDBC import ClienteTarifaDaoJDBC


class LogicaClientes:
    """Reglas de negocio de clientes: perfil, altas, edición e inscripciones."""

    def __init__(self):
        self._usuario_dao = UsuarioDaoJDBC()
        self._cliente_dao = ClienteDaoJDBC()
        self._cliente_consultas_dao = ClienteConsultasDaoJDBC()
        self._menor_dao = MenorDaoJDBC()
        self._adulto_dao = AdultoDaoJDBC()
        self._inscripcion_dao = InscripcionDaoJDBC()
        self._inscripcion_consultas_dao = InscripcionConsultasDaoJDBC()
        self._clase_consultas_dao = ClaseConsultasDaoJDBC()
        self._cliente_tarifa_dao = ClienteTarifaDaoJDBC()

    def _cifrar(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    # ── CLIENTES ─────────────────────────────────────────────────────

    def contar_usuarios(self):
        return len(self._cliente_dao.select())

    def contar_usuarios(self):
        return self._cliente_consultas_dao.recepcion_total_clientes()

        return [
            (
                cliente.id_cliente,
                cliente.estado_pagado,
                cliente.calorias_acumuladas
            )
            for cliente in clientes
        ]

    def listar_clientes_completo(self):
        return self._cliente_consultas_dao.listar_clientes_completo()

    def buscar_clientes(self, texto):
        return self._cliente_consultas_dao.buscar_clientes(texto)

    def buscar_clientes_estado(self, estado):
        return self._cliente_consultas_dao.buscar_clientes_estado(estado)

    def datos_inicio_cliente(self, id_cliente):
        if not id_cliente:
            raise ValueError("Debe indicarse el cliente")

        return self._cliente_dao.selectInicioCliente(id_cliente)

    # ── RECEPCIÓN / CLIENTES ─────────────────────────────────────────

    def recepcion_total_clientes(self):
        return self._cliente_consultas_dao.recepcion_total_clientes()

    def recepcion_total_clientes_lista(self):
        return self._cliente_consultas_dao.recepcion_total_clientes_lista()

    def recepcion_clientes_recientes(self):
        return self._cliente_consultas_dao.recepcion_clientes_recientes()

    def recepcion_nuevos_clientes_mes(self):
        return self._cliente_consultas_dao.recepcion_nuevos_clientes_mes()

    def recepcion_listar_clientes_filtrados(self, dni="", tipo="Todos", plan="Todos"):
        return self._cliente_consultas_dao.recepcion_listar_clientes_filtrados(
            dni,
            tipo,
            plan
        )

    def recepcion_guardar_cambios_cliente(self, id_cliente, dni, nombre, telefono,
                                          email, direccion, fecha_nacimiento,
                                          estado_pagado):
        if not id_cliente:
            raise ValueError("Debe indicarse el cliente")

        if not dni or not nombre:
            raise ValueError("DNI y nombre son obligatorios")

        estado = estado_pagado.lower().strip()

        if estado not in ("abonado", "pendiente"):
            raise ValueError("El estado de pago debe ser abonado o pendiente")

        return self._cliente_consultas_dao.recepcion_guardar_cambios_cliente(
            id_cliente,
            dni.strip(),
            nombre.strip(),
            telefono.strip(),
            email.strip(),
            direccion.strip(),
            fecha_nacimiento,
            estado
        )

    def buscar_cliente_acceso_por_dni_o_id(self, texto):
        return self._cliente_consultas_dao.buscar_cliente_acceso_por_dni_o_id(texto)

    # ── ALTA DE CLIENTE DESDE RECEPCIÓN ──────────────────────────────

    def crear_cliente_desde_recepcion(self, dni, nombre, telefono, email, username,
                                      password, direccion, fecha_nacimiento,
                                      es_menor=False, dni_tutor="", nombre_tutor="",plan="Basico"):
        obligatorios = [
            dni,
            nombre,
            telefono,
            email,
            username,
            password,
            direccion,
            fecha_nacimiento
        ]

        if not all(str(x).strip() for x in obligatorios):
            raise ValueError("Faltan datos obligatorios del cliente")

        if es_menor and (not dni_tutor or not nombre_tutor):
            raise ValueError("Un cliente menor debe tener DNI y nombre del tutor")

        usuario_existente = self._usuario_dao.selectByUsername(username.strip())

        if usuario_existente is not None:
            raise ValueError("Ya existe un usuario con ese nombre de usuario")

        usuario_vo = UsuarioVO(
            None,
            dni.strip(),
            nombre.strip(),
            telefono.strip(),
            email.strip(),
            username.strip(),
            self._cifrar(password),
            1,
            direccion.strip(),
            None,
            fecha_nacimiento
        )

        self._usuario_dao.insert(usuario_vo)

        usuario_creado = self._usuario_dao.selectByUsername(username.strip())

        if usuario_creado is None:
            raise ValueError("No se pudo recuperar el cliente recién creado")

        id_cliente = usuario_creado.id_usuario

        cliente_vo = ClientesVO(
            id_cliente=id_cliente,
            estado_pagado="pendiente",
            calorias_acumuladas=0
        )

        self._cliente_dao.insert(cliente_vo)

        if es_menor:
            menor_vo = MenorVO(
                id_cliente=id_cliente,
                dni_tutor=dni_tutor.strip(),
                nombre_tutor=nombre_tutor.strip()
            )
            self._menor_dao.insert(menor_vo)
        else:
            try:
                adulto_vo = AdultoVO(id_cliente=id_cliente)
                self._adulto_dao.insert(adulto_vo)
            except Exception:
                pass

        self._asignar_tarifa_cliente(id_cliente, plan)
        return id_cliente

    def _obtener_id_tarifa_por_plan(self, plan):
        plan = str(plan).strip().lower()

        if plan in ("premium", "plan premium"):
            return 2

        return 1

    def _asignar_tarifa_cliente(self, id_cliente, plan):
        id_tarifa = self._obtener_id_tarifa_por_plan(plan)

        return self._cliente_tarifa_dao.asignar_tarifa_activa(
            id_cliente,
            id_tarifa
        )

    # ── INSCRIPCIONES DEL CLIENTE ───────────────────────────────────

    def inscribirse_clase(self, id_cliente, id_clase):
        if not id_cliente:
            raise ValueError("Debe indicarse el cliente")

        if not id_clase:
            raise ValueError("Debe indicarse la clase")

        inscripciones = self._inscripcion_dao.selectByCliente(id_cliente)

        for inscripcion in inscripciones:
            if inscripcion.id_clase == id_clase and inscripcion.estado == "inscrito":
                raise ValueError("Ya estás inscrito en esta clase")

        inscripcion_vo = InscripcionVO(
            None,
            id_cliente,
            id_clase,
            None,
            "inscrito"
        )

        return self._inscripcion_dao.insert(inscripcion_vo)

    def desapuntarse_clase(self, id_cliente, id_clase):
        if not id_cliente:
            raise ValueError("Debe indicarse el cliente")

        if not id_clase:
            raise ValueError("Debe indicarse la clase")

        inscripciones = self._inscripcion_dao.selectByCliente(id_cliente)

        for inscripcion in inscripciones:
            if inscripcion.id_clase == id_clase and inscripcion.estado == "inscrito":
                return self._inscripcion_dao.updateEstado(
                    inscripcion.id_inscripcion,
                    "cancelado"
                )

        raise ValueError("No estás inscrito en esa clase")

    def clases_inscritas_cliente(self, id_cliente):
        if not id_cliente:
            raise ValueError("Debe indicarse el cliente")

        return self._inscripcion_consultas_dao.clases_inscritas_cliente(id_cliente)

    def inscribirse_clase_por_nombre(self, id_cliente, nombre_actividad):
        if not nombre_actividad:
            raise ValueError("No se ha seleccionado ninguna clase")

        clases = self._clase_consultas_dao.buscar_clases(nombre_actividad)

        if not clases:
            raise ValueError("No se encontró ninguna clase con ese nombre")

        id_clase = clases[0][0]

        return self.inscribirse_clase(id_cliente, id_clase)
    

    def validar_datos_registro_cliente(self, dni, nombre, telefono, direccion,
                                    email, fecha, username, password,
                                    confirmar_password, es_adulto, es_menor,
                                    plan="Basico"):
        if not all([dni, nombre, telefono, direccion, email, fecha, username, password, confirmar_password]):
            raise ValueError("Completa todos los datos obligatorios")

        if password != confirmar_password:
            raise ValueError("Las contraseñas no coinciden")

        if not es_adulto and not es_menor:
            raise ValueError("Selecciona si el cliente es adulto o menor")

        if str(plan).strip().lower() not in ("basico", "básico", "premium"):
            raise ValueError("Selecciona un plan válido")

        return True

    def convertir_fecha_a_bd(self, fecha):
        try:
            return datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            return datetime.strptime(fecha, "%Y-%m-%d").strftime("%Y-%m-%d")