from src.modelo.VO.ClaseVO import ClaseVO
from src.modelo.VO.AsistenciaVO import AsistenciaVO

from src.modelo.dao.ClaseDaoJDBC import ClaseDaoJDBC
from src.modelo.dao.ClaseConsultasDaoJDBC import ClaseConsultasDaoJDBC
from src.modelo.dao.InscripcionDaoJDBC import InscripcionDaoJDBC
from src.modelo.dao.InscripcionConsultasDaoJDBC import InscripcionConsultasDaoJDBC
from src.modelo.dao.AsistenciaDaoJDBC import AsistenciaDaoJDBC
from src.modelo.dao.AsistenciaConsultasDaoJDBC import AsistenciaConsultasDaoJDBC


class LogicaClases:
    """Lógica de negocio para clases, inscripciones y asistencia.
    """

    def __init__(self):
        # DAOs de clases
        self._clase_dao              = ClaseDaoJDBC()
        self._clase_consultas_dao    = ClaseConsultasDaoJDBC()
        # DAOs de inscripciones
        self._inscripcion_dao            = InscripcionDaoJDBC()
        self._inscripcion_consultas_dao  = InscripcionConsultasDaoJDBC()
        # DAOs de asistencia
        self._asistencia_dao             = AsistenciaDaoJDBC()
        self._asistencia_consultas_dao   = AsistenciaConsultasDaoJDBC()

    # Clases

    def clases_ocupacion_cliente(self):
        """Devuelve todas las clases con sala, inscritos y aforo
        como lista de ClaseOcupacionClienteVO. Usada en la vista del cliente."""
        return self._clase_consultas_dao.clases_ocupacion_cliente()

    def clases_hoy_entrenador(self, id_entrenador):
        """Devuelve el número de clases que tiene el entrenador programadas para hoy.
        Lanza ValueError si no se indica el entrenador."""
        if not id_entrenador:
            raise ValueError("Debe indicarse el entrenador")
        return self._clase_consultas_dao.clases_hoy_entrenador(id_entrenador)

    def contar_clases(self):
        """Devuelve el número total de clases registradas en el sistema."""
        return len(self._clase_dao.select())

    def listar_clases(self):
        """Devuelve todas las clases como lista de ClaseVO."""
        return self._clase_dao.select()

    def buscar_clases(self, texto):
        """Busca clases cuyo nombre contenga el texto indicado.
        Devuelve lista de ClaseVO."""
        return self._clase_consultas_dao.buscar_clases(texto)

    def buscar_clase(self, id_clase):
        """Devuelve los datos completos de una clase por su ID como ClaseVO,
        o None si no existe. Lanza ValueError si no se indica la clase."""
        if not id_clase:
            raise ValueError("Debe indicarse la clase")
        return self._clase_consultas_dao.buscar_clase(id_clase)

    def clases_de_entrenador(self, id_entrenador):
        """Devuelve todas las clases asignadas a un entrenador como lista de ClaseVO.
        Lanza ValueError si no se indica el entrenador."""
        if not id_entrenador:
            raise ValueError("Debe indicarse el entrenador")
        return self._clase_dao.selectByEntrenador(id_entrenador)

    def registrar_clase(self, id_entrenador, id_sala, nombre_actividad,
                        calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                        duracion, aforo_maximo, nivel_intensidad):
        """Da de alta una nueva clase validando nombre y aforo.
        Lanza ValueError si el nombre está vacío o el aforo es 0 o negativo."""
        if not nombre_actividad:
            raise ValueError("El nombre de la clase es obligatorio")
        if int(aforo_maximo) <= 0:
            raise ValueError("El aforo debe ser mayor que cero")

        clase_vo = ClaseVO(
            None, id_entrenador, id_sala, nombre_actividad,
            calorias_estimadas, dia_semana, hora_inicio, hora_fin,
            duracion, aforo_maximo, nivel_intensidad
        )
        return self._clase_dao.insert(clase_vo)

    def modificar_clase(self, id_clase, id_entrenador, id_sala, nombre_actividad,
                        calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                        duracion, aforo_maximo, nivel_intensidad):
        """Actualiza todos los campos de una clase existente.
        Lanza ValueError si falta el ID, el nombre o el aforo es inválido."""
        if not id_clase:
            raise ValueError("Debe indicarse la clase")
        if not nombre_actividad:
            raise ValueError("El nombre de la clase es obligatorio")
        if int(aforo_maximo) <= 0:
            raise ValueError("El aforo debe ser mayor que cero")

        clase_vo = ClaseVO(
            id_clase, id_entrenador, id_sala, nombre_actividad,
            calorias_estimadas, dia_semana, hora_inicio, hora_fin,
            duracion, aforo_maximo, nivel_intensidad
        )
        return self._clase_dao.update(clase_vo)

    def eliminar_clase(self, id_clase):
        """Elimina una clase de la base de datos 
        Devuelve el número de filas afectadas."""
        return self._clase_dao.delete(id_clase)

    def guardar_cambios_clase_tabla(self, id_clase, nombre, dia,
                                    hora_ini, hora_fin, aforo, nivel):
        """Actualiza los campos editables de una clase desde la tabla del admin.
        Mantiene el entrenador, sala, calorías y duración originales.
        Lanza ValueError si la clase no existe o los datos son inválidos."""
        if not id_clase:
            raise ValueError("Debe indicarse la clase")
        if not nombre:
            raise ValueError("El nombre de la clase es obligatorio")
        if int(aforo) <= 0:
            raise ValueError("El aforo debe ser mayor que cero")

        # Recuperar la clase original para conservar los campos no editables
        clase = self._clase_dao.selectById(int(id_clase))
        if clase is None:
            raise ValueError("Clase no encontrada")

        clase_actualizada = ClaseVO(
            clase.id_clase, clase.id_entrenador, clase.id_sala,
            nombre, clase.calorias_estimadas, dia, hora_ini, hora_fin,
            clase.duracion, int(aforo), nivel
        )
        return self._clase_dao.update(clase_actualizada)

    def ocupacion_clases(self):
        """Devuelve la ocupación de todas las clases como lista de OcupacionClaseVO."""
        return self._clase_consultas_dao.ocupacion_clases()

    def clases_entrenador_tabla(self, id_entrenador):
        """Devuelve las clases del entrenador con sala, horario y capacidad
        como lista de ClaseEntrenadorVO, listas para mostrar en tabla."""
        return self._clase_consultas_dao.clases_entrenador_tabla(id_entrenador)

    def ocupacion_clases_entrenador(self, id_entrenador):
        """Devuelve la ocupación de las clases del entrenador
        como lista de OcupacionClaseVO."""
        return self._clase_consultas_dao.ocupacion_clases_entrenador(id_entrenador)

    def informacion_clase_con_sala(self, id_clase):
        """Devuelve los datos de una clase junto con el nombre de su sala
        como ClaseSalaVO, o None si no existe."""
        return self._clase_consultas_dao.informacion_clase_con_sala(id_clase)

    def clientes_inscritos_clase(self, id_clase):
        """Devuelve los clientes inscritos en una clase como lista de ClienteInscritoVO."""
        return self._inscripcion_consultas_dao.clientes_inscritos_clase(id_clase)

    # Inscripciones

    def contar_inscripciones(self):
        """Devuelve el número de inscripciones activas (estado = 'inscrito')."""
        inscripciones = self._inscripcion_dao.select()
        return sum(1 for i in inscripciones if i.estado == "inscrito")

    def contar_inscripciones_clase(self, nombre_actividad):
        """Devuelve el número de inscritos en la clase con el nombre indicado."""
        return self._inscripcion_consultas_dao.contar_inscripciones_clase(nombre_actividad)

    def listar_inscripciones_resumen(self):
        """Devuelve todas las inscripciones con datos de cliente y clase
        como lista de InscripcionResumenVO."""
        return self._inscripcion_consultas_dao.listar_inscripciones_resumen()

    def buscar_inscripciones(self, texto):
        """Busca inscripciones cuyo cliente o clase contenga el texto indicado."""
        return self._inscripcion_consultas_dao.buscar_inscripciones(texto)

    def estadisticas_inscripciones(self):
        """Devuelve estadísticas globales de inscripciones: total, clase más/menos
        inscrita y ocupación media, como diccionario."""
        return self._inscripcion_consultas_dao.estadisticas_inscripciones()

    # asistencia a clases

    def consultar_asistencia_clase(self, id_clase):
        """Devuelve todos los registros de asistencia de una clase
        como lista de AsistenciaRegistroVO."""
        return self._asistencia_consultas_dao.consultar_asistencia_clase(id_clase)

    def asistencia_clase_fecha(self, id_clase, fecha):
        """Devuelve los registros de asistencia de una clase en una fecha concreta
        como lista de AsistenciaRegistroVO."""
        return self._asistencia_consultas_dao.asistencia_clase_fecha(id_clase, fecha)

    def registrar_asistencia(self, id_cliente, id_clase, fecha, presente):
        """Registra la asistencia de un cliente a una clase en una fecha.
        Lanza ValueError si falta algún campo obligatorio."""
        if not id_cliente:
            raise ValueError("Debe indicarse el cliente")
        if not id_clase:
            raise ValueError("Debe indicarse la clase")
        if not fecha:
            raise ValueError("Debe indicarse la fecha")
        return self._asistencia_consultas_dao.registrar_asistencia(
            id_cliente, id_clase, fecha, presente
        )

    def registrar_asistencia_lista(self, id_clase, fecha, ids_presentes):
        """Registra la asistencia de todos los inscritos en una clase.
        Marca como 'si' a los clientes en ids_presentes y 'no' al resto.
        Lanza ValueError si falta la clase o la fecha."""
        if not id_clase:
            raise ValueError("Debe indicarse la clase")
        if not fecha:
            raise ValueError("Debe indicarse la fecha")

        inscritos = self._inscripcion_dao.selectByClase(id_clase)
        for inscripcion in inscritos:
            presente = "si" if inscripcion.id_cliente in ids_presentes else "no"
            asistencia_vo = AsistenciaVO(
                None, inscripcion.id_cliente, id_clase, fecha, presente
            )
            self._asistencia_dao.insert(asistencia_vo)
        return True

    def calcular_calorias_cliente(self, id_cliente):
        """Devuelve las calorías totales acumuladas por el cliente."""
        return self._asistencia_consultas_dao.calcular_calorias_cliente(id_cliente)

    def estadisticas_cliente(self, id_cliente):
        """Devuelve estadísticas de asistencia del cliente como diccionario."""
        return self._asistencia_consultas_dao.estadisticas_cliente(id_cliente)

    def historial_cliente(self, id_cliente):
        """Devuelve el historial completo de asistencia de un cliente
        como lista de AsistenciaVO."""
        return self._asistencia_dao.selectByCliente(id_cliente)

    def ranking_clientes_activos(self):
        """Devuelve el ranking de clientes por número de asistencias."""
        return self._asistencia_consultas_dao.ranking_clientes_activos()

    # Entrenador 

    def total_inscritos_clases_entrenador(self, id_entrenador):
        """Devuelve el número total de alumnos inscritos en todas las clases
        del entrenador indicado."""
        clases = self.clases_de_entrenador(id_entrenador)
        total = 0
        for clase in clases:
            total += len(self.clientes_inscritos_clase(clase.id_clase))
        return total

    def ocupacion_media_entrenador(self, id_entrenador):
        """Devuelve el porcentaje de ocupación media de todas las clases
        del entrenador, redondeado a 2 decimales."""
        ocupaciones = self.ocupacion_clases_entrenador(id_entrenador)
        if not ocupaciones:
            return 0
        suma = sum(float(o.porcentaje or 0) for o in ocupaciones)
        return round(suma / len(ocupaciones), 2)

    def resumen_ocupacion_entrenador(self, id_entrenador):
        """Devuelve un diccionario con el resumen de ocupación de las clases
        del entrenador: total de clases, ocupación media, clases llenas,
        clase más llena y plazas libres en esa clase."""
        datos_ocupacion = self.ocupacion_clases_entrenador(id_entrenador)

        if not datos_ocupacion:
            return {
                "total_clases": 0, "ocupacion_media": 0,
                "clases_llenas": 0, "clase_mas_llena": None,
                "plazas_libres_mas_llena": 0
            }

        total_ocupacion = 0
        clases_llenas   = 0
        clase_mas_llena = datos_ocupacion[0]

        for dato in datos_ocupacion:
            inscritos = int(dato.inscritos or 0)
            aforo     = int(dato.aforo_maximo or 0)
            ocupacion = float(dato.porcentaje or 0)

            total_ocupacion += ocupacion

            # Clase llena: todos los inscritos igualan o superan el aforo
            if aforo > 0 and inscritos >= aforo:
                clases_llenas += 1

            # Actualizar la clase más llena si supera la actual
            if ocupacion > float(clase_mas_llena.porcentaje or 0):
                clase_mas_llena = dato

        ocupacion_media = round(total_ocupacion / len(datos_ocupacion), 2)
        plazas_libres   = int(clase_mas_llena.aforo_maximo or 0) - int(clase_mas_llena.inscritos or 0)

        return {
            "total_clases":          len(datos_ocupacion),
            "ocupacion_media":       ocupacion_media,
            "clases_llenas":         clases_llenas,
            "clase_mas_llena":       clase_mas_llena,
            "plazas_libres_mas_llena": plazas_libres,
        }

    def resumen_asistencia_clase(self, id_clase, fecha):
        """Calcula presentes, ausentes y pendientes para una clase en una fecha.
        Devuelve un diccionario con: total, presentes, ausentes, pendientes,
        mapa {id_cliente: presente} y lista de datos de inscritos."""
        datos       = self.clientes_inscritos_clase(id_clase)
        asistencias = self.asistencia_clase_fecha(id_clase, fecha)
        mapa        = {a.id_cliente: a.presente for a in asistencias}
        presentes   = sum(1 for v in mapa.values() if v == 'si')
        ausentes    = sum(1 for v in mapa.values() if v == 'no')
        pendientes  = len(datos) - presentes - ausentes
        return {
            'total':     len(datos),
            'presentes': presentes,
            'ausentes':  ausentes,
            'pendientes': pendientes,
            'mapa':      mapa,
            'datos':     datos,
        }

    def estadisticas_perfil_entrenador(self, id_entrenador):
        """Calcula el total de alumnos y el porcentaje de asistencia global
        del entrenador. Devuelve dict con: total_clientes, pct_asistencia."""
        clases         = self.clases_de_entrenador(id_entrenador)
        total_clientes = sum(len(self.clientes_inscritos_clase(c.id_clase)) for c in clases)
        total_reg = total_pres = 0
        for c in clases:
            for a in self.consultar_asistencia_clase(c.id_clase):
                total_reg += 1
                if a.presente == 'si':
                    total_pres += 1
        pct = f'{round(total_pres * 100 / total_reg, 2)}%' if total_reg > 0 else '0%'
        return {'total_clientes': total_clientes, 'pct_asistencia': pct}

    # Funciones asistencia

    def normalizar_estado_asistencia(self, estado):
        """Convierte distintas formas de indicar asistencia a los valores
        estándar de la BD: 'si', 'no' o 'pendiente'."""
        estado = str(estado).strip().lower()
        if estado in ["si", "sí", "asistio", "asistió", "presente"]:
            return "si"
        if estado in ["no", "ausencia", "ausente"]:
            return "no"
        return "pendiente"

    def registrar_asistencia_normalizada(self, id_cliente, id_clase, fecha, estado):
        """Normaliza el estado de asistencia y lo registra si es 'si' o 'no'.
        Ignora los estados 'pendiente' y devuelve None en ese caso."""
        estado_normalizado = self.normalizar_estado_asistencia(estado)
        if estado_normalizado == "pendiente":
            return None
        return self.registrar_asistencia(id_cliente, id_clase, fecha, estado_normalizado)

    def datos_clase_asistencia(self, id_clase):
        """Devuelve los datos básicos de una clase (nombre, día y horario)
        como diccionario, para la pantalla de asistencia del entrenador.
        Compatible con ClaseVO y con tuplas. Devuelve None si no existe."""
        clase = self.buscar_clase(id_clase)
        if not clase:
            return None

        # Si buscar_clase devuelve un ClaseVO accedemos por atributos
        if hasattr(clase, "nombre_actividad"):
            return {
                "nombre":      clase.nombre_actividad,
                "dia":         clase.dia_semana,
                "hora_inicio": clase.hora_inicio,
                "hora_fin":    clase.hora_fin,
            }

        # Compatibilidad con tupla (id, id_ent, id_sala, nombre, cal, dia, h_ini, h_fin, ...)
        return {
            "nombre":      clase[3],
            "dia":         clase[5],
            "hora_inicio": clase[6],
            "hora_fin":    clase[7],
        }