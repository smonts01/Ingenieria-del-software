class InscripcionResumenVO:
    """VO que representa una inscripción con datos del cliente y la clase, devuelto por consultas JOIN."""

    def __init__(self, nombre_cliente, nombre_actividad, fecha_inscripcion, estado):
        self._nombre_cliente    = nombre_cliente
        self._nombre_actividad  = nombre_actividad
        self._fecha_inscripcion = fecha_inscripcion
        self._estado            = estado

    @property
    def nombre_cliente(self):    return self._nombre_cliente
    @property
    def nombre_actividad(self):  return self._nombre_actividad
    @property
    def fecha_inscripcion(self): return self._fecha_inscripcion
    @property
    def estado(self):            return self._estado
