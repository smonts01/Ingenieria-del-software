from src.modelo.dao.EstadisticasConsultasDaoJDBC import EstadisticasConsultasDaoJDBC

class LogicaEstadisticas:
    """Cálculos y consultas agregadas de estadísticas."""

    def __init__(self):
        self._estadisticas_consultas_dao = EstadisticasConsultasDaoJDBC()

    def estadisticas_admin(self):
        return self._estadisticas_consultas_dao.estadisticas_admin()

    def ranking_usuarios_activos_estadisticas(self):
        return self._estadisticas_consultas_dao.ranking_usuarios_activos_estadisticas()

    def ocupacion_por_clase_estadisticas(self):
        return self._estadisticas_consultas_dao.ocupacion_por_clase_estadisticas()