class Cliente_tarifaVO:
    def __init__(self, id_cliente_tarifa=None, id_cliente=None, id_tarifa=None,
                 fecha_contratacion=None, estado="activa"):
        self.id_cliente_tarifa = id_cliente_tarifa
        self.id_cliente = id_cliente
        self.id_tarifa = id_tarifa
        self.fecha_contratacion = fecha_contratacion
        self.estado = estado

    def __str__(self):
        return (
            f"Cliente_tarifaVO("
            f"id_cliente_tarifa={self.id_cliente_tarifa}, "
            f"id_cliente={self.id_cliente}, "
            f"id_tarifa={self.id_tarifa}, "
            f"fecha_contratacion={self.fecha_contratacion}, "
            f"estado={self.estado})"
        )
    