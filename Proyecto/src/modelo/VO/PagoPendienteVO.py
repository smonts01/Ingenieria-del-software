class PagoPendienteVO:
    """VO que representa un pago pendiente con datos del cliente y tarifa."""

    def __init__(self, id_pago, nombre_cliente, nombre_tarifa, importe, fecha, tipo_cuota):
        self._id_pago         = id_pago
        self._nombre_cliente  = nombre_cliente
        self._nombre_tarifa   = nombre_tarifa
        self._importe         = importe
        self._fecha           = fecha
        self._tipo_cuota      = tipo_cuota

    @property
    def id_pago(self):        return self._id_pago
    @property
    def nombre_cliente(self): return self._nombre_cliente
    @property
    def nombre_tarifa(self):  return self._nombre_tarifa
    @property
    def importe(self):        return self._importe
    @property
    def fecha(self):          return self._fecha
    @property
    def tipo_cuota(self):     return self._tipo_cuota
