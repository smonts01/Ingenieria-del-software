class PagoVO:
    def __init__(self, id_pago=None, id_cliente=None, id_contable=None,
                 id_tarifa=None, importe=None, metodo_pago=None, fecha_pago=None):
        self.id_pago = id_pago
        self.id_cliente = id_cliente
        self.id_contable = id_contable
        self.id_tarifa = id_tarifa
        self.importe = importe
        self.metodo_pago = metodo_pago
        self.fecha_pago = fecha_pago
    
    