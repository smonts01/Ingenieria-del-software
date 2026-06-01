from src.modelo.dao.DaoJDBCBase import DaoJDBCBase


class EstadisticasConsultasDaoJDBC(DaoJDBCBase):

    def estadisticas_admin(self):
        clientes_activos = self.consultar("""SELECT COUNT(*) FROM clientes""")
        reservas = self.consultar("""SELECT COUNT(*) FROM inscripcion WHERE estado = 'inscrito'""")
        asistencias = self.consultar("""SELECT COUNT(*) FROM asistencia WHERE presente = 'si'""")
        clases_activas = self.consultar("""SELECT COUNT(*) FROM clase""")
        entrenadores = self.consultar("""SELECT COUNT(*) FROM entrenador""")
        salas = self.consultar("""SELECT COUNT(DISTINCT id_sala) FROM clase""")
        ocupacion = self.consultar("""
            SELECT COALESCE(ROUND(
                (COUNT(i.id_inscripcion) / NULLIF(SUM(c.aforo_maximo), 0)) * 100
            ), 0)
            FROM clase c
            LEFT JOIN inscripcion i
                ON c.id_clase = i.id_clase
            AND i.estado = 'inscrito'
        """)
        return {
            "clientes_activos": clientes_activos[0][0] if clientes_activos else 0,
            "reservas": reservas[0][0] if reservas else 0,
            "asistencias": asistencias[0][0] if asistencias else 0,
            "clases_activas": clases_activas[0][0] if clases_activas else 0,
            "entrenadores": entrenadores[0][0] if entrenadores else 0,
            "salas": salas[0][0] if salas else 0,
            "ocupacion": ocupacion[0][0] if ocupacion else 0
        }

    def ranking_usuarios_activos_estadisticas(self):
        return self.consultar("""
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
        """)

    def ocupacion_por_clase_estadisticas(self):
        return self.consultar("""
            SELECT c.nombre_actividad,
                   COALESCE(ROUND(
                       (COUNT(i.id_inscripcion) / NULLIF(c.aforo_maximo, 0)) * 100
                   ), 0) AS ocupacion
            FROM clase c
            LEFT JOIN inscripcion i
                ON c.id_clase = i.id_clase
            AND i.estado = 'inscrito'
            GROUP BY c.id_clase, c.nombre_actividad, c.aforo_maximo
            ORDER BY ocupacion DESC
            LIMIT 4
        """)
