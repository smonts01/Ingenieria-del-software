from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.Cliente_tarifaVO import Cliente_tarifaVO


class ClienteTarifaDaoJDBC(Conexion):
    """DAO para la tabla cliente_tarifa (relación M:N entre clientes y tarifas)."""

    SQL_SELECT = "SELECT id_cliente, id_tarifa, fecha_inicio, fecha_fin FROM cliente_tarifa"
    SQL_SELECT_BY_CLIENTE = "SELECT id_cliente, id_tarifa, fecha_inicio, fecha_fin FROM cliente_tarifa WHERE id_cliente = ?"
    SQL_SELECT_BY_TARIFA = "SELECT id_cliente, id_tarifa, fecha_inicio, fecha_fin FROM cliente_tarifa WHERE id_tarifa = ?"
    SQL_SELECT_BY_PK = "SELECT id_cliente, id_tarifa, fecha_inicio, fecha_fin FROM cliente_tarifa WHERE id_cliente = ? AND id_tarifa = ?"
    SQL_INSERT = "INSERT INTO cliente_tarifa (id_cliente, id_tarifa, fecha_inicio, fecha_fin) VALUES (?, ?, ?, ?)"
    SQL_UPDATE = "UPDATE cliente_tarifa SET fecha_inicio=?, fecha_fin=? WHERE id_cliente=? AND id_tarifa=?"
    SQL_DELETE = "DELETE FROM cliente_tarifa WHERE id_cliente = ? AND id_tarifa = ?"

    SQL_DESACTIVAR_ANTERIORES = """
            UPDATE cliente_tarifa
            SET estado = 'inactiva'
            WHERE id_cliente = ?
            AND estado = 'activa'
        """

    SQL_INSERT = """
            INSERT INTO cliente_tarifa
                (id_cliente, id_tarifa, fecha_contratacion, estado)
            VALUES
                (?, ?, CURDATE(), 'activa')
        """

    def _rowToVO(self, row) -> Cliente_tarifaVO:
        id_cliente, id_tarifa, fecha_inicio, fecha_fin = row
        return ClienteTarifaVO(id_cliente, id_tarifa, fecha_inicio, fecha_fin)

    def select(self) -> list[Cliente_tarifaVO]:
        """Recupera todas las asignaciones cliente-tarifa."""
        cursor = self.getCursor()
        resultado = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                resultado.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar cliente_tarifa:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return resultado

    def selectByCliente(self, id_cliente: int) -> list[Cliente_tarifaVO]:
        """Recupera todas las tarifas asignadas a un cliente."""
        cursor = self.getCursor()
        resultado = []
        try:
            cursor.execute(self.SQL_SELECT_BY_CLIENTE, (id_cliente,))
            for row in cursor.fetchall():
                resultado.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar cliente_tarifa por cliente:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return resultado

    def selectByTarifa(self, id_tarifa: int) -> list[Cliente_tarifaVO]:
        """Recupera todos los clientes asignados a una tarifa."""
        cursor = self.getCursor()
        resultado = []
        try:
            cursor.execute(self.SQL_SELECT_BY_TARIFA, (id_tarifa,))
            for row in cursor.fetchall():
                resultado.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar cliente_tarifa por tarifa:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return resultado

    def selectByPk(self, id_cliente: int, id_tarifa: int) -> Cliente_tarifaVO:
        """Recupera una asignación por su clave primaria compuesta."""
        cursor = self.getCursor()
        vo = None
        try:
            cursor.execute(self.SQL_SELECT_BY_PK, (id_cliente, id_tarifa))
            row = cursor.fetchone()
            if row:
                vo = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar cliente_tarifa por PK:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return vo

    def insert(self, vo: Cliente_tarifaVO) -> int:
        """Asigna una tarifa a un cliente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (vo.id_cliente, vo.id_tarifa, vo.fecha_inicio, vo.fecha_fin))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar cliente_tarifa:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def update(self, vo: Cliente_tarifaVO) -> int:
        """Actualiza las fechas de una asignación cliente-tarifa. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (vo.fecha_inicio, vo.fecha_fin, vo.id_cliente, vo.id_tarifa))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar cliente_tarifa:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_cliente: int, id_tarifa: int) -> int:
        """Elimina la asignación de una tarifa a un cliente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_cliente, id_tarifa))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar cliente_tarifa:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def asignar_tarifa_activa(self, id_cliente, id_tarifa):
        cursor = self.getCursor()
        rows = 0

        try:
            cursor.execute(self.SQL_DESACTIVAR_ANTERIORES, (id_cliente,))
            cursor.execute(self.SQL_INSERT, (id_cliente, id_tarifa))
            rows = cursor.rowcount

        except Exception as e:
            print("Error al asignar tarifa activa al cliente:", e)

        finally:
            cursor.close()
            self.closeConnection()

        return rows