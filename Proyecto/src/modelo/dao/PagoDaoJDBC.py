from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.PagoVO import PagoVO


class PagoDaoJDBC(Conexion):

    SQL_SELECT            = "SELECT id_pago, id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago, estado, tipo_cuota FROM pago"
    SQL_SELECT_BY_ID      = "SELECT id_pago, id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago, estado, tipo_cuota FROM pago WHERE id_pago = ?"
    SQL_SELECT_BY_CLIENTE = "SELECT id_pago, id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago, estado, tipo_cuota FROM pago WHERE id_cliente = ?"
    SQL_INSERT            = "INSERT INTO pago (id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago, estado, tipo_cuota) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    SQL_UPDATE            = "UPDATE pago SET id_cliente=?, id_contable=?, id_tarifa=?, importe=?, metodo_pago=?, fecha_pago=?, estado=?, tipo_cuota=? WHERE id_pago=?"
    SQL_UPDATE_ESTADO     = "UPDATE pago SET estado=? WHERE id_pago=?"
    SQL_DELETE            = "DELETE FROM pago WHERE id_pago = ?"

    def _rowToVO(self, row) -> PagoVO:
        id_pago, id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago, estado, tipo_cuota = row
        return PagoVO(id_pago, id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago, estado, tipo_cuota)

    def select(self) -> list[PagoVO]:
        """Recupera todos los pagos."""
        cursor = self.getCursor()
        pagos = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                pagos.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar pagos:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return pagos

    def selectById(self, id_pago: int) -> PagoVO:
        """Recupera un pago por su ID."""
        cursor = self.getCursor()
        pago = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_pago,))
            row = cursor.fetchone()
            if row:
                pago = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar pago por ID:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return pago

    def selectByCliente(self, id_cliente: int) -> list[PagoVO]:
        """Recupera todos los pagos de un cliente."""
        cursor = self.getCursor()
        pagos = []
        try:
            cursor.execute(self.SQL_SELECT_BY_CLIENTE, (id_cliente,))
            for row in cursor.fetchall():
                pagos.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar pagos por cliente:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return pagos

    def insert(self, vo: PagoVO) -> int:
        """Inserta un nuevo pago. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (
                vo.id_cliente, vo.id_contable, vo.id_tarifa, vo.importe,
                vo.metodo_pago, vo.fecha_pago, vo.estado, vo.tipo_cuota
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar pago:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def update(self, vo: PagoVO) -> int:
        """Actualiza un pago existente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (
                vo.id_cliente, vo.id_contable, vo.id_tarifa, vo.importe,
                vo.metodo_pago, vo.fecha_pago, vo.estado, vo.tipo_cuota, vo.id_pago
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar pago:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def updateEstado(self, id_pago: int, estado: str) -> int:
        """Actualiza únicamente el estado de un pago. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE_ESTADO, (estado, id_pago))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar estado de pago:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_pago: int) -> int:
        """Elimina un pago por su ID. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_pago,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar pago:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows
