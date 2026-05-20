from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.AdminitradorVo import AdminitradorVO


class AdministradorDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_administrador FROM administrador"
    SQL_SELECT_BY_ID = "SELECT id_administrador FROM administrador WHERE id_administrador = ?"
    SQL_INSERT = "INSERT INTO administrador (id_administrador) VALUES (?)"
    SQL_DELETE = "DELETE FROM administrador WHERE id_administrador = ?"

    def row_to_vo(self, row):
        return AdminitradorVO(row[0])

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
            cursor.execute(self.SQL_INSERT, (vo.id_administrador,))
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
