from src.modelo.dao.DaoJDBCBase import DaoJDBCBase
from src.modelo.VO.ContableVO import ContableVO


class ContableDaoJDBC(DaoJDBCBase):

    SQL_SELECT = "SELECT id_contable, titulacion, id_administrador_registra FROM contable"
    SQL_SELECT_BY_ID = "SELECT id_contable, titulacion, id_administrador_registra FROM contable WHERE id_contable = ?"
    SQL_INSERT = "INSERT INTO contable (titulacion, id_administrador_registra) VALUES (?, ?)"
    SQL_UPDATE = "UPDATE contable SET titulacion=?, id_administrador_registra=? WHERE id_contable=?"
    SQL_DELETE = "DELETE FROM contable WHERE id_contable = ?"

    def _rowToVO(self, row) -> ContableVO:
        id_contable, titulacion, id_administrador_registra = row
        return ContableVO(id_contable, titulacion, id_administrador_registra)

    def select(self) -> list[ContableVO]:
        """Recupera todos los contables."""
        cursor = self.getCursor()
        contables = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                contables.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar contables:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return contables

    def selectById(self, id_contable: int) -> ContableVO:
        """Recupera un contable por su ID."""
        cursor = self.getCursor()
        contable = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_contable,))
            row = cursor.fetchone()
            if row:
                contable = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar contable por ID:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return contable

    def insert(self, vo: ContableVO) -> int:
        """Inserta un nuevo contable. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (vo.titulacion, vo.id_administrador_registra))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar contable:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def update(self, vo: ContableVO) -> int:
        """Actualiza un contable existente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (vo.titulacion, vo.id_administrador_registra, vo.id_contable))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar contable:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_contable: int) -> int:
        """Elimina un contable por su ID. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_contable,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar contable:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows
