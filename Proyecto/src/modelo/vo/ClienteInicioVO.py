class ClienteInicioVO:
    """
    Value Object que agrupa toda la información necesaria para inicializar
    las pantallas del cliente.
    """

    def __init__(
        self,
        # Datos básicos del usuario
        id_cliente: int,
        nombre: str,
        email: str,
        telefono: str,
        direccion: str,
        fecha_nacimiento: str,          # str "DD/MM/YYYY" listo para mostrar
        fecha_registro: str,            # str "mes YYYY"  ej. "enero 2024"

        # Datos específicos de cliente 
        estado_pagado: str,             # 'abonado' | 'pendiente'
        calorias_acumuladas: int,       # total histórico acumulado en BD

        # Tarifa activa 
        nombre_tarifa: str,             # ej. "Cuota mensual"
        precio_tarifa: float,           # ej. 35.00

        # Último pago registrado 
        ultimo_pago_importe: float,     # ej. 35.00
        ultimo_pago_fecha: str,         # str "Mes YYYY"  ej. "Mayo 2026"
        ultimo_pago_estado: str,        # 'abonado' | 'pendiente'

        # Clases esta semana (página Inicio, card1) 
        clases_semana: int,             # nº de asistencias con presente='si'
                                        # en la semana en curso

        # Calorías esta semana (página Inicio, card3) 
        calorias_semana: int,           # suma de calorias_estimadas de clases
                                        # asistidas esta semana

        # Asistencias este mes (página Inicio, card4) 
        asistencias_mes: int,           # asistencias con presente='si' en el mes
        inscripciones_mes: int,         # total inscripciones activas del mes

        # Próximas clases inscritas (tabla Inicio) 
        # Lista de dicts con claves:
        #   'nombre_actividad', 'fecha', 'hora_inicio', 'nombre_sala'
        proximas_clases: list,

        # Estadísticas semanales (página Estadísticas) 
        entrenos_semana: int,           # asistencias con presente='si' esta semana
        tiempo_semana_min: int,         # suma de duracion (minutos) esta semana
        entrenos_semana_anterior: int,  # para calcular el delta "+N vs sem. ant."
        tiempo_semana_anterior_min: int,

        # Racha de días consecutivos entrenando
        racha_dias: int,

        # Distribución por tipo de clase (%)
        # Dict con claves libres según especialidades reales del gym,
        # los valores son enteros que suman 100.
        # Ejemplo: {'Fuerza': 40, 'Cardio': 30, 'Flexibilidad': 20, 'Otros': 10}
        distribucion_tipos: dict,
    ):
        # Usuario 
        self.id_cliente              = id_cliente
        self.nombre                  = nombre
        self.email                   = email
        self.telefono                = telefono
        self.direccion               = direccion
        self.fecha_nacimiento        = fecha_nacimiento
        self.fecha_registro          = fecha_registro

        # Cliente 
        self.estado_pagado           = estado_pagado
        self.calorias_acumuladas     = calorias_acumuladas

        # Tarifa y pagos 
        self.nombre_tarifa           = nombre_tarifa
        self.precio_tarifa           = precio_tarifa
        self.ultimo_pago_importe     = ultimo_pago_importe
        self.ultimo_pago_fecha       = ultimo_pago_fecha
        self.ultimo_pago_estado      = ultimo_pago_estado

        # Inicio 
        self.clases_semana           = clases_semana
        self.calorias_semana         = calorias_semana
        self.asistencias_mes         = asistencias_mes
        self.inscripciones_mes       = inscripciones_mes
        self.proximas_clases         = proximas_clases   # list[dict]

        # Estadísticas 
        self.entrenos_semana         = entrenos_semana
        self.tiempo_semana_min       = tiempo_semana_min
        self.entrenos_semana_anterior     = entrenos_semana_anterior
        self.tiempo_semana_anterior_min   = tiempo_semana_anterior_min
        self.racha_dias              = racha_dias
        self.distribucion_tipos      = distribucion_tipos  # dict[str, int]

    # Helpers de presentación

    def get_tiempo_semana_str(self) -> str:
        """Devuelve el tiempo semanal formateado como 'Xh Ym'."""
        h = self.tiempo_semana_min // 60
        m = self.tiempo_semana_min % 60
        return f"{h}h {m}m"

    def get_delta_entrenos_str(self) -> str:
        """Diferencia de entrenamientos respecto a la semana anterior."""
        delta = self.entrenos_semana - self.entrenos_semana_anterior
        signo = "+" if delta >= 0 else ""
        return f"{signo}{delta} vs semana anterior"

    def get_delta_tiempo_str(self) -> str:
        """Diferencia de tiempo respecto a la semana anterior."""
        delta_min = self.tiempo_semana_min - self.tiempo_semana_anterior_min
        signo = "+" if delta_min >= 0 else "-"
        delta_min = abs(delta_min)
        h = delta_min // 60
        m = delta_min % 60
        partes = []
        if h:
            partes.append(f"{h}h")
        if m:
            partes.append(f"{m}m")
        return f"{signo}{''.join(partes)} vs semana anterior"

    def get_asistencias_str(self) -> str:
        """Formato 'X/Y' para la card de asistencias."""
        return f"{self.asistencias_mes}/{self.inscripciones_mes}"

    def get_precio_str(self) -> str:
        """Precio del último pago formateado con símbolo €."""
        return f"{self.ultimo_pago_importe:.2f} €"

    def __repr__(self) -> str:
        return (
            f"ClienteInicioVO(id={self.id_cliente}, nombre='{self.nombre}', "
            f"estado_pagado='{self.estado_pagado}', "
            f"calorias_acumuladas={self.calorias_acumuladas})"
        )
