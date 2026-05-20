from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.RecepcionistaVO import RecepcionistaVO


class RecepcionistaDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_recepcionista, turno, id_administrador_registra FROM recepcionista"
    SQL_SELECT_BY_ID = "SELECT id_recepcionista, turno, id_administrador_registra FROM recepcionista WHERE id_recepcionista = ?"
    SQL_INSERT = "INSERT INTO recepcionista (turno, id_administrador_registra) VALUES (?, ?)"
    SQL_UPDATE = "UPDATE recepcionista SET turno=?, id_administrador_registra=? WHERE id_recepcionista = ?"
    SQL_DELETE = "DELETE FROM recepcionista WHERE id_recepcionista = ?"

    def row_to_vo(self, row):
        return RecepcionistaVO(row[0], row[1], row[2])

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
            cursor.execute(self.SQL_INSERT, (vo.turno, vo.id_administrador_registra,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    def update(self, vo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE, (vo.turno, vo.id_administrador_registra, vo.id_recepcionista,))
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
