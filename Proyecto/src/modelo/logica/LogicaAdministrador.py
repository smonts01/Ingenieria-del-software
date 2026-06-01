class LogicaAdministrador:
    """
    Lógica de negocio del perfil Administrador.

    Esta clase no accede a la interfaz ni ejecuta SQL. Agrupa las operaciones
    del administrador y delega la persistencia al servicio/DAO correspondiente.
    """

    def __init__(self, servicio):
        self.servicio = servicio

    def registrar_clase(self, id_entrenador, id_sala, nombre_actividad,
                        calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                        duracion, aforo_maximo, nivel_intensidad):
        if not str(nombre_actividad).strip():
            raise ValueError("El nombre de la clase es obligatorio")
        if int(aforo_maximo) <= 0:
            raise ValueError("El aforo debe ser mayor que cero")
        return self.servicio.registrar_clase(
            id_entrenador, id_sala, nombre_actividad, calorias_estimadas,
            dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo,
            nivel_intensidad
        )

    def guardar_cambios_clase_tabla(self, id_clase, nombre, dia, hora_ini, hora_fin, aforo, nivel):
        if not str(nombre).strip():
            raise ValueError("El nombre de la clase es obligatorio")
        if int(aforo) <= 0:
            raise ValueError("El aforo debe ser mayor que cero")
        return self.servicio.guardar_cambios_clase_tabla(id_clase, nombre, dia, hora_ini, hora_fin, aforo, nivel)

    def validar_estado_pago(self, estado):
        estado = str(estado).lower().strip()
        if estado not in ("abonado", "pendiente"):
            raise ValueError("El estado de pago debe ser abonado o pendiente")
        return estado
