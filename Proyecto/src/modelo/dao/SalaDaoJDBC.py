from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.SalaVO import SalaVO


class SalaDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_sala, nombre, aforo_maximo, tipo_zona FROM sala"
    SQL_SELECT_BY_ID = "SELECT id_sala, nombre, aforo_maximo, tipo_zona FROM sala WHERE id_sala = ?"
    SQL_INSERT = "INSERT INTO sala (nombre, aforo_maximo, tipo_zona) VALUES (?, ?, ?)"
    SQL_UPDATE = "UPDATE sala SET nombre=?, aforo_maximo=?, tipo_zona=? WHERE id_sala=?"
    SQL_DELETE = "DELETE FROM sala WHERE id_sala = ?"

    def _rowToVO(self, row) -> SalaVO:
        id_sala, nombre, aforo_maximo, tipo_zona = row
        return SalaVO(id_sala, nombre, aforo_maximo, tipo_zona)

    def select(self) -> list[SalaVO]:
        """Recupera todas las salas."""
        cursor = self.getCursor()
        salas = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                salas.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar salas:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return salas

    def selectById(self, id_sala: int) -> SalaVO:
        """Recupera una sala por su ID."""
        cursor = self.getCursor()
        sala = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_sala,))
            row = cursor.fetchone()
            if row:
                sala = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar sala por ID:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return sala

    def insert(self, vo: SalaVO) -> int:
        """Inserta una nueva sala. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (vo.nombre, vo.aforo_maximo, vo.tipo_zona))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar sala:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def update(self, vo: SalaVO) -> int:
        """Actualiza una sala existente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (vo.nombre, vo.aforo_maximo, vo.tipo_zona, vo.id_sala))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar sala:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_sala: int) -> int:
        """Elimina una sala por su ID. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_sala,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar sala:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows
