from datetime import date, datetime

from src.modelo.VO.PagoVO import PagoVO

from src.modelo.dao.PagoDaoJDBC import PagoDaoJDBC
from src.modelo.dao.PagoConsultasDaoJDBC import PagoConsultasDaoJDBC
from src.modelo.dao.TarifaDaoJDBC import TarifaDaoJDBC
from src.modelo.dao.TarifaConsultasDaoJDBC import TarifaConsultasDaoJDBC
from src.modelo.dao.InformeDaoJDBC import InformeDaoJDBC
from src.modelo.dao.InformeConsultasDaoJDBC import InformeConsultasDaoJDBC
from src.modelo.dao.EmpleadoConsultasDaoJDBC import EmpleadoConsultasDaoJDBC


class LogicaPagos:
    """Lógica de negocio para pagos, tarifas e informes económicos.
    """

    def __init__(self):
        # DAOs de pagos
        self._pago_dao           = PagoDaoJDBC()
        self._pago_consultas_dao = PagoConsultasDaoJDBC()
        # DAOs de tarifas
        self._tarifa_dao           = TarifaDaoJDBC()
        self._tarifa_consultas_dao = TarifaConsultasDaoJDBC()
        # DAOs de informes
        self._informe_dao           = InformeDaoJDBC()
        self._informe_consultas_dao = InformeConsultasDaoJDBC()
        # DAO de empleados (para salarios)
        self._empleado_consultas_dao = EmpleadoConsultasDaoJDBC()

    # Pagos

    def registrar_pago(self, id_cliente, id_contable, id_tarifa, importe, metodo_pago):
        """Registra un pago e inmediatamente marca al cliente como abonado.

        Valida que todos los campos sean correctos y que el importe sea positivo.
        Devuelve el número de filas afectadas en la tabla pago.
        Lanza ValueError si falta algún campo o el importe es inválido.
        """
        if not id_cliente:   raise ValueError("Debe indicarse el cliente")
        if not id_contable:  raise ValueError("Debe indicarse el contable")
        if not id_tarifa:    raise ValueError("Debe indicarse la tarifa")
        if not metodo_pago:  raise ValueError("Debe indicarse el método de pago")

        try:
            importe_float = float(importe)
        except ValueError:
            raise ValueError("El importe debe ser numérico")

        if importe_float <= 0:
            raise ValueError("El importe debe ser mayor que cero")

        metodo_pago = self.normalizar_metodo_pago(metodo_pago)

        pago_vo = PagoVO(
            id_pago=None,
            id_cliente=id_cliente,
            id_contable=id_contable,
            id_tarifa=id_tarifa,
            importe=importe_float,
            metodo_pago=metodo_pago,
            fecha_pago=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        filas = self._pago_dao.insert(pago_vo)

        # Si el pago se insertó correctamente, actualizar estado del cliente
        if filas:
            self._pago_consultas_dao.marcar_cliente_abonado(id_cliente)

        return filas


    def buscar_cliente_pendiente_por_dni_admin(self, dni):
        """Busca clientes con pago pendiente cuyo DNI coincida con el texto indicado.
        Devuelve lista de ClientePendienteAdminVO."""
        return self._pago_consultas_dao.buscar_cliente_pendiente_por_dni_admin(dni)

    def listar_pagos(self):
        """Devuelve todos los pagos registrados como lista de PagoVO."""
        return self._pago_dao.select()

    def pagos_pendientes(self):
        """Devuelve todos los clientes con pago pendiente como lista de PagoPendienteVO."""
        return self._pago_consultas_dao.pagos_pendientes()

    def pagos_cliente(self, id_cliente):
        """Devuelve todos los pagos de un cliente como lista de PagoVO.
        Lanza ValueError si no se indica el cliente."""
        if not id_cliente:
            raise ValueError("Debe indicarse el cliente")
        return self._pago_dao.selectByCliente(id_cliente)

    def listar_pagos_pendientes_admin(self):
        """Devuelve los clientes con pago pendiente para la tabla del admin
        como lista de ClientePendienteAdminVO."""
        return self._pago_consultas_dao.listar_pagos_pendientes_admin()

    def buscar_pago_pendiente_por_dni(self, dni):
        """Busca el pago pendiente de un cliente por DNI exacto.
        Devuelve la fila del primer resultado o None.
        Lanza ValueError si no se introduce el DNI."""
        if not dni:
            raise ValueError("Debe introducirse el DNI")
        return self._pago_consultas_dao.buscar_pago_pendiente_por_dni(dni)

    def primer_pago_pendiente(self):
        """Devuelve los datos del primer cliente con pago pendiente,
        para precargar el formulario de cobro del contable."""
        return self._pago_consultas_dao.primer_pago_pendiente()

    # Informes económicos

    def informe_pagos_realizados(self):
        """Devuelve todos los pagos realizados como lista de InformePagoVO."""
        return self._pago_consultas_dao.informe_pagos_realizados()

    def informe_pagos_por_mes(self):
        """Devuelve los ingresos agrupados por mes como lista de IngresoMesVO
        """
        return self.ingresos_por_mes()

    def total_ingresos(self):
        """Devuelve la suma total de todos los pagos registrados."""
        return self._pago_consultas_dao.total_ingresos()

    def ingresos_por_mes(self):
        """Devuelve los ingresos de los últimos 6 meses como lista de IngresoMesVO."""
        return self._pago_consultas_dao.ingresos_por_mes()

    def ingresos_mes_actual(self):
        """Devuelve el total de ingresos del mes en curso."""
        return self._pago_consultas_dao.ingresos_mes_actual()

    def ingresos_anio_actual(self):
        """Devuelve el total de ingresos del año en curso."""
        return self._pago_consultas_dao.ingresos_anio_actual()

    def numero_clientes_pendientes_pago(self):
        """Devuelve el número de clientes con estado de pago pendiente."""
        return self._pago_consultas_dao.numero_clientes_pendientes_pago()

    def importe_pendiente_cobrar(self):
        """Devuelve el importe total pendiente de cobrar de todos los clientes."""
        return self._pago_consultas_dao.importe_pendiente_cobrar()

    # Tarifas

    def listar_tarifas(self):
        """Devuelve todas las tarifas del sistema como lista de TarifaVO."""
        return self._tarifa_dao.select()

    def contar_clientes_tarifa(self, nombre_tarifa):
        """Devuelve el número de clientes activos en la tarifa indicada.
        Lanza ValueError si no se indica el nombre de la tarifa."""
        if not nombre_tarifa:
            raise ValueError("Debe indicarse el nombre de la tarifa")
        return self._tarifa_consultas_dao.contar_clientes_tarifa(nombre_tarifa)

    # Generar informes

    def generar_informe(self, id_contable, tipo):
        """Registra un nuevo informe en la base de datos.
        Lanza ValueError si falta el contable o el tipo."""
        if not id_contable:
            raise ValueError("Debe indicarse el contable")
        if not tipo:
            raise ValueError("Debe indicarse el tipo de informe")
        return self._informe_consultas_dao.generar_informe(id_contable, tipo)

    def listar_informes(self):
        """Devuelve todos los informes registrados como lista de InformeVO."""
        return self._informe_dao.select()

    def informe_salarios(self):
        """Devuelve el listado de salarios del personal como lista de SalarioVO."""
        return self._informe_consultas_dao.informe_salarios()

    # Tablas de administrador y contable

    def clientes_pendientes_admin(self):
        """Devuelve los clientes con pago pendiente para la pantalla del admin
        como lista de ClientePendienteAdminVO."""
        return self._pago_consultas_dao.clientes_pendientes_admin()

    def pagos_pendientes_inicio_contable(self):
        """Devuelve los primeros 10 clientes con pago pendiente para el inicio
        del contable como lista de PagoPendienteInicioVO."""
        return self._pago_consultas_dao.pagos_pendientes_inicio_contable()

    def ultimos_pagos_inicio_contable(self):
        """Devuelve los últimos 10 pagos registrados para el inicio del contable
        como lista de UltimoPagoVO."""
        return self._pago_consultas_dao.ultimos_pagos_inicio_contable()

    # Todo lo relacionado con interfaz contable

    def cobros_hoy_contable(self):
        """Devuelve el número de pagos registrados hoy."""
        return self._pago_consultas_dao.cobros_hoy_contable()

    def num_pagos_pendientes_contable(self):
        """Devuelve el número total de clientes con pago pendiente."""
        return self._pago_consultas_dao.num_pagos_pendientes_contable()

    def ingresos_mes_contable(self):
        """Devuelve los ingresos del mes en curso para el panel del contable."""
        return self._pago_consultas_dao.ingresos_mes_contable()

    def num_tarifas_activas_contable(self):
        """Devuelve el número de tarifas activas en el sistema."""
        return self._tarifa_consultas_dao.num_tarifas_activas_contable()

    def num_informes_mes_contable(self):
        """Devuelve el número de informes generados en el mes actual."""
        return self._informe_consultas_dao.num_informes_mes_contable()

    def contable_clientes_con_deuda(self):
        """Devuelve el número de clientes con deuda pendiente."""
        return self._pago_consultas_dao.contable_clientes_con_deuda()

    def contable_importe_pendiente(self):
        """Devuelve el importe total pendiente de cobrar."""
        return self._pago_consultas_dao.contable_importe_pendiente()

    def contable_pagos_vencidos(self):
        """Devuelve el número de pagos cuya fecha ya ha vencido y no están abonados."""
        return self._pago_consultas_dao.contable_pagos_vencidos()

    def contable_pagos_vencen_semana(self):
        """Devuelve el número de pagos que vencen en los próximos 7 días."""
        return self._pago_consultas_dao.contable_pagos_vencen_semana()

    def buscar_cliente_tarifa_por_dni(self, dni):
        """Devuelve los datos del cliente y su tarifa activa por DNI exacto.
        Lanza ValueError si no se introduce el DNI."""
        if not dni:
            raise ValueError("Debe introducirse el DNI del cliente")
        return self._pago_consultas_dao.buscar_cliente_tarifa_por_dni(dni)

    def registrar_pago_contable(self, dni_cliente, id_contable, metodo_pago, fecha_pago):
        """Registra el pago de un cliente identificado por DNI.
        Lanza ValueError si falta algún campo obligatorio."""
        if not dni_cliente: raise ValueError("Introduce el DNI del cliente")
        if not id_contable: raise ValueError("Debe indicarse el contable")
        if not metodo_pago: raise ValueError("Selecciona un método de pago")
        if not fecha_pago:  raise ValueError("Debe indicarse la fecha de pago")

        metodo_pago = self.normalizar_metodo_pago(metodo_pago)
        return self._pago_consultas_dao.registrar_pago_contable(
            dni_cliente, id_contable, metodo_pago, fecha_pago
        )

    def fecha_pago_actual(self):
        """Devuelve la fecha y hora actuales formateadas para insertar en la BD."""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def contable_tarifas_economica(self):
        """Devuelve las tarifas con precio y duración para la pantalla de
        gestión económica como lista de TarifaEconomicaVO."""
        return self._tarifa_consultas_dao.contable_tarifas_economica()

    def contable_salarios_personal(self):
        """Devuelve el listado de salarios del personal como lista de SalarioVO."""
        return self._empleado_consultas_dao.contable_salarios_personal()

    def contable_total_nominas(self):
        """Devuelve la suma total de todas las nóminas del personal."""
        return self._pago_consultas_dao.contable_total_nominas()

    def contable_balance_economico(self):
        """Devuelve una tupla (ingresos, gastos, balance) con el balance global."""
        return self._pago_consultas_dao.contable_balance_economico()

    def informe_balance_mensual_contable(self):
        """Genera el informe de balance mensual usando el total de nóminas como gasto.
        Devuelve lista de BalanceMensualVO."""
        gasto_mensual = self.contable_total_nominas()
        return self._informe_consultas_dao.informe_balance_mensual_contable(gasto_mensual)

    def informe_gestion_economica_contable(self):
        """Genera el informe de gestión económica con ingresos, gastos, balance,
        importe pendiente, tarifas activas y nóminas del mes.
        Devuelve lista de GestionEconomicaVO."""
        ingresos        = self.ingresos_mes_contable()
        gastos          = self.contable_gastos_mes()
        balance         = self.contable_balance_mes()
        pendiente       = self.contable_importe_pendiente()
        tarifas_activas = self.num_tarifas_activas_contable()
        nominas         = self.contable_total_nominas()
        return self._informe_consultas_dao.informe_gestion_economica_contable(
            ingresos, gastos, balance, pendiente, tarifas_activas, nominas
        )

    def contable_gastos_mes(self):
        """Devuelve los gastos del mes actual (equivale al total de nóminas)."""
        return self._pago_consultas_dao.contable_gastos_mes()

    def contable_balance_mes(self):
        """Devuelve el balance del mes: ingresos del mes menos nóminas."""
        return self._pago_consultas_dao.contable_balance_mes()

    def historial_informes_contable(self):
        """Devuelve el historial de informes generados como lista de HistorialInformeVO."""
        return self._informe_consultas_dao.historial_informes_contable()

    def contable_pagos_registrados(self, id_contable):
        """Devuelve el número de pagos registrados por un contable concreto.
        Lanza ValueError si no se indica el contable."""
        if not id_contable:
            raise ValueError("Debe indicarse el contable")
        return self._pago_consultas_dao.contable_pagos_registrados(id_contable)

    def contable_pendientes_revisados(self):
        """Devuelve el número de clientes con pago pendiente
        """
        return self._pago_consultas_dao.contable_pendientes_revisados()

    def contable_informes_generados_usuario(self, id_contable):
        """Devuelve el número de informes generados por un contable concreto.
        Lanza ValueError si no se indica el contable."""
        if not id_contable:
            raise ValueError("Debe indicarse el contable")
        return self._informe_consultas_dao.contable_informes_generados_usuario(id_contable)

    def contable_importe_gestionado(self, id_contable):
        """Devuelve el importe total gestionado por un contable concreto.
        Lanza ValueError si no se indica el contable."""
        if not id_contable:
            raise ValueError("Debe indicarse el contable")
        return self._pago_consultas_dao.contable_importe_gestionado(id_contable)

    # Reglas que hay que cumplir

    def es_pago_vencido(self, fecha_pago) -> bool:
        """Determina si una fecha de pago ha vencido (es anterior a hoy).

        Acepta fecha como string 'YYYY-MM-DD', objeto date o datetime.
        Devuelve False si la fecha no se puede convertir.
        """
        fecha_convertida = fecha_pago

        # Convertir string a date
        if isinstance(fecha_pago, str):
            try:
                fecha_convertida = datetime.strptime(fecha_pago[:10], "%Y-%m-%d").date()
            except Exception:
                return False
        # Convertir datetime a date
        elif hasattr(fecha_pago, "date"):
            fecha_convertida = fecha_pago.date()

        if fecha_convertida is None:
            return False

        return fecha_convertida < date.today()

    def normalizar_metodo_pago(self, metodo_pago) -> str:
        """Valida y normaliza el método de pago a minúsculas.

        Métodos aceptados: tarjeta, efectivo, transferencia, bizum.
        Lanza ValueError si el método no es válido.
        """
        metodo = str(metodo_pago).strip().lower()
        metodos_validos = ["tarjeta", "efectivo", "transferencia", "bizum"]
        if metodo not in metodos_validos:
            raise ValueError(
                "Método de pago no válido. Selecciona tarjeta, efectivo, transferencia o bizum."
            )
        return metodo

    def _valor(self, objeto, atributos, indice, defecto=None):
        """Extrae un valor de un objeto VO o tupla de forma segura.

        Primero intenta obtener el valor por atributo (VO).
        Si no existe, lo intenta por índice (tupla).
        Devuelve defecto si ninguna opción funciona.
        Útil para código que debe ser compatible con ambos formatos.
        """
        if not isinstance(atributos, (list, tuple)):
            atributos = [atributos]
        for atributo in atributos:
            if hasattr(objeto, atributo):
                return getattr(objeto, atributo)
        try:
            return objeto[indice]
        except Exception:
            return defecto

    def _pago_pendiente_a_tupla(self, pago):
        """Convierte un PagoPendienteVO a tupla para compatibilidad.
        Si ya es tupla o lista, la devuelve tal cual."""
        if isinstance(pago, (tuple, list)):
            return tuple(pago)
        return (
            pago.id_pago,
            pago.nombre_cliente,
            pago.nombre_tarifa,
            pago.importe,
            pago.fecha,
        )