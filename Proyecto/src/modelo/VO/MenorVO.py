class MenorVO:
    def __init__(self, id_cliente, dni_tutor, nombre_tutor):
        self._id_cliente = id_cliente
        self._dni_tutor = dni_tutor
        self._nombre_tutor = nombre_tutor
        
    @property
    def id_cliente(self):
        return self._id_cliente
    
    @property
    def dni_tutor(self):
        return self._dni_tutor
    
    @property
    def nombre_tutor (self):
        return self._nombre_tutor