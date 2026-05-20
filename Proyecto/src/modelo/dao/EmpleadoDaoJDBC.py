from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.EmpleadosVO import EmpleadoVO


class EmpleadoDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_empleado, salario FROM empleados"
    SQL_SELECT_BY_ID = "SELECT id_empleado, salario FROM empleados WHERE id_empleado = ?"
    SQL_INSERT = "INSERT INTO empleados (salario) VALUES (?)"
    SQL_UPDATE = "UPDATE empleados SET salario=? WHERE id_empleado = ?"
    SQL_DELETE = "DELETE FROM empleados WHERE id_empleado = ?"

    def row_to_vo(self, row):
        return EmpleadoVO(row[0], row[1])

    def select(self):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_SELECT)
            return [self.row_to_vo(row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def select_by_id(self, id):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id,))
            row = cursor.fetchone()
            return self.row_to_vo(row) if row else None
        finally:
            cursor.close()

    def insert(self, vo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_INSERT, (vo.salario,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    def update(self, vo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE, (vo.salario, vo.id_empleado,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()

    def delete(self, id):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_DELETE, (id,))
            self.conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close()
