class TrabajadorVO:
    """VO que representa un trabajador con su rol, devuelto por consultas JOIN."""

    def __init__(self, id_usuario, dni, nombre, telefono, email,
                 username, nombre_rol, direccion, fecha_nacimiento):
        self._id_usuario      = id_usuario
        self._dni             = dni
        self._nombre          = nombre
        self._telefono        = telefono
        self._email           = email
        self._username        = username
        self._nombre_rol      = nombre_rol
        self._direccion       = direccion
        self._fecha_nacimiento = fecha_nacimiento

    @property
    def id_usuario(self):       return self._id_usuario
    @property
    def dni(self):              return self._dni
    @property
    def nombre(self):           return self._nombre
    @property
    def telefono(self):         return self._telefono
    @property
    def email(self):            return self._email
    @property
    def username(self):         return self._username
    @property
    def nombre_rol(self):       return self._nombre_rol
    @property
    def direccion(self):        return self._direccion
    @property
    def fecha_nacimiento(self): return self._fecha_nacimiento
