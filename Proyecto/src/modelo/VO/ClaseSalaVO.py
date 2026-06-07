class ClaseSalaVO:
    """VO para información de clase con sala."""
    def __init__(self, nombre_actividad, sala, dia_semana, hora_inicio, hora_fin, aforo_maximo=None):
        self._nombre_actividad = nombre_actividad
        self._sala             = sala
        self._dia_semana       = dia_semana
        self._hora_inicio      = hora_inicio
        self._hora_fin         = hora_fin
        self._aforo_maximo     = aforo_maximo
    @property
    def nombre_actividad(self): return self._nombre_actividad
    @property
    def sala(self):             return self._sala
    @property
    def dia_semana(self):       return self._dia_semana
    @property
    def hora_inicio(self):      return self._hora_inicio
    @property
    def hora_fin(self):         return self._hora_fin
    @property
    def aforo_maximo(self):     return self._aforo_maximo
