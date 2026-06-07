from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.ClaseVO import ClaseVO


class ClaseDaoJDBC:
    """
    DAO para la tabla clase.
    """


    # Columnas comunes a todas las consultas SELECT
    _COLS = ("id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, "
             "dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad")

    # Todas las clases
    SQL_SELECT = f"SELECT {_COLS} FROM clase"

    # Una clase por su ID
    SQL_SELECT_BY_ID = f"SELECT {_COLS} FROM clase WHERE id_clase = ?"

    # Todas las clases de un entrenador
    SQL_SELECT_BY_ENTRENADOR = f"SELECT {_COLS} FROM clase WHERE id_entrenador = ?"

    # Todas las clases de una sala
    SQL_SELECT_BY_SALA = f"SELECT {_COLS} FROM clase WHERE id_sala = ?"

    # Insertar una nueva clase
    SQL_INSERT = (
        "INSERT INTO clase "
        "(id_entrenador, id_sala, nombre_actividad, calorias_estimadas, "
        "dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )

    # Actualizar todos los campos de una clase por su ID
    SQL_UPDATE = (
        "UPDATE clase "
        "SET id_entrenador=?, id_sala=?, nombre_actividad=?, calorias_estimadas=?, "
        "dia_semana=?, hora_inicio=?, hora_fin=?, duracion=?, aforo_maximo=?, nivel_intensidad=? "
        "WHERE id_clase=?"
    )

    # Eliminar una clase por su ID
    SQL_DELETE = "DELETE FROM clase WHERE id_clase = ?"



    def __init__(self):
        self._conexion = Conexion()



    def _rowToVO(self, row) -> ClaseVO:
        """Convierte una fila de la BD en un ClaseVO."""
        (id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas,
         dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad) = row
        return ClaseVO(
            id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas,
            dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad
        )

    # Consultas

    def select(self) -> list:
        """Devuelve todas las clases como lista de ClaseVO."""
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
        """Devuelve la clase con el ID indicado como ClaseVO,
        o None si no existe."""
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

    def selectByEntrenador(self, id_entrenador: int) -> list:
        """Devuelve todas las clases asignadas a un entrenador como lista de ClaseVO."""
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

    def selectBySala(self, id_sala: int) -> list:
        """Devuelve todas las clases programadas en una sala como lista de ClaseVO."""
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

# Añadir

    def insert(self, vo: ClaseVO) -> int:
        """Inserta una nueva clase a partir de un ClaseVO.
        Devuelve el número de filas afectadas."""
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

    # ediciones

    def update(self, vo: ClaseVO) -> int:
        """Actualiza todos los campos de una clase a partir de un ClaseVO.
        Devuelve el número de filas afectadas."""
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

    # Eliminar clase desde admin

    def delete(self, id_clase: int) -> int:
        """Elimina la clase con el ID indicado.
        Devuelve el número de filas afectadas."""
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