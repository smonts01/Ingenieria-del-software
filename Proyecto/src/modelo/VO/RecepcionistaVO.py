class RecepcionistaVO:
    def __init__(self, id_recepcionista, turno, id_administrador_registra):
        self._id_recepcionista = id_recepcionista
        self._turno = turno
        self._id_administrador_registra = id_administrador_registra
        
    @property
    def id_recepcionista(self):
        return self._id_recepcionista
    
    @property
    def turno(self):
        return self._turno
    
    @property
    def id_administrador_registra(self):
        return self._id_administrador_registra