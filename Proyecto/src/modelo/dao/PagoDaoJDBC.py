from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.PagoVO import PagoVO


class PagoDaoJDBC:

    SQL_SELECT = """
        SELECT id_pago, id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago
        FROM pago
    """

    SQL_SELECT_BY_ID = """
        SELECT id_pago, id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago
        FROM pago
        WHERE id_pago = ?
    """

    SQL_SELECT_BY_CLIENTE = """
        SELECT id_pago, id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago
        FROM pago
        WHERE id_cliente = ?
    """

    SQL_INSERT = """
        INSERT INTO pago
            (id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago)
        VALUES
            (?, ?, ?, ?, ?, ?)
    """

    SQL_UPDATE = """
        UPDATE pago
        SET id_cliente = ?,
            id_contable = ?,
            id_tarifa = ?,
            importe = ?,
            metodo_pago = ?,
            fecha_pago = ?
        WHERE id_pago = ?
    """



    def __init__(self):
        self._conexion = Conexion()  

    def _rowToVO(self, row) -> PagoVO:
        id_pago, id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago = row

        return PagoVO(
            id_pago=id_pago,
            id_cliente=id_cliente,
            id_contable=id_contable,
            id_tarifa=id_tarifa,
            importe=importe,
            metodo_pago=metodo_pago,
            fecha_pago=fecha_pago
        )

    def select(self) -> list[PagoVO]:
        cursor = self._conexion.getCursor()
        pagos = []

        try:
            cursor.execute(self.SQL_SELECT)

            for row in cursor.fetchall():
                pagos.append(self._rowToVO(row))

        except Exception as e:
            print("Error al seleccionar pagos:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return pagos

    def selectById(self, id_pago: int) -> PagoVO:
        cursor = self._conexion.getCursor()
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
            self._conexion.closeConnection()

        return pago

    def selectByCliente(self, id_cliente: int) -> list[PagoVO]:
        cursor = self._conexion.getCursor()
        pagos = []

        try:
            cursor.execute(self.SQL_SELECT_BY_CLIENTE, (id_cliente,))

            for row in cursor.fetchall():
                pagos.append(self._rowToVO(row))

        except Exception as e:
            print("Error al seleccionar pagos por cliente:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return pagos

    def insert(self, vo: PagoVO) -> int:
        cursor = self._conexion.getCursor()
        rows = 0

        try:
            cursor.execute(
                self.SQL_INSERT,
                (
                    vo.id_cliente,
                    vo.id_contable,
                    vo.id_tarifa,
                    vo.importe,
                    vo.metodo_pago,
                    vo.fecha_pago
                )
            )

            rows = cursor.rowcount

        except Exception as e:
            print("Error al insertar pago:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows

    def update(self, vo: PagoVO) -> int:
        cursor = self._conexion.getCursor()
        rows = 0

        try:
            cursor.execute(
                self.SQL_UPDATE,
                (
                    vo.id_cliente,
                    vo.id_contable,
                    vo.id_tarifa,
                    vo.importe,
                    vo.metodo_pago,
                    vo.fecha_pago,
                    vo.id_pago
                )
            )

            rows = cursor.rowcount

        except Exception as e:
            print("Error al actualizar pago:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows

