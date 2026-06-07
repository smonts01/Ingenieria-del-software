from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.MenorVO import MenorVO


class MenorDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_cliente, dni_tutor, nombre_tutor FROM menor"
    SQL_SELECT_BY_ID = "SELECT id_cliente, dni_tutor, nombre_tutor FROM menor WHERE id_cliente = ?"
    SQL_INSERT = "INSERT INTO menor (id_cliente, dni_tutor, nombre_tutor) VALUES (?, ?, ?)"
    SQL_UPDATE = "UPDATE menor SET dni_tutor=?, nombre_tutor=? WHERE id_cliente=?"

    def __init__(self):
        self._conexion = Conexion()  

    def _rowToVO(self, row) -> MenorVO:
        id_cliente, dni_tutor, nombre_tutor = row
        return MenorVO(id_cliente, dni_tutor, nombre_tutor)

    def select(self) -> list[MenorVO]:
        """Recupera todos los menores."""
        cursor = self._conexion.getCursor()
        menores = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                menores.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar menores:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return menores

    def selectById(self, id_cliente: int) -> MenorVO:
        """Recupera un menor por su ID de cliente."""
        cursor = self._conexion.getCursor()
        menor = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_cliente,))
            row = cursor.fetchone()
            if row:
                menor = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar menor por ID:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return menor

    def insert(self, vo: MenorVO) -> int:
        """Inserta un nuevo menor. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (vo.id_cliente, vo.dni_tutor, vo.nombre_tutor))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar menor:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    def update(self, vo: MenorVO) -> int:
        """Actualiza los datos del tutor de un menor. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (vo.dni_tutor, vo.nombre_tutor, vo.id_cliente))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar menor:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows


