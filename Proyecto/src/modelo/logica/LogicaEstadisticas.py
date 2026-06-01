class LogicaEstadisticas:
    """Cálculos y consultas agregadas de estadísticas."""

    def __init__(self, servicio):
        self.servicio = servicio

    def estadisticas_admin(self):
        return self.servicio.estadisticas_admin()

    def ranking_usuarios_activos_estadisticas(self):
        return self.servicio.ranking_usuarios_activos_estadisticas()

    def ocupacion_por_clase_estadisticas(self):
        return self.servicio.ocupacion_por_clase_estadisticas()
