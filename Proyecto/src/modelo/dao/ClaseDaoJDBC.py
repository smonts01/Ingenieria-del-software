from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.ClaseVO import ClaseVO

class ClaseDaoJDBC(ClaseVO, Conexion):
    SQL_SELECT              = "SELECT id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad FROM clase"
    SQL_SELECT_BY_ID        = "SELECT id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad FROM clase WHERE id_clase = ?"
    SQL_SELECT_BY_ENTRENADOR = "SELECT id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad FROM clase WHERE id_entrenador = ?"
    SQL_SELECT_BY_SALA      = "SELECT id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad FROM clase WHERE id_sala = ?"
    SQL_INSERT              = "INSERT INTO clase (id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    SQL_UPDATE              = "UPDATE clase SET id_entrenador=?, id_sala=?, nombre_actividad=?, calorias_estimadas=?, dia_semana=?, hora_inicio=?, hora_fin=?, duracion=?, aforo_maximo=?, nivel_intensidad=? WHERE id_clase=?"
    SQL_DELETE              = "DELETE FROM clase WHERE id_clase = ?"

    def _rowToVO(self, row) -> ClaseVO:
        id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad = row
        return ClaseVO(id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad)

    def select(self) -> list[ClaseVO]:
        cursor = self.getCursor()
        clases = []
        try:
            cursor.execute(self.SQL_SELECT)
            rows = cursor.fetchall()
            for row in rows:
                clases.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar clases:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return clases

    def selectById(self, id_clase: int) -> ClaseVO:
        cursor = self.getCursor()
        clase = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_clase,))
            row = cursor.fetchone()
            if row:
                clase = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar clase por ID:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return clase

    def selectByEntrenador(self, id_entrenador: int) -> list[ClaseVO]:
        cursor = self.getCursor()
        clases = []
        try:
            cursor.execute(self.SQL_SELECT_BY_ENTRENADOR, (id_entrenador,))
            rows = cursor.fetchall()
            for row in rows:
                clases.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar clases por entrenador:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return clases

    def selectBySala(self, id_sala: int) -> list[ClaseVO]:
        cursor = self.getCursor()
        clases = []
        try:
            cursor.execute(self.SQL_SELECT_BY_SALA, (id_sala,))
            rows = cursor.fetchall()
            for row in rows:
                clases.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar clases por sala:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return clases

    def insert(self, clase: ClaseVO) -> int:
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (
                clase.id_entrenador, clase.id_sala, clase.nombre_actividad,
                clase.calorias_estimadas, clase.dia_semana, clase.hora_inicio,
                clase.hora_fin, clase.duracion, clase.aforo_maximo, clase.nivel_intensidad
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar clase:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return rows

    def update(self, clase: ClaseVO) -> int:
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (
                clase.id_entrenador, clase.id_sala, clase.nombre_actividad,
                clase.calorias_estimadas, clase.dia_semana, clase.hora_inicio,
                clase.hora_fin, clase.duracion, clase.aforo_maximo,
                clase.nivel_intensidad, clase.id_clase
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar clase:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_clase: int) -> int:
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_clase,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar clase:", e)
        finally:
            if cursor:
                cursor.close()
            self.closeConnection()
        return rows