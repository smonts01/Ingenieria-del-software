from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.InformeVO import InformeVO


class InformeDaoJDBC(Conexion):

    SQL_SELECT       = "SELECT id_informe, id_contable, tipo_informe, fecha_generacion FROM informe"
    SQL_SELECT_BY_ID = "SELECT id_informe, id_contable, tipo_informe, fecha_generacion FROM informe WHERE id_informe = ?"
    SQL_SELECT_BY_CONTABLE = "SELECT id_informe, id_contable, tipo_informe, fecha_generacion FROM informe WHERE id_contable = ?"
    SQL_INSERT       = "INSERT INTO informe (id_contable, tipo_informe, fecha_generacion) VALUES (?, ?, ?)"
    SQL_UPDATE       = "UPDATE informe SET id_contable=?, tipo_informe=?, fecha_generacion=? WHERE id_informe=?"
    SQL_DELETE       = "DELETE FROM informe WHERE id_informe = ?"

    def _rowToVO(self, row) -> InformeVO:
        id_informe, id_contable, tipo_informe, fecha_generacion = row
        return InformeVO(id_informe, id_contable, tipo_informe, fecha_generacion)

    def select(self) -> list[InformeVO]:
        """Recupera todos los informes."""
        cursor = self.getCursor()
        informes = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                informes.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar informes:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return informes

    def selectById(self, id_informe: int) -> InformeVO:
        """Recupera un informe por su ID."""
        cursor = self.getCursor()
        informe = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_informe,))
            row = cursor.fetchone()
            if row:
                informe = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar informe por ID:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return informe

    def selectByContable(self, id_contable: int) -> list[InformeVO]:
        """Recupera todos los informes generados por un contable."""
        cursor = self.getCursor()
        informes = []
        try:
            cursor.execute(self.SQL_SELECT_BY_CONTABLE, (id_contable,))
            for row in cursor.fetchall():
                informes.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar informes por contable:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return informes

    def insert(self, vo: InformeVO) -> int:
        """Inserta un nuevo informe. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (vo.id_contable, vo.tipo_informe, vo.fecha_generacion))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar informe:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def update(self, vo: InformeVO) -> int:
        """Actualiza un informe existente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (vo.id_contable, vo.tipo_informe, vo.fecha_generacion, vo.id_informe))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar informe:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_informe: int) -> int:
        """Elimina un informe por su ID. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_informe,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar informe:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows
