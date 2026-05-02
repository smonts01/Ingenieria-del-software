class TarifaVO:
    def __init__(self, id_tarifa, nombre, precio_mensual, servicios_incluidos, fecha_inicio, fecha_fin):
        self._id_tarifa = id_tarifa
        self._nombre = nombre
        self._precio_mensual = precio_mensual
        self._servicios_incluidos = servicios_incluidos
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        
    @property
    def id_tarifa(self):
        return self._id_tarifa
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def precio_mensual(self):
        return self._precio_mensual
    
    @property
    def servicios_incluidos(self):
        return self._servicios_incluidos
    
    @property
    def fecha_inicio(self):
        return self._fecha_inicio
    
    @property
    def fecha_fin(self):
        return self._fecha_fin