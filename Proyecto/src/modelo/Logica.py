from src.modelo.logica.LogicaAutenticacion import LogicaAutenticacion
from src.modelo.logica.LogicaClientes import LogicaClientes
from src.modelo.logica.LogicaRecepcionista import LogicaRecepcionista
from src.modelo.logica.LogicaPagos import LogicaPagos
from src.modelo.logica.LogicaClases import LogicaClases
from src.modelo.logica.LogicaEstadisticas import LogicaEstadisticas
from src.modelo.logica.LogicaUsuarios import LogicaUsuarios
from src.modelo.logica.LogicaBackup import LogicaBackup
from src.modelo.logica.LogicaInformes import LogicaInformes


class Logica:
    """
    Capa de lógica de negocio de la aplicación.

    Los controladores llaman a esta clase. Esta clase coordina los módulos
    de lógica específicos. Ningún controlador debe acceder directamente
    a DAO ni ejecutar SQL.
    """

    def __init__(self):
        self._auth = LogicaAutenticacion()
        self._usuarios = LogicaUsuarios()
        self._clientes = LogicaClientes()
        self._recepcion = LogicaRecepcionista()
        self._pagos = LogicaPagos()
        self._clases = LogicaClases()
        self._estadisticas = LogicaEstadisticas()
        self._backup = LogicaBackup()
        self._informes = LogicaInformes()

    # ── Autenticación ───────────────────────────────────────────────────
    def iniciar_sesion(self, username, password):
        return self._auth.iniciar_sesion(username, password)

    # ── Usuarios / perfiles ─────────────────────────────────────────────
    def registrar_usuario(self, *args, **kwargs):
        return self._usuarios.registrar_usuario(*args, **kwargs)

    def crear_usuario_completo(self, *args, **kwargs):
        return self._usuarios.crear_usuario_completo(*args, **kwargs)

    def modificar_usuario(self, *args, **kwargs):
        return self._usuarios.modificar_usuario(*args, **kwargs)

    def perfil_usuario(self, *args, **kwargs):
        return self._usuarios.perfil_usuario(*args, **kwargs)

    def eliminar_usuario(self, *args, **kwargs):
        return self._usuarios.eliminar_usuario(*args, **kwargs)

    def buscar_usuario(self, *args, **kwargs):
        return self._usuarios.buscar_usuario(*args, **kwargs)

    def listar_usuarios(self, *args, **kwargs):
        return self._usuarios.listar_usuarios(*args, **kwargs)

    def cambiar_password(self, *args, **kwargs):
        return self._usuarios.cambiar_password(*args, **kwargs)

    def crear_relacion_usuario_por_rol(self, *args, **kwargs):
        return self._usuarios.crear_relacion_usuario_por_rol(*args, **kwargs)
    
    def resumen_trabajadores_por_rol(self, trabajadores):
        return self._usuarios.resumen_trabajadores_por_rol(trabajadores)

    # ── Trabajadores ────────────────────────────────────────────────────
    def contar_trabajadores(self):
        return self._usuarios.contar_trabajadores()

    def contar_por_rol(self, rol):
        return self._usuarios.contar_por_rol(rol)

    def listar_trabajadores_completo(self):
        return self._usuarios.listar_trabajadores_completo()

    def buscar_trabajadores(self, texto):
        return self._usuarios.buscar_trabajadores(texto)

    def buscar_trabajadores_rol(self, rol):
        return self._usuarios.buscar_trabajadores_rol(rol)

    def guardar_cambios_trabajador(self, *args, **kwargs):
        return self._usuarios.guardar_cambios_trabajador(*args, **kwargs)

    def registrar_empleado(self, *args, **kwargs):
        return self._usuarios.registrar_empleado(*args, **kwargs)

    def registrar_entrenador(self, *args, **kwargs):
        return self._usuarios.registrar_entrenador(*args, **kwargs)

    def registrar_recepcionista(self, *args, **kwargs):
        return self._usuarios.registrar_recepcionista(*args, **kwargs)

    def registrar_contable(self, *args, **kwargs):
        return self._usuarios.registrar_contable(*args, **kwargs)

    def registrar_administrador(self, *args, **kwargs):
        return self._usuarios.registrar_administrador(*args, **kwargs)

    def listar_empleados(self, *args, **kwargs):
        return self._usuarios.listar_empleados(*args, **kwargs)

    # ── Clientes ────────────────────────────────────────────────────────

    def calorias_semana_por_dia(self, id_cliente):
        return self._clientes.calorias_semana_por_dia(id_cliente)
    
    def calcular_objetivo_semanal(self, calorias_semana):
        return self._clientes.calcular_objetivo_semanal(calorias_semana)

    def clases_asistidas_cliente(self, id_cliente):
        return self._clientes.clases_asistidas_cliente(id_cliente)

    def desapuntarse_clase_por_nombre(self, id_cliente, nombre_actividad):
        return self._clientes.desapuntarse_clase_por_nombre(id_cliente, nombre_actividad)
    
    def contar_usuarios(self):
        return self._clientes.contar_usuarios()

    def listar_clientes(self):
        return self._clientes.listar_clientes()

    def listar_clientes_completo(self):
        return self._clientes.listar_clientes_completo()

    def buscar_clientes(self, texto):
        return self._clientes.buscar_clientes(texto)

    def buscar_clientes_estado(self, estado):
        return self._clientes.buscar_clientes_estado(estado)

    def datos_inicio_cliente(self, id_cliente):
        return self._clientes.datos_inicio_cliente(id_cliente)

    def crear_cliente_desde_recepcion(self, *args, **kwargs):
        return self._clientes.crear_cliente_desde_recepcion(*args, **kwargs)

    def recepcion_total_clientes(self):
        return self._clientes.recepcion_total_clientes()

    def recepcion_total_clientes_lista(self):
        return self._clientes.recepcion_total_clientes_lista()

    def recepcion_clientes_recientes(self):
        return self._clientes.recepcion_clientes_recientes()

    def recepcion_nuevos_clientes_mes(self):
        return self._clientes.recepcion_nuevos_clientes_mes()

    def recepcion_listar_clientes_filtrados(self, dni="", tipo="Todos", plan="Todos"):
        return self._clientes.recepcion_listar_clientes_filtrados(dni, tipo, plan)

    def recepcion_guardar_cambios_cliente(self, *args, **kwargs):
        return self._clientes.recepcion_guardar_cambios_cliente(*args, **kwargs)
    
    

    # ── Recepción ───────────────────────────────────────────────────────
    def recepcion_entradas_hoy(self):
        return self._recepcion.recepcion_entradas_hoy()

    def recepcion_nuevos_usuarios_hoy(self):
        return self._recepcion.recepcion_nuevos_usuarios_hoy()

    def recepcion_clases_hoy(self):
        return self._recepcion.recepcion_clases_hoy()

    def recepcion_ultimos_registros_acceso(self):
        return self._recepcion.recepcion_ultimos_registros_acceso()

    def buscar_cliente_acceso_por_dni_o_id(self, texto):
        return self._recepcion.buscar_cliente_acceso_por_dni_o_id(texto)

    def registrar_acceso_cliente_control(self, id_usuario, tipo_acceso):
        return self._recepcion.registrar_acceso_cliente_control(id_usuario, tipo_acceso)

    def listar_ultimos_accesos_control(self):
        return self._recepcion.listar_ultimos_accesos_control()

    def registrar_acceso(self, *args, **kwargs):
        return self._recepcion.registrar_acceso(*args, **kwargs)

    def listar_accesos(self):
        return self._recepcion.listar_accesos()

    def ultimo_acceso_cliente(self, id_usuario):
        return self._recepcion.ultimo_acceso_cliente(id_usuario)
    
    def validar_datos_registro_cliente(self, *args, **kwargs):
        return self._clientes.validar_datos_registro_cliente(*args, **kwargs)

    def convertir_fecha_a_bd(self, fecha):
        return self._clientes.convertir_fecha_a_bd(fecha)

    # ── Clases / inscripciones / asistencia ─────────────────────────────
    def clases_ocupacion_cliente(self):
        return self._clases.clases_ocupacion_cliente()

    def clases_hoy_entrenador(self, id_entrenador):
        return self._clases.clases_hoy_entrenador(id_entrenador)
    
    
    def contar_clases(self):
        return self._clases.contar_clases()

    def listar_clases(self):
        return self._clases.listar_clases()

    def buscar_clases(self, texto):
        return self._clases.buscar_clases(texto)

    def clases_de_entrenador(self, id_entrenador):
        return self._clases.clases_de_entrenador(id_entrenador)

    def registrar_clase(self, *args, **kwargs):
        return self._clases.registrar_clase(*args, **kwargs)

    def guardar_cambios_clase_tabla(self, *args, **kwargs):
        return self._clases.guardar_cambios_clase_tabla(*args, **kwargs)

    def modificar_clase(self, *args, **kwargs):
        return self._clases.modificar_clase(*args, **kwargs)

    def eliminar_clase(self, *args, **kwargs):
        return self._clases.eliminar_clase(*args, **kwargs)

    def ocupacion_clases(self):
        return self._clases.ocupacion_clases()

    def contar_inscripciones(self):
        return self._clases.contar_inscripciones()

    def contar_inscripciones_clase(self, nombre):
        return self._clases.contar_inscripciones_clase(nombre)

    def listar_inscripciones_resumen(self):
        return self._clases.listar_inscripciones_resumen()

    def buscar_inscripciones(self, texto):
        return self._clases.buscar_inscripciones(texto)

    def estadisticas_inscripciones(self):
        return self._clases.estadisticas_inscripciones()

    def consultar_asistencia_clase(self, id_clase):
        return self._clases.consultar_asistencia_clase(id_clase)

    def registrar_asistencia(self, *args, **kwargs):
        return self._clases.registrar_asistencia(*args, **kwargs)

    def asistencia_clase_fecha(self, *args, **kwargs):
        return self._clases.asistencia_clase_fecha(*args, **kwargs)

    def buscar_clase(self, id_clase):
        return self._clases.buscar_clase(id_clase)

    def clases_entrenador_tabla(self, id_entrenador):
        return self._clases.clases_entrenador_tabla(id_entrenador)

    def ocupacion_clases_entrenador(self, id_entrenador):
        return self._clases.ocupacion_clases_entrenador(id_entrenador)

    def informacion_clase_con_sala(self, id_clase):
        return self._clases.informacion_clase_con_sala(id_clase)

    def clientes_inscritos_clase(self, id_clase):
        return self._clases.clientes_inscritos_clase(id_clase)

    def registrar_asistencia_lista(self, *args, **kwargs):
        return self._clases.registrar_asistencia_lista(*args, **kwargs)

    def calcular_calorias_cliente(self, *args, **kwargs):
        return self._clases.calcular_calorias_cliente(*args, **kwargs)

    def estadisticas_cliente(self, *args, **kwargs):
        return self._clases.estadisticas_cliente(*args, **kwargs)

    def historial_cliente(self, *args, **kwargs):
        return self._clases.historial_cliente(*args, **kwargs)

    def ranking_clientes_activos(self, *args, **kwargs):
        return self._clases.ranking_clientes_activos(*args, **kwargs)

    def inscribirse_clase_por_nombre(self, id_cliente, nombre_actividad):
        return self._clientes.inscribirse_clase_por_nombre(id_cliente, nombre_actividad)

    def inscribirse_clase(self, id_cliente, id_clase):
        return self._clientes.inscribirse_clase(id_cliente, id_clase)

    def desapuntarse_clase(self, id_cliente, id_clase):
        return self._clientes.desapuntarse_clase(id_cliente, id_clase)

    def clases_inscritas_cliente(self, id_cliente):
        return self._clientes.clases_inscritas_cliente(id_cliente)
    
    
    def total_inscritos_clases_entrenador(self, id_entrenador):
        return self._clases.total_inscritos_clases_entrenador(id_entrenador)

    def ocupacion_media_entrenador(self, id_entrenador):
        return self._clases.ocupacion_media_entrenador(id_entrenador)

    def resumen_ocupacion_entrenador(self, id_entrenador):
        return self._clases.resumen_ocupacion_entrenador(id_entrenador)

    def registrar_asistencia_normalizada(self, id_cliente, id_clase, fecha, estado):
        return self._clases.registrar_asistencia_normalizada(
            id_cliente,
            id_clase,
            fecha,
            estado
        )
    
    def normalizar_estado_asistencia(self, estado):
        return self._clases.normalizar_estado_asistencia(estado)
    
    def datos_clase_asistencia(self, id_clase):
        return self._clases.datos_clase_asistencia(id_clase)

    # ── Pagos / contabilidad ────────────────────────────────────────────
    def primer_pago_pendiente(self):
        return self._pagos.primer_pago_pendiente()
    
    def registrar_pago(self, *args, **kwargs):
        return self._pagos.registrar_pago(*args, **kwargs)

    def marcar_pago_abonado(self, id_pago):
        return self._pagos.marcar_pago_abonado(id_pago)

    def listar_pagos(self):
        return self._pagos.listar_pagos()

    def pagos_pendientes(self):
        return self._pagos.pagos_pendientes()

    def pagos_cliente(self, id_cliente):
        return self._pagos.pagos_cliente(id_cliente)

    def listar_pagos_pendientes_admin(self):
        return self._pagos.listar_pagos_pendientes_admin()

    def clientes_pendientes_admin(self):
        return self._pagos.clientes_pendientes_admin()

    def buscar_pago_pendiente_por_dni(self, dni):
        return self._pagos.buscar_pago_pendiente_por_dni(dni)

    def buscar_cliente_pendiente_por_dni_admin(self, dni):
        return self._pagos.buscar_cliente_pendiente_por_dni_admin(dni)

    def ingresos_mes_actual(self):
        return self._pagos.ingresos_mes_actual()

    def ingresos_anio_actual(self):
        return self._pagos.ingresos_anio_actual()

    def numero_clientes_pendientes_pago(self):
        return self._pagos.numero_clientes_pendientes_pago()

    def importe_pendiente_cobrar(self):
        return self._pagos.importe_pendiente_cobrar()

    def ingresos_por_mes(self):
        return self._pagos.ingresos_por_mes()

    def total_ingresos(self):
        return self._pagos.total_ingresos()

    def contar_clientes_tarifa(self, nombre_tarifa):
        return self._pagos.contar_clientes_tarifa(nombre_tarifa)

    def listar_tarifas(self):
        return self._pagos.listar_tarifas()

    def generar_informe(self, id_contable, tipo):
        return self._informes.generar_informe(id_contable, tipo)
    
    def exportar_pdf_informe(self, id_contable, tipo, cabeceras, filas):
        return self._informes.exportar_pdf(id_contable, tipo, cabeceras, filas)

    def listar_informes(self):
        return self._pagos.listar_informes()

    def informe_pagos_realizados(self):
        return self._pagos.informe_pagos_realizados()

    def informe_pagos_por_mes(self):
        return self._pagos.informe_pagos_por_mes()

    def informe_salarios(self):
        return self._pagos.informe_salarios()
    
    def es_pago_vencido(self, fecha_pago):
        return self._pagos.es_pago_vencido(fecha_pago)

    def normalizar_metodo_pago(self, metodo_pago):
        return self._pagos.normalizar_metodo_pago(metodo_pago)

    # ── Contable ────────────────────────────────────────────────────────
    def cobros_hoy_contable(self):
        return self._pagos.cobros_hoy_contable()

    def ultimos_pagos_inicio_contable(self):
        return self._pagos.ultimos_pagos_inicio_contable()

    def pagos_pendientes_inicio_contable(self):
        return self._pagos.pagos_pendientes_inicio_contable()

    def num_pagos_pendientes_contable(self):
        return self._pagos.num_pagos_pendientes_contable()

    def ingresos_mes_contable(self):
        return self._pagos.ingresos_mes_contable()

    def num_tarifas_activas_contable(self):
        return self._pagos.num_tarifas_activas_contable()

    def num_informes_mes_contable(self):
        return self._informes.num_informes_mes_contable()

    def contable_clientes_con_deuda(self):
        return self._pagos.contable_clientes_con_deuda()

    def contable_importe_pendiente(self):
        return self._pagos.contable_importe_pendiente()

    def contable_pagos_vencidos(self):
        return self._pagos.contable_pagos_vencidos()

    def contable_pagos_vencen_semana(self):
        return self._pagos.contable_pagos_vencen_semana()

    def buscar_cliente_tarifa_por_dni(self, dni):
        return self._pagos.buscar_cliente_tarifa_por_dni(dni)

    def registrar_pago_contable(self, dni_cliente, id_contable, metodo_pago, fecha_pago):
        return self._pagos.registrar_pago_contable(
            dni_cliente,
            id_contable,
            metodo_pago,
            fecha_pago
        )

    def contable_tarifas_economica(self):
        return self._pagos.contable_tarifas_economica()

    def contable_salarios_personal(self):
        return self._pagos.contable_salarios_personal()

    def contable_total_nominas(self):
        return self._pagos.contable_total_nominas()

    def contable_balance_economico(self):
        return self._pagos.contable_balance_economico()

    def informe_balance_mensual_contable(self):
        return self._pagos.informe_balance_mensual_contable()

    def informe_gestion_economica_contable(self):
        return self._pagos.informe_gestion_economica_contable()

    def contable_gastos_mes(self):
        return self._pagos.contable_gastos_mes()

    def contable_balance_mes(self):
        return self._pagos.contable_balance_mes()

    def historial_informes_contable(self):
        return self._informes.historial_informes_contable()

    def contable_pagos_registrados(self, id_contable):
        return self._pagos.contable_pagos_registrados(id_contable)

    def contable_pendientes_revisados(self):
        return self._pagos.contable_pendientes_revisados()

    def contable_informes_generados_usuario(self, id_contable):
        return self._informes.contable_informes_generados_usuario(id_contable)

    def contable_importe_gestionado(self, id_contable):
        return self._pagos.contable_importe_gestionado(id_contable)

    # ── Estadísticas ────────────────────────────────────────────────────
    def estadisticas_admin(self):
        return self._estadisticas.estadisticas_admin()

    def ranking_usuarios_activos_estadisticas(self):
        return self._estadisticas.ranking_usuarios_activos_estadisticas()

    def ocupacion_por_clase_estadisticas(self):
        return self._estadisticas.ocupacion_por_clase_estadisticas()

    # ── Copias de seguridad ─────────────────────────────────────────────
    def crear_copia_seguridad(self):
        return self._backup.crear_copia_seguridad()

    def restaurar_copia_seguridad(self, ruta_sql):
        return self._backup.restaurar_copia_seguridad(ruta_sql)

    # ── Validación y utilidades de usuario ──────────────────────────────
    def validar_nuevo_usuario(self, dni, nombre, telefono, email,
                               username, password, confirmar, fecha_texto):
        return self._usuarios.validar_nuevo_usuario(
            dni, nombre, telefono, email, username, password, confirmar, fecha_texto)

    def rol_texto_a_id(self, rol_texto):
        return self._usuarios.rol_texto_a_id(rol_texto)

    # ── Utilidades de pagos ──────────────────────────────────────────────
    def fecha_pago_actual(self):
        return self._pagos.fecha_pago_actual()

    # ── Utilidades de clientes ───────────────────────────────────────────
    def periodo_semana_actual(self):
        return self._clientes.periodo_semana_actual()

    def texto_estado_pago(self, estado_pagado):
        return self._clientes.texto_estado_pago(estado_pagado)

    # ── Estadísticas del entrenador ──────────────────────────────────────
    def resumen_asistencia_clase(self, id_clase, fecha):
        return self._clases.resumen_asistencia_clase(id_clase, fecha)

    def estadisticas_perfil_entrenador(self, id_entrenador):
        return self._clases.estadisticas_perfil_entrenador(id_entrenador)