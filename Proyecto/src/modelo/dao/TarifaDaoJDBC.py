from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.TarifaVO import TarifaVO


class TarifaDaoJDBC:

    SQL_SELECT = """
        SELECT id_tarifa, nombre, precio_mensual, servicios_incluidos, fecha_inicio 
        FROM tarifa
    """

    SQL_SELECT_BY_ID = """
        SELECT id_tarifa, nombre, precio_mensual, servicios_incluidos, fecha_inicio 
        FROM tarifa 
        WHERE id_tarifa = ?
    """

    SQL_INSERT = """
        INSERT INTO tarifa 
            (nombre, precio_mensual, servicios_incluidos, fecha_inicio) 
        VALUES 
            (?, ?, ?, ?)
    """

    SQL_UPDATE = """
        UPDATE tarifa 
        SET nombre = ?, 
            precio_mensual = ?, 
            servicios_incluidos = ?, 
            fecha_inicio = ? 
        WHERE id_tarifa = ?
    """

    SQL_DELETE = """
        DELETE FROM tarifa 
        WHERE id_tarifa = ?
    """

    def __init__(self):
        self._conexion = Conexion()  


    def _rowToVO(self, row) -> TarifaVO:
        return TarifaVO(*row)

    def select(self) -> list[TarifaVO]:
        cursor = self._conexion.getCursor()
        tarifas = []

        try:
            cursor.execute(self.SQL_SELECT)

            for row in cursor.fetchall():
                tarifas.append(self._rowToVO(row))

        except Exception as e:
            print("Error al seleccionar tarifas:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return tarifas

    def selectById(self, id_tarifa: int) -> TarifaVO:
        cursor = self._conexion.getCursor()
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
            self._conexion.closeConnection()

        return tarifa

    def insert(self, vo: TarifaVO) -> int:
        cursor = self._conexion.getCursor()
        rows = 0

        try:
            cursor.execute(
                self.SQL_INSERT,
                (
                    vo.nombre,
                    vo.precio_mensual,
                    vo.servicios_incluidos,
                    vo.fecha_inicio
                )
            )

            rows = cursor.rowcount

        except Exception as e:
            print("Error al insertar tarifa:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows

    def update(self, vo: TarifaVO) -> int:
        cursor = self._conexion.getCursor()
        rows = 0

        try:
            cursor.execute(
                self.SQL_UPDATE,
                (
                    vo.nombre,
                    vo.precio_mensual,
                    vo.servicios_incluidos,
                    vo.fecha_inicio,
                    vo.id_tarifa
                )
            )

            rows = cursor.rowcount

        except Exception as e:
            print("Error al actualizar tarifa:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows

    def delete(self, id_tarifa: int) -> int:
        cursor = self._conexion.getCursor()
        rows = 0

        try:
            cursor.execute(self.SQL_DELETE, (id_tarifa,))
            rows = cursor.rowcount

        except Exception as e:
            print("Error al eliminar tarifa:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows