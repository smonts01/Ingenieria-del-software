from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.TarifaVO import TarifaVO


class TarifaDaoJDBC(Conexion):

    SQL_SELECT       = "SELECT id_tarifa, nombre, precio_mensual, servicios_incluidos, fecha_inicio, fecha_fin FROM tarifa"
    SQL_SELECT_BY_ID = "SELECT id_tarifa, nombre, precio_mensual, servicios_incluidos, fecha_inicio, fecha_fin FROM tarifa WHERE id_tarifa = ?"
    SQL_INSERT       = "INSERT INTO tarifa (nombre, precio_mensual, servicios_incluidos, fecha_inicio, fecha_fin) VALUES (?, ?, ?, ?, ?)"
    SQL_UPDATE       = "UPDATE tarifa SET nombre=?, precio_mensual=?, servicios_incluidos=?, fecha_inicio=?, fecha_fin=? WHERE id_tarifa=?"
    SQL_DELETE       = "DELETE FROM tarifa WHERE id_tarifa = ?"

    def _rowToVO(self, row) -> TarifaVO:
        id_tarifa, nombre, precio_mensual, servicios_incluidos, fecha_inicio, fecha_fin = row
        return TarifaVO(id_tarifa, nombre, precio_mensual, servicios_incluidos, fecha_inicio, fecha_fin)

    def select(self) -> list[TarifaVO]:
        """Recupera todas las tarifas."""
        cursor = self.getCursor()
        tarifas = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                tarifas.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar tarifas:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return tarifas

    def selectById(self, id_tarifa: int) -> TarifaVO:
        """Recupera una tarifa por su ID."""
        cursor = self.getCursor()
        tarifa = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_tarifa,))
            row = cursor.fetchone()
            if row:
                tarifa = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar tarifa por ID:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return tarifa

    def insert(self, vo: TarifaVO) -> int:
        """Inserta una nueva tarifa. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (
                vo.nombre, vo.precio_mensual, vo.servicios_incluidos,
                vo.fecha_inicio, vo.fecha_fin
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar tarifa:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def update(self, vo: TarifaVO) -> int:
        """Actualiza una tarifa existente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (
                vo.nombre, vo.precio_mensual, vo.servicios_incluidos,
                vo.fecha_inicio, vo.fecha_fin, vo.id_tarifa
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar tarifa:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_tarifa: int) -> int:
        """Elimina una tarifa por su ID. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_tarifa,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar tarifa:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows
