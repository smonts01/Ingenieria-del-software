class InformePagoVO:
    """VO para el informe de pagos realizados."""
    def __init__(self, cliente, tarifa, importe, fecha, metodo):
        self._cliente = cliente
        self._tarifa  = tarifa
        self._importe = importe
        self._fecha   = fecha
        self._metodo  = metodo
    @property
    def cliente(self): return self._cliente
    @property
    def tarifa(self):  return self._tarifa
    @property
    def importe(self): return self._importe
    @property
    def fecha(self):   return self._fecha
    @property
    def metodo(self):  return self._metodo
