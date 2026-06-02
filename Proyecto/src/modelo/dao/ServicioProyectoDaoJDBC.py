import hashlib
from datetime import datetime

from src.modelo.dao.UsuarioDaoJDBC import UsuarioDaoJDBC
from src.modelo.dao.ClienteDaoJDBC import ClienteDaoJDBC
from src.modelo.dao.EmpleadoDaoJDBC import EmpleadoDaoJDBC
from src.modelo.dao.AdministradorDaoJDBC import AdministradorDaoJDBC
from src.modelo.dao.EntrenadorDaoJDBC import EntrenadorDaoJDBC
from src.modelo.dao.RecepcionistaDaoJDBC import RecepcionistaDaoJDBC
from src.modelo.dao.ContableDaoJDBC import ContableDaoJDBC
from src.modelo.dao.ClaseDaoJDBC import ClaseDaoJDBC
from src.modelo.dao.InscripcionDaoJDBC import InscripcionDaoJDBC
from src.modelo.dao.AsistenciaDaoJDBC import AsistenciaDaoJDBC
from src.modelo.dao.PagoDaoJDBC import PagoDaoJDBC
from src.modelo.dao.RegistroAccesoDaoJDBC import RegistroAccesoDaoJDBC
from src.modelo.dao.TarifaDaoJDBC import TarifaDaoJDBC
from src.modelo.dao.InformeDaoJDBC import InformeDaoJDBC
from src.modelo.dao.MenorDaoJDBC import MenorDaoJDBC
from src.modelo.dao.AdultoDaoJDBC import AdultoDaoJDBC
from src.modelo.dao.RolesDaoJDBC import RolesDaoJDBC

from src.modelo.dao.UsuarioConsultasDaoJDBC import UsuarioConsultasDaoJDBC
from src.modelo.dao.ClienteConsultasDaoJDBC import ClienteConsultasDaoJDBC
from src.modelo.dao.EmpleadoConsultasDaoJDBC import EmpleadoConsultasDaoJDBC
from src.modelo.dao.ClaseConsultasDaoJDBC import ClaseConsultasDaoJDBC
from src.modelo.dao.InscripcionConsultasDaoJDBC import InscripcionConsultasDaoJDBC
from src.modelo.dao.AsistenciaConsultasDaoJDBC import AsistenciaConsultasDaoJDBC
from src.modelo.dao.PagoConsultasDaoJDBC import PagoConsultasDaoJDBC
from src.modelo.dao.RegistroAccesoConsultasDaoJDBC import RegistroAccesoConsultasDaoJDBC
from src.modelo.dao.TarifaConsultasDaoJDBC import TarifaConsultasDaoJDBC
from src.modelo.dao.InformeConsultasDaoJDBC import InformeConsultasDaoJDBC
from src.modelo.dao.EstadisticasConsultasDaoJDBC import EstadisticasConsultasDaoJDBC

from src.modelo.VO.UsuarioVO import UsuarioVO
from src.modelo.VO.ClientesVO import ClientesVO
from src.modelo.VO.EmpleadosVO import EmpleadoVO
from src.modelo.VO.AdminitradorVO import AdminitradorVO
from src.modelo.VO.EntrenadorVO import EntrenadorVO
from src.modelo.VO.RecepcionistaVO import RecepcionistaVO
from src.modelo.VO.ContableVO import ContableVO
from src.modelo.VO.ClaseVO import ClaseVO
from src.modelo.VO.InscripcionVO import InscripcionVO
from src.modelo.VO.AsistenciaVO import AsistenciaVO
from src.modelo.VO.PagoVO import PagoVO
from src.modelo.VO.Registro_accesoVO import RegistroAccesoVO
from src.modelo.VO.MenorVO import MenorVO
from src.modelo.VO.AdultoVO import AdultoVO


class ServicioProyectoDaoJDBC:
    """Servicio coordinador de persistencia.

    Esta clase ya no contiene consultas SQL directas. Coordina DAOs concretos y
    DAOs de consultas específicas. La lógica de negocio queda en src/modelo/logica
    y los controladores solo deben llamar a Logica.
    """

    def __init__(self):
        # DAOs de entidad / VO
        self._usuario_dao = UsuarioDaoJDBC()
        self._cliente_dao = ClienteDaoJDBC()
        self._menor_dao = MenorDaoJDBC()
        self._adulto_dao = AdultoDaoJDBC()
        self._empleado_dao = EmpleadoDaoJDBC()
        self._admin_dao = AdministradorDaoJDBC()
        self._entrenador_dao = EntrenadorDaoJDBC()
        self._recep_dao = RecepcionistaDaoJDBC()
        self._contable_dao = ContableDaoJDBC()
        self._clase_dao = ClaseDaoJDBC()
        self._inscripcion_dao = InscripcionDaoJDBC()
        self._asistencia_dao = AsistenciaDaoJDBC()
        self._pago_dao = PagoDaoJDBC()
        self._acceso_dao = RegistroAccesoDaoJDBC()
        self._tarifa_dao = TarifaDaoJDBC()
        self._informe_dao = InformeDaoJDBC()
        self._roles_dao = RolesDaoJDBC()

        # DAOs de consultas complejas / informes / JOINs
        self._usuario_consultas_dao = UsuarioConsultasDaoJDBC()
        self._cliente_consultas_dao = ClienteConsultasDaoJDBC()
        self._empleado_consultas_dao = EmpleadoConsultasDaoJDBC()
        self._clase_consultas_dao = ClaseConsultasDaoJDBC()
        self._inscripcion_consultas_dao = InscripcionConsultasDaoJDBC()
        self._asistencia_consultas_dao = AsistenciaConsultasDaoJDBC()
        self._pago_consultas_dao = PagoConsultasDaoJDBC()
        self._registro_acceso_consultas_dao = RegistroAccesoConsultasDaoJDBC()
        self._tarifa_consultas_dao = TarifaConsultasDaoJDBC()
        self._informe_consultas_dao = InformeConsultasDaoJDBC()
        self._estadisticas_consultas_dao = EstadisticasConsultasDaoJDBC()

    def _cifrar(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    # ── AUTENTICACIÓN ─────────────────────────────────────────────────────
    def iniciar_sesion(self, username: str, password: str):
        vo = self._usuario_dao.selectByUsername(username)
        if vo is None:
            return None
        password_cifrada = self._cifrar(password)
        if vo.password_hash != password and vo.password_hash != password_cifrada:
            return None
        rol = self._roles_dao.nombre_rol_por_id(vo.id_rol) or "cliente"
        return {
            "id_usuario": vo.id_usuario,
            "nombre": vo.nombre,
            "username": vo.username,
            "rol": rol,
        }

    # ── USUARIOS ─────────────────────────────────────────────────────────
    def registrar_usuario(self, dni, nombre, telefono, email, username, password, id_rol, direccion, fecha_nacimiento):
        vo = UsuarioVO(None, dni, nombre, telefono, email, username,
                       self._cifrar(password), id_rol, direccion, None, fecha_nacimiento)
        return self._usuario_dao.insert(vo)

    def modificar_usuario(self, id_usuario: int, telefono: str, email: str, direccion: str):
        vo = self._usuario_dao.selectById(id_usuario)
        if vo is None:
            raise ValueError(f"Usuario {id_usuario} no encontrado")
        vo_actualizado = UsuarioVO(vo.id_usuario, vo.dni, vo.nombre, telefono, email,
                                   vo.username, vo.password_hash, vo.id_rol,
                                   direccion, vo.fecha_registro, vo.fecha_nacimiento)
        return self._usuario_dao.update(vo_actualizado)

    def eliminar_usuario(self, id_usuario: int): return self._usuario_dao.delete(id_usuario)
    def buscar_usuario(self, id_usuario: int): return self._usuario_dao.selectById(id_usuario)
    def perfil_usuario(self, id_usuario: int): return self._usuario_consultas_dao.perfil_usuario(id_usuario)

    def listar_usuarios(self):
        return [(v.id_usuario, v.dni, v.nombre, v.telefono, v.email, v.username,
                 v.id_rol, v.direccion, v.fecha_nacimiento)
                for v in self._usuario_dao.select()]

    def cambiar_password(self, id_usuario: int, nueva_password: str):
        vo = self._usuario_dao.selectById(id_usuario)
        if vo is None:
            raise ValueError("Usuario no encontrado")
        vo_nuevo = UsuarioVO(vo.id_usuario, vo.dni, vo.nombre, vo.telefono, vo.email,
                             vo.username, self._cifrar(nueva_password), vo.id_rol,
                             vo.direccion, vo.fecha_registro, vo.fecha_nacimiento)
        return self._usuario_dao.update(vo_nuevo)

    # ── CLIENTES ─────────────────────────────────────────────────────────
    def registrar_cliente(self, id_cliente: int):
        return self._cliente_dao.insert(ClientesVO(id_cliente=id_cliente, estado_pagado="pendiente", calorias_acumuladas=0))

    def contar_usuarios(self): return len(self._cliente_dao.select())
    def listar_clientes(self): return [(v.id_cliente, v.estado_pagado, v.calorias_acumuladas) for v in self._cliente_dao.select()]
    def listar_clientes_completo(self): return self._cliente_consultas_dao.listar_clientes_completo()
    def buscar_clientes(self, texto: str): return self._cliente_consultas_dao.buscar_clientes(texto)
    def buscar_clientes_estado(self, estado: str): return self._cliente_consultas_dao.buscar_clientes_estado(estado)
    def datos_inicio_cliente(self, id_cliente: int): return self._cliente_dao.selectInicioCliente(id_cliente)
    def recepcion_total_clientes(self): return self._cliente_consultas_dao.recepcion_total_clientes()
    def recepcion_total_clientes_lista(self): return self._cliente_consultas_dao.recepcion_total_clientes_lista()
    def recepcion_clientes_recientes(self): return self._cliente_consultas_dao.recepcion_clientes_recientes()
    def recepcion_nuevos_clientes_mes(self): return self._cliente_consultas_dao.recepcion_nuevos_clientes_mes()
    def recepcion_listar_clientes_filtrados(self, dni="", tipo="Todos", plan="Todos"):
        return self._cliente_consultas_dao.recepcion_listar_clientes_filtrados(dni, tipo, plan)
    def recepcion_guardar_cambios_cliente(self, *args): return self._cliente_consultas_dao.recepcion_guardar_cambios_cliente(*args)
    def buscar_cliente_acceso_por_dni_o_id(self, texto): return self._cliente_consultas_dao.buscar_cliente_acceso_por_dni_o_id(texto)

    def insertar_cliente_recepcion(self, dni, nombre, telefono, email, username, password, direccion, fecha_nacimiento, es_menor=False, dni_tutor="", nombre_tutor=""):
        usuario_existente = self._usuario_dao.selectByUsername(username)
        if usuario_existente is not None:
            raise ValueError("Ya existe un usuario con ese nombre de usuario")
        id_cliente = self.crear_usuario_completo(dni, nombre, telefono, email, username, password, 1, direccion, fecha_nacimiento)
        if es_menor:
            self._menor_dao.insert(MenorVO(id_cliente=id_cliente, dni_tutor=dni_tutor, nombre_tutor=nombre_tutor))
        else:
            try:
                self._adulto_dao.insert(AdultoVO(id_cliente=id_cliente))
            except Exception:
                pass
        return id_cliente

    # ── TRABAJADORES / ROLES ─────────────────────────────────────────────
    def registrar_empleado(self, id_empleado: int, salario: float = 0.0): return self._empleado_dao.insert(EmpleadoVO(id_empleado=id_empleado, salario=salario))
    def registrar_entrenador(self, id_entrenador: int, especialidad: str, id_admin: int): return self._entrenador_dao.insert(EntrenadorVO(id_entrenador=id_entrenador, especialidad=especialidad, id_administrador_registra=id_admin))
    def registrar_recepcionista(self, id_recep: int, turno: str, id_admin: int): return self._recep_dao.insert(RecepcionistaVO(id_recepcionista=id_recep, turno=turno, id_administrador_registra=id_admin))
    def registrar_contable(self, id_contable: int, titulacion: str, id_admin: int): return self._contable_dao.insert(ContableVO(id_contable=id_contable, titulacion=titulacion, id_administrador_registra=id_admin))
    def registrar_administrador(self, id_admin: int): return self._admin_dao.insert(AdminitradorVO(id_administrador=id_admin))
    def contar_trabajadores(self): return len(self._empleado_dao.select())
    def contar_por_rol(self, nombre_rol: str): return self._empleado_consultas_dao.contar_por_rol(nombre_rol)
    def listar_trabajadores_completo(self): return self._empleado_consultas_dao.listar_trabajadores_completo()
    def buscar_trabajadores(self, texto: str): return self._empleado_consultas_dao.buscar_trabajadores(texto)
    def buscar_trabajadores_rol(self, rol: str): return self._empleado_consultas_dao.buscar_trabajadores_rol(rol)
    def listar_empleados(self): return [(v.id_empleado, v.salario) for v in self._empleado_dao.select()]
    def guardar_cambios_trabajador(self, id_usuario, nombre, telefono, email, direccion): return self.modificar_usuario(id_usuario, telefono, email, direccion)

    # ── CLASES ───────────────────────────────────────────────────────────
    def contar_clases(self): return len(self._clase_dao.select())
    def listar_clases(self):
        return [(v.id_clase, v.nombre_actividad, v.dia_semana, v.hora_inicio,
                 v.hora_fin, v.aforo_maximo, v.nivel_intensidad, v.calorias_estimadas)
                for v in self._clase_dao.select()]
    def clases_de_entrenador(self, id_entrenador: int):
        return [(v.id_clase, v.nombre_actividad, v.dia_semana, v.hora_inicio,
                 v.hora_fin, v.aforo_maximo, v.nivel_intensidad)
                for v in self._clase_dao.selectByEntrenador(id_entrenador)]
    def registrar_clase(self, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad):
        vo = ClaseVO(None, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad)
        return self._clase_dao.insert(vo)
    def modificar_clase(self, id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad):
        vo = ClaseVO(id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad)
        return self._clase_dao.update(vo)
    def eliminar_clase(self, id_clase: int): return self._clase_dao.delete(id_clase)
    def buscar_clases(self, texto: str): return self._clase_consultas_dao.buscar_clases(texto)
    def ocupacion_clases(self): return self._clase_consultas_dao.ocupacion_clases()
    def guardar_cambios_clase_tabla(self, id_clase, nombre, dia, hora_ini, hora_fin, aforo, nivel):
        clase = self._clase_dao.selectById(int(id_clase))
        if clase is None:
            raise ValueError("Clase no encontrada")
        vo = ClaseVO(clase.id_clase, clase.id_entrenador, clase.id_sala, nombre,
                     clase.calorias_estimadas, dia, hora_ini, hora_fin,
                     clase.duracion, int(aforo), nivel)
        return self._clase_dao.update(vo)
    def clases_entrenador_tabla(self, id_entrenador): return self._clase_consultas_dao.clases_entrenador_tabla(id_entrenador)
    def ocupacion_clases_entrenador(self, id_entrenador): return self._clase_consultas_dao.ocupacion_clases_entrenador(id_entrenador)
    def informacion_clase_con_sala(self, id_clase): return self._clase_consultas_dao.informacion_clase_con_sala(id_clase)
    def buscar_clase(self, id_clase): return self._clase_consultas_dao.buscar_clase(id_clase)
    def recepcion_clases_hoy(self): return self._clase_consultas_dao.recepcion_clases_hoy()

    # ── INSCRIPCIONES ────────────────────────────────────────────────────
    def contar_inscripciones(self): return sum(1 for v in self._inscripcion_dao.select() if v.estado == "inscrito")
    def buscar_inscripciones(self, texto: str): return self._inscripcion_consultas_dao.buscar_inscripciones(texto)
    def contar_inscripciones_clase(self, nombre_actividad: str): return self._inscripcion_consultas_dao.contar_inscripciones_clase(nombre_actividad)
    def inscribirse_clase(self, id_cliente: int, id_clase: int):
        vos = self._inscripcion_dao.selectByCliente(id_cliente)
        for v in vos:
            if v.id_clase == id_clase and v.estado == "inscrito":
                raise ValueError("Ya estás inscrito en esta clase")
        return self._inscripcion_dao.insert(InscripcionVO(None, id_cliente, id_clase, None, "inscrito"))
    def desapuntarse_clase(self, id_cliente: int, id_clase: int):
        for v in self._inscripcion_dao.selectByCliente(id_cliente):
            if v.id_clase == id_clase and v.estado == "inscrito":
                return self._inscripcion_dao.updateEstado(v.id_inscripcion, "cancelado")
        raise ValueError("No estás inscrito en esa clase")
    def clases_inscritas_cliente(self, id_cliente: int): return self._inscripcion_consultas_dao.clases_inscritas_cliente(id_cliente)
    def clientes_inscritos_clase(self, id_clase: int): return self._inscripcion_consultas_dao.clientes_inscritos_clase(id_clase)
    def listar_inscripciones_resumen(self): return self._inscripcion_consultas_dao.listar_inscripciones_resumen()
    def estadisticas_inscripciones(self): return self._inscripcion_consultas_dao.estadisticas_inscripciones()
    def inscribirse_clase_por_nombre(self, id_cliente, nombre_actividad):
        clases = self.buscar_clases(nombre_actividad)
        if not clases:
            raise ValueError("No se encontró ninguna clase con ese nombre")
        id_clase = clases[0][0]
        return self.inscribirse_clase(id_cliente, id_clase)

    # ── ASISTENCIA ───────────────────────────────────────────────────────
    def registrar_asistencia_lista(self, id_clase: int, fecha: str, ids_presentes: list):
        inscritos = self._inscripcion_dao.selectByClase(id_clase)
        for ins in inscritos:
            presente = "si" if ins.id_cliente in ids_presentes else "no"
            self._asistencia_dao.insert(AsistenciaVO(None, ins.id_cliente, id_clase, fecha, presente))
        return True
    def calcular_calorias_cliente(self, id_cliente: int): return self._asistencia_consultas_dao.calcular_calorias_cliente(id_cliente)
    def estadisticas_cliente(self, id_cliente: int): return self._asistencia_consultas_dao.estadisticas_cliente(id_cliente)
    def historial_cliente(self, id_cliente: int): return [(v.id_asistencia, v.id_clase, v.fecha, v.presente) for v in self._asistencia_dao.selectByCliente(id_cliente)]
    def ranking_clientes_activos(self): return self._asistencia_consultas_dao.ranking_clientes_activos()
    def consultar_asistencia_clase(self, id_clase: int): return self._asistencia_consultas_dao.consultar_asistencia_clase(id_clase)
    def asistencia_clase_fecha(self, id_clase, fecha): return self._asistencia_consultas_dao.asistencia_clase_fecha(id_clase, fecha)
    def registrar_asistencia(self, id_cliente, id_clase, fecha, presente): return self._asistencia_consultas_dao.registrar_asistencia(id_cliente, id_clase, fecha, presente)

    # ── PAGOS / TARIFAS / INFORMES ───────────────────────────────────────
    def registrar_pago(self, id_cliente, id_contable, id_tarifa, importe, metodo_pago, tipo_cuota):
        vo = PagoVO(None, id_cliente, id_contable, id_tarifa, importe, metodo_pago,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pendiente", tipo_cuota)
        return self._pago_dao.insert(vo)
    def marcar_pago_abonado(self, id_pago: int): return self._pago_consultas_dao.marcar_pago_abonado(id_pago)
    def listar_pagos(self): return [(v.id_pago, v.id_cliente, v.id_contable, v.id_tarifa, v.importe, v.metodo_pago, v.fecha_pago, v.estado, v.tipo_cuota) for v in self._pago_dao.select()]
    def pagos_pendientes(self): return self._pago_consultas_dao.pagos_pendientes()
    def pagos_cliente(self, id_cliente: int): return [(v.id_pago, v.importe, v.metodo_pago, v.fecha_pago, v.estado, v.tipo_cuota) for v in self._pago_dao.selectByCliente(id_cliente)]
    def informe_pagos_realizados(self): return self._pago_consultas_dao.informe_pagos_realizados()
    def informe_pagos_por_mes(self): return self.ingresos_por_mes()
    def total_ingresos(self): return self._pago_consultas_dao.total_ingresos()
    def ingresos_por_mes(self): return self._pago_consultas_dao.ingresos_por_mes()
    def contar_clientes_tarifa(self, nombre_tarifa: str): return self._tarifa_consultas_dao.contar_clientes_tarifa(nombre_tarifa)
    def listar_tarifas(self): return [(v.id_tarifa, v.nombre, v.precio_mensual, v.servicios_incluidos, v.fecha_inicio, v.fecha_fin) for v in self._tarifa_dao.select()]
    def generar_informe(self, id_contable: int, tipo: str): return self._informe_consultas_dao.generar_informe(id_contable, tipo)
    def listar_informes(self): return [(v.id_informe, v.id_contable, v.tipo_informe, v.fecha_generacion) for v in self._informe_dao.select()]
    def informe_salarios(self): return self._informe_consultas_dao.informe_salarios()
    def ingresos_mes_actual(self): return self._pago_consultas_dao.ingresos_mes_actual()
    def ingresos_anio_actual(self): return self._pago_consultas_dao.ingresos_anio_actual()
    def numero_clientes_pendientes_pago(self): return self._pago_consultas_dao.numero_clientes_pendientes_pago()
    def importe_pendiente_cobrar(self): return self._pago_consultas_dao.importe_pendiente_cobrar()
    def listar_pagos_pendientes_admin(self): return self._pago_consultas_dao.listar_pagos_pendientes_admin()
    def buscar_pago_pendiente_por_dni(self, dni): return self._pago_consultas_dao.buscar_pago_pendiente_por_dni(dni)


    # ── CONTABLE ─────────────────────────────────────────────────────────
    def cobros_hoy_contable(self): return self._pago_consultas_dao.cobros_hoy_contable()
    def ultimos_pagos_inicio_contable(self): return self._pago_consultas_dao.ultimos_pagos_inicio_contable()
    def pagos_pendientes_inicio_contable(self): return self._pago_consultas_dao.pagos_pendientes_inicio_contable()
    def num_pagos_pendientes_contable(self): return self._pago_consultas_dao.num_pagos_pendientes_contable()
    def ingresos_mes_contable(self): return self._pago_consultas_dao.ingresos_mes_contable()
    def contable_clientes_con_deuda(self): return self._pago_consultas_dao.contable_clientes_con_deuda()
    def contable_importe_pendiente(self): return self._pago_consultas_dao.contable_importe_pendiente()
    def contable_pagos_vencidos(self): return self._pago_consultas_dao.contable_pagos_vencidos()
    def contable_pagos_vencen_semana(self): return self._pago_consultas_dao.contable_pagos_vencen_semana()
    def buscar_cliente_tarifa_por_dni(self, dni): return self._pago_consultas_dao.buscar_cliente_tarifa_por_dni(dni)
    def registrar_pago_contable(self, dni_cliente, id_contable, metodo_pago, fecha_pago): return self._pago_consultas_dao.registrar_pago_contable(dni_cliente, id_contable, metodo_pago, fecha_pago)
    def num_tarifas_activas_contable(self): return self._tarifa_consultas_dao.num_tarifas_activas_contable()
    def contable_tarifas_economica(self): return self._tarifa_consultas_dao.contable_tarifas_economica()
    def contable_salarios_personal(self): return self._empleado_consultas_dao.contable_salarios_personal()
    def contable_total_nominas(self): return self._pago_consultas_dao.contable_total_nominas()
    def contable_balance_economico(self): return self._pago_consultas_dao.contable_balance_economico()
    def num_informes_mes_contable(self): return self._informe_consultas_dao.num_informes_mes_contable()
    def contable_gastos_mes(self): return self._pago_consultas_dao.contable_gastos_mes()
    def contable_balance_mes(self): return self._pago_consultas_dao.contable_balance_mes()
    def historial_informes_contable(self): return self._informe_consultas_dao.historial_informes_contable()
    def contable_pagos_registrados(self, id_contable): return self._pago_consultas_dao.contable_pagos_registrados(id_contable)
    def contable_pendientes_revisados(self): return self._pago_consultas_dao.contable_pendientes_revisados()
    def contable_informes_generados_usuario(self, id_contable): return self._informe_consultas_dao.contable_informes_generados_usuario(id_contable)
    def contable_importe_gestionado(self, id_contable): return self._pago_consultas_dao.contable_importe_gestionado(id_contable)

    def informe_balance_mensual_contable(self):
        total_nominas = self.contable_total_nominas()
        gasto_mensual = total_nominas / 12 if total_nominas else 0
        return self._informe_consultas_dao.informe_balance_mensual_contable(gasto_mensual)

    def informe_gestion_economica_contable(self):
        ingresos, gastos, balance = self.contable_balance_economico()
        pendiente = self.contable_importe_pendiente()
        tarifas_activas = self.num_tarifas_activas_contable()
        nominas = self.contable_total_nominas()
        return self._informe_consultas_dao.informe_gestion_economica_contable(
            ingresos, gastos, balance, pendiente, tarifas_activas, nominas
        )

    # ── REGISTRO DE ACCESO / RECEPCIÓN ───────────────────────────────────
    def registrar_acceso(self, id_usuario: int, tipo_acceso: str):
        vo = RegistroAccesoVO(None, id_usuario, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tipo_acceso)
        return self._acceso_dao.insert(vo)
    def listar_accesos(self): return [(v.id_registro, v.id_usuario, v.fecha_hora_registro, v.tipo_acceso) for v in self._acceso_dao.select()]
    def recepcion_entradas_hoy(self): return self._registro_acceso_consultas_dao.recepcion_entradas_hoy()
    def recepcion_nuevos_usuarios_hoy(self): return self._usuario_consultas_dao.recepcion_nuevos_usuarios_hoy()
    def recepcion_ultimos_registros_acceso(self): return self._registro_acceso_consultas_dao.recepcion_ultimos_registros_acceso()
    def ultimo_acceso_cliente(self, id_usuario): return self._registro_acceso_consultas_dao.ultimo_acceso_cliente(id_usuario)
    def listar_ultimos_accesos_control(self): return self._registro_acceso_consultas_dao.listar_ultimos_accesos_control()

    # ── USUARIO COMPLETO / RELACIONES POR ROL ────────────────────────────
    def crear_relacion_usuario_por_rol(self, id_usuario: int, id_rol: int, id_admin: int):
        if id_rol == 1:
            return self.registrar_cliente(id_usuario)
        self.registrar_empleado(id_usuario, 0.00)
        if id_rol == 2:
            return self.registrar_entrenador(id_usuario, "General", id_admin)
        if id_rol == 3:
            return self.registrar_recepcionista(id_usuario, "mañana", id_admin)
        if id_rol == 4:
            return self.registrar_administrador(id_usuario)
        if id_rol == 5:
            return self.registrar_contable(id_usuario, "ADE", id_admin)
        raise ValueError("Rol no reconocido")

    def crear_usuario_completo(self, dni, nombre, telefono, email, username, password, id_rol, direccion, fecha_nacimiento, id_admin_registra=None):
        self.registrar_usuario(dni, nombre, telefono, email, username, password, id_rol, direccion, fecha_nacimiento)
        usuario_vo = self._usuario_dao.selectByUsername(username)
        if usuario_vo is None:
            raise ValueError("No se pudo obtener el usuario recién creado")
        self.crear_relacion_usuario_por_rol(usuario_vo.id_usuario, id_rol,
                                            id_admin_registra if id_admin_registra is not None else usuario_vo.id_usuario)
        return usuario_vo.id_usuario

    # ── ESTADÍSTICAS ─────────────────────────────────────────────────────
    def estadisticas_admin(self): return self._estadisticas_consultas_dao.estadisticas_admin()
    def ranking_usuarios_activos_estadisticas(self): return self._estadisticas_consultas_dao.ranking_usuarios_activos_estadisticas()
    def ocupacion_por_clase_estadisticas(self): return self._estadisticas_consultas_dao.ocupacion_por_clase_estadisticas()

    def clientes_pendientes_admin(self):
        return self._pago_consultas_dao.clientes_pendientes_admin()
