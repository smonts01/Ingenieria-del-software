class RegistroAccesoVO:
    def __init__(self, id_registro, id_usuario, fecha_hora_registro, tipo_acceso):
        self._id_registro = id_registro
        self._id_usuario = id_usuario
        self._fecha_hora_registro = fecha_hora_registro
        self._tipo_acceso = tipo_acceso
        
    @property
    def id_registro(self):
        return self._id_registro
    
    @property
    def id_usuario(self):
        return self._id_usuario
    
    @property
    def fecha_hora_registro(self):
        return self._fecha_hora_registro
    
    @property
    def tipo_acceso(self):
        return self._tipo_acceso