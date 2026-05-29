class ClaseVO:
    def __init__(self, id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad):
        self._id_clase = id_clase
        self._id_entrenador = id_entrenador
        self._id_sala = id_sala 
        self._nombre_actividad = nombre_actividad
        self._calorias_estimadas = calorias_estimadas
        self._dia_semana = dia_semana
        self._hora_inicio = hora_inicio
        self._hora_fin = hora_fin
        self._duracion = duracion
        self._aforo_maximo = aforo_maximo
        self._nivel_intensidad = nivel_intensidad
        
    @property
    def id_clase(self):
        return self._id_clase
    
    @property
    def id_entrenador(self):
        return self._id_entrenador
    
    @property
    def id_sala(self):
        return self._id_sala
    
    @property
    def nombre_actividad(self):
        return self._nombre_actividad
    
    @property
    def calorias_estimadas(self):
        return self._calorias_estimadas
    
    @property
    def dia_semana(self):
        return self._dia_semana
    
    @property
    def hora_inicio(self):
        return self._hora_inicio
    
    @property
    def hora_fin(self):
        return self._hora_fin
    
    @property
    def duracion(self):
        return self._duracion
    
    @property
    def aforo_maximo(self):
        return self._aforo_maximo
    
    @property
    def nivel_intensidad(self):
        return self._nivel_intensidad