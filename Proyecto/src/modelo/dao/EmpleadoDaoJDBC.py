from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.EmpleadosVO import EmpleadoVO


class EmpleadoDaoJDBC:

    SQL_SELECT = "SELECT id_empleado, salario FROM empleados"
    SQL_SELECT_BY_ID = "SELECT id_empleado, salario FROM empleados WHERE id_empleado = ?"
    SQL_INSERT = "INSERT INTO empleados (id_empleado, salario) VALUES (?, ?)"
    SQL_UPDATE = "UPDATE empleados SET salario=? WHERE id_empleado=?"
    SQL_DELETE = "DELETE FROM empleados WHERE id_empleado = ?"

    def __init__(self):
        self._conexion = Conexion()  

    def _rowToVO(self, row) -> EmpleadoVO:
        id_empleado, salario = row
        return EmpleadoVO(id_empleado, salario)

    def select(self) -> list[EmpleadoVO]:
        """Recupera todos los empleados."""
        cursor = self._conexion.getCursor()
        empleados = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                empleados.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar empleados:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return empleados

    def selectById(self, id_empleado: int) -> EmpleadoVO:
        """Recupera un empleado por su ID."""
        cursor = self._conexion.getCursor()
        empleado = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_empleado,))
            row = cursor.fetchone()
            if row:
                empleado = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar empleado por ID:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return empleado

    def insert(self, vo: EmpleadoVO) -> int:
        """Inserta un nuevo empleado. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (vo.id_empleado, vo.salario))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar empleado:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    def update(self, vo: EmpleadoVO) -> int:
        """Actualiza el salario de un empleado. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (vo.salario, vo.id_empleado))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar empleado:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    def delete(self, id_empleado: int) -> int:
        """Elimina un empleado por su ID. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_empleado,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar empleado:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows
