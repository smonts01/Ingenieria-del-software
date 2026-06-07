from src.modelo.dao.DaoJDBCBase import DaoJDBCBase
from src.modelo.VO.AsistenciaRegistroVO import AsistenciaRegistroVO
from src.modelo.VO.EstadisticaAsistenciaVO import EstadisticaAsistenciaVO
from src.modelo.VO.RankingClienteVO import RankingClienteVO


class AsistenciaConsultasDaoJDBC(DaoJDBCBase):

    SQL_CALCULAR_CALORIAS_CLIENTE = ("SELECT COALESCE(SUM(c.calorias_estimadas), 0) "
                                     "FROM asistencia a JOIN clase c ON a.id_clase = c.id_clase "
                                     "WHERE a.id_cliente = ? AND a.presente = 'si'")

    SQL_ESTADISTICAS_CLIENTE = ("SELECT c.nombre_actividad, COUNT(*) as asistencias, SUM(c.calorias_estimadas) as calorias "
                                "FROM asistencia a JOIN clase c ON a.id_clase = c.id_clase "
                                "WHERE a.id_cliente = ? AND a.presente = 'si' "
                                "GROUP BY c.nombre_actividad")

    SQL_RANKING_CLIENTES_ACTIVOS = ("SELECT u.nombre, COUNT(*) as asistencias "
                                    "FROM asistencia a JOIN usuarios u ON a.id_cliente = u.id_usuario "
                                    "WHERE a.presente = 'si' "
                                    "GROUP BY u.id_usuario, u.nombre "
                                    "ORDER BY asistencias DESC LIMIT 20")

    SQL_ASISTENCIA_CLASE = ("SELECT u.nombre, a.fecha, a.presente "
                            "FROM asistencia a "
                            "JOIN usuarios u ON a.id_cliente = u.id_usuario "
                            "WHERE a.id_clase = ? "
                            "ORDER BY a.fecha DESC, u.nombre")

    SQL_ASISTENCIA_CLASE_FECHA = ("SELECT id_cliente, presente "
                                  "FROM asistencia "
                                  "WHERE id_clase = ? "
                                  "AND fecha = ? "
                                  "ORDER BY id_asistencia")

    SQL_REGISTRAR_ASISTENCIA = ("DELETE FROM asistencia "
                                "WHERE id_cliente = ? "
                                "AND id_clase = ? "
                                "AND fecha = ?")

    SQL_EJECUTAR = ("INSERT INTO asistencia (id_cliente, id_clase, fecha, presente) "
                    "VALUES (?, ?, ?, ?)")

    def calcular_calorias_cliente(self, id_cliente: int):
        datos = self.consultar(self.SQL_CALCULAR_CALORIAS_CLIENTE, (id_cliente,))
        return int(datos[0][0]) if datos else 0

    def estadisticas_cliente(self, id_cliente: int):
        filas = self.consultar(self.SQL_ESTADISTICAS_CLIENTE, (id_cliente,))
        return [EstadisticaAsistenciaVO(f[0], f[1], f[2]) for f in filas]

    def ranking_clientes_activos(self):
        filas = self.consultar(self.SQL_RANKING_CLIENTES_ACTIVOS)
        return [RankingClienteVO(f[0], f[1]) for f in filas]

    def consultar_asistencia_clase(self, id_clase: int):
        filas = self.consultar(self.SQL_ASISTENCIA_CLASE, (id_clase,))
        return [AsistenciaRegistroVO(f[0], f[1]) for f in filas]

    def asistencia_clase_fecha(self, id_clase, fecha):
        filas = self.consultar(self.SQL_ASISTENCIA_CLASE_FECHA, (id_clase, fecha))
        return [AsistenciaRegistroVO(f[0], f[1]) for f in filas]

    def registrar_asistencia(self, id_cliente, id_clase, fecha, presente):
        self.ejecutar(self.SQL_REGISTRAR_ASISTENCIA, (id_cliente, id_clase, fecha))
        return self.ejecutar(self.SQL_EJECUTAR, (id_cliente, id_clase, fecha, presente))