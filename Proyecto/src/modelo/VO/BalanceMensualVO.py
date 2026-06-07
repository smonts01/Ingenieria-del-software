class BalanceMensualVO:
    """VO para el informe de balance mensual."""
    def __init__(self, anio, mes, ingresos, gastos, balance):
        self._anio     = anio
        self._mes      = mes
        self._ingresos = ingresos
        self._gastos   = gastos
        self._balance  = balance
    @property
    def anio(self):     return self._anio
    @property
    def mes(self):      return self._mes
    @property
    def ingresos(self): return self._ingresos
    @property
    def gastos(self):   return self._gastos
    @property
    def balance(self):  return self._balance
