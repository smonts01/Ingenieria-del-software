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
        return self._clase_consultas_dao.clases_entrenador_tabla(id_entrenador)

    def ocupacion_clases_entrenador(self, id_entrenador):
        return self._clase_consultas_dao.ocupacion_clases_entrenador(id_entrenador)

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