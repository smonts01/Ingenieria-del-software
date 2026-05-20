from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.PagoVO import PagoVO


class PagoDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_pago, id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago, estado, tipo_cuota FROM pago"
    SQL_SELECT_BY_ID = "SELECT id_pago, id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago, estado, tipo_cuota FROM pago WHERE id_pago = ?"
    SQL_INSERT = "INSERT INTO pago (id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago, estado, tipo_cuota) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    SQL_UPDATE = "UPDATE pago SET id_cliente=?, id_contable=?, id_tarifa=?, importe=?, metodo_pago=?, fecha_pago=?, estado=?, tipo_cuota=? WHERE id_pago = ?"
    SQL_DELETE = "DELETE FROM pago WHERE id_pago = ?"

    def row_to_vo(self, row):
        return PagoVO(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

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
            cursor.execute(self.SQL_INSERT, (vo.id_cliente, vo.id_contable, vo.id_tarifa, vo.importe, vo.metodo_pago, vo.fecha_pago, vo.estado, vo.tipo_cuota,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    def update(self, vo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE, (vo.id_cliente, vo.id_contable, vo.id_tarifa, vo.importe, vo.metodo_pago, vo.fecha_pago, vo.estado, vo.tipo_cuota, vo.id_pago,))
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
