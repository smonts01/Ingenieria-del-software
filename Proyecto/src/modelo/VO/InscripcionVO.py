class InscripcionVO:
    def __init__(self, id_inscripcion, id_cliente, id_clase, fecha_inscripcion, estado):
        self._id_inscripcion = id_inscripcion
        self._id_cliente = id_cliente
        self._id_clase = id_clase
        self._fecha_inscripcion = fecha_inscripcion
        self._estado = estado
        
    @property
    def id_inscripcion(self):
        return self._id_inscripcion
    
    @property
    def id_cliente(self):
        return self._id_cliente
    
    @property
    def id_clase(self):
        return self._id_clase
    
    @property
    def fecha_inscripcion(self):
        return self._fecha_inscripcion
    
    @property
    def estado(self):
        return self._estado