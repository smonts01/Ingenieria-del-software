class LogicaPagos:
    """Reglas de negocio relacionadas con pagos e informes económicos."""

    def __init__(self, servicio):
        self.servicio = servicio

    def registrar_pago(self, id_cliente, id_contable, id_tarifa, importe, metodo_pago, tipo_cuota):
        if float(importe) <= 0:
            raise ValueError("El importe debe ser mayor que cero")
        return self.servicio.registrar_pago(id_cliente, id_contable, id_tarifa, importe, metodo_pago, tipo_cuota)

    def marcar_pago_abonado(self, id_pago):
        if not id_pago:
            raise ValueError("Debe seleccionarse un pago")
        return self.servicio.marcar_pago_abonado(id_pago)
