from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.EntrenadorVO import EntrenadorVO


class EntrenadorDaoJDBC:

    # Consulta todos los entrenadores de la tabla entrenador
    SQL_SELECT = """
        SELECT id_entrenador, id_administrador_registra
        FROM entrenador
    """

    # Consulta un entrenador concreto usando su id
    SQL_SELECT_BY_ID = """
        SELECT id_entrenador, id_administrador_registra
        FROM entrenador
        WHERE id_entrenador = ?
    """

    # Inserta un nuevo entrenador en la tabla
    # Los interrogantes se rellenan luego con los valores del VO
    SQL_INSERT = """
        INSERT INTO entrenador
            (id_entrenador, id_administrador_registra)
        VALUES
            (?, ?)
    """

    # Actualiza el administrador que registró al entrenador
    # El WHERE indica qué entrenador concreto se modifica
    SQL_UPDATE = """
        UPDATE entrenador
        SET id_administrador_registra = ?
        WHERE id_entrenador = ?
    """

    # Elimina un entrenador por su id
    SQL_DELETE = """
        DELETE FROM entrenador
        WHERE id_entrenador = ?
    """

    def __init__(self):
        # Crea una conexión con la base de datos
        # A través de esta conexión se obtiene el cursor para ejecutar SQL
        self._conexion = Conexion()  

    def _rowToVO(self, row) -> EntrenadorVO:
        # Convierte una fila de la base de datos en un objeto EntrenadorVO

        # Desempaqueto la fila recibida de la BD.
        id_entrenador, id_administrador_registra = row

        # Creo y devuelvo un VO con los datos de esa fila
        return EntrenadorVO(
            id_entrenador=id_entrenador,
            id_administrador_registra=id_administrador_registra
        )

    def select(self) -> list[EntrenadorVO]:
        cursor = self._conexion.getCursor()
        entrenadores = []

        try:
            # Ejecuta la consulta que selecciona todos los entrenadores
            cursor.execute(self.SQL_SELECT)

            for row in cursor.fetchall():
                # Cada fila se convierte en un EntrenadorVO
                entrenadores.append(self._rowToVO(row))

        except Exception as e:
            print("Error al seleccionar entrenadores:", e)

        finally:
            # Siempre se cierra el cursor y la conexión
            cursor.close()
            self._conexion.closeConnection()

        # Devuelve la lista de entrenadores

        return entrenadores

    def selectById(self, id_entrenador: int) -> EntrenadorVO:
        #Busca un entrenador concreto por su id

        cursor = self._conexion.getCursor()
        entrenador = None

        try:
            # El parámetro id_entrenador sustituye al ? del SQL_SELECT_BY_ID.
            cursor.execute(self.SQL_SELECT_BY_ID, (id_entrenador,))
            row = cursor.fetchone()

            if row:
                entrenador = self._rowToVO(row)

        except Exception as e:
            print("Error al seleccionar entrenador por ID:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return entrenador

    def insert(self, vo: EntrenadorVO) -> int:
        #Inserta un nuevo entrenador en la base de datos

        cursor = self._conexion.getCursor()
        rows = 0

        try:
            # Los valores del VO sustituyen a los ? del SQL_INSERT
            cursor.execute(self.SQL_INSERT, (vo.id_entrenador, vo.id_administrador_registra))

            rows = cursor.rowcount

        except Exception as e:
            print("Error al insertar entrenador:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows

    def update(self, vo: EntrenadorVO) -> int:
        #Actualiza un entrenador existente

        cursor = self._conexion.getCursor()
        rows = 0

        try:
            #id_administrador_registra para el SET
            #id_entrenador para el WHERE
            cursor.execute(self.SQL_UPDATE, (vo.id_administrador_registra,vo.id_entrenador))

            rows = cursor.rowcount

        except Exception as e:
            print("Error al actualizar entrenador:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows

    def delete(self, id_entrenador: int) -> int:
        #Elimina un entrenador de la base de datos por su id
        cursor = self._conexion.getCursor()
        rows = 0

        try:
            cursor.execute(self.SQL_DELETE, (id_entrenador,))
            rows = cursor.rowcount

        except Exception as e:
            print("Error al eliminar entrenador:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows