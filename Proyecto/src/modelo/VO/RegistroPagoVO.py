class RegistroPagoVO:
    """VO que transporta los datos del formulario de registro de pago
    desde el controlador al modelo."""

    def __init__(self, dni_cliente, id_contable, metodo_pago, fecha_pago):
        self._dni_cliente  = dni_cliente
        self._id_contable  = id_contable
        self._metodo_pago  = metodo_pago
        self._fecha_pago   = fecha_pago

    @property
    def dni_cliente(self):  return self._dni_cliente
    @property
    def id_contable(self):  return self._id_contable
    @property
    def metodo_pago(self):  return self._metodo_pago
    @property
    def fecha_pago(self):   return self._fecha_pago
