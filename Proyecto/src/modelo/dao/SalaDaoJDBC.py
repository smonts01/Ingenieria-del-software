from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.SalaVO import SalaVO


class SalaDaoJDBC:

    SQL_SELECT = """
        SELECT id_sala, nombre, aforo_maximo
        FROM sala
    """

    SQL_SELECT_BY_ID = """
        SELECT id_sala, nombre, aforo_maximo
        FROM sala
        WHERE id_sala = ?
    """



    def __init__(self):
        self._conexion = Conexion()  

    def _rowToVO(self, row) -> SalaVO:
        id_sala, nombre, aforo_maximo = row

        return SalaVO(
            id_sala=id_sala,
            nombre=nombre,
            aforo_maximo=aforo_maximo
        )

    def select(self) -> list[SalaVO]:
        """Recupera todas las salas."""
        cursor = self._conexion.getCursor()
        salas = []

        try:
            cursor.execute(self.SQL_SELECT)

            for row in cursor.fetchall():
                salas.append(self._rowToVO(row))

        except Exception as e:
            print("Error al seleccionar salas:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()
        return salas

    def selectById(self, id_sala: int) -> SalaVO:
        """Recupera una sala por su ID."""
        cursor = self._conexion.getCursor()
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
            self._conexion.closeConnection()
        return sala

    