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
    """Reglas de negocio relacionadas con pagos, tarifas e informes económicos."""

    def __init__(self):
        self._pago_dao = PagoDaoJDBC()
        self._pago_consultas_dao = PagoConsultasDaoJDBC()

        self._tarifa_dao = TarifaDaoJDBC()
        self._tarifa_consultas_dao = TarifaConsultasDaoJDBC()

        self._informe_dao = InformeDaoJDBC()
        self._informe_consultas_dao = InformeConsultasDaoJDBC()

        self._empleado_consultas_dao = EmpleadoConsultasDaoJDBC()

    # ── PAGOS ─────────────────────────────────────────────────────

    def registrar_pago(self, id_cliente, id_contable, id_tarifa, importe, metodo_pago, tipo_cuota):
        if not id_cliente:
            raise ValueError("Debe indicarse el cliente")

        if not id_contable:
            raise ValueError("Debe indicarse el contable")

        if not id_tarifa:
            raise ValueError("Debe indicarse la tarifa")

        if not metodo_pago:
            raise ValueError("Debe indicarse el método de pago")

        if not tipo_cuota:
            raise ValueError("Debe indicarse el tipo de cuota")

        try:
            importe_float = float(importe)
        except ValueError:
            raise ValueError("El importe debe ser numérico")

        if importe_float <= 0:
            raise ValueError("El importe debe ser mayor que cero")

        pago_vo = PagoVO(
            None,
            id_cliente,
            id_contable,
            id_tarifa,
            importe_float,
            metodo_pago,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pendiente",
            tipo_cuota
        )

        return self._pago_dao.insert(pago_vo)

    def marcar_pago_abonado(self, id_pago):
        if not id_pago:
            raise ValueError("Debe seleccionarse un pago")

        return self._pago_consultas_dao.marcar_pago_abonado(id_pago)

    def listar_pagos(self):
        pagos = self._pago_dao.select()

        return [
            (
                pago.id_pago,
                pago.id_cliente,
                pago.id_contable,
                pago.id_tarifa,
                pago.importe,
                pago.metodo_pago,
                pago.fecha_pago,
                pago.estado,
                pago.tipo_cuota
            )
            for pago in pagos
        ]

    def pagos_pendientes(self):
        return self._pago_consultas_dao.pagos_pendientes()

    def pagos_cliente(self, id_cliente):
        if not id_cliente:
            raise ValueError("Debe indicarse el cliente")

        pagos = self._pago_dao.selectByCliente(id_cliente)

        return [
            (
                pago.id_pago,
                pago.importe,
                pago.metodo_pago,
                pago.fecha_pago,
                pago.estado,
                pago.tipo_cuota
            )
            for pago in pagos
        ]

    def listar_pagos_pendientes_admin(self):
        return self._pago_consultas_dao.listar_pagos_pendientes_admin()

    def buscar_pago_pendiente_por_dni(self, dni):
        if not dni:
            raise ValueError("Debe introducirse el DNI")

        return self._pago_consultas_dao.buscar_pago_pendiente_por_dni(dni)

    # ── INFORMES ECONÓMICOS ────────────────────────────────────────

    def informe_pagos_realizados(self):
        return self._pago_consultas_dao.informe_pagos_realizados()

    def informe_pagos_por_mes(self):
        return self.ingresos_por_mes()

    def total_ingresos(self):
        return self._pago_consultas_dao.total_ingresos()

    def ingresos_por_mes(self):
        return self._pago_consultas_dao.ingresos_por_mes()

    def ingresos_mes_actual(self):
        return self._pago_consultas_dao.ingresos_mes_actual()

    def ingresos_anio_actual(self):
        return self._pago_consultas_dao.ingresos_anio_actual()

    def numero_clientes_pendientes_pago(self):
        return self._pago_consultas_dao.numero_clientes_pendientes_pago()

    def importe_pendiente_cobrar(self):
        return self._pago_consultas_dao.importe_pendiente_cobrar()

    # ── TARIFAS ────────────────────────────────────────────────────

    def listar_tarifas(self):
        tarifas = self._tarifa_dao.select()

        return [
            (
                tarifa.id_tarifa,
                tarifa.nombre,
                tarifa.precio_mensual,
                tarifa.servicios_incluidos,
                tarifa.fecha_inicio,
                tarifa.fecha_fin
            )
            for tarifa in tarifas
        ]

    def contar_clientes_tarifa(self, nombre_tarifa):
        if not nombre_tarifa:
            raise ValueError("Debe indicarse el nombre de la tarifa")

        return self._tarifa_consultas_dao.contar_clientes_tarifa(nombre_tarifa)

    # ── INFORMES ───────────────────────────────────────────────────

    def generar_informe(self, id_contable, tipo):
        if not id_contable:
            raise ValueError("Debe indicarse el contable")

        if not tipo:
            raise ValueError("Debe indicarse el tipo de informe")

        return self._informe_consultas_dao.generar_informe(id_contable, tipo)

    def listar_informes(self):
        informes = self._informe_dao.select()

        return [
            (
                informe.id_informe,
                informe.id_contable,
                informe.tipo_informe,
                informe.fecha_generacion
            )
            for informe in informes
        ]

    def informe_salarios(self):
        return self._informe_consultas_dao.informe_salarios()

    # ── TABLA ADMINISTRADOR / CONTABLE ─────────────────────────────

    def clientes_pendientes_admin(self):
        return self._pago_consultas_dao.clientes_pendientes_admin()

    def pagos_pendientes_inicio_contable(self):
        return self._pago_consultas_dao.pagos_pendientes_inicio_contable()

    def ultimos_pagos_inicio_contable(self):
        return self._pago_consultas_dao.ultimos_pagos_inicio_contable()
    

    # ── CONTABLE ───────────────────────────────────────────────────

    def cobros_hoy_contable(self):
        return self._pago_consultas_dao.cobros_hoy_contable()

    def num_pagos_pendientes_contable(self):
        return self._pago_consultas_dao.num_pagos_pendientes_contable()

    def ingresos_mes_contable(self):
        return self._pago_consultas_dao.ingresos_mes_contable()

    def num_tarifas_activas_contable(self):
        return self._tarifa_consultas_dao.num_tarifas_activas_contable()

    def num_informes_mes_contable(self):
        return self._informe_consultas_dao.num_informes_mes_contable()

    def contable_clientes_con_deuda(self):
        return self._pago_consultas_dao.contable_clientes_con_deuda()

    def contable_importe_pendiente(self):
        return self._pago_consultas_dao.contable_importe_pendiente()

    def contable_pagos_vencidos(self):
        return self._pago_consultas_dao.contable_pagos_vencidos()

    def contable_pagos_vencen_semana(self):
        return self._pago_consultas_dao.contable_pagos_vencen_semana()

    def buscar_cliente_tarifa_por_dni(self, dni):
        if not dni:
            raise ValueError("Debe introducirse el DNI del cliente")

        return self._pago_consultas_dao.buscar_cliente_tarifa_por_dni(dni)

    def registrar_pago_contable(self, dni_cliente, id_contable, metodo_pago, fecha_pago):
        if not dni_cliente:
            raise ValueError("Introduce el DNI del cliente")

        if not id_contable:
            raise ValueError("Debe indicarse el contable")

        if not metodo_pago:
            raise ValueError("Selecciona un método de pago")

        if not fecha_pago:
            raise ValueError("Debe indicarse la fecha de pago")

        return self._pago_consultas_dao.registrar_pago_contable(
            dni_cliente,
            id_contable,
            metodo_pago,
            fecha_pago
        )

    def contable_tarifas_economica(self):
        return self._tarifa_consultas_dao.contable_tarifas_economica()

    def contable_salarios_personal(self):
        return self._empleado_consultas_dao.contable_salarios_personal()

    def contable_total_nominas(self):
        return self._empleado_consultas_dao.contable_total_nominas()

    def contable_balance_economico(self):
        return self._pago_consultas_dao.contable_balance_economico()

    def informe_balance_mensual_contable(self):
        return self._informe_consultas_dao.informe_balance_mensual_contable()

    def informe_gestion_economica_contable(self):
        return self._informe_consultas_dao.informe_gestion_economica_contable()

    def contable_gastos_mes(self):
        return self._pago_consultas_dao.contable_gastos_mes()

    def contable_balance_mes(self):
        return self._pago_consultas_dao.contable_balance_mes()

    def historial_informes_contable(self):
        return self._informe_consultas_dao.historial_informes_contable()

    def contable_pagos_registrados(self, id_contable):
        if not id_contable:
            raise ValueError("Debe indicarse el contable")

        return self._pago_consultas_dao.contable_pagos_registrados(id_contable)

    def contable_pendientes_revisados(self):
        return self._pago_consultas_dao.contable_pendientes_revisados()

    def contable_informes_generados_usuario(self, id_contable):
        if not id_contable:
            raise ValueError("Debe indicarse el contable")

        return self._informe_consultas_dao.contable_informes_generados_usuario(id_contable)

    def contable_importe_gestionado(self, id_contable):
        if not id_contable:
            raise ValueError("Debe indicarse el contable")

        return self._pago_consultas_dao.contable_importe_gestionado(id_contable)
    

    def es_pago_vencido(self, fecha_pago):
        """
        Regla de negocio:
        Un pago está vencido si su fecha es anterior a la fecha actual.
        """
        fecha_convertida = fecha_pago

        if isinstance(fecha_pago, str):
            try:
                fecha_convertida = datetime.strptime(fecha_pago[:10], "%Y-%m-%d").date()
            except Exception:
                return False

        elif hasattr(fecha_pago, "date"):
            fecha_convertida = fecha_pago.date()

        if fecha_convertida is None:
            return False

        return fecha_convertida < date.today()

    
    def normalizar_metodo_pago(self, metodo_pago):
        """
        Regla de negocio:
        Solo se aceptan los métodos de pago válidos de la aplicación.
        """
        metodo = str(metodo_pago).strip().lower()

        metodos_validos = ["tarjeta", "efectivo", "transferencia", "bizum"]

        if metodo not in metodos_validos:
            raise ValueError(
                "Método de pago no válido. Selecciona tarjeta, efectivo, transferencia o bizum."
            )

        return metodo