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
