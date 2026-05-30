from src.modelo.dao.ServicioProyectoDaoJDBC import ServicioProyectoDaoJDBC


class Logica:
    """
    Capa de lógica de negocio.

    No contiene SQL ni accede directamente a la base de datos. Todas las
    operaciones de persistencia se delegan en ServicioProyectoDaoJDBC y en los
    DAO específicos, cumpliendo el patrón DAO/VO y separando el Modelo de la BD.
    """

    def __init__(self):
        self._dao = ServicioProyectoDaoJDBC()

    def __getattr__(self, nombre):
        """Delegación controlada para mantener la API usada por los controladores."""
        return getattr(self._dao, nombre)

    def estadisticas_admin(self):
        return self._dao.estadisticas_admin()


    def ranking_usuarios_activos_estadisticas(self):
        return self._dao.ranking_usuarios_activos_estadisticas()


    def ocupacion_por_clase_estadisticas(self):
        return self._dao.ocupacion_por_clase_estadisticas()
