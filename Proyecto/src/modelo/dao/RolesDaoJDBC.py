from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.RolesVO import RolesVO


class RolesDaoJDBC:
    """DAO para la tabla roles.

    Gestiona los roles de usuario del sistema (administrador, cliente,
    entrenador, contable, recepcionista). Solo permite consultas.
    """

    # Todos los roles del sistema
    SQL_SELECT = "SELECT id_rol, nombre_rol FROM roles"

    # Un rol por su ID
    SQL_SELECT_BY_ID = "SELECT id_rol, nombre_rol FROM roles WHERE id_rol = ?"


    def __init__(self):
        self._conexion = Conexion()


    def _rowToVO(self, row) -> RolesVO:
        """Convierte una fila de la BD en un RolesVO."""
        id_rol, nombre_rol = row
        return RolesVO(id_rol, nombre_rol)


    def select(self) -> list:
        """Devuelve todos los roles del sistema como lista de RolesVO."""
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
        """Devuelve el rol con el ID indicado como RolesVO,
        o None si no existe."""
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

    def nombre_rol_por_id(self, id_rol: int) -> str:
        """Devuelve el nombre del rol con el ID indicado,
        o None si no existe. Método de conveniencia sobre selectById."""
        rol = self.selectById(id_rol)
        return rol.nombre_rol if rol else None
