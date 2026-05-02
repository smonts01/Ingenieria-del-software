class ContableVO:
    def __init__(self, id_contable, titulacion, id_administrador_registra):
        self._id_contable = id_contable
        self._titulacion = titulacion
        self._id_administrador_registra = id_administrador_registra
        
    @property
    def id_contable(self):
        return self._id_contable
    
    @property
    def titulacion(self):
        return self._titulacion
    
    @property
    def id_administrador_registra(self):
        return self._id_administrador_registra