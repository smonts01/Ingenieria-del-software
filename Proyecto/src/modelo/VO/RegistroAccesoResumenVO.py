class RegistroAccesoResumenVO:
    """VO que representa un registro de acceso con datos del usuario, devuelto por consultas JOIN."""

    def __init__(self, nombre, dni, tipo_acceso, fecha_hora_registro):
        self._nombre               = nombre
        self._dni                  = dni
        self._tipo_acceso          = tipo_acceso
        self._fecha_hora_registro  = fecha_hora_registro

    @property
    def nombre(self):              return self._nombre
    @property
    def dni(self):                 return self._dni
    @property
    def tipo_acceso(self):         return self._tipo_acceso
    @property
    def fecha_hora_registro(self): return self._fecha_hora_registro
