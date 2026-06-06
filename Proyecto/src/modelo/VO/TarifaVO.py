class TarifaVO:
    def __init__(self, id_tarifa=None, nombre=None, precio_mensual=None,
                 servicios_incluidos=None, fecha_inicio=None):
        self.id_tarifa = id_tarifa
        self.nombre = nombre
        self.precio_mensual = precio_mensual
        self.servicios_incluidos = servicios_incluidos
        self.fecha_inicio = fecha_inicio