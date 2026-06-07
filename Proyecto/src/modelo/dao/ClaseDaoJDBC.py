from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.ClaseVO import ClaseVO


class ClaseDaoJDBC:

    SQL_SELECT = "SELECT id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad FROM clase"
    SQL_SELECT_BY_ID = "SELECT id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad FROM clase WHERE id_clase = ?"
    SQL_SELECT_BY_ENTRENADOR = "SELECT id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad FROM clase WHERE id_entrenador = ?"
    SQL_SELECT_BY_SALA = "SELECT id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad FROM clase WHERE id_sala = ?"
    SQL_INSERT = "INSERT INTO clase (id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    SQL_UPDATE = "UPDATE clase SET id_entrenador=?, id_sala=?, nombre_actividad=?, calorias_estimadas=?, dia_semana=?, hora_inicio=?, hora_fin=?, duracion=?, aforo_maximo=?, nivel_intensidad=? WHERE id_clase=?"
    SQL_DELETE = "DELETE FROM clase WHERE id_clase = ?"

    def __init__(self):
        self._conexion = Conexion()   
    
    def _rowToVO(self, row) -> ClaseVO:
        id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad = row
        return ClaseVO(id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad)

    def select(self) -> list[ClaseVO]:
        """Recupera todas las clases."""
        cursor = self._conexion.getCursor()
        clases = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                clases.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar clases:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return clases

    def selectById(self, id_clase: int) -> ClaseVO:
        """Recupera una clase por su ID."""
        cursor = self._conexion.getCursor()
        clase = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_clase,))
            row = cursor.fetchone()
            if row:
                clase = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar clase por ID:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return clase

    def selectByEntrenador(self, id_entrenador: int) -> list[ClaseVO]:
        """Recupera todas las clases de un entrenador."""
        cursor = self._conexion.getCursor()
        clases = []
        try:
            cursor.execute(self.SQL_SELECT_BY_ENTRENADOR, (id_entrenador,))
            for row in cursor.fetchall():
                clases.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar clases por entrenador:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return clases

    def selectBySala(self, id_sala: int) -> list[ClaseVO]:
        """Recupera todas las clases de una sala."""
        cursor = self._conexion.getCursor()
        clases = []
        try:
            cursor.execute(self.SQL_SELECT_BY_SALA, (id_sala,))
            for row in cursor.fetchall():
                clases.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar clases por sala:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return clases

    def insert(self, vo: ClaseVO) -> int:
        """Inserta una nueva clase. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (
                vo.id_entrenador, vo.id_sala, vo.nombre_actividad,
                vo.calorias_estimadas, vo.dia_semana, vo.hora_inicio,
                vo.hora_fin, vo.duracion, vo.aforo_maximo, vo.nivel_intensidad
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar clase:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    def update(self, vo: ClaseVO) -> int:
        """Actualiza una clase existente. Retorna filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (
                vo.id_entrenador, vo.id_sala, vo.nombre_actividad,
                vo.calorias_estimadas, vo.dia_semana, vo.hora_inicio,
                vo.hora_fin, vo.duracion, vo.aforo_maximo,
                vo.nivel_intensidad, vo.id_clase
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar clase:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    def delete(self, id_clase):
        cursor = self._conexion.getCursor()
        rows = 0

        try:
            cursor.execute(self.SQL_DELETE, (id_clase,))
            rows = cursor.rowcount

        except Exception as e:
            print("Error al eliminar clase:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows
