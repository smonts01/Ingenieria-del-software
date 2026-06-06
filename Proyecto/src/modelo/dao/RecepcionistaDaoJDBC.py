from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.RecepcionistaVO import RecepcionistaVO


class RecepcionistaDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_recepcionista, turno, id_administrador_registra FROM recepcionista"
    SQL_SELECT_BY_ID = "SELECT id_recepcionista, turno, id_administrador_registra FROM recepcionista WHERE id_recepcionista = ?"
    SQL_INSERT = "INSERT INTO recepcionista (id_recepcionista, turno, id_administrador_registra) VALUES (?, ?, ?)"
    SQL_UPDATE = "UPDATE recepcionista SET turno=?, id_administrador_registra=? WHERE id_recepcionista=?"
    SQL_DELETE = "DELETE FROM recepcionista WHERE id_recepcionista = ?"

    def _rowToVO(self, row) -> RecepcionistaVO:
        id_recepcionista, id_administrador_registra = row
        return RecepcionistaVO(id_recepcionista, id_administrador_registra)

    def select(self) -> list[RecepcionistaVO]:
        """Recupera todos los recepcionistas."""
        cursor = self.getCursor()
        recepcionistas = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                recepcionistas.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar recepcionistas:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return recepcionistas

    def selectById(self, id_recepcionista: int) -> RecepcionistaVO:
        """Recupera un recepcionista por su ID."""
        cursor = self.getCursor()
        recepcionista = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_recepcionista,))
            row = cursor.fetchone()
            if row:
                recepcionista = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar recepcionista por ID:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return recepcionista

    def insert(self, vo: RecepcionistaVO) -> int:
        """Inserta un nuevo recepcionista. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (vo.id_recepcionista, vo.id_administrador_registra))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar recepcionista:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def update(self, vo: RecepcionistaVO) -> int:
        """Actualiza un recepcionista existente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (vo.id_administrador_registra, vo.id_recepcionista))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar recepcionista:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_recepcionista: int) -> int:
        """Elimina un recepcionista por su ID. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_recepcionista,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar recepcionista:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows
