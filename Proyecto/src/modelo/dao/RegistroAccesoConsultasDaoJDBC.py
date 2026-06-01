from src.modelo.dao.DaoJDBCBase import DaoJDBCBase


class RegistroAccesoConsultasDaoJDBC(DaoJDBCBase):

    def recepcion_entradas_hoy(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM registro_acceso
            WHERE tipo_acceso = 'entrada'
            AND DATE(fecha_hora_registro) = CURDATE()
        """)
        return datos[0][0] if datos else 0

    def recepcion_ultimos_registros_acceso(self):
        return self.consultar("""
            SELECT u.nombre,
                   u.dni,
                   r.tipo_acceso,
                   r.fecha_hora_registro
            FROM registro_acceso r
            JOIN usuarios u ON r.id_usuario = u.id_usuario
            ORDER BY r.fecha_hora_registro DESC
            LIMIT 8
        """)

    def ultimo_acceso_cliente(self, id_usuario):
        datos = self.consultar("""
            SELECT tipo_acceso
            FROM registro_acceso
            WHERE id_usuario = ?
            ORDER BY fecha_hora_registro DESC
            LIMIT 1
        """, (id_usuario,))
        return datos[0][0] if datos else None

    def listar_ultimos_accesos_control(self):
        return self.consultar("""
            SELECT u.nombre,
                   u.dni,
                   r.tipo_acceso,
                   r.fecha_hora_registro
            FROM registro_acceso r
            INNER JOIN usuarios u ON r.id_usuario = u.id_usuario
            ORDER BY r.fecha_hora_registro DESC
            LIMIT 20
        """)
