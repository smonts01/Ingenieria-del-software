from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.AdminitradorVO import AdminitradorVO


class AdministradorDaoJDBC(Conexion):

    SQL_SELECT      = "SELECT id_administrador FROM administrador"
    SQL_SELECT_BY_ID = "SELECT id_administrador FROM administrador WHERE id_administrador = ?"
    SQL_INSERT      = "INSERT INTO administrador (id_administrador) VALUES (?)"
    SQL_DELETE      = "DELETE FROM administrador WHERE id_administrador = ?"

    def _rowToVO(self, row) -> AdminitradorVO:
        return AdminitradorVO(row[0])

    def select(self) -> list[AdminitradorVO]:
        """Recupera todos los administradores."""
        cursor = self.getCursor()
        administradores = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                administradores.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar administradores:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return administradores

    def selectById(self, id_administrador: int) -> AdminitradorVO:
        """Recupera un administrador por su ID."""
        cursor = self.getCursor()
        administrador = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_administrador,))
            row = cursor.fetchone()
            if row:
                administrador = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar administrador por ID:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return administrador

    def insert(self, vo: AdminitradorVO) -> int:
        """Inserta un nuevo administrador. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (vo.id_administrador,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar administrador:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_administrador: int) -> int:
        """Elimina un administrador por su ID. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_administrador,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar administrador:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows
