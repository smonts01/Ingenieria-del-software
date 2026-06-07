class PagoPendienteInicioVO:
    """VO para pagos pendientes en la tabla de inicio del contable."""
    def __init__(self, cliente, importe_pendiente, fecha_limite):
        self._cliente           = cliente
        self._importe_pendiente = importe_pendiente
        self._fecha_limite      = fecha_limite
    @property
    def cliente(self):           return self._cliente
    @property
    def importe_pendiente(self): return self._importe_pendiente
    @property
    def fecha_limite(self):      return self._fecha_limite
