from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.AsistenciaVO import AsistenciaVO


class AsistenciaDaoJDBC:

    SQL_SELECT = "SELECT id_asistencia, id_cliente, id_clase, fecha, presente FROM asistencia"
    SQL_SELECT_BY_ID = "SELECT id_asistencia, id_cliente, id_clase, fecha, presente FROM asistencia WHERE id_asistencia = ?"
    SQL_SELECT_BY_CLIENTE = "SELECT id_asistencia, id_cliente, id_clase, fecha, presente FROM asistencia WHERE id_cliente = ?"
    SQL_SELECT_BY_CLASE = "SELECT id_asistencia, id_cliente, id_clase, fecha, presente FROM asistencia WHERE id_clase = ?"
    SQL_INSERT = "INSERT INTO asistencia (id_cliente, id_clase, fecha, presente) VALUES (?, ?, ?, ?)"
    SQL_UPDATE = "UPDATE asistencia SET presente=? WHERE id_asistencia=?"

    def __init__(self):
        self._conexion = Conexion()  

    def _rowToVO(self, row) -> AsistenciaVO:
        id_asistencia, id_cliente, id_clase, fecha, presente = row
        return AsistenciaVO(id_asistencia, id_cliente, id_clase, fecha, presente)

    def select(self) -> list[AsistenciaVO]:
        """Recupera todas las asistencias."""
        cursor = self._conexion.getCursor()
        asistencias = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                asistencias.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar asistencias:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return asistencias

    def selectById(self, id_asistencia: int) -> AsistenciaVO:
        """Recupera una asistencia por su ID."""
        cursor = self._conexion.getCursor()
        asistencia = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_asistencia,))
            row = cursor.fetchone()
            if row:
                asistencia = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar asistencia por ID:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return asistencia

    def selectByCliente(self, id_cliente: int) -> list[AsistenciaVO]:
        """Recupera todas las asistencias de un cliente."""
        cursor = self._conexion.getCursor()
        asistencias = []
        try:
            cursor.execute(self.SQL_SELECT_BY_CLIENTE, (id_cliente,))
            for row in cursor.fetchall():
                asistencias.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar asistencias por cliente:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return asistencias

    def selectByClase(self, id_clase: int) -> list[AsistenciaVO]:
        """Recupera todas las asistencias de una clase."""
        cursor = self._conexion.getCursor()
        asistencias = []
        try:
            cursor.execute(self.SQL_SELECT_BY_CLASE, (id_clase,))
            for row in cursor.fetchall():
                asistencias.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar asistencias por clase:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return asistencias

    def insert(self, vo: AsistenciaVO) -> int:
        """Registra una nueva asistencia. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (
                vo.id_cliente, vo.id_clase, vo.fecha, vo.presente
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar asistencia:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    def update(self, vo: AsistenciaVO) -> int:
        """Actualiza el estado de presencia de una asistencia. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (vo.presente, vo.id_asistencia))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar asistencia:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows


