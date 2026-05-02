class ClientesVo:
    def __init__(self, id_cliente, estado_pagado, calorias_acumuladas):
        self._id_cliente = id_cliente
        self._estado_pagado = estado_pagado
        self._calorias_acumuladas = calorias_acumuladas
        
    @property
    def id_cliente(self):
        return self._id_cliente
    
    @property
    def estado_pagado(self):
        return self._estado_pagado
    
    @property
    def calorias_acumuladas(self):
        return self._calorias_acumuladas