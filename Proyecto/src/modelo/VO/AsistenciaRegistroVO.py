class AsistenciaRegistroVO:
    """VO que representa el estado de asistencia de un cliente a una clase en una fecha."""

    def __init__(self, id_cliente, presente):
        self._id_cliente = id_cliente
        self._presente   = presente

    @property
    def id_cliente(self): return self._id_cliente
    @property
    def presente(self):   return self._presente
