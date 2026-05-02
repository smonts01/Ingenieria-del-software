class PagoVO:
    def __init__(self, id_pago, id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago, estado, tipo_cuota):
        self._id_pago = id_pago
        self._id_cliente = id_cliente
        self._id_contable = id_contable
        self._id_tarifa = id_tarifa
        self._importe = importe
        self._metodo_pago = metodo_pago
        self._fecha_pago = fecha_pago
        self._estado = estado
        self._tipo_cuota = tipo_cuota
        
    @property
    def id_pago(self):
        return self._id_pago
    
    @property
    def id_cliente(self):
        return self._id_cliente
    
    @property
    def id_contable(self):
        return self._id_contable
    
    @property
    def id_tarifa(self):
        return self._id_tarifa
    
    @property
    def importe(self):
        return self._importe
    
    @property
    def metodo_pago(self):
        return self._metodo_pago
    
    @property
    def fecha_pago(self):
        return self._fecha_pago
    
    @property
    def estado(self):
        return self._estado
    
    @property
    def tipo_cuota(self):
        return self._tipo_cuota
    
    