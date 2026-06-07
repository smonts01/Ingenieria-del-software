class OcupacionAdminVO:
    """VO para la ocupación de clases en estadísticas del admin."""
    def __init__(self, nombre_actividad, ocupacion):
        self._nombre_actividad = nombre_actividad
        self._ocupacion        = ocupacion
    @property
    def nombre_actividad(self): return self._nombre_actividad
    @property
    def ocupacion(self):        return self._ocupacion
