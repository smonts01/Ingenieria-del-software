class GestionEconomicaVO:
    """VO para filas del informe de gestión económica."""
    def __init__(self, concepto, valor):
        self._concepto = concepto
        self._valor    = valor
    @property
    def concepto(self): return self._concepto
    @property
    def valor(self):    return self._valor
