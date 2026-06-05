from src.modelo.dao.DaoJDBCBase import DaoJDBCBase
from src.modelo.VO.RegistroAccesoResumenVO import RegistroAccesoResumenVO


class RegistroAccesoConsultasDaoJDBC(DaoJDBCBase):

    SQL_RECEPCION_ENTRADAS = """
        SELECT COUNT(*)
        FROM registro_acceso
        WHERE tipo_acceso = 'entrada'
        AND DATE(fecha_hora_registro) = CURDATE()
    """

    SQL_ULTIMOS_REGISTROS = """
        SELECT u.nombre,
               u.dni,
               r.tipo_acceso,
               r.fecha_hora_registro
        FROM registro_acceso r
        JOIN usuarios u ON r.id_usuario = u.id_usuario
        ORDER BY r.fecha_hora_registro DESC
        LIMIT 8
    """

    SQL_ULTIMO_ACCESO_CLIENTE = """
        SELECT tipo_acceso
        FROM registro_acceso
        WHERE id_usuario = ?
        ORDER BY fecha_hora_registro DESC
        LIMIT 1
    """

    SQL_ACCESOS_CONTROL = """
        SELECT u.nombre,
               u.dni,
               r.tipo_acceso,
               r.fecha_hora_registro
        FROM registro_acceso r
        INNER JOIN usuarios u ON r.id_usuario = u.id_usuario
        ORDER BY r.fecha_hora_registro DESC
        LIMIT 20
    """

    def _rowToVO(self, row) -> RegistroAccesoResumenVO:
        return RegistroAccesoResumenVO(row[0], row[1], row[2], row[3])

    def recepcion_entradas_hoy(self):
        datos = self.consultar(self.SQL_RECEPCION_ENTRADAS)
        return datos[0][0] if datos else 0

    def recepcion_ultimos_registros_acceso(self):
        filas = self.consultar(self.SQL_ULTIMOS_REGISTROS)
        return [self._rowToVO(f) for f in filas]

    def ultimo_acceso_cliente(self, id_usuario):
        datos = self.consultar(self.SQL_ULTIMO_ACCESO_CLIENTE, (id_usuario,))
        return datos[0][0] if datos else None

    def listar_ultimos_accesos_control(self):
        filas = self.consultar(self.SQL_ACCESOS_CONTROL)
        return [self._rowToVO(f) for f in filas]