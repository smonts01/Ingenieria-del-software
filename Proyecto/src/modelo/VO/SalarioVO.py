class SalarioVO:
    """VO para los salarios del personal."""
    def __init__(self, nombre, rol, salario):
        self._nombre  = nombre
        self._rol     = rol
        self._salario = salario
    @property
    def nombre(self):  return self._nombre
    @property
    def rol(self):     return self._rol
    @property
    def salario(self): return self._salario
