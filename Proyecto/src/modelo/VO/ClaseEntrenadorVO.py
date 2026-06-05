class ClaseEntrenadorVO:
    """VO que representa una clase con datos de sala y capacidad para el entrenador."""

    def __init__(self, nombre_actividad, sala, horario, dia_semana, capacidad):
        self._nombre_actividad = nombre_actividad
        self._sala             = sala
        self._horario          = horario
        self._dia_semana       = dia_semana
        self._capacidad        = capacidad

    @property
    def nombre_actividad(self): return self._nombre_actividad
    @property
    def sala(self):             return self._sala
    @property
    def horario(self):          return self._horario
    @property
    def dia_semana(self):       return self._dia_semana
    @property
    def capacidad(self):        return self._capacidad