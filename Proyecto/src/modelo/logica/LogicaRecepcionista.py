class LogicaRecepcionista:
    """Reglas de negocio propias de recepción."""

    def __init__(self, servicio):
        self.servicio = servicio

    def registrar_acceso_cliente_control(self, id_usuario, tipo_acceso):
        tipo_acceso = tipo_acceso.lower().strip()
        if tipo_acceso not in ("entrada", "salida"):
            raise ValueError("Tipo de acceso no válido")

        ultimo = self.servicio.ultimo_acceso_cliente(id_usuario)
        if tipo_acceso == "salida" and ultimo != "entrada":
            raise ValueError("No se puede registrar una salida sin una entrada previa")
        if tipo_acceso == "entrada" and ultimo == "entrada":
            raise ValueError("Este cliente ya tiene una entrada registrada sin salida")

        return self.servicio.registrar_acceso(id_usuario, tipo_acceso)

    def buscar_cliente_acceso_por_dni_o_id(self, texto):
        if not str(texto).strip():
            return None
        return self.servicio.buscar_cliente_acceso_por_dni_o_id(texto)
