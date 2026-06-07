from src.modelo.dao.DaoJDBCBase import DaoJDBCBase
from src.modelo.VO.OcupacionAdminVO import OcupacionAdminVO
from src.modelo.VO.RankingClienteVO import RankingClienteVO


class EstadisticasConsultasDaoJDBC(DaoJDBCBase):
    """DAO de consultas estadísticas para el panel del administrador.
    """


    # Total de clientes registrados en el sistema
    SQL_CLIENTES_ACTIVOS = "SELECT COUNT(*) FROM clientes"

    # Total de inscripciones activas en clases
    SQL_RESERVAS = "SELECT COUNT(*) FROM inscripcion WHERE estado = 'inscrito'"

    # Total de asistencias confirmadas 
    SQL_ASISTENCIAS = "SELECT COUNT(*) FROM asistencia WHERE presente = 'si'"

    # Total de clases dadas de alta en el sistema
    SQL_CLASES_ACTIVAS = "SELECT COUNT(*) FROM clase"

    # Total de entrenadores registrados
    SQL_ENTRENADORES = "SELECT COUNT(*) FROM entrenador"

    # Número de salas distintas con alguna clase asignada
    SQL_SALAS = "SELECT COUNT(DISTINCT id_sala) FROM clase"

    # Porcentaje de ocupación media de todas las clases
    SQL_OCUPACION_GLOBAL = """
        SELECT COALESCE(ROUND(AVG(pct), 1), 0)
        FROM (
            SELECT
                (COUNT(i.id_inscripcion) * 100.0 / NULLIF(c.aforo_maximo, 0)) AS pct
            FROM clase c
            LEFT JOIN inscripcion i
                ON c.id_clase = i.id_clase
               AND i.estado = 'inscrito'
            GROUP BY c.id_clase, c.aforo_maximo
        ) AS ocupaciones
    """

    # Ranking de los 8 clientes con más asistencias confirmadas,
    # incluyendo el nombre de la última clase a la que asistieron
    SQL_RANKING_USUARIOS_ACTIVOS = """
        SELECT u.nombre,
               COUNT(a.id_asistencia)          AS asistencias,
               COALESCE(MAX(c.nombre_actividad), '-') AS ultima_clase,
               'Activo'                         AS estado
        FROM usuarios u
        JOIN clientes cli ON u.id_usuario = cli.id_cliente
        LEFT JOIN asistencia a
            ON cli.id_cliente = a.id_cliente
           AND a.presente = 'si'
        LEFT JOIN clase c
            ON a.id_clase = c.id_clase
        GROUP BY u.id_usuario, u.nombre
        ORDER BY asistencias DESC, u.nombre ASC
        LIMIT 8
    """

    # Porcentaje de ocupación de las 4 clases más ocupadas
    SQL_OCUPACION_POR_CLASE = """
        SELECT c.nombre_actividad,
               COALESCE(ROUND(
                   COUNT(i.id_inscripcion) * 100.0 / NULLIF(c.aforo_maximo, 0)
               ), 0) AS ocupacion
        FROM clase c
        LEFT JOIN inscripcion i
            ON c.id_clase = i.id_clase
           AND i.estado = 'inscrito'
        GROUP BY c.id_clase, c.nombre_actividad, c.aforo_maximo
        ORDER BY ocupacion DESC
        LIMIT 4
    """

    # Consulta

    def estadisticas_admin(self) -> dict:
        """Devuelve un diccionario con los contadores del panel de estadísticas
        del administrador: clientes, reservas, asistencias, clases, entrenadores,
        salas y ocupación media global."""
        clientes_activos = self.consultar(self.SQL_CLIENTES_ACTIVOS)
        reservas         = self.consultar(self.SQL_RESERVAS)
        asistencias      = self.consultar(self.SQL_ASISTENCIAS)
        clases_activas   = self.consultar(self.SQL_CLASES_ACTIVAS)
        entrenadores     = self.consultar(self.SQL_ENTRENADORES)
        salas            = self.consultar(self.SQL_SALAS)
        ocupacion        = self.consultar(self.SQL_OCUPACION_GLOBAL)
        return {
            "clientes_activos": clientes_activos[0][0] if clientes_activos else 0,
            "reservas":         reservas[0][0]         if reservas         else 0,
            "asistencias":      asistencias[0][0]      if asistencias      else 0,
            "clases_activas":   clases_activas[0][0]   if clases_activas   else 0,
            "entrenadores":     entrenadores[0][0]      if entrenadores     else 0,
            "salas":            salas[0][0]             if salas            else 0,
            "ocupacion":        ocupacion[0][0]         if ocupacion        else 0,
        }

    def ranking_usuarios_activos_estadisticas(self) -> list:
        """Devuelve los 8 clientes más activos como lista de RankingClienteVO,
        ordenados de mayor a menor número de asistencias."""
        filas = self.consultar(self.SQL_RANKING_USUARIOS_ACTIVOS)
        return [RankingClienteVO(f[0], f[1], f[2], f[3]) for f in filas]

    def ocupacion_por_clase_estadisticas(self) -> list:
        """Devuelve las 4 clases con mayor ocupación como lista de OcupacionAdminVO,
        con el nombre de la clase y su porcentaje de ocupación."""
        filas = self.consultar(self.SQL_OCUPACION_POR_CLASE)
        return [OcupacionAdminVO(f[0], f[1]) for f in filas]