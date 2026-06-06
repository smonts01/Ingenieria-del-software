from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.ContableVO import ContableVO


class ContableDaoJDBC(Conexion):

    SQL_SELECT = """
        SELECT id_contable, id_administrador_registra
        FROM contable
    """

    SQL_SELECT_BY_ID = """
        SELECT id_contable, id_administrador_registra
        FROM contable
        WHERE id_contable = ?
    """

    SQL_INSERT = """
        INSERT INTO contable
            (id_contable, id_administrador_registra)
        VALUES
            (?, ?)
    """

    SQL_UPDATE = """
        UPDATE contable
        SET id_administrador_registra = ?
        WHERE id_contable = ?
    """

    SQL_DELETE = """
        DELETE FROM contable
        WHERE id_contable = ?
    """

    def _rowToVO(self, row) -> ContableVO:
        id_contable, id_administrador_registra = row
        return ContableVO(id_contable, id_administrador_registra)

    def select(self) -> list[ContableVO]:
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

    def selectById(self, id_contable: int):
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
        cursor = self.getCursor()
        rows = 0

        try:
            cursor.execute(
                self.SQL_INSERT,
                (
                    vo.id_contable,
                    vo.id_administrador_registra
                )
            )
            rows = cursor.rowcount

        except Exception as e:
            print("Error al insertar contable:", e)

        finally:
            cursor.close()
            self.closeConnection()

        return rows

    def update(self, vo: ContableVO) -> int:
        cursor = self.getCursor()
        rows = 0

        try:
            cursor.execute(
                self.SQL_UPDATE,
                (
                    vo.id_administrador_registra,
                    vo.id_contable
                )
            )
            rows = cursor.rowcount

        except Exception as e:
            print("Error al actualizar contable:", e)

        finally:
            cursor.close()
            self.closeConnection()

        return rows

    def delete(self, id_contable: int) -> int:
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