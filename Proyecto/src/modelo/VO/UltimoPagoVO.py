class UltimoPagoVO:
    """VO para los últimos pagos en el inicio del contable."""
    def __init__(self, cliente, tarifa, importe, fecha, estado):
        self._cliente = cliente
        self._tarifa  = tarifa
        self._importe = importe
        self._fecha   = fecha
        self._estado  = estado
    @property
    def cliente(self): return self._cliente
    @property
    def tarifa(self):  return self._tarifa
    @property
    def importe(self): return self._importe
    @property
    def fecha(self):   return self._fecha
    @property
    def estado(self):  return self._estado
