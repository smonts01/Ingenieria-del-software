from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.Cliente_tarifaVO import Cliente_tarifaVO


class ClienteTarifaDaoJDBC:
    """DAO para la tabla cliente_tarifa."""

    SQL_SELECT = """
        SELECT 
            id_cliente_tarifa,
            id_cliente,
            id_tarifa,
            fecha_contratacion,
            estado
        FROM cliente_tarifa
    """

    SQL_SELECT_BY_CLIENTE = """
        SELECT 
            id_cliente_tarifa,
            id_cliente,
            id_tarifa,
            fecha_contratacion,
            estado
        FROM cliente_tarifa
        WHERE id_cliente = ?
    """

    SQL_SELECT_ACTIVA_BY_CLIENTE = """
        SELECT 
            id_cliente_tarifa,
            id_cliente,
            id_tarifa,
            fecha_contratacion,
            estado
        FROM cliente_tarifa
        WHERE id_cliente = ?
          AND estado = 'activa'
    """

    SQL_INSERT = """
        INSERT INTO cliente_tarifa
            (id_cliente, id_tarifa, fecha_contratacion, estado)
        VALUES
            (?, ?, CURDATE(), 'activa')
    """

    SQL_DESACTIVAR_ANTERIORES = """
        UPDATE cliente_tarifa
        SET estado = 'inactiva'
        WHERE id_cliente = ?
          AND estado = 'activa'
    """

    SQL_UPDATE = """
        UPDATE cliente_tarifa
        SET id_tarifa = ?, fecha_contratacion = ?, estado = ?
        WHERE id_cliente_tarifa = ?
    """

    SQL_DELETE = """
        DELETE FROM cliente_tarifa
        WHERE id_cliente_tarifa = ?
    """

    def __init__(self):
        self._conexion = Conexion()  

    def _rowToVO(self, row) -> Cliente_tarifaVO:
        id_cliente_tarifa, id_cliente, id_tarifa, fecha_contratacion, estado = row

        return Cliente_tarifaVO(
            id_cliente_tarifa=id_cliente_tarifa,
            id_cliente=id_cliente,
            id_tarifa=id_tarifa,
            fecha_contratacion=fecha_contratacion,
            estado=estado
        )

    def select(self) -> list[Cliente_tarifaVO]:
        cursor = self._conexion.getCursor()
        resultado = []

        try:
            cursor.execute(self.SQL_SELECT)

            for row in cursor.fetchall():
                resultado.append(self._rowToVO(row))

        except Exception as e:
            print("Error al seleccionar cliente_tarifa:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return resultado

    def selectByCliente(self, id_cliente: int) -> list[Cliente_tarifaVO]:
        cursor = self._conexion.getCursor()
        resultado = []

        try:
            cursor.execute(self.SQL_SELECT_BY_CLIENTE, (id_cliente,))

            for row in cursor.fetchall():
                resultado.append(self._rowToVO(row))

        except Exception as e:
            print("Error al seleccionar cliente_tarifa por cliente:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return resultado

    def selectActivaByCliente(self, id_cliente: int):
        cursor = self._conexion.getCursor()
        vo = None

        try:
            cursor.execute(self.SQL_SELECT_ACTIVA_BY_CLIENTE, (id_cliente,))
            row = cursor.fetchone()

            if row:
                vo = self._rowToVO(row)

        except Exception as e:
            print("Error al seleccionar tarifa activa del cliente:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return vo

    def insert(self, id_cliente: int, id_tarifa: int) -> int:
        cursor = self._conexion.getCursor()
        rows = 0

        try:
            cursor.execute(self.SQL_INSERT, (id_cliente, id_tarifa))
            rows = cursor.rowcount

        except Exception as e:
            print("Error al insertar cliente_tarifa:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows

    def asignar_tarifa_activa(self, id_cliente: int, id_tarifa: int) -> int:
        cursor = self._conexion.getCursor()
        rows = 0

        try:
            cursor.execute(self.SQL_DESACTIVAR_ANTERIORES, (id_cliente,))
            cursor.execute(self.SQL_INSERT, (id_cliente, id_tarifa))
            rows = cursor.rowcount

        except Exception as e:
            print("Error al asignar tarifa activa al cliente:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows

    def update(self, vo: Cliente_tarifaVO) -> int:
        cursor = self._conexion.getCursor()
        rows = 0

        try:
            cursor.execute(
                self.SQL_UPDATE,
                (
                    vo.id_tarifa,
                    vo.fecha_contratacion,
                    vo.estado,
                    vo.id_cliente_tarifa
                )
            )
            rows = cursor.rowcount

        except Exception as e:
            print("Error al actualizar cliente_tarifa:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows

    def delete(self, id_cliente_tarifa: int) -> int:
        cursor = self._conexion.getCursor()
        rows = 0

        try:
            cursor.execute(self.SQL_DELETE, (id_cliente_tarifa,))
            rows = cursor.rowcount

        except Exception as e:
            print("Error al eliminar cliente_tarifa:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows