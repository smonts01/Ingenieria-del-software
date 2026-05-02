class InformeVO:
    def __init__(self, id_informe, id_contable, tipo_informe, fecha_generacion):
        self._id_informe = id_informe
        self._id_contable = id_contable
        self._tipo_informe = tipo_informe
        self._fecha_generacion = fecha_generacion
        
        
    @property
    def id_informe(self):
        return self._id_informe
    
    @property
    def id_contable(self):
        return self._id_contable
    
    @property
    def tipo_inform(self):
        return self._tipo_informe
    
    @property
    def fecha_genracion(self):
        return self._fecha_generacion
    