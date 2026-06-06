from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.SalaVO import SalaVO


class SalaDaoJDBC(Conexion):

    SQL_SELECT = """
        SELECT id_sala, nombre, aforo_maximo
        FROM sala
    """

    SQL_SELECT_BY_ID = """
        SELECT id_sala, nombre, aforo_maximo
        FROM sala
        WHERE id_sala = ?
    """

    SQL_INSERT = """
        INSERT INTO sala
            (nombre, aforo_maximo)
        VALUES
            (?, ?)
    """

    SQL_UPDATE = """
        UPDATE sala
        SET nombre = ?,
            aforo_maximo = ?
        WHERE id_sala = ?
    """

    SQL_DELETE = """
        DELETE FROM sala
        WHERE id_sala = ?
    """

    def _rowToVO(self, row) -> SalaVO:
        id_sala, nombre, aforo_maximo = row

        return SalaVO(
            id_sala=id_sala,
            nombre=nombre,
            aforo_maximo=aforo_maximo
        )

    def select(self) -> list[SalaVO]:
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
        cursor = self.getCursor()
        rows = 0

        try:
            cursor.execute(
                self.SQL_INSERT,
                (
                    vo.nombre,
                    vo.aforo_maximo
                )
            )

            rows = cursor.rowcount

        except Exception as e:
            print("Error al insertar sala:", e)

        finally:
            cursor.close()
            self.closeConnection()

        return rows

    def update(self, vo: SalaVO) -> int:
        cursor = self.getCursor()
        rows = 0

        try:
            cursor.execute(
                self.SQL_UPDATE,
                (
                    vo.nombre,
                    vo.aforo_maximo,
                    vo.id_sala
                )
            )

            rows = cursor.rowcount

        except Exception as e:
            print("Error al actualizar sala:", e)

        finally:
            cursor.close()
            self.closeConnection()

        return rows

    def delete(self, id_sala: int) -> int:
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