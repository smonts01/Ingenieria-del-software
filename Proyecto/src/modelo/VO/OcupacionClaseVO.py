class OcupacionClaseVO:
    """VO que representa la ocupación de una clase."""

    def __init__(self, id_clase, nombre_actividad, inscritos, aforo_maximo, porcentaje):
        self._id_clase          = id_clase
        self._nombre_actividad  = nombre_actividad
        self._inscritos         = inscritos
        self._aforo_maximo      = aforo_maximo
        self._porcentaje        = porcentaje

    @property
    def id_clase(self):         return self._id_clase
    @property
    def nombre_actividad(self): return self._nombre_actividad
    @property
    def inscritos(self):        return self._inscritos
    @property
    def aforo_maximo(self):     return self._aforo_maximo
    @property
    def porcentaje(self):       return self._porcentaje