class ModificacionPerfilVO:
    """VO que transporta los datos de modificación de perfil
    desde el controlador al modelo."""

    def __init__(self, id_usuario, telefono, email, direccion):
        self._id_usuario = id_usuario
        self._telefono   = telefono
        self._email      = email
        self._direccion  = direccion

    @property
    def id_usuario(self): return self._id_usuario
    @property
    def telefono(self):   return self._telefono
    @property
    def email(self):      return self._email
    @property
    def direccion(self):  return self._direccion
