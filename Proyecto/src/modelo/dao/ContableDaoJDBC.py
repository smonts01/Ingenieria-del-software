from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.ContableVO import ContableVO


class ContableDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_contable, titulacion, id_administrador_registra FROM contable"
    SQL_SELECT_BY_ID = "SELECT id_contable, titulacion, id_administrador_registra FROM contable WHERE id_contable = ?"
    SQL_INSERT = "INSERT INTO contable (titulacion, id_administrador_registra) VALUES (?, ?)"
    SQL_UPDATE = "UPDATE contable SET titulacion=?, id_administrador_registra=? WHERE id_contable = ?"
    SQL_DELETE = "DELETE FROM contable WHERE id_contable = ?"

    def row_to_vo(self, row):
        return ContableVO(row[0], row[1], row[2])

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
            cursor.execute(self.SQL_INSERT, (vo.titulacion, vo.id_administrador_registra,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    def update(self, vo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE, (vo.titulacion, vo.id_administrador_registra, vo.id_contable,))
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
