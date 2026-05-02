class AdminitradorVO:
    def __init__(self, id_administrador):
        self._id_adminitrador = id_administrador
        
    @property
    def id_administrador(self):
        return self._id_administrador