# Importamos jaydebeapi porque el proyecto usa conexión JDBC con MySQL.
import jaydebeapi


class Conexion:

# Clase base para gestionar la conexión con la base de datos.

    def __init__(
        self,
        host='localhost',
        database='stayfit_database',
        user='root',
        password='250706' # Esta contraseña hay que cambiarla a la de cada persona
    ):
        # Dirección del servidor de base de datos.
        self._host = host

        # Nombre de la base de datos del proyecto.
        self._database = database

        # Usuario de MySQL.
        self._user = user

        # Contraseña de MySQL.
        self._password = password

        self.conexion = self.createConnection()

    def createConnection(self):
        """
        Crea la conexión JDBC con MySQL.
        Devuelve:
        - La conexión si se ha podido crear correctamente.
        - None si ha ocurrido algún error.
        """

        try:
            # Nombre del driver JDBC de MySQL.
            jdbc_driver = "com.mysql.cj.jdbc.Driver"

            # Ruta del archivo .jar del conector JDBC de MySQL.
            jar_file = "lib/mysql-connector-j-9.7.0.jar"

            # Se crea la conexión con la base de datos usando jaydebeapi.
            self.conexion = jaydebeapi.connect(
                jdbc_driver,
                f"jdbc:mysql://{self._host}/{self._database}"
                f"?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC",

                # Credenciales de acceso a MySQL.
                [self._user, self._password],

                # Driver .jar necesario para conectar con MySQL.
                jar_file
            )

            # AutoCommit en True significa que cada INSERT, UPDATE o DELETE
            # se confirma automáticamente en la base de datos.
            self.conexion.jconn.setAutoCommit(True)

            # Devolvemos la conexión creada.
            return self.conexion

        except Exception as e:
            # Si falla la conexión, mostramos el error y devolvemos None.
            print("Error creando conexión:", e)
            return None

    def getCursor(self):
        """
        Devuelve un cursor para ejecutar consultas SQL.
        Los DAO usan este método para hacer SELECT, INSERT, UPDATE o DELETE.
        """

        # Si la conexión no existe, se intenta crear de nuevo.
        if self.conexion is None:
            self.createConnection()

        # Devolvemos el cursor asociado a la conexión.
        return self.conexion.cursor()

    def closeConnection(self):
        """
        Cierra la conexión con la base de datos.
        """

        try:
            # Si hay conexión abierta, se cierra.
            if self.conexion:
                self.conexion.close()

                # Se deja a None para indicar que ya no hay conexión activa.
                self.conexion = None

        except Exception as e:
            # Si ocurre algún error al cerrar, se muestra por consola.
            print("Error cerrando conexión:", e)