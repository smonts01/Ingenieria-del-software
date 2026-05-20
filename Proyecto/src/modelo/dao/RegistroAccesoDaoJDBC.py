from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.Registro_accesoVO import RegistroAccesoVO


class RegistroAccesoDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_registro, id_usuario, fecha_hora_registro, tipo_acceso FROM registro_acceso"
    SQL_SELECT_BY_ID = "SELECT id_registro, id_usuario, fecha_hora_registro, tipo_acceso FROM registro_acceso WHERE id_registro = ?"
    SQL_INSERT = "INSERT INTO registro_acceso (id_usuario, fecha_hora_registro, tipo_acceso) VALUES (?, ?, ?)"
    SQL_UPDATE = "UPDATE registro_acceso SET id_usuario=?, fecha_hora_registro=?, tipo_acceso=? WHERE id_registro = ?"
    SQL_DELETE = "DELETE FROM registro_acceso WHERE id_registro = ?"

    def row_to_vo(self, row):
        return RegistroAccesoVO(row[0], row[1], row[2], row[3])

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
            cursor.execute(self.SQL_INSERT, (vo.id_usuario, vo.fecha_hora_registro, vo.tipo_acceso,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    def update(self, vo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE, (vo.id_usuario, vo.fecha_hora_registro, vo.tipo_acceso, vo.id_registro,))
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
