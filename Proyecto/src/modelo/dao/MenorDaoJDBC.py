from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.MenorVO import MenorVO


class MenorDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_cliente, dni_tutor, nombre_tutor FROM menor"
    SQL_SELECT_BY_ID = "SELECT id_cliente, dni_tutor, nombre_tutor FROM menor WHERE id_cliente = ?"
    SQL_INSERT = "INSERT INTO menor (dni_tutor, nombre_tutor) VALUES (?, ?)"
    SQL_UPDATE = "UPDATE menor SET dni_tutor=?, nombre_tutor=? WHERE id_cliente = ?"
    SQL_DELETE = "DELETE FROM menor WHERE id_cliente = ?"

    def row_to_vo(self, row):
        return MenorVO(row[0], row[1], row[2])

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
            cursor.execute(self.SQL_INSERT, (vo.dni_tutor, vo.nombre_tutor,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    def update(self, vo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE, (vo.dni_tutor, vo.nombre_tutor, vo.id_cliente,))
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
