from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.ClientesVO import ClientesVO

class ClienteDaoJDBC(ClientesVO, Conexion):
    SQL_SELECT              = "SELECT id_cliente, estado_pagado, calorias_acumuladas FROM clientes"
    SQL_SELECT_BY_ID        = "SELECT id_cliente, estado_pagado, calorias_acumuladas FROM clientes WHERE id_cliente = ?"
    SQL_INSERT              = "INSERT INTO clientes (id_cliente, estado_pagado, calorias_acumuladas) VALUES (?, ?, ?)"
    SQL_UPDATE              = "UPDATE clientes SET estado_pagado=?, calorias_acumuladas=? WHERE id_cliente=?"
    SQL_UPDATE_ESTADO       = "UPDATE clientes SET estado_pagado=? WHERE id_cliente=?"
    SQL_UPDATE_CALORIAS     = "UPDATE clientes SET calorias_acumuladas=? WHERE id_cliente=?"
    SQL_DELETE              = "DELETE FROM clientes WHERE id_cliente = ?"

    def _rowToVO(self, row) -> ClientesVO:
        id_cliente, estado_pagado, calorias_acumuladas = row
        return ClientesVO(id_cliente, estado_pagado, calorias_acumuladas)

    def select(self) -> list[ClientesVO]:
        """Recupera todos los clientes"""
        cursor = self.getCursor()
        clientes = []
        try:
            cursor.execute(self.SQL_SELECT)
            rows = cursor.fetchall()
            for row in rows:
                clientes.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar clientes:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return clientes

    def selectById(self, id_cliente: int) -> ClientesVO:
        """Recupera el cliente con ese ID"""
        cursor = self.getCursor()
        cliente = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_cliente,))
            row = cursor.fetchone()
            if row:
                cliente = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar cliente por ID:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return cliente

    def insert(self, cliente: ClientesVO) -> int:
        """Inserta un nuevo cliente"""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (
                cliente.id_cliente, cliente.estado_pagado, cliente.calorias_acumuladas
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar cliente:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return rows

    def update(self, cliente: ClientesVO) -> int:
        """Actualiza un nuevo cliente"""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (
                cliente.estado_pagado, cliente.calorias_acumuladas, cliente.id_cliente
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar cliente:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return rows

    def updateEstadoPagado(self, id_cliente: int, estado_pagado: str) -> int:
        """Actualiza el estado del pago del cliente con ese ID"""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE_ESTADO, (estado_pagado, id_cliente))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar estado de pago:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return rows

    def updateCalorias(self, id_cliente: int, calorias: int) -> int:
        """Actualiza las calorias del cliente con ese ID"""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE_CALORIAS, (calorias, id_cliente))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar calorías:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_cliente: int) -> int:
        """Elimina el cliente con ese ID"""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_cliente,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar cliente:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return rows