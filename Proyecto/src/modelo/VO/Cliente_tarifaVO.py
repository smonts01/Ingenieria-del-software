class Cliente_tarifaVO:
    def __init__(self, id_cliente_tarifa, id_cliente, id_tarifa, fecha_contratacion, estado):
        self._id_cliente_tarifa = id_cliente_tarifa
        self._id_cliente = id_cliente
        self._id_tarifa = id_tarifa
        self._fecha_contratacion = fecha_contratacion
        self._estado = estado
        
    @property
    def id_cliente_tarifa(self):
        return self._id_cliente_tarifa
    
    @property
    def id_cliente(self):
        return self._id_cliente
    
    @property
    def id_tarifa(self):
        return self._id_tarifa
    
    @property
    def fecha_contratacion(self):
        return self._fecha_contratacion
    
    @property
    def estado(self):
        return self._estado