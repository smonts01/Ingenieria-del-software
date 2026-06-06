from src.modelo.dao.DaoJDBCBase import DaoJDBCBase
 
 
class EstadisticasConsultasDaoJDBC(DaoJDBCBase):
 
    SQL_CLIENTES_ACTIVOS = "SELECT COUNT(*) FROM clientes"
 
    SQL_RESERVAS = "SELECT COUNT(*) FROM inscripcion WHERE estado = 'inscrito'"
 
    SQL_ASISTENCIAS = "SELECT COUNT(*) FROM asistencia WHERE presente = 'si'"
 
    SQL_CLASES_ACTIVAS = "SELECT COUNT(*) FROM clase"
 
    SQL_ENTRENADORES = "SELECT COUNT(*) FROM entrenador"
 
    SQL_SALAS = "SELECT COUNT(DISTINCT id_sala) FROM clase"
 
    SQL_OCUPACION_GLOBAL = """
        SELECT COALESCE(ROUND(AVG(pct), 1), 0)
        FROM (
            SELECT 
                (COUNT(i.id_inscripcion) * 100.0 / NULLIF(c.aforo_maximo, 0)) AS pct
            FROM clase c
            LEFT JOIN inscripcion i
                ON c.id_clase = i.id_clase
            AND i.estado = 'inscrito'
            GROUP BY 
                c.id_clase,
                c.aforo_maximo
        ) AS ocupaciones
    """
 
    SQL_RANKING_USUARIOS_ACTIVOS = """
        SELECT u.nombre,
               COUNT(a.id_asistencia) AS asistencias,
               COALESCE(MAX(c.nombre_actividad), '-') AS ultima_clase,
               'Activo' AS estado
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
 
    SQL_OCUPACION_POR_CLASE = """
        SELECT c.nombre_actividad,
            COALESCE(ROUND(
                (COUNT(i.id_inscripcion) * 100.0 / NULLIF(c.aforo_maximo, 0))
            ), 0) AS ocupacion
        FROM clase c
        LEFT JOIN inscripcion i
            ON c.id_clase = i.id_clase
        AND i.estado = 'inscrito'
        GROUP BY c.id_clase, c.nombre_actividad, c.aforo_maximo
        ORDER BY ocupacion DESC
        LIMIT 4
    """
 
    def estadisticas_admin(self):
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
 
    def ranking_usuarios_activos_estadisticas(self):
        return self.consultar(self.SQL_RANKING_USUARIOS_ACTIVOS)
 
    def ocupacion_por_clase_estadisticas(self):
        return self.consultar(self.SQL_OCUPACION_POR_CLASE)
 