from src.modelo.dao.DaoJDBCBase import DaoJDBCBase


class ClaseConsultasDaoJDBC(DaoJDBCBase):

    def buscar_clases(self, texto: str):
        t = f"%{texto.lower().strip()}%"
        return self.consultar("""
            SELECT id_clase, nombre_actividad, dia_semana, hora_inicio,
                   hora_fin, aforo_maximo, nivel_intensidad, calorias_estimadas
            FROM clase
            WHERE LOWER(nombre_actividad) LIKE ?
            ORDER BY nombre_actividad
        """, (t,))

    def ocupacion_clases(self):
        return self.consultar("""
            SELECT c.id_clase, c.nombre_actividad,
                   COUNT(i.id_inscripcion) AS inscritos, c.aforo_maximo,
                   ROUND(COUNT(i.id_inscripcion)*100.0/c.aforo_maximo,1) AS pct
            FROM clase c
            LEFT JOIN inscripcion i ON c.id_clase=i.id_clase AND i.estado='inscrito'
            GROUP BY c.id_clase, c.nombre_actividad, c.aforo_maximo
            ORDER BY pct DESC
        """)

    def clases_entrenador_tabla(self, id_entrenador):
        return self.consultar("""
            SELECT c.nombre_actividad,
                   s.nombre AS sala,
                   CONCAT(c.hora_inicio, ' - ', c.hora_fin) AS horario,
                   c.dia_semana,
                   CONCAT(COUNT(i.id_inscripcion), '/', c.aforo_maximo) AS capacidad
            FROM clase c
            INNER JOIN sala s ON c.id_sala = s.id_sala
            LEFT JOIN inscripcion i
                ON c.id_clase = i.id_clase
                AND i.estado = 'inscrito'
            WHERE c.id_entrenador = ?
            GROUP BY c.id_clase,
                     c.nombre_actividad,
                     s.nombre,
                     c.hora_inicio,
                     c.hora_fin,
                     c.dia_semana,
                     c.aforo_maximo
            ORDER BY c.hora_inicio
        """, (id_entrenador,))

    def ocupacion_clases_entrenador(self, id_entrenador):
        return self.consultar("""
            SELECT c.id_clase,
                   c.nombre_actividad,
                   COUNT(i.id_inscripcion) AS inscritos,
                   c.aforo_maximo,
                   CAST(COUNT(i.id_inscripcion) * 100.0 / c.aforo_maximo AS DECIMAL(5,2)) AS ocupacion
            FROM clase c
            LEFT JOIN inscripcion i
                ON c.id_clase = i.id_clase
                AND i.estado = 'inscrito'
            WHERE c.id_entrenador = ?
            GROUP BY c.id_clase,
                     c.nombre_actividad,
                     c.aforo_maximo
            ORDER BY ocupacion DESC
        """, (id_entrenador,))

    def informacion_clase_con_sala(self, id_clase):
        datos = self.consultar("""
            SELECT c.nombre_actividad,
                   s.nombre,
                   c.dia_semana,
                   c.hora_inicio,
                   c.hora_fin,
                   c.aforo_maximo
            FROM clase c
            INNER JOIN sala s ON c.id_sala = s.id_sala
            WHERE c.id_clase = ?
        """, (id_clase,))
        return datos[0] if datos else None

    def buscar_clase(self, id_clase):
        datos = self.consultar("""
            SELECT id_clase,
                   id_entrenador,
                   id_sala,
                   nombre_actividad,
                   calorias_estimadas,
                   dia_semana,
                   hora_inicio,
                   hora_fin,
                   duracion,
                   aforo_maximo,
                   nivel_intensidad
            FROM clase
            WHERE id_clase = ?
        """, (id_clase,))
        return datos[0] if datos else None

    def recepcion_clases_hoy(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM clase
            WHERE LOWER(dia_semana) = LOWER(
                CASE DAYOFWEEK(CURDATE())
                    WHEN 1 THEN 'domingo'
                    WHEN 2 THEN 'lunes'
                    WHEN 3 THEN 'martes'
                    WHEN 4 THEN 'miércoles'
                    WHEN 5 THEN 'jueves'
                    WHEN 6 THEN 'viernes'
                    WHEN 7 THEN 'sábado'
                END
            )
        """)
        return datos[0][0] if datos else 0
