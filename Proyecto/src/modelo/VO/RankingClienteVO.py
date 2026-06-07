class RankingClienteVO:
    """VO para el ranking de clientes más activos."""
    def __init__(self, nombre, asistencias, ultima_clase=None, estado=None):
        self._nombre       = nombre
        self._asistencias  = asistencias
        self._ultima_clase = ultima_clase
        self._estado       = estado
    @property
    def nombre(self):       return self._nombre
    @property
    def asistencias(self):  return self._asistencias
    @property
    def ultima_clase(self): return self._ultima_clase if self._ultima_clase is not None else '-'
    @property
    def estado(self):       return self._estado if self._estado is not None else 'Activo'
