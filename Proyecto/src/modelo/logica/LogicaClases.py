class LogicaClases:
    """Reglas de negocio de clases, aforo e inscripciones."""

    def __init__(self, servicio):
        self.servicio = servicio

    def registrar_clase(self, id_entrenador, id_sala, nombre_actividad,
                        calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                        duracion, aforo_maximo, nivel_intensidad):
        if not nombre_actividad:
            raise ValueError("El nombre de la clase es obligatorio")
        if int(aforo_maximo) <= 0:
            raise ValueError("El aforo debe ser mayor que cero")
        return self.servicio.registrar_clase(
            id_entrenador, id_sala, nombre_actividad, calorias_estimadas,
            dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad
        )

    def guardar_cambios_clase_tabla(self, id_clase, nombre, dia, hora_ini, hora_fin, aforo, nivel):
        if int(aforo) <= 0:
            raise ValueError("El aforo debe ser mayor que cero")
        return self.servicio.guardar_cambios_clase_tabla(id_clase, nombre, dia, hora_ini, hora_fin, aforo, nivel)
