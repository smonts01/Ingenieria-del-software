from src.modelo.VO.ClaseVO import ClaseVO
from src.modelo.VO.AsistenciaVO import AsistenciaVO

from src.modelo.dao.ClaseDaoJDBC import ClaseDaoJDBC
from src.modelo.dao.ClaseConsultasDaoJDBC import ClaseConsultasDaoJDBC
from src.modelo.dao.InscripcionDaoJDBC import InscripcionDaoJDBC
from src.modelo.dao.InscripcionConsultasDaoJDBC import InscripcionConsultasDaoJDBC
from src.modelo.dao.AsistenciaDaoJDBC import AsistenciaDaoJDBC
from src.modelo.dao.AsistenciaConsultasDaoJDBC import AsistenciaConsultasDaoJDBC


class LogicaClases:
    """Reglas de negocio de clases, aforo, inscripciones y asistencia."""

    def __init__(self):
        self._clase_dao = ClaseDaoJDBC()
        self._clase_consultas_dao = ClaseConsultasDaoJDBC()
        self._inscripcion_dao = InscripcionDaoJDBC()
        self._inscripcion_consultas_dao = InscripcionConsultasDaoJDBC()
        self._asistencia_dao = AsistenciaDaoJDBC()
        self._asistencia_consultas_dao = AsistenciaConsultasDaoJDBC()

    # ── CLASES ─────────────────────────────────────────────────────

    def clases_hoy_entrenador(self, id_entrenador):
        if not id_entrenador:
            raise ValueError("Debe indicarse el entrenador")

        return self._clase_consultas_dao.clases_hoy_entrenador(id_entrenador)

    def contar_clases(self):
        return len(self._clase_dao.select())

    def listar_clases(self):
        clases = self._clase_dao.select()

        return [
            (
                clase.id_clase,
                clase.nombre_actividad,
                clase.dia_semana,
                clase.hora_inicio,
                clase.hora_fin,
                clase.aforo_maximo,
                clase.nivel_intensidad,
                clase.calorias_estimadas
            )
            for clase in clases
        ]

    def buscar_clases(self, texto):
        return self._clase_consultas_dao.buscar_clases(texto)

    def buscar_clase(self, id_clase):
        if not id_clase:
            raise ValueError("Debe indicarse la clase")

        return self._clase_consultas_dao.buscar_clase(id_clase)

    def clases_de_entrenador(self, id_entrenador):
        if not id_entrenador:
            raise ValueError("Debe indicarse el entrenador")

        clases = self._clase_dao.selectByEntrenador(id_entrenador)

        return [
            (
                clase.id_clase,
                clase.nombre_actividad,
                clase.dia_semana,
                clase.hora_inicio,
                clase.hora_fin,
                clase.aforo_maximo,
                clase.nivel_intensidad
            )
            for clase in clases
        ]

    def registrar_clase(self, id_entrenador, id_sala, nombre_actividad,
                        calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                        duracion, aforo_maximo, nivel_intensidad):
        if not nombre_actividad:
            raise ValueError("El nombre de la clase es obligatorio")

        if int(aforo_maximo) <= 0:
            raise ValueError("El aforo debe ser mayor que cero")

        clase_vo = ClaseVO(
            None,
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
        )

        return self._clase_dao.insert(clase_vo)

    def modificar_clase(self, id_clase, id_entrenador, id_sala, nombre_actividad,
                        calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                        duracion, aforo_maximo, nivel_intensidad):
        if not id_clase:
            raise ValueError("Debe indicarse la clase")

        if not nombre_actividad:
            raise ValueError("El nombre de la clase es obligatorio")

        if int(aforo_maximo) <= 0:
            raise ValueError("El aforo debe ser mayor que cero")

        clase_vo = ClaseVO(
            id_clase,
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
        )

        return self._clase_dao.update(clase_vo)

    def eliminar_clase(self, id_clase):
        if not id_clase:
            raise ValueError("Debe indicarse la clase")

        return self._clase_dao.delete(id_clase)

    def guardar_cambios_clase_tabla(self, id_clase, nombre, dia, hora_ini, hora_fin, aforo, nivel):
        if not id_clase:
            raise ValueError("Debe indicarse la clase")

        if not nombre:
            raise ValueError("El nombre de la clase es obligatorio")

        if int(aforo) <= 0:
            raise ValueError("El aforo debe ser mayor que cero")

        clase = self._clase_dao.selectById(int(id_clase))

        if clase is None:
            raise ValueError("Clase no encontrada")

        clase_actualizada = ClaseVO(
            clase.id_clase,
            clase.id_entrenador,
            clase.id_sala,
            nombre,
            clase.calorias_estimadas,
            dia,
            hora_ini,
            hora_fin,
            clase.duracion,
            int(aforo),
            nivel
        )

        return self._clase_dao.update(clase_actualizada)

    def ocupacion_clases(self):
        return self._clase_consultas_dao.ocupacion_clases()

    
    def clases_entrenador_tabla(self, id_entrenador):
        """
        Datos preparados para tablas del entrenador.
        El DAO devuelve ClaseEntrenadorVO y aquí lo convertimos a tuplas.
        """
        clases = self._clase_consultas_dao.clases_entrenador_tabla(id_entrenador)

        return [
            (
                clase.nombre_actividad,
                clase.sala,
                clase.horario,
                clase.dia_semana,
                clase.capacidad
            )
            for clase in clases
        ]

    def ocupacion_clases_entrenador(self, id_entrenador):
        """
        Datos preparados para la tabla de ocupación del entrenador.
        El DAO devuelve OcupacionClaseVO y aquí lo convertimos a tuplas.
        """
        ocupaciones = self._clase_consultas_dao.ocupacion_clases_entrenador(id_entrenador)

        return [
            (
                ocupacion.id_clase,
                ocupacion.nombre_actividad,
                ocupacion.inscritos,
                ocupacion.aforo_maximo,
                ocupacion.porcentaje
            )
            for ocupacion in ocupaciones
        ]

    def informacion_clase_con_sala(self, id_clase):
        return self._clase_consultas_dao.informacion_clase_con_sala(id_clase)

    def clientes_inscritos_clase(self, id_clase):
        return self._inscripcion_consultas_dao.clientes_inscritos_clase(id_clase)

    # ── INSCRIPCIONES ───────────────────────────────────────────────

    def contar_inscripciones(self):
        inscripciones = self._inscripcion_dao.select()
        return sum(1 for inscripcion in inscripciones if inscripcion.estado == "inscrito")

    def contar_inscripciones_clase(self, nombre_actividad):
        return self._inscripcion_consultas_dao.contar_inscripciones_clase(nombre_actividad)

    def listar_inscripciones_resumen(self):
        return self._inscripcion_consultas_dao.listar_inscripciones_resumen()

    def buscar_inscripciones(self, texto):
        return self._inscripcion_consultas_dao.buscar_inscripciones(texto)

    def estadisticas_inscripciones(self):
        return self._inscripcion_consultas_dao.estadisticas_inscripciones()

    # ── ASISTENCIA ──────────────────────────────────────────────────

    def consultar_asistencia_clase(self, id_clase):
        return self._asistencia_consultas_dao.consultar_asistencia_clase(id_clase)

    def asistencia_clase_fecha(self, id_clase, fecha):
        return self._asistencia_consultas_dao.asistencia_clase_fecha(id_clase, fecha)

    def registrar_asistencia(self, id_cliente, id_clase, fecha, presente):
        if not id_cliente:
            raise ValueError("Debe indicarse el cliente")

        if not id_clase:
            raise ValueError("Debe indicarse la clase")

        if not fecha:
            raise ValueError("Debe indicarse la fecha")

        return self._asistencia_consultas_dao.registrar_asistencia(
            id_cliente,
            id_clase,
            fecha,
            presente
        )

    def registrar_asistencia_lista(self, id_clase, fecha, ids_presentes):
        if not id_clase:
            raise ValueError("Debe indicarse la clase")

        if not fecha:
            raise ValueError("Debe indicarse la fecha")

        inscritos = self._inscripcion_dao.selectByClase(id_clase)

        for inscripcion in inscritos:
            presente = "si" if inscripcion.id_cliente in ids_presentes else "no"

            asistencia_vo = AsistenciaVO(
                None,
                inscripcion.id_cliente,
                id_clase,
                fecha,
                presente
            )

            self._asistencia_dao.insert(asistencia_vo)

        return True

    def calcular_calorias_cliente(self, id_cliente):
        return self._asistencia_consultas_dao.calcular_calorias_cliente(id_cliente)

    def estadisticas_cliente(self, id_cliente):
        return self._asistencia_consultas_dao.estadisticas_cliente(id_cliente)

    def historial_cliente(self, id_cliente):
        asistencias = self._asistencia_dao.selectByCliente(id_cliente)

        return [
            (
                asistencia.id_asistencia,
                asistencia.id_clase,
                asistencia.fecha,
                asistencia.presente
            )
            for asistencia in asistencias
        ]

    def ranking_clientes_activos(self):
        return self._asistencia_consultas_dao.ranking_clientes_activos()
    
    
    
    def total_inscritos_clases_entrenador(self, id_entrenador):
        clases = self.clases_de_entrenador(id_entrenador)
        total = 0

        for clase in clases:
            inscritos = self.clientes_inscritos_clase(clase[0])
            total += len(inscritos)

        return total

    def ocupacion_media_entrenador(self, id_entrenador):
        ocupaciones = self.ocupacion_clases_entrenador(id_entrenador)

        if not ocupaciones:
            return 0

        suma = 0

        for ocupacion in ocupaciones:
            suma += float(ocupacion[4] or 0)

        return round(suma / len(ocupaciones), 2)

    def resumen_ocupacion_entrenador(self, id_entrenador):
        datos_ocupacion = self.ocupacion_clases_entrenador(id_entrenador)

        if not datos_ocupacion:
            return {
                "total_clases": 0,
                "ocupacion_media": 0,
                "clases_llenas": 0,
                "clase_mas_llena": None,
                "plazas_libres_mas_llena": 0
            }

        total_ocupacion = 0
        clases_llenas = 0
        clase_mas_llena = datos_ocupacion[0]

        for dato in datos_ocupacion:
            inscritos = int(dato[2] or 0)
            aforo = int(dato[3] or 0)
            ocupacion = float(dato[4] or 0)

            total_ocupacion += ocupacion

            if aforo > 0 and inscritos >= aforo:
                clases_llenas += 1

            if ocupacion > float(clase_mas_llena[4] or 0):
                clase_mas_llena = dato

        ocupacion_media = round(total_ocupacion / len(datos_ocupacion), 2)
        plazas_libres = int(clase_mas_llena[3] or 0) - int(clase_mas_llena[2] or 0)

        return {
            "total_clases": len(datos_ocupacion),
            "ocupacion_media": ocupacion_media,
            "clases_llenas": clases_llenas,
            "clase_mas_llena": clase_mas_llena,
            "plazas_libres_mas_llena": plazas_libres
        }

    def normalizar_estado_asistencia(self, estado):
        estado = str(estado).strip().lower()

        if estado in ["si", "sí", "asistio", "asistió", "presente"]:
            return "si"

        if estado in ["no", "ausencia", "ausente"]:
            return "no"

        return "pendiente"

    def registrar_asistencia_normalizada(self, id_cliente, id_clase, fecha, estado):
        estado_normalizado = self.normalizar_estado_asistencia(estado)

        if estado_normalizado == "pendiente":
            return None

        return self.registrar_asistencia(
            id_cliente,
            id_clase,
            fecha,
            estado_normalizado
        )
    
    def datos_clase_asistencia(self, id_clase):
        """
        Devuelve los datos básicos de una clase preparados para la pantalla
        de asistencia del entrenador.
        """
        clase = self.buscar_clase(id_clase)

        if not clase:
            return None

        # Si buscar_clase devuelve ClaseVO
        if hasattr(clase, "nombre_actividad"):
            return {
                "nombre": clase.nombre_actividad,
                "dia": clase.dia_semana,
                "hora_inicio": clase.hora_inicio,
                "hora_fin": clase.hora_fin
            }

        # Si buscar_clase devuelve tupla/lista
        return {
            "nombre": clase[3],
            "dia": clase[5],
            "hora_inicio": clase[6],
            "hora_fin": clase[7]
        }