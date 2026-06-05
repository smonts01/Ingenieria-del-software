from src.modelo.dao.DaoJDBCBase import DaoJDBCBase
 
 
class InscripcionConsultasDaoJDBC(DaoJDBCBase):
 
    SQL_BUSCAR_INSCRIPCIONES = """
        SELECT u.nombre, c.nombre_actividad, i.fecha_inscripcion, i.estado
        FROM inscripcion i
        JOIN usuarios u ON i.id_cliente = u.id_usuario
        JOIN clase c ON i.id_clase = c.id_clase
        WHERE i.estado = 'inscrito'
          AND (LOWER(u.nombre) LIKE ? OR LOWER(c.nombre_actividad) LIKE ?
               OR LOWER(i.estado) LIKE ?)
        ORDER BY i.fecha_inscripcion DESC
    """
 
    SQL_CONTAR_INSCRIPCIONES_CLASE = """
        SELECT COUNT(*)
        FROM inscripcion i
        JOIN clase c ON i.id_clase = c.id_clase
        WHERE LOWER(c.nombre_actividad) LIKE ? AND i.estado = 'inscrito'
    """
 
    SQL_CLASES_INSCRITAS_CLIENTE = """
        SELECT c.id_clase, c.nombre_actividad, c.dia_semana,
               c.hora_inicio, c.hora_fin, c.nivel_intensidad
        FROM inscripcion i JOIN clase c ON i.id_clase = c.id_clase
        WHERE i.id_cliente = ? AND i.estado = 'inscrito'
        ORDER BY c.dia_semana
    """
 
    SQL_CLIENTES_INSCRITOS_CLASE = """
        SELECT u.id_usuario, u.nombre, u.telefono, u.email
        FROM inscripcion i
        INNER JOIN usuarios u ON i.id_cliente = u.id_usuario
        WHERE i.id_clase = ? AND i.estado = 'inscrito'
        ORDER BY u.nombre
    """
 
    SQL_LISTAR_INSCRIPCIONES_RESUMEN = """
        SELECT u.nombre, c.nombre_actividad, i.fecha_inscripcion, i.estado
        FROM inscripcion i
        JOIN usuarios u ON i.id_cliente = u.id_usuario
        JOIN clase c ON i.id_clase = c.id_clase
        WHERE i.estado = 'inscrito'
        ORDER BY i.fecha_inscripcion DESC
        LIMIT 50
    """
 
    SQL_TOTAL_INSCRITAS = "SELECT COUNT(*) FROM inscripcion WHERE estado='inscrito'"
 
    SQL_CLASE_MAS_INSCRITA = """
        SELECT c.nombre_actividad, COUNT(*) n
        FROM inscripcion i JOIN clase c ON i.id_clase = c.id_clase
        WHERE i.estado = 'inscrito'
        GROUP BY c.nombre_actividad ORDER BY n DESC LIMIT 1
    """
 
    SQL_CLASE_MENOS_INSCRITA = """
        SELECT c.nombre_actividad, COUNT(*) n
        FROM inscripcion i JOIN clase c ON i.id_clase = c.id_clase
        WHERE i.estado = 'inscrito'
        GROUP BY c.nombre_actividad ORDER BY n ASC LIMIT 1
    """
 
    SQL_OCUPACION_MEDIA = """
        SELECT ROUND(AVG(pct), 1)
        FROM (
            SELECT COUNT(i.id_inscripcion) * 100.0 / c.aforo_maximo AS pct
            FROM clase c
            LEFT JOIN inscripcion i ON c.id_clase = i.id_clase AND i.estado = 'inscrito'
            GROUP BY c.id_clase, c.aforo_maximo
        ) t
    """
 
    def buscar_inscripciones(self, texto: str):
        t = f"%{texto.lower().strip()}%"
        return self.consultar(self.SQL_BUSCAR_INSCRIPCIONES, (t, t, t))
 
    def contar_inscripciones_clase(self, nombre_actividad: str):
        t = f"%{nombre_actividad.lower().strip()}%"
        datos = self.consultar(self.SQL_CONTAR_INSCRIPCIONES_CLASE, (t,))
        return datos[0][0] if datos else 0
 
    def clases_inscritas_cliente(self, id_cliente: int):
        return self.consultar(self.SQL_CLASES_INSCRITAS_CLIENTE, (id_cliente,))
 
    def clientes_inscritos_clase(self, id_clase: int):
        return self.consultar(self.SQL_CLIENTES_INSCRITOS_CLASE, (id_clase,))
 
    def listar_inscripciones_resumen(self):
        return self.consultar(self.SQL_LISTAR_INSCRIPCIONES_RESUMEN)
 
    def estadisticas_inscripciones(self):
        total_r  = self.consultar(self.SQL_TOTAL_INSCRITAS)
        mas_r    = self.consultar(self.SQL_CLASE_MAS_INSCRITA)
        menos_r  = self.consultar(self.SQL_CLASE_MENOS_INSCRITA)
        ocup_r   = self.consultar(self.SQL_OCUPACION_MEDIA)
        return {
            "total":       total_r[0][0]  if total_r                     else 0,
            "clase_mas":   mas_r[0][0]    if mas_r                       else "-",
            "num_mas":     mas_r[0][1]    if mas_r                       else 0,
            "clase_menos": menos_r[0][0]  if menos_r                     else "-",
            "num_menos":   menos_r[0][1]  if menos_r                     else 0,
            "ocupacion":   ocup_r[0][0]   if ocup_r and ocup_r[0][0]    else 0,
        }