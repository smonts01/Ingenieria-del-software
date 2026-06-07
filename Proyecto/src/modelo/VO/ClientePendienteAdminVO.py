class ClientePendienteAdminVO:
    """VO para clientes con pagos pendientes en la vista del administrador."""
    def __init__(self, cliente, dni, tarifa, importe_pendiente, fecha_limite):
        self._cliente          = cliente
        self._dni              = dni
        self._tarifa           = tarifa
        self._importe_pendiente = importe_pendiente
        self._fecha_limite     = fecha_limite

    @property
    def cliente(self):           return self._cliente
    @property
    def dni(self):               return self._dni
    @property
    def tarifa(self):            return self._tarifa
    @property
    def importe_pendiente(self): return self._importe_pendiente
    @property
    def fecha_limite(self):      return self._fecha_limite
