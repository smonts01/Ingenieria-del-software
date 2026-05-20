from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.EntrenadorVO import EntrenadorVO


class EntrenadorDaoJDBC(Conexion):

    SQL_SELECT       = "SELECT id_entrenador, especialidad, id_administrador_registra FROM entrenador"
    SQL_SELECT_BY_ID = "SELECT id_entrenador, especialidad, id_administrador_registra FROM entrenador WHERE id_entrenador = ?"
    SQL_INSERT       = "INSERT INTO entrenador (id_entrenador, especialidad, id_administrador_registra) VALUES (?, ?, ?)"
    SQL_UPDATE       = "UPDATE entrenador SET especialidad=?, id_administrador_registra=? WHERE id_entrenador=?"
    SQL_DELETE       = "DELETE FROM entrenador WHERE id_entrenador = ?"

    def _rowToVO(self, row) -> EntrenadorVO:
        id_entrenador, especialidad, id_administrador_registra = row
        return EntrenadorVO(id_entrenador, especialidad, id_administrador_registra)

    def select(self) -> list[EntrenadorVO]:
        """Recupera todos los entrenadores."""
        cursor = self.getCursor()
        entrenadores = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                entrenadores.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar entrenadores:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return entrenadores

    def selectById(self, id_entrenador: int) -> EntrenadorVO:
        """Recupera un entrenador por su ID."""
        cursor = self.getCursor()
        entrenador = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_entrenador,))
            row = cursor.fetchone()
            if row:
                entrenador = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar entrenador por ID:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return entrenador

    def insert(self, vo: EntrenadorVO) -> int:
        """Inserta un nuevo entrenador. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (vo.id_entrenador, vo.especialidad, vo.id_administrador_registra))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar entrenador:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def update(self, vo: EntrenadorVO) -> int:
        """Actualiza un entrenador existente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (vo.especialidad, vo.id_administrador_registra, vo.id_entrenador))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar entrenador:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_entrenador: int) -> int:
        """Elimina un entrenador por su ID. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_entrenador,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar entrenador:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows
