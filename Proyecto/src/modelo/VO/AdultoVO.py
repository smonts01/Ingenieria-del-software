class AdultoVO:
    def __init__(self, id_cliente):
        self._id_cliente = id_cliente
        
    @property
    def id_cliente(self):
        return self._id_cliente