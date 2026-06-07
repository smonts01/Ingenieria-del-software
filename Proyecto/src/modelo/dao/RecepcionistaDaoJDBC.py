from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.RecepcionistaVO import RecepcionistaVO


class RecepcionistaDaoJDBC:
    """
    DAO para la tabla recepcionista.
    Gestiona los datos específicos del rol recepcionista
    """


    SQL_SELECT = """
        SELECT id_recepcionista, id_administrador_registra
        FROM recepcionista
    """

    SQL_SELECT_BY_ID = """
        SELECT id_recepcionista, id_administrador_registra
        FROM recepcionista
        WHERE id_recepcionista = ?
    """

    SQL_INSERT = """
        INSERT INTO recepcionista
            (id_recepcionista, id_administrador_registra)
        VALUES
            (?, ?)
    """

    SQL_UPDATE = """
        UPDATE recepcionista
        SET id_administrador_registra = ?
        WHERE id_recepcionista = ?
    """


    def __init__(self):
        self._conexion = Conexion()

    # Conversión fila → VO

    def _rowToVO(self, row) -> RecepcionistaVO:
        """Convierte una fila de la BD en un RecepcionistaVO."""
        id_recepcionista, id_administrador_registra = row
        return RecepcionistaVO(
            id_recepcionista=id_recepcionista,
            id_administrador_registra=id_administrador_registra
        )

    # Consultas

    def select(self) -> list:
        """Devuelve todos los recepcionistas como lista de RecepcionistaVO."""
        cursor = self._conexion.getCursor()
        recepcionistas = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                recepcionistas.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar recepcionistas:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return recepcionistas

    def selectById(self, id_recepcionista: int) -> RecepcionistaVO:
        """Devuelve el recepcionista con el ID indicado como RecepcionistaVO,
        o None si no existe."""
        cursor = self._conexion.getCursor()
        recepcionista = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_recepcionista,))
            row = cursor.fetchone()
            if row:
                recepcionista = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar recepcionista por ID:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return recepcionista

    # Añadir

    def insert(self, vo: RecepcionistaVO) -> int:
        """Inserta un nuevo recepcionista a partir de un RecepcionistaVO.
        Devuelve el número de filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(
                self.SQL_INSERT,
                (vo.id_recepcionista, vo.id_administrador_registra)
            )
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar recepcionista:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

    # Modificaciones

    def update(self, vo: RecepcionistaVO) -> int:
        """Actualiza el administrador que registró al recepcionista.
        Devuelve el número de filas afectadas."""
        cursor = self._conexion.getCursor()
        rows = 0
        try:
            cursor.execute(
                self.SQL_UPDATE,
                (vo.id_administrador_registra, vo.id_recepcionista)
            )
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar recepcionista:", e)
        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows

