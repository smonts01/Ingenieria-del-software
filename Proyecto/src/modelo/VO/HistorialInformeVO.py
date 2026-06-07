class HistorialInformeVO:
    """VO para el historial de informes del contable."""
    def __init__(self, id_informe, contable, tipo_informe, fecha):
        self._id_informe   = id_informe
        self._contable     = contable
        self._tipo_informe = tipo_informe
        self._fecha        = fecha
    @property
    def id_informe(self):   return self._id_informe
    @property
    def contable(self):     return self._contable
    @property
    def tipo_informe(self): return self._tipo_informe
    @property
    def fecha(self):        return self._fecha
