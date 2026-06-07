class TarifaEconomicaVO:
    """VO para tarifas en gestión económica."""
    def __init__(self, nombre, precio, duracion):
        self._nombre   = nombre
        self._precio   = precio
        self._duracion = duracion
    @property
    def nombre(self):   return self._nombre
    @property
    def precio(self):   return self._precio
    @property
    def duracion(self): return self._duracion
