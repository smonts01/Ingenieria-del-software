from src.modelo.dao.DaoJDBCBase import DaoJDBCBase


class InscripcionConsultasDaoJDBC(DaoJDBCBase):

    def buscar_inscripciones(self, texto: str):
        t = f"%{texto.lower().strip()}%"
        return self.consultar("""
            SELECT u.nombre,
                   c.nombre_actividad,
                   i.fecha_inscripcion,
                   i.estado
            FROM inscripcion i
            JOIN usuarios u ON i.id_cliente = u.id_usuario
            JOIN clase c ON i.id_clase = c.id_clase
            WHERE i.estado = 'inscrito'
              AND (
                    LOWER(u.nombre) LIKE ?
                 OR LOWER(c.nombre_actividad) LIKE ?
                 OR LOWER(i.estado) LIKE ?
              )
            ORDER BY i.fecha_inscripcion DESC
        """, (t, t, t))

    def contar_inscripciones_clase(self, nombre_actividad: str):
        t = f"%{nombre_actividad.lower().strip()}%"
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM inscripcion i
            JOIN clase c ON i.id_clase = c.id_clase
            WHERE LOWER(c.nombre_actividad) LIKE ? AND i.estado = 'inscrito'
        """, (t,))
        return datos[0][0] if datos else 0

    def clases_inscritas_cliente(self, id_cliente: int):
        return self.consultar("""
            SELECT c.id_clase, c.nombre_actividad, c.dia_semana,
                   c.hora_inicio, c.hora_fin, c.nivel_intensidad
            FROM inscripcion i JOIN clase c ON i.id_clase = c.id_clase
            WHERE i.id_cliente = ? AND i.estado = 'inscrito'
            ORDER BY c.dia_semana
        """, (id_cliente,))

    def clientes_inscritos_clase(self, id_clase: int):
        return self.consultar("""
            SELECT u.id_usuario,
                   u.nombre,
                   u.telefono,
                   u.email
            FROM inscripcion i
            INNER JOIN usuarios u ON i.id_cliente = u.id_usuario
            WHERE i.id_clase = ?
              AND i.estado = 'inscrito'
            ORDER BY u.nombre
        """, (id_clase,))

    def listar_inscripciones_resumen(self):
        return self.consultar("""
            SELECT u.nombre, c.nombre_actividad, i.fecha_inscripcion, i.estado
            FROM inscripcion i
            JOIN usuarios u ON i.id_cliente = u.id_usuario
            JOIN clase c ON i.id_clase = c.id_clase
            WHERE i.estado = 'inscrito'
            ORDER BY i.fecha_inscripcion DESC LIMIT 50
        """)

    def estadisticas_inscripciones(self):
        total_r = self.consultar("SELECT COUNT(*) FROM inscripcion WHERE estado='inscrito'")
        mas_r = self.consultar("""
            SELECT c.nombre_actividad, COUNT(*) n FROM inscripcion i
            JOIN clase c ON i.id_clase=c.id_clase
            WHERE i.estado='inscrito' GROUP BY c.nombre_actividad ORDER BY n DESC LIMIT 1
        """)
        menos_r = self.consultar("""
            SELECT c.nombre_actividad, COUNT(*) n FROM inscripcion i
            JOIN clase c ON i.id_clase=c.id_clase
            WHERE i.estado='inscrito' GROUP BY c.nombre_actividad ORDER BY n ASC LIMIT 1
        """)
        ocup_r = self.consultar("""
            SELECT ROUND(AVG(pct),1) FROM (
                SELECT COUNT(i.id_inscripcion)*100.0/c.aforo_maximo pct
                FROM clase c LEFT JOIN inscripcion i
                ON c.id_clase=i.id_clase AND i.estado='inscrito'
                GROUP BY c.id_clase, c.aforo_maximo) t
        """)
        return {
            "total": total_r[0][0] if total_r else 0,
            "clase_mas": mas_r[0][0] if mas_r else "-",
            "num_mas": mas_r[0][1] if mas_r else 0,
            "clase_menos": menos_r[0][0] if menos_r else "-",
            "num_menos": menos_r[0][1] if menos_r else 0,
            "ocupacion": ocup_r[0][0] if ocup_r and ocup_r[0][0] else 0,
        }
