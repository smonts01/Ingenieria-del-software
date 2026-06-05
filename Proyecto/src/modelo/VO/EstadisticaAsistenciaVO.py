class EstadisticaAsistenciaVO:
    """VO que representa estadísticas de asistencia de un cliente a una actividad."""

    def __init__(self, nombre_actividad, asistencias, calorias):
        self._nombre_actividad = nombre_actividad
        self._asistencias      = asistencias
        self._calorias         = calorias

    @property
    def nombre_actividad(self): return self._nombre_actividad
    @property
    def asistencias(self):      return self._asistencias
    @property
    def calorias(self):         return self._calorias
