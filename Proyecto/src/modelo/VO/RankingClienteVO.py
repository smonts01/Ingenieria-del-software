class RankingClienteVO:
    """VO que representa un cliente en el ranking de más activos."""

    def __init__(self, nombre, asistencias):
        self._nombre      = nombre
        self._asistencias = asistencias

    @property
    def nombre(self):      return self._nombre
    @property
    def asistencias(self): return self._asistencias
