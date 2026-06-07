class ClienteInscritoVO:
    """VO para clientes inscritos en una clase."""
    def __init__(self, id_cliente, nombre, telefono, email):
        self._id_cliente = id_cliente
        self._nombre     = nombre
        self._telefono   = telefono
        self._email      = email
    @property
    def id_cliente(self): return self._id_cliente
    @property
    def nombre(self):     return self._nombre
    @property
    def telefono(self):   return self._telefono
    @property
    def email(self):      return self._email
