from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.InformeVO import InformeVO


class InformeDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_informe, id_contable, tipo_informe, fecha_generacion FROM informe"
    SQL_SELECT_BY_ID = "SELECT id_informe, id_contable, tipo_informe, fecha_generacion FROM informe WHERE id_informe = ?"
    SQL_INSERT = "INSERT INTO informe (id_contable, tipo_informe, fecha_generacion) VALUES (?, ?, ?)"
    SQL_UPDATE = "UPDATE informe SET id_contable=?, tipo_informe=?, fecha_generacion=? WHERE id_informe = ?"
    SQL_DELETE = "DELETE FROM informe WHERE id_informe = ?"

    def row_to_vo(self, row):
        return InformeVO(row[0], row[1], row[2], row[3])

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
            cursor.execute(self.SQL_INSERT, (vo.id_contable, vo.tipo_informe, vo.fecha_generacion,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    def update(self, vo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE, (vo.id_contable, vo.tipo_informe, vo.fecha_generacion, vo.id_informe,))
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
