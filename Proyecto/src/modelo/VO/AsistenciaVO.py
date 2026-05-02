class AsistenciaVO:
    def __init__(self, id_asistencia, id_cliente, id_clase, fecha, presente):
        self._id_asistencia = id_asistencia
        self._id_cliente = id_cliente
        self._id_clase = id_clase
        self._fecha = fecha
        self._presente = presente
        
    @property
    def id_asistencia(self):
        return self._id_asistencia
    
    @property
    def id_cliente(self):
        return self._id_cliente
    
    @property
    def id_clase(self):
        return self._id_clase
    
    @property
    def fecha(self):
        return self._fecha
    
    @property
    def presente(self):
        return self._presente
        