class NuevoUsuarioFormVO:
    """VO que transporta los datos del formulario de registro de usuario
    desde el controlador al modelo."""

    def __init__(self, dni, nombre, telefono, email, username, password,
                 id_rol, direccion, fecha_nacimiento):
        self._dni              = dni
        self._nombre           = nombre
        self._telefono         = telefono
        self._email            = email
        self._username         = username
        self._password         = password
        self._id_rol           = id_rol
        self._direccion        = direccion
        self._fecha_nacimiento = fecha_nacimiento

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
    def password(self):         return self._password
    @property
    def id_rol(self):           return self._id_rol
    @property
    def direccion(self):        return self._direccion
    @property
    def fecha_nacimiento(self): return self._fecha_nacimiento
