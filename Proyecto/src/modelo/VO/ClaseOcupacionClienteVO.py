class ClaseOcupacionClienteVO:
    """VO para clases con ocupación en la vista del cliente."""
    def __init__(self, id_clase, nombre_actividad, dia_semana,
                 hora_inicio, hora_fin, sala, inscritos, aforo_maximo):
        self._id_clase         = id_clase
        self._nombre_actividad = nombre_actividad
        self._dia_semana       = dia_semana
        self._hora_inicio      = hora_inicio
        self._hora_fin         = hora_fin
        self._sala             = sala
        self._inscritos        = inscritos
        self._aforo_maximo     = aforo_maximo
    @property
    def id_clase(self):         return self._id_clase
    @property
    def nombre_actividad(self): return self._nombre_actividad
    @property
    def dia_semana(self):       return self._dia_semana
    @property
    def hora_inicio(self):      return self._hora_inicio
    @property
    def hora_fin(self):         return self._hora_fin
    @property
    def sala(self):             return self._sala
    @property
    def inscritos(self):        return self._inscritos
    @property
    def aforo_maximo(self):     return self._aforo_maximo
