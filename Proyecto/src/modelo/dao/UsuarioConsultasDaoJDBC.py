from src.modelo.dao.DaoJDBCBase import DaoJDBCBase


class UsuarioConsultasDaoJDBC(DaoJDBCBase):

    def perfil_usuario(self, id_usuario: int):
        sql = """
            SELECT u.id_usuario,
                   u.dni,
                   u.nombre,
                   u.telefono,
                   u.email,
                   u.username,
                   r.nombre_rol,
                   u.direccion,
                   u.fecha_registro,
                   u.fecha_nacimiento
            FROM usuarios u
            INNER JOIN roles r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = ?
        """
        datos = self.consultar(sql, (id_usuario,))
        return datos[0] if datos else None

    def recepcion_nuevos_usuarios_hoy(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM usuarios
            WHERE DATE(fecha_registro) = CURDATE()
        """)
        return datos[0][0] if datos else 0
