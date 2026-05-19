from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.AsistenciaVO import AsistenciaVO

class AsistenciaDaoJDBC(AsistenciaVO, Conexion):
    SQL_SELECT           = "SELECT id_asistencia, id_cliente, id_clase, fecha, presente FROM asistencia"
    SQL_SELECT_BY_CLIENTE = "SELECT id_asistencia, id_cliente, id_clase, fecha, presente FROM asistencia WHERE id_cliente = ?"
    SQL_SELECT_BY_CLASE  = "SELECT id_asistencia, id_cliente, id_clase, fecha, presente FROM asistencia WHERE id_clase = ?"
    SQL_INSERT           = "INSERT INTO asistencia (id_cliente, id_clase, fecha, presente) VALUES (?, ?, ?, ?)"
    SQL_UPDATE           = "UPDATE asistencia SET presente=? WHERE id_asistencia=?"
    SQL_DELETE           = "DELETE FROM asistencia WHERE id_asistencia = ?"

    def _rowToVO(self, row) -> AsistenciaVO:
        id_asistencia, id_cliente, id_clase, fecha, presente = row
        return AsistenciaVO(id_asistencia, id_cliente, id_clase, fecha, presente)

    def select(self) -> list[AsistenciaVO]:
        cursor = self.getCursor()
        asistencias = []
        try:
            cursor.execute(self.SQL_SELECT)
            rows = cursor.fetchall()
            for row in rows:
                asistencias.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar asistencias:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return asistencias

    def selectByCliente(self, id_cliente: int) -> list[AsistenciaVO]:
        cursor = self.getCursor()
        asistencias = []
        try:
            cursor.execute(self.SQL_SELECT_BY_CLIENTE, (id_cliente,))
            rows = cursor.fetchall()
            for row in rows:
                asistencias.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar asistencias por cliente:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return asistencias

    def selectByClase(self, id_clase: int) -> list[AsistenciaVO]:
        cursor = self.getCursor()
        asistencias = []
        try:
            cursor.execute(self.SQL_SELECT_BY_CLASE, (id_clase,))
            rows = cursor.fetchall()
            for row in rows:
                asistencias.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar asistencias por clase:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return asistencias

    def insert(self, asistencia: AsistenciaVO) -> int:
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (
                asistencia.id_cliente, asistencia.id_clase,
                asistencia.fecha, asistencia.presente
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar asistencia:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return rows

    def update(self, asistencia: AsistenciaVO) -> int:
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (asistencia.presente, asistencia.id_asistencia))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar asistencia:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_asistencia: int) -> int:
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_asistencia,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar asistencia:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return rows