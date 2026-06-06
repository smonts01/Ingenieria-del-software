from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.RolesVO import RolesVO


class RolesDaoJDBC:

    SQL_SELECT = "SELECT id_rol, nombre_rol FROM roles"
    SQL_SELECT_BY_ID = "SELECT id_rol, nombre_rol FROM roles WHERE id_rol = ?"
    SQL_INSERT = "INSERT INTO roles (nombre_rol) VALUES (?)"
    SQL_UPDATE = "UPDATE roles SET nombre_rol=? WHERE id_rol=?"
    SQL_DELETE = "DELETE FROM roles WHERE id_rol = ?"

    def __init__(self):
        self._conexion = Conexion()  

    def _rowToVO(self, row) -> RolesVO:
        id_rol, nombre_rol = row
        return RolesVO(id_rol, nombre_rol)

    def select(self) -> list[RolesVO]:
        """Recupera todos los roles."""
        cursor = self._conexion.getCursor()
        roles = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                roles.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar roles:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return roles

    def selectById(self, id_rol: int) -> RolesVO:
        """Recupera un rol por su ID."""
        cursor = self._conexion.getCursor()
        rol = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_rol,))
            row = cursor.fetchone()
            if row:
                rol = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar rol por ID:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rol

    def insert(self, vo: RolesVO) -> int:
        """Inserta un nuevo rol. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (vo.nombre_rol,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar rol:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    def update(self, vo: RolesVO) -> int:
        """Actualiza un rol existente. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (vo.nombre_rol, vo.id_rol))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar rol:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    def delete(self, id_rol: int) -> int:
        """Elimina un rol por su ID. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_rol,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar rol:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    def nombre_rol_por_id(self, id_rol):
        rol = self.selectById(id_rol)
        return rol.nombre_rol if rol else None

