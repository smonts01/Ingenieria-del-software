from src.modelo.dao.DaoJDBCBase import DaoJDBCBase


class UsuarioConsultasDaoJDBC(DaoJDBCBase):

    SQL_PERFIL = ("SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email, u.username, r.nombre_rol, u.direccion, u.fecha_registro, u.fecha_nacimiento "
                "FROM usuarios u "
                "INNER JOIN roles r ON u.id_rol = r.id_rol "
                "WHERE u.id_usuario = ?")

    SQL_RECEPCION = ("SELECT COUNT(*) "
                    "FROM usuarios "
                    "WHERE DATE(fecha_registro) = CURDATE()")

    def perfil_usuario(self, id_usuario: int):
        datos = self.consultar(self.SQL_PERFIL, (id_usuario,))
        return datos[0] if datos else None

    def recepcion_nuevos_usuarios_hoy(self):
        datos = self.consultar(self.SQL_RECEPCION)
        return datos[0][0] if datos else 0
