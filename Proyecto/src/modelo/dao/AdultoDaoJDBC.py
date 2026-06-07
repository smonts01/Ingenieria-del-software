# Importamos la clase Conexion para poder abrir conexión con la base de datos.
# Los DAO usan esta clase para obtener un cursor y ejecutar consultas SQL.
from src.modelo.conexion.Conexion import Conexion

# Importamos el VO de Adulto.
# El VO sirve para transportar los datos de un cliente adulto entre capas.
from src.modelo.VO.AdultoVO import AdultoVO


class AdultoDaoJDBC:
    """
    DAO de Adulto.
    Responsabilidad:
    - Acceder a la tabla adulto de la base de datos.
    - Ejecutar consultas SELECT e INSERT.
    - Convertir las filas de la base de datos en objetos AdultoVO.
    
    Adulto esta dentro de cliente, es decir es un tipo de cliente pero mayor de edad
    """

    # Consultas SQL al inicio.

    # Recupera todos los clientes adultos.
    SQL_SELECT = """
        SELECT id_cliente
        FROM adulto
    """

    # Recupera un cliente adulto concreto por su ID.
    SQL_SELECT_BY_ID = """
        SELECT id_cliente
        FROM adulto
        WHERE id_cliente = ?
    """

    # Inserta un nuevo registro en la tabla adulto.
    SQL_INSERT = """
        INSERT INTO adulto
            (id_cliente)
        VALUES
            (?)
    """

    def __init__(self):
        # Creamos una conexión usando la clase Conexion.
        self._conexion = Conexion()

    def _rowToVO(self, row) -> AdultoVO:
        """
        Convierte una fila de la base de datos en un objeto AdultoVO.
        row[0] corresponde a id_cliente.
        """
        return AdultoVO(row[0])

    def select(self) -> list[AdultoVO]:
        """
        Recupera todos los adultos de la base de datos.
        Devuelve:
        - Una lista de objetos AdultoVO.
        """

        # Pedimos un cursor a la conexión.
        # El cursor permite ejecutar consultas SQL.
        cursor = self._conexion.getCursor()

        # Lista donde se guardarán los adultos recuperados.
        adultos = []

        try:
            # Ejecutamos la consulta SELECT.
            cursor.execute(self.SQL_SELECT)

            # Recorremos todas las filas devueltas por la consulta.
            for row in cursor.fetchall():

                # Convertimos cada fila en VO y la añadimos a la lista.
                adultos.append(self._rowToVO(row))

        except Exception as e:
            # Si ocurre un error, se muestra por consola.
            print("Error al seleccionar adultos:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        # Devolvemos la lista de adultos.
        return adultos

    def selectById(self, id_cliente: int) -> AdultoVO:
        """
        Recupera un adulto por su ID de cliente.
        Parámetro:
        - id_cliente: identificador del cliente.
        Devuelve:
        - AdultoVO si existe.
        - None si no se encuentra.
        """

        cursor = self._conexion.getCursor()
        adulto = None

        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_cliente,))

            # Obtenemos una única fila.
            row = cursor.fetchone()

            # Si existe resultado, lo convertimos a VO.
            if row:
                adulto = self._rowToVO(row)

        except Exception as e:
            print("Error al seleccionar adulto por ID:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return adulto

    def insert(self, vo: AdultoVO) -> int:
        """
        Inserta un nuevo adulto en la base de datos.
        Parámetro:
        - vo: objeto AdultoVO con el id_cliente.
        Devuelve:
        - Número de filas afectadas.
        """

        cursor = self._conexion.getCursor()
        rows = 0

        try:
            # Insertamos el id del cliente adulto usando el VO.
            cursor.execute(self.SQL_INSERT, (vo.id_cliente,))

            # rowcount indica cuántas filas se han añasido
            rows = cursor.rowcount

        except Exception as e:
            print("Error al insertar adulto:", e)

        finally:
            cursor.close()
            self._conexion.closeConnection()

        return rows