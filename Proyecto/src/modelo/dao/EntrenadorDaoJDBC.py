from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.EntrenadorVO import EntrenadorVO


class EntrenadorDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_entrenador, especialidad, id_administrador_registra FROM entrenador"
    SQL_SELECT_BY_ID = "SELECT id_entrenador, especialidad, id_administrador_registra FROM entrenador WHERE id_entrenador = ?"
    SQL_INSERT = "INSERT INTO entrenador (especialidad, id_administrador_registra) VALUES (?, ?)"
    SQL_UPDATE = "UPDATE entrenador SET especialidad=?, id_administrador_registra=? WHERE id_entrenador = ?"
    SQL_DELETE = "DELETE FROM entrenador WHERE id_entrenador = ?"

    def row_to_vo(self, row):
        return EntrenadorVO(row[0], row[1], row[2])

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
            cursor.execute(self.SQL_INSERT, (vo.especialidad, vo.id_administrador_registra,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    def update(self, vo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE, (vo.especialidad, vo.id_administrador_registra, vo.id_entrenador,))
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
