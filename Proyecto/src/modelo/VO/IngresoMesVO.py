class IngresoMesVO:
    """VO para ingresos mensuales del gráfico del admin."""
    def __init__(self, anio, mes, total):
        self._anio  = anio
        self._mes   = mes
        self._total = total
    @property
    def anio(self):  return self._anio
    @property
    def mes(self):   return self._mes
    @property
    def total(self): return self._total
