from src.modelo.dao.DaoJDBCBase import DaoJDBCBase
 
 
class EmpleadoConsultasDaoJDBC(DaoJDBCBase):
 
    SQL_CONTAR_POR_ROL = """
        SELECT COUNT(*)
        FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol
        WHERE LOWER(r.nombre_rol) = ?
    """
 
    SQL_LISTAR_TRABAJADORES_COMPLETO = """
        SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
               u.username, r.nombre_rol, u.direccion, u.fecha_nacimiento
        FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol
        WHERE r.nombre_rol IN ('entrenador','recepcionista','contable','administrador')
        ORDER BY r.nombre_rol, u.nombre
    """
 
    SQL_BUSCAR_TRABAJADORES = """
        SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
               u.username, r.nombre_rol, u.direccion, u.fecha_nacimiento
        FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol
        WHERE r.nombre_rol IN ('entrenador','recepcionista','contable','administrador')
          AND (LOWER(u.nombre) LIKE ? OR LOWER(u.username) LIKE ?
               OR LOWER(u.dni) LIKE ?)
        ORDER BY u.nombre
    """
 
    SQL_BUSCAR_TRABAJADORES_ROL = """
        SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
               u.username, r.nombre_rol, u.direccion, u.fecha_nacimiento
        FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol
        WHERE LOWER(r.nombre_rol) = ?
        ORDER BY u.nombre
    """
 
    SQL_SALARIOS_PERSONAL = """
        SELECT u.nombre,
               r.nombre_rol,
               CONCAT(e.salario, ' €') AS salario
        FROM empleados e
        INNER JOIN usuarios u ON e.id_empleado = u.id_usuario
        INNER JOIN roles r ON u.id_rol = r.id_rol
        ORDER BY r.nombre_rol, u.nombre
    """
 
    def contar_por_rol(self, nombre_rol: str):
        datos = self.consultar(self.SQL_CONTAR_POR_ROL, (nombre_rol.lower(),))
        return datos[0][0] if datos else 0
 
    def listar_trabajadores_completo(self):
        return self.consultar(self.SQL_LISTAR_TRABAJADORES_COMPLETO)
 
    def buscar_trabajadores(self, texto: str):
        t = f"%{texto.lower().strip()}%"
        return self.consultar(self.SQL_BUSCAR_TRABAJADORES, (t, t, t))
 
    def buscar_trabajadores_rol(self, rol: str):
        return self.consultar(self.SQL_BUSCAR_TRABAJADORES_ROL, (rol.lower(),))
 
    def contable_salarios_personal(self):
        return self.consultar(self.SQL_SALARIOS_PERSONAL)