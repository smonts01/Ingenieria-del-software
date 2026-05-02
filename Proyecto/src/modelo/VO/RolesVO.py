class RolesVO:
    def __init__(self, id_rol, nombre_rol):
        self._id_rol = id_rol
        self._nombre_rol = nombre_rol
        
    @property
    def id_rol(self):
        return self._id_rol
    
    @property
    def nombre_rol(self):
        return self._nombre_rol