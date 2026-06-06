from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.InscripcionVO import InscripcionVO


class InscripcionDaoJDBC:

    SQL_SELECT = "SELECT id_inscripcion, id_cliente, id_clase, fecha_inscripcion, estado FROM inscripcion"
    SQL_SELECT_BY_ID = "SELECT id_inscripcion, id_cliente, id_clase, fecha_inscripcion, estado FROM inscripcion WHERE id_inscripcion = ?"
    SQL_SELECT_BY_CLIENTE = "SELECT id_inscripcion, id_cliente, id_clase, fecha_inscripcion, estado FROM inscripcion WHERE id_cliente = ?"
    SQL_SELECT_BY_CLASE = "SELECT id_inscripcion, id_cliente, id_clase, fecha_inscripcion, estado FROM inscripcion WHERE id_clase = ?"
    SQL_INSERT = "INSERT INTO inscripcion (id_cliente, id_clase, estado) VALUES (?, ?, ?)"
    SQL_UPDATE_ESTADO = "UPDATE inscripcion SET estado=? WHERE id_inscripcion=?"
    SQL_DELETE = "DELETE FROM inscripcion WHERE id_inscripcion = ?"


    def __init__(self):
        self._conexion = Conexion()  

    def _rowToVO(self, row) -> InscripcionVO:
        id_inscripcion, id_cliente, id_clase, fecha_inscripcion, estado = row
        return InscripcionVO(id_inscripcion, id_cliente, id_clase, fecha_inscripcion, estado)

    def select(self) -> list[InscripcionVO]:
        """Recupera todas las inscripciones."""
        cursor = self._conexion.getCursor()
        inscripciones = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                inscripciones.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar inscripciones:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return inscripciones

    def selectById(self, id_inscripcion: int) -> InscripcionVO:
        """Recupera una inscripción por su ID."""
        cursor = self._conexion.getCursor()
        inscripcion = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_inscripcion,))
            row = cursor.fetchone()
            if row:
                inscripcion = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar inscripción por ID:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return inscripcion

    def selectByCliente(self, id_cliente: int) -> list[InscripcionVO]:
        """Recupera todas las inscripciones de un cliente."""
        cursor = self._conexion.getCursor()
        inscripciones = []
        try:
            cursor.execute(self.SQL_SELECT_BY_CLIENTE, (id_cliente,))
            for row in cursor.fetchall():
                inscripciones.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar inscripciones por cliente:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return inscripciones

    def selectByClase(self, id_clase: int) -> list[InscripcionVO]:
        """Recupera todas las inscripciones de una clase."""
        cursor = self._conexion.getCursor()
        inscripciones = []
        try:
            cursor.execute(self.SQL_SELECT_BY_CLASE, (id_clase,))
            for row in cursor.fetchall():
                inscripciones.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar inscripciones por clase:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return inscripciones

    def insert(self, vo: InscripcionVO) -> int:
        """Inserta una nueva inscripción. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (vo.id_cliente, vo.id_clase, vo.estado))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar inscripción:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    def updateEstado(self, id_inscripcion: int, estado: str) -> int:
        """Actualiza el estado de una inscripción ('inscrito'/'cancelado'). Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE_ESTADO, (estado, id_inscripcion))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar estado de inscripción:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    def delete(self, id_inscripcion: int) -> int:
        """Elimina una inscripción por su ID. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_inscripcion,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar inscripción:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows
