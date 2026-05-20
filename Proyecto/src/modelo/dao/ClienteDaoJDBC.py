from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.ClientesVO import ClientesVO


class ClienteDaoJDBC(Conexion):

    SQL_SELECT          = "SELECT id_cliente, estado_pagado, calorias_acumuladas FROM clientes"
    SQL_SELECT_BY_ID    = "SELECT id_cliente, estado_pagado, calorias_acumuladas FROM clientes WHERE id_cliente = ?"
    SQL_INSERT          = "INSERT INTO clientes (id_cliente, estado_pagado, calorias_acumuladas) VALUES (?, ?, ?)"
    SQL_UPDATE          = "UPDATE clientes SET estado_pagado=?, calorias_acumuladas=? WHERE id_cliente=?"
    SQL_UPDATE_ESTADO   = "UPDATE clientes SET estado_pagado=? WHERE id_cliente=?"
    SQL_UPDATE_CALORIAS = "UPDATE clientes SET calorias_acumuladas=? WHERE id_cliente=?"
    SQL_DELETE          = "DELETE FROM clientes WHERE id_cliente = ?"

    def _rowToVO(self, row) -> ClientesVO:
        id_cliente, estado_pagado, calorias_acumuladas = row
        return ClientesVO(id_cliente, estado_pagado, calorias_acumuladas)

    def select(self) -> list[ClientesVO]:
        """Recupera todos los clientes."""
        cursor = self.getCursor()
        clientes = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                clientes.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar clientes:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return clientes

    def selectById(self, id_cliente: int) -> ClientesVO:
        """Recupera un cliente por su ID."""
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
            cursor.close()
            self.closeConnection()
        return cliente

    def insert(self, vo: ClientesVO) -> int:
        """Inserta un nuevo cliente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (
                vo.id_cliente, vo.estado_pagado, vo.calorias_acumuladas
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar cliente:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def update(self, vo: ClientesVO) -> int:
        """Actualiza un cliente existente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (
                vo.estado_pagado, vo.calorias_acumuladas, vo.id_cliente
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar cliente:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def updateEstadoPagado(self, id_cliente: int, estado_pagado: str) -> int:
        """Actualiza únicamente el estado de pago de un cliente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE_ESTADO, (estado_pagado, id_cliente))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar estado de pago:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def updateCalorias(self, id_cliente: int, calorias_acumuladas: int) -> int:
        """Actualiza únicamente las calorías acumuladas de un cliente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE_CALORIAS, (calorias_acumuladas, id_cliente))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar calorías:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_cliente: int) -> int:
        """Elimina un cliente por su ID. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_cliente,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar cliente:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows
