from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.TarifaVO import TarifaVO


class TarifaDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_tarifa, nombre, precio_mensual, servicios_incluidos, fecha_inicio, fecha_fin FROM tarifa"
    SQL_SELECT_BY_ID = "SELECT id_tarifa, nombre, precio_mensual, servicios_incluidos, fecha_inicio, fecha_fin FROM tarifa WHERE id_tarifa = ?"
    SQL_INSERT = "INSERT INTO tarifa (nombre, precio_mensual, servicios_incluidos, fecha_inicio, fecha_fin) VALUES (?, ?, ?, ?, ?)"
    SQL_UPDATE = "UPDATE tarifa SET nombre=?, precio_mensual=?, servicios_incluidos=?, fecha_inicio=?, fecha_fin=? WHERE id_tarifa = ?"
    SQL_DELETE = "DELETE FROM tarifa WHERE id_tarifa = ?"

    def row_to_vo(self, row):
        return TarifaVO(row[0], row[1], row[2], row[3], row[4], row[5])

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
            cursor.execute(self.SQL_INSERT, (vo.nombre, vo.precio_mensual, vo.servicios_incluidos, vo.fecha_inicio, vo.fecha_fin,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    def update(self, vo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE, (vo.nombre, vo.precio_mensual, vo.servicios_incluidos, vo.fecha_inicio, vo.fecha_fin, vo.id_tarifa,))
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
