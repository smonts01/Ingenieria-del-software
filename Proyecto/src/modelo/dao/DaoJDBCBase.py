from src.modelo.conexion.Conexion import Conexion


class DaoJDBCBase:
    """Base común para DAOs de consultas complejas.

        Centraliza las operaciones SQL auxiliares para los DAO del proyecto.
    """

    def __init__(self):
        self._conexion = Conexion()

    def consultar(self, sql, parametros=()):
        cursor = self._conexion.getCursor()
        try:
            cursor.execute(sql, parametros)
            return cursor.fetchall()
        finally:
            cursor.close()

    def ejecutar(self, sql, parametros=()):
        cursor = self._conexion.getCursor()
        try:
            cursor.execute(sql, parametros)
            try:
                self._conexion.conexion.commit()
            except Exception:
                pass
            return cursor.rowcount
        finally:
            cursor.close()
    
    def closeConnection(self):
        self._conexion.closeConnection()
