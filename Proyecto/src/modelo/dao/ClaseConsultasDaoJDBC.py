from src.modelo.dao.DaoJDBCBase import DaoJDBCBase
from src.modelo.VO.ClaseVO import ClaseVO
from src.modelo.VO.OcupacionClaseVO import OcupacionClaseVO
from src.modelo.VO.ClaseEntrenadorVO import ClaseEntrenadorVO


class ClaseConsultasDaoJDBC(DaoJDBCBase):

    SQL_BUSCAR_CLASES = ("SELECT id_clase, nombre_actividad, dia_semana, hora_inicio, hora_fin, aforo_maximo, nivel_intensidad, calorias_estimadas "
                         "FROM clase "
                         "WHERE LOWER(nombre_actividad) LIKE ? "
                         "ORDER BY nombre_actividad")

    SQL_OCUPACION_CLASE = ("SELECT c.id_clase, c.nombre_actividad, COUNT(i.id_inscripcion) AS inscritos, c.aforo_maximo, ROUND(COUNT(i.id_inscripcion)*100.0/c.aforo_maximo,1) AS pct "
                           "FROM clase c "
                           "LEFT JOIN inscripcion i ON c.id_clase=i.id_clase AND i.estado='inscrito' "
                           "GROUP BY c.id_clase, c.nombre_actividad, c.aforo_maximo "
                           "ORDER BY pct DESC")

    SQL_CLASES_ENTRENADOR_TABLA = ("SELECT c.nombre_actividad, "
                                    "s.nombre AS sala, "
                                    "CONCAT(TIME_FORMAT(c.hora_inicio, '%H:%i'), ' - ', TIME_FORMAT(c.hora_fin, '%H:%i')) AS horario, "
                                    "c.dia_semana, "
                                    "CONCAT(COUNT(i.id_inscripcion), '/', c.aforo_maximo) AS capacidad "
                                    "FROM clase c "
                                    "INNER JOIN sala s ON c.id_sala = s.id_sala "
                                    "LEFT JOIN inscripcion i "
                                    "ON c.id_clase = i.id_clase "
                                    "AND i.estado = 'inscrito' "
                                    "WHERE c.id_entrenador = ? "
                                    "GROUP BY c.id_clase, c.nombre_actividad, s.nombre, c.hora_inicio, c.hora_fin, c.dia_semana, c.aforo_maximo "
                                    "ORDER BY FIELD(c.dia_semana, 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'), c.hora_inicio")


    SQL_OCUPACION = ("SELECT c.id_clase, c.nombre_actividad, COUNT(i.id_inscripcion) AS inscritos, c.aforo_maximo, CAST(COUNT(i.id_inscripcion) * 100.0 / c.aforo_maximo AS DECIMAL(5,2)) AS ocupacion "
                     "FROM clase c "
                     "LEFT JOIN inscripcion i "
                     "ON c.id_clase = i.id_clase "
                     "AND i.estado = 'inscrito' "
                     "WHERE c.id_entrenador = ? "
                     "GROUP BY c.id_clase, c.nombre_actividad, c.aforo_maximo "
                     "ORDER BY ocupacion DESC")

    SQL_INFORMACION_SALA = ("SELECT c.nombre_actividad, s.nombre, c.dia_semana, c.hora_inicio, c.hora_fin, c.aforo_maximo "
                            "FROM clase c "
                            "INNER JOIN sala s ON c.id_sala = s.id_sala "
                            "WHERE c.id_clase = ?")

    SQL_BUSCAR_CLASE = ("SELECT id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad "
                        "FROM clase "
                        "WHERE id_clase = ?")

    SQL_RECEPCION_CLASES_HOY = ("SELECT COUNT(*) "
                                "FROM clase "
                                "WHERE LOWER(dia_semana) = LOWER( "
                                "CASE DAYOFWEEK(CURDATE()) "
                                "WHEN 1 THEN 'domingo' "
                                "WHEN 2 THEN 'lunes' "
                                "WHEN 3 THEN 'martes' "
                                "WHEN 4 THEN 'miércoles' "
                                "WHEN 5 THEN 'jueves' "
                                "WHEN 6 THEN 'viernes' "
                                "WHEN 7 THEN 'sábado' "
                                "END "
                                ")")
    
    SQL_CLASES_HOY_ENTRENADOR = ("SELECT COUNT(*) "
                                "FROM clase "
                                "WHERE id_entrenador = ? "
                                "AND LOWER(dia_semana) = LOWER( "
                                "CASE DAYOFWEEK(CURDATE()) "
                                "WHEN 1 THEN 'domingo' "
                                "WHEN 2 THEN 'lunes' "
                                "WHEN 3 THEN 'martes' "
                                "WHEN 4 THEN 'miercoles' "
                                "WHEN 5 THEN 'jueves' "
                                "WHEN 6 THEN 'viernes' "
                                "WHEN 7 THEN 'sabado' "
                                "END)")


    def clases_hoy_entrenador(self, id_entrenador):
        datos = self.consultar(self.SQL_CLASES_HOY_ENTRENADOR, (id_entrenador,))
        return datos[0][0] if datos else 0
    
    
    def buscar_clases(self, texto: str):
        t = f"%{texto.lower().strip()}%"
        filas = self.consultar(self.SQL_BUSCAR_CLASES, (t,))
        return [ClaseVO(f[0], None, None, f[1], f[7], f[2], f[3], f[4], None, f[5], f[6])
                for f in filas]

    def ocupacion_clases(self):
        filas = self.consultar(self.SQL_OCUPACION_CLASE)
        return [OcupacionClaseVO(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    def clases_entrenador_tabla(self, id_entrenador):
        filas = self.consultar(self.SQL_CLASES_ENTRENADOR_TABLA, (id_entrenador,))
        return [ClaseEntrenadorVO(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    def ocupacion_clases_entrenador(self, id_entrenador):
        filas = self.consultar(self.SQL_OCUPACION, (id_entrenador,))
        return [OcupacionClaseVO(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    def informacion_clase_con_sala(self, id_clase):
        datos = self.consultar(self.SQL_INFORMACION_SALA, (id_clase,))
        return datos[0] if datos else None

    def buscar_clase(self, id_clase):
        datos = self.consultar(self.SQL_BUSCAR_CLASE, (id_clase,))
        if not datos:
            return None
        f = datos[0]
        return ClaseVO(f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10])

    def recepcion_clases_hoy(self):
        datos = self.consultar(self.SQL_RECEPCION_CLASES_HOY)
        return datos[0][0] if datos else 0