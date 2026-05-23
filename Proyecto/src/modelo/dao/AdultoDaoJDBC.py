from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.AdultoVO import AdultoVO


class AdultoDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_cliente FROM adulto"
    SQL_SELECT_BY_ID = "SELECT id_cliente FROM adulto WHERE id_cliente = ?"
    SQL_INSERT = "INSERT INTO adulto (id_cliente) VALUES (?)"
    SQL_DELETE = "DELETE FROM adulto WHERE id_cliente = ?"

    def _rowToVO(self, row) -> AdultoVO:
        return AdultoVO(row[0])

    def select(self) -> list[AdultoVO]:
        """Recupera todos los adultos."""
        cursor = self.getCursor()
        adultos = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                adultos.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar adultos:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return adultos

    def selectById(self, id_cliente: int) -> AdultoVO:
        """Recupera un adulto por su ID de cliente."""
        cursor = self.getCursor()
        adulto = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_cliente,))
            row = cursor.fetchone()
            if row:
                adulto = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar adulto por ID:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return adulto

    def insert(self, vo: AdultoVO) -> int:
        """Inserta un nuevo adulto. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (vo.id_cliente,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar adulto:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_cliente: int) -> int:
        """Elimina un adulto por su ID de cliente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_cliente,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar adulto:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows
