from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.Registro_accesoVO import RegistroAccesoVO


class RegistroAccesoDaoJDBC:

    SQL_SELECT = "SELECT id_registro, id_usuario, fecha_hora_registro, tipo_acceso FROM registro_acceso"
    SQL_SELECT_BY_ID = "SELECT id_registro, id_usuario, fecha_hora_registro, tipo_acceso FROM registro_acceso WHERE id_registro = ?"
    SQL_SELECT_BY_USUARIO = "SELECT id_registro, id_usuario, fecha_hora_registro, tipo_acceso FROM registro_acceso WHERE id_usuario = ?"
    SQL_INSERT = "INSERT INTO registro_acceso (id_usuario, fecha_hora_registro, tipo_acceso) VALUES (?, ?, ?)"
    SQL_UPDATE = "UPDATE registro_acceso SET id_usuario=?, fecha_hora_registro=?, tipo_acceso=? WHERE id_registro=?"
    SQL_DELETE = "DELETE FROM registro_acceso WHERE id_registro = ?"

    def __init__(self):
        self._conexion = Conexion()  

    def _rowToVO(self, row) -> RegistroAccesoVO:
        id_registro, id_usuario, fecha_hora_registro, tipo_acceso = row
        return RegistroAccesoVO(id_registro, id_usuario, fecha_hora_registro, tipo_acceso)

    def select(self) -> list[RegistroAccesoVO]:
        """Recupera todos los registros de acceso."""
        cursor = self._conexion.getCursor()
        registros = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                registros.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar registros de acceso:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return registros

    def selectById(self, id_registro: int) -> RegistroAccesoVO:
        """Recupera un registro de acceso por su ID."""
        cursor = self._conexion.getCursor()
        registro = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_registro,))
            row = cursor.fetchone()
            if row:
                registro = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar registro de acceso por ID:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return registro

    def selectByUsuario(self, id_usuario: int) -> list[RegistroAccesoVO]:
        """Recupera todos los registros de acceso de un usuario."""
        cursor = self._conexion.getCursor()
        registros = []
        try:
            cursor.execute(self.SQL_SELECT_BY_USUARIO, (id_usuario,))
            for row in cursor.fetchall():
                registros.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar registros por usuario:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return registros

    def insert(self, vo: RegistroAccesoVO) -> int:
        """Registra un nuevo acceso. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (vo.id_usuario, vo.fecha_hora_registro, vo.tipo_acceso))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar registro de acceso:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    def update(self, vo: RegistroAccesoVO) -> int:
        """Actualiza un registro de acceso. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (vo.id_usuario, vo.fecha_hora_registro, vo.tipo_acceso, vo.id_registro))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar registro de acceso:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    def delete(self, id_registro: int) -> int:
        """Elimina un registro de acceso por su ID. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_registro,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar registro de acceso:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows
