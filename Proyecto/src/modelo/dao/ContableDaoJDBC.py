from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.ContableVO import ContableVO


class ContableDaoJDBC:

    # Selecciona todos los contables de la tabla.
    SQL_SELECT = """
        SELECT id_contable, id_administrador_registra
        FROM contable
    """

    # Selecciona un contable concreto por su id.
    SQL_SELECT_BY_ID = """
        SELECT id_contable, id_administrador_registra
        FROM contable
        WHERE id_contable = ?
    """

    # Inserta un nuevo contable.
    # Los ? se sustituyen después por los valores del VO.
    SQL_INSERT = """
        INSERT INTO contable
            (id_contable, id_administrador_registra)
        VALUES
            (?, ?)
    """
    
    # Actualiza el administrador que registró a un contable.
    # El WHERE indica qué contable se modifica.
    SQL_UPDATE = """
        UPDATE contable
        SET id_administrador_registra = ?
        WHERE id_contable = ?
    """

    # Elimina un contable por su id.
    SQL_DELETE = """
        DELETE FROM contable
        WHERE id_contable = ?
    """

    def __init__(self):
        # Crea la conexión con la base de datos.
        # Desde esta conexión se obtiene el cursor para ejecutar consultas SQL.
        self._conexion = Conexion()  

    def _rowToVO(self, row) -> ContableVO:
        #Convierte una fila de la base de datos en un objeto ContableVO

        # Separo los valores de la fila recibida desde la BD
        id_contable, id_administrador_registra = row

        # Creo y devuelvo el VO con esos datos
        return ContableVO(id_contable, id_administrador_registra)

    
    #Devuelve todos los contables de la base de datos
    def select(self) -> list[ContableVO]:

        cursor = self._conexion.getCursor()
        contables = []

        try:
            # Ejecuta la consulta que trae todos los contables
            cursor.execute(self.SQL_SELECT)

            for row in cursor.fetchall():
                # Cada fila se convierte en un ContableVO
                contables.append(self._rowToVO(row))

        except Exception as e:
            print("Error al seleccionar contables:", e)

        finally:
            # Cerramos cursor y conexión para liberar recursos
            cursor.close()
            self._conexion.closeConnection()

        return contables


    #Busca un contable por su id
    def selectById(self, id_contable: int):
        cursor = self._conexion.getCursor()
        contable = None

        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_contable,))
            row = cursor.fetchone()

            if row:
                contable = self._rowToVO(row)

        except Exception as e:
            print("Error al seleccionar contable por ID:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return contable


    #Inserta un nuevo contable en la base de datos
    def insert(self, vo: ContableVO) -> int:

        #Recibe un ContableVO con los datos a insertar
        cursor = self._conexion.getCursor()
        rows = 0

        try:
            # Los valores del VO sustituyen a los ? del SQL_INSERT
            cursor.execute(
                self.SQL_INSERT,
                (
                    vo.id_contable,
                    vo.id_administrador_registra
                )
            )
            rows = cursor.rowcount

        except Exception as e:
            print("Error al insertar contable:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows

    def update(self, vo: ContableVO) -> int:
        #Actualiza un contable existente

        cursor = self._conexion.getCursor()
        rows = 0

        try:
            cursor.execute(
                self.SQL_UPDATE,
                (
                    vo.id_administrador_registra,
                    vo.id_contable
                )
            )
            rows = cursor.rowcount

        except Exception as e:
            print("Error al actualizar contable:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows

    def delete(self, id_contable: int) -> int:
        #Elimina un contable por su id

        cursor = self._conexion.getCursor()
        rows = 0

        try:
            # El id_contable sustituye al ? del SQL_DELETE
            cursor.execute(self.SQL_DELETE, (id_contable,))
            rows = cursor.rowcount

        except Exception as e:
            print("Error al eliminar contable:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows