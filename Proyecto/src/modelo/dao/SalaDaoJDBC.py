from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.SalaVO import SalaVO


class SalaDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_sala, nombre, aforo_maximo, tipo_zona FROM sala"
    SQL_SELECT_BY_ID = "SELECT id_sala, nombre, aforo_maximo, tipo_zona FROM sala WHERE id_sala = ?"
    SQL_INSERT = "INSERT INTO sala (nombre, aforo_maximo, tipo_zona) VALUES (?, ?, ?)"
    SQL_UPDATE = "UPDATE sala SET nombre=?, aforo_maximo=?, tipo_zona=? WHERE id_sala = ?"
    SQL_DELETE = "DELETE FROM sala WHERE id_sala = ?"

    def row_to_vo(self, row):
        return SalaVO(row[0], row[1], row[2], row[3])

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
            cursor.execute(self.SQL_INSERT, (vo.nombre, vo.aforo_maximo, vo.tipo_zona,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    def update(self, vo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE, (vo.nombre, vo.aforo_maximo, vo.tipo_zona, vo.id_sala,))
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
