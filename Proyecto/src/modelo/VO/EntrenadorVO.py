class EntrenadorVO:
    def __init__(self, id_entrenador, especialidad, id_administrador_registra):
        self._id_entrenador = id_entrenador
        self._especialidad = especialidad
        self._id_administrador_registra = id_administrador_registra
        
    @property
    def id_entrenador(self):
        return self._id_entrenador
    
    @property
    def especialidad(self):
        return self._especialidad
    
    @property
    def id_administrador_registra(self):
        return self._id_administrador_registra