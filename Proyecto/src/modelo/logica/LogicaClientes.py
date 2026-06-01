class LogicaClientes:
    """Reglas de negocio de clientes: perfil, altas, edición e inscripciones."""

    def __init__(self, servicio):
        self.servicio = servicio

    def crear_cliente_desde_recepcion(self, dni, nombre, telefono, email, username,
                                      password, direccion, fecha_nacimiento,
                                      es_menor=False, dni_tutor="", nombre_tutor=""):
        obligatorios = [dni, nombre, telefono, email, username, password, direccion, fecha_nacimiento]
        if not all(str(x).strip() for x in obligatorios):
            raise ValueError("Faltan datos obligatorios del cliente")
        if es_menor and (not dni_tutor or not nombre_tutor):
            raise ValueError("Un cliente menor debe tener DNI y nombre del tutor")
        return self.servicio.insertar_cliente_recepcion(
            dni.strip(), nombre.strip(), telefono.strip(), email.strip(), username.strip(),
            password, direccion.strip(), fecha_nacimiento, es_menor,
            dni_tutor.strip(), nombre_tutor.strip()
        )

    def recepcion_guardar_cambios_cliente(self, id_cliente, dni, nombre, telefono,
                                          email, direccion, fecha_nacimiento,
                                          estado_pagado):
        if not dni or not nombre:
            raise ValueError("DNI y nombre son obligatorios")
        estado = estado_pagado.lower().strip()
        if estado not in ("abonado", "pendiente"):
            raise ValueError("El estado de pago debe ser abonado o pendiente")
        return self.servicio.recepcion_guardar_cambios_cliente(
            id_cliente, dni.strip(), nombre.strip(), telefono.strip(), email.strip(),
            direccion.strip(), fecha_nacimiento, estado
        )

    def inscribirse_clase_por_nombre(self, id_cliente, nombre_actividad):
        if not nombre_actividad:
            raise ValueError("No se ha seleccionado ninguna clase")
        return self.servicio.inscribirse_clase_por_nombre(id_cliente, nombre_actividad)

    def inscribirse_clase(self, id_cliente, id_clase):
        return self.servicio.inscribirse_clase(id_cliente, id_clase)
