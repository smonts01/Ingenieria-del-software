# Importamos la clase Conexion para poder abrir conexión con la base de datos.
# Los DAO usan esta clase para obtener un cursor y ejecutar consultas SQL.
from src.modelo.conexion.Conexion import Conexion

# Importamos el VO de Administrador.
# El VO sirve para transportar los datos del administrador entre capas.
from src.modelo.VO.AdminitradorVO import AdminitradorVO


class AdministradorDaoJDBC:
    """
    DAO del administrador.
    Responsabilidad:
    - Acceder a la tabla administrador de la base de datos.
    - Ejecutar consultas SELECT e INSERT.
    - Convertir las filas de la base de datos en objetos VO.
    """

    # Consultas SQL al inicio.

    # Recupera todos los administradores.
    SQL_SELECT = """
        SELECT id_administrador
        FROM administrador
    """

    # Recupera un administrador concreto por su ID.
    SQL_SELECT_BY_ID = """
        SELECT id_administrador
        FROM administrador
        WHERE id_administrador = ?
    """

    # Inserta un nuevo administrador.
    SQL_INSERT = """
        INSERT INTO administrador
            (id_administrador)
        VALUES
            (?)
    """

    def __init__(self):
        # Creamos una conexión usando la clase Conexion.
        # Así no repetimos el código de conexión en cada DAO.
        self._conexion = Conexion()

    def _rowToVO(self, row) -> AdminitradorVO:
        """
        Convierte una fila de la base de datos en un objeto VO.
        row[0] corresponde a id_administrador.
        """
        return AdminitradorVO(row[0])

    def select(self) -> list[AdminitradorVO]:
        """
        Recupera todos los administradores de la base de datos.
        Devuelve:
        - Una lista de objetos AdminitradorVO.
        """

        # Pedimos un cursor a la conexión.
        cursor = self._conexion.getCursor()

        # Lista donde se guardarán los administradores recuperados.
        administradores = []

        try:
            # Ejecutamos la consulta SELECT.
            cursor.execute(self.SQL_SELECT)

            # Recorremos las filas y las convertimos a VO.
            for row in cursor.fetchall():
                administradores.append(self._rowToVO(row))

        except Exception as e:
            print("Error al seleccionar administradores:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return administradores

    def selectById(self, id_administrador: int) -> AdminitradorVO:
        """
        Recupera un administrador por su ID.
        Devuelve:
        - AdminitradorVO si existe.
        - None si no se encuentra.
        """

        cursor = self._conexion.getCursor()
        administrador = None

        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_administrador,))

            row = cursor.fetchone()

            if row:
                administrador = self._rowToVO(row)

        except Exception as e:
            print("Error al seleccionar administrador por ID:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return administrador

    def insert(self, vo: AdminitradorVO) -> int:
        """
        Inserta un nuevo administrador en la base de datos.
        Parámetro:
        - vo: objeto AdminitradorVO con el id_administrador.
        Devuelve:
        - Número de filas afectadas.
        """

        cursor = self._conexion.getCursor()
        rows = 0

        try:
            # Insertamos el id del administrador usando los datos del VO
            cursor.execute(self.SQL_INSERT, (vo.id_administrador,))

            # rowcount indica cuántas filas se han insertado
            rows = cursor.rowcount

        except Exception as e:
            print("Error al insertar administrador:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()
        return rows