class SalaVO:
    def __init__(self, id_sala, nombre, aforo_maximo, tipo_zona):
        self._id_sala = id_sala
        self._nombre = nombre
        self._aforo_maximo = aforo_maximo
        self._tipo_zona = tipo_zona
        
    @property
    def id_sala(self):
        return self._id_sala
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def aforo_maximo(self):
        return self._aforo_maximo
    
    @property
    def tipo_zona(self):
        return self._tipo_zona