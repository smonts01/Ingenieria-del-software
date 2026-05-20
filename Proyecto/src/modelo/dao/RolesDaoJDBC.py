from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.RolesVO import RolesVO


class RolesDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_rol, nombre_rol FROM roles"
    SQL_SELECT_BY_ID = "SELECT id_rol, nombre_rol FROM roles WHERE id_rol = ?"
    SQL_INSERT = "INSERT INTO roles (nombre_rol) VALUES (?)"
    SQL_UPDATE = "UPDATE roles SET nombre_rol=? WHERE id_rol = ?"
    SQL_DELETE = "DELETE FROM roles WHERE id_rol = ?"

    def row_to_vo(self, row):
        return RolesVO(row[0], row[1])

    def select(self):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_SELECT)
            return [self.row_to_vo(row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def select_by_id(self, id):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id,))
            row = cursor.fetchone()
            return self.row_to_vo(row) if row else None
        finally:
            cursor.close()

    def insert(self, vo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_INSERT, (vo.nombre_rol,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    def update(self, vo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE, (vo.nombre_rol, vo.id_rol,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    def delete(self, id):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_DELETE, (id,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()
