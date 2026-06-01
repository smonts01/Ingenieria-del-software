from src.modelo.dao.ServicioProyectoDaoJDBC import ServicioProyectoDaoJDBC
from src.modelo.logica.LogicaAutenticacion import LogicaAutenticacion
from src.modelo.logica.LogicaClientes import LogicaClientes
from src.modelo.logica.LogicaRecepcionista import LogicaRecepcionista
from src.modelo.logica.LogicaPagos import LogicaPagos
from src.modelo.logica.LogicaClases import LogicaClases
from src.modelo.logica.LogicaEstadisticas import LogicaEstadisticas
from src.modelo.logica.LogicaAdministrador import LogicaAdministrador


class Logica:
    """
    Capa de lógica de negocio de la aplicación.

    Los controladores llaman a esta clase. Esta clase valida reglas de negocio
    y coordina los módulos de lógica específicos. Ningún controlador debe
    acceder directamente a DAO ni ejecutar SQL.
    """

    def __init__(self):
        self._servicio = ServicioProyectoDaoJDBC()
        self._auth = LogicaAutenticacion(self._servicio)
        self._clientes = LogicaClientes(self._servicio)
        self._recepcion = LogicaRecepcionista(self._servicio)
        self._pagos = LogicaPagos(self._servicio)
        self._clases = LogicaClases(self._servicio)
        self._estadisticas = LogicaEstadisticas(self._servicio)
        self._admin = LogicaAdministrador(self._servicio)

    # ── Autenticación ─────────────────────────────────────────────────────
    def iniciar_sesion(self, username, password):
        return self._auth.iniciar_sesion(username, password)

    # ── Usuarios / perfiles ───────────────────────────────────────────────
    def registrar_usuario(self, *args, **kwargs): return self._servicio.registrar_usuario(*args, **kwargs)
    def crear_usuario_completo(self, *args, **kwargs): return self._servicio.crear_usuario_completo(*args, **kwargs)
    def modificar_usuario(self, *args, **kwargs): return self._servicio.modificar_usuario(*args, **kwargs)
    def perfil_usuario(self, *args, **kwargs): return self._servicio.perfil_usuario(*args, **kwargs)
    def datos_inicio_cliente(self, *args, **kwargs): return self._servicio.datos_inicio_cliente(*args, **kwargs)

    # ── Clientes ─────────────────────────────────────────────────────────
    def contar_usuarios(self): return self._servicio.contar_usuarios()
    def listar_clientes(self): return self._servicio.listar_clientes()
    def listar_clientes_completo(self): return self._servicio.listar_clientes_completo()
    def buscar_clientes(self, texto): return self._servicio.buscar_clientes(texto)
    def crear_cliente_desde_recepcion(self, *args, **kwargs): return self._clientes.crear_cliente_desde_recepcion(*args, **kwargs)
    def recepcion_total_clientes_lista(self): return self._servicio.recepcion_total_clientes_lista()
    def recepcion_nuevos_clientes_mes(self): return self._servicio.recepcion_nuevos_clientes_mes()
    def recepcion_listar_clientes_filtrados(self, dni="", tipo="Todos", plan="Todos"):
        return self._servicio.recepcion_listar_clientes_filtrados(dni, tipo, plan)
    def recepcion_guardar_cambios_cliente(self, *args, **kwargs): return self._clientes.recepcion_guardar_cambios_cliente(*args, **kwargs)

    # ── Recepción ────────────────────────────────────────────────────────
    def recepcion_total_clientes(self): return self._servicio.recepcion_total_clientes()
    def recepcion_entradas_hoy(self): return self._servicio.recepcion_entradas_hoy()
    def recepcion_nuevos_usuarios_hoy(self): return self._servicio.recepcion_nuevos_usuarios_hoy()
    def recepcion_clases_hoy(self): return self._servicio.recepcion_clases_hoy()
    def recepcion_ultimos_registros_acceso(self): return self._servicio.recepcion_ultimos_registros_acceso()
    def recepcion_clientes_recientes(self): return self._servicio.recepcion_clientes_recientes()
    def buscar_cliente_acceso_por_dni_o_id(self, texto): return self._recepcion.buscar_cliente_acceso_por_dni_o_id(texto)
    def registrar_acceso_cliente_control(self, id_usuario, tipo_acceso): return self._recepcion.registrar_acceso_cliente_control(id_usuario, tipo_acceso)
    def listar_ultimos_accesos_control(self): return self._servicio.listar_ultimos_accesos_control()
    def registrar_acceso(self, *args, **kwargs): return self._servicio.registrar_acceso(*args, **kwargs)
    def listar_accesos(self): return self._servicio.listar_accesos()

    # ── Trabajadores ─────────────────────────────────────────────────────
    def contar_trabajadores(self): return self._servicio.contar_trabajadores()
    def contar_por_rol(self, rol): return self._servicio.contar_por_rol(rol)
    def listar_trabajadores_completo(self): return self._servicio.listar_trabajadores_completo()
    def buscar_trabajadores(self, texto): return self._servicio.buscar_trabajadores(texto)
    def buscar_trabajadores_rol(self, rol): return self._servicio.buscar_trabajadores_rol(rol)
    def guardar_cambios_trabajador(self, *args, **kwargs): return self._servicio.guardar_cambios_trabajador(*args, **kwargs)

    # ── Clases / inscripciones / asistencia ──────────────────────────────
    def contar_clases(self): return self._servicio.contar_clases()
    def listar_clases(self): return self._servicio.listar_clases()
    def buscar_clases(self, texto): return self._servicio.buscar_clases(texto)
    def clases_de_entrenador(self, id_entrenador): return self._servicio.clases_de_entrenador(id_entrenador)
    def registrar_clase(self, *args, **kwargs): return self._admin.registrar_clase(*args, **kwargs)
    def guardar_cambios_clase_tabla(self, *args, **kwargs): return self._admin.guardar_cambios_clase_tabla(*args, **kwargs)
    def contar_inscripciones_clase(self, nombre): return self._servicio.contar_inscripciones_clase(nombre)
    def listar_inscripciones_resumen(self): return self._servicio.listar_inscripciones_resumen()
    def buscar_inscripciones(self, texto): return self._servicio.buscar_inscripciones(texto)
    def estadisticas_inscripciones(self): return self._servicio.estadisticas_inscripciones()
    def inscribirse_clase_por_nombre(self, id_cliente, nombre_actividad): return self._clientes.inscribirse_clase_por_nombre(id_cliente, nombre_actividad)
    def consultar_asistencia_clase(self, id_clase): return self._servicio.consultar_asistencia_clase(id_clase)
    def registrar_asistencia(self, *args, **kwargs): return self._servicio.registrar_asistencia(*args, **kwargs)
    def asistencia_clase_fecha(self, *args, **kwargs): return self._servicio.asistencia_clase_fecha(*args, **kwargs)
    def buscar_clase(self, id_clase): return self._servicio.buscar_clase(id_clase)
    def clases_entrenador_tabla(self, id_entrenador): return self._servicio.clases_entrenador_tabla(id_entrenador)
    def ocupacion_clases_entrenador(self, id_entrenador): return self._servicio.ocupacion_clases_entrenador(id_entrenador)
    def informacion_clase_con_sala(self, id_clase): return self._servicio.informacion_clase_con_sala(id_clase)
    def clientes_inscritos_clase(self, id_clase): return self._servicio.clientes_inscritos_clase(id_clase)

    # ── Pagos / contabilidad ─────────────────────────────────────────────
    def registrar_pago(self, *args, **kwargs): return self._pagos.registrar_pago(*args, **kwargs)
    def marcar_pago_abonado(self, id_pago): return self._pagos.marcar_pago_abonado(id_pago)
    def listar_pagos(self): return self._servicio.listar_pagos()
    def pagos_pendientes(self): return self._servicio.pagos_pendientes()
    def listar_pagos_pendientes_admin(self): return self._servicio.listar_pagos_pendientes_admin()
    def buscar_pago_pendiente_por_dni(self, dni): return self._servicio.buscar_pago_pendiente_por_dni(dni)
    def ingresos_mes_actual(self): return self._servicio.ingresos_mes_actual()
    def ingresos_anio_actual(self): return self._servicio.ingresos_anio_actual()
    def numero_clientes_pendientes_pago(self): return self._servicio.numero_clientes_pendientes_pago()
    def importe_pendiente_cobrar(self): return self._servicio.importe_pendiente_cobrar()
    def ingresos_por_mes(self): return self._servicio.ingresos_por_mes()
    def contar_clientes_tarifa(self, nombre_tarifa): return self._servicio.contar_clientes_tarifa(nombre_tarifa)
    def generar_informe(self, *args, **kwargs): return self._servicio.generar_informe(*args, **kwargs)
    def listar_informes(self): return self._servicio.listar_informes()
    def informe_pagos_realizados(self): return self._servicio.informe_pagos_realizados()
    def informe_pagos_por_mes(self): return self._servicio.informe_pagos_por_mes()
    def informe_salarios(self): return self._servicio.informe_salarios()


    # ── Delegaciones explícitas restantes ───────────────────────────────
    def eliminar_usuario(self, *args, **kwargs): return self._servicio.eliminar_usuario(*args, **kwargs)
    def buscar_usuario(self, *args, **kwargs): return self._servicio.buscar_usuario(*args, **kwargs)
    def listar_usuarios(self, *args, **kwargs): return self._servicio.listar_usuarios(*args, **kwargs)
    def cambiar_password(self, *args, **kwargs): return self._servicio.cambiar_password(*args, **kwargs)
    def registrar_cliente(self, *args, **kwargs): return self._servicio.registrar_cliente(*args, **kwargs)
    def buscar_clientes_estado(self, *args, **kwargs): return self._servicio.buscar_clientes_estado(*args, **kwargs)
    def insertar_cliente_recepcion(self, *args, **kwargs): return self._servicio.insertar_cliente_recepcion(*args, **kwargs)
    def registrar_empleado(self, *args, **kwargs): return self._servicio.registrar_empleado(*args, **kwargs)
    def registrar_entrenador(self, *args, **kwargs): return self._servicio.registrar_entrenador(*args, **kwargs)
    def registrar_recepcionista(self, *args, **kwargs): return self._servicio.registrar_recepcionista(*args, **kwargs)
    def registrar_contable(self, *args, **kwargs): return self._servicio.registrar_contable(*args, **kwargs)
    def registrar_administrador(self, *args, **kwargs): return self._servicio.registrar_administrador(*args, **kwargs)
    def listar_empleados(self, *args, **kwargs): return self._servicio.listar_empleados(*args, **kwargs)
    def modificar_clase(self, *args, **kwargs): return self._servicio.modificar_clase(*args, **kwargs)
    def eliminar_clase(self, *args, **kwargs): return self._servicio.eliminar_clase(*args, **kwargs)
    def ocupacion_clases(self, *args, **kwargs): return self._servicio.ocupacion_clases(*args, **kwargs)
    def contar_inscripciones(self, *args, **kwargs): return self._servicio.contar_inscripciones(*args, **kwargs)
    def inscribirse_clase(self, *args, **kwargs): return self._servicio.inscribirse_clase(*args, **kwargs)
    def desapuntarse_clase(self, *args, **kwargs): return self._servicio.desapuntarse_clase(*args, **kwargs)
    def clases_inscritas_cliente(self, *args, **kwargs): return self._servicio.clases_inscritas_cliente(*args, **kwargs)
    def registrar_asistencia_lista(self, *args, **kwargs): return self._servicio.registrar_asistencia_lista(*args, **kwargs)
    def calcular_calorias_cliente(self, *args, **kwargs): return self._servicio.calcular_calorias_cliente(*args, **kwargs)
    def estadisticas_cliente(self, *args, **kwargs): return self._servicio.estadisticas_cliente(*args, **kwargs)
    def historial_cliente(self, *args, **kwargs): return self._servicio.historial_cliente(*args, **kwargs)
    def ranking_clientes_activos(self, *args, **kwargs): return self._servicio.ranking_clientes_activos(*args, **kwargs)
    def pagos_cliente(self, *args, **kwargs): return self._servicio.pagos_cliente(*args, **kwargs)
    def total_ingresos(self, *args, **kwargs): return self._servicio.total_ingresos(*args, **kwargs)
    def listar_tarifas(self, *args, **kwargs): return self._servicio.listar_tarifas(*args, **kwargs)
    def ultimo_acceso_cliente(self, *args, **kwargs): return self._servicio.ultimo_acceso_cliente(*args, **kwargs)
    def crear_relacion_usuario_por_rol(self, *args, **kwargs): return self._servicio.crear_relacion_usuario_por_rol(*args, **kwargs)


    # ── Contable ─────────────────────────────────────────────────────────
    def cobros_hoy_contable(self): return self._servicio.cobros_hoy_contable()
    def ultimos_pagos_inicio_contable(self): return self._servicio.ultimos_pagos_inicio_contable()
    def pagos_pendientes_inicio_contable(self): return self._servicio.pagos_pendientes_inicio_contable()
    def num_pagos_pendientes_contable(self): return self._servicio.num_pagos_pendientes_contable()
    def ingresos_mes_contable(self): return self._servicio.ingresos_mes_contable()
    def num_tarifas_activas_contable(self): return self._servicio.num_tarifas_activas_contable()
    def num_informes_mes_contable(self): return self._servicio.num_informes_mes_contable()
    def contable_clientes_con_deuda(self): return self._servicio.contable_clientes_con_deuda()
    def contable_importe_pendiente(self): return self._servicio.contable_importe_pendiente()
    def contable_pagos_vencidos(self): return self._servicio.contable_pagos_vencidos()
    def contable_pagos_vencen_semana(self): return self._servicio.contable_pagos_vencen_semana()
    def buscar_cliente_tarifa_por_dni(self, dni): return self._servicio.buscar_cliente_tarifa_por_dni(dni)
    def registrar_pago_contable(self, dni_cliente, id_contable, metodo_pago, fecha_pago): return self._servicio.registrar_pago_contable(dni_cliente, id_contable, metodo_pago, fecha_pago)
    def contable_tarifas_economica(self): return self._servicio.contable_tarifas_economica()
    def contable_salarios_personal(self): return self._servicio.contable_salarios_personal()
    def contable_total_nominas(self): return self._servicio.contable_total_nominas()
    def contable_balance_economico(self): return self._servicio.contable_balance_economico()
    def informe_balance_mensual_contable(self): return self._servicio.informe_balance_mensual_contable()
    def informe_gestion_economica_contable(self): return self._servicio.informe_gestion_economica_contable()
    def contable_gastos_mes(self): return self._servicio.contable_gastos_mes()
    def contable_balance_mes(self): return self._servicio.contable_balance_mes()
    def historial_informes_contable(self): return self._servicio.historial_informes_contable()
    def contable_pagos_registrados(self, id_contable): return self._servicio.contable_pagos_registrados(id_contable)
    def contable_pendientes_revisados(self): return self._servicio.contable_pendientes_revisados()
    def contable_informes_generados_usuario(self, id_contable): return self._servicio.contable_informes_generados_usuario(id_contable)
    def contable_importe_gestionado(self, id_contable): return self._servicio.contable_importe_gestionado(id_contable)

    # ── Estadísticas ──────────────────────────────────────────────────────
    def estadisticas_admin(self): return self._estadisticas.estadisticas_admin()
    def ranking_usuarios_activos_estadisticas(self): return self._estadisticas.ranking_usuarios_activos_estadisticas()
    def ocupacion_por_clase_estadisticas(self): return self._estadisticas.ocupacion_por_clase_estadisticas()
