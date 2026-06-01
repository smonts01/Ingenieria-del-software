from src.modelo.dao.DaoJDBCBase import DaoJDBCBase


class EmpleadoConsultasDaoJDBC(DaoJDBCBase):

    def contar_por_rol(self, nombre_rol: str):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol
            WHERE LOWER(r.nombre_rol) = ?
        """, (nombre_rol.lower(),))
        return datos[0][0] if datos else 0

    def listar_trabajadores_completo(self):
        return self.consultar("""
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, r.nombre_rol, u.direccion, u.fecha_nacimiento
            FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol
            WHERE r.nombre_rol IN ('entrenador','recepcionista','contable','administrador')
            ORDER BY r.nombre_rol, u.nombre
        """)

    def buscar_trabajadores(self, texto: str):
        t = f"%{texto.lower().strip()}%"
        return self.consultar("""
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, r.nombre_rol, u.direccion, u.fecha_nacimiento
            FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol
            WHERE r.nombre_rol IN ('entrenador','recepcionista','contable','administrador')
              AND (LOWER(u.nombre) LIKE ? OR LOWER(u.username) LIKE ?
                   OR LOWER(u.dni) LIKE ?)
            ORDER BY u.nombre
        """, (t, t, t))

    def buscar_trabajadores_rol(self, rol: str):
        return self.consultar("""
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, r.nombre_rol, u.direccion, u.fecha_nacimiento
            FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol
            WHERE LOWER(r.nombre_rol) = ?
            ORDER BY u.nombre
        """, (rol.lower(),))


    def contable_salarios_personal(self):
        return self.consultar("""
            SELECT u.nombre,
                   r.nombre_rol,
                   CONCAT(e.salario, ' €') AS salario
            FROM empleados e
            INNER JOIN usuarios u ON e.id_empleado = u.id_usuario
            INNER JOIN roles r ON u.id_rol = r.id_rol
            ORDER BY r.nombre_rol, u.nombre
        """)
