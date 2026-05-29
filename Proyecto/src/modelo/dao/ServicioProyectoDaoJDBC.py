import hashlib
from datetime import datetime

from src.modelo.dao.UsuarioDaoJDBC       import UsuarioDaoJDBC
from src.modelo.dao.ClienteDaoJDBC       import ClienteDaoJDBC
from src.modelo.dao.EmpleadoDaoJDBC      import EmpleadoDaoJDBC
from src.modelo.dao.AdministradorDaoJDBC import AdministradorDaoJDBC
from src.modelo.dao.EntrenadorDaoJDBC    import EntrenadorDaoJDBC
from src.modelo.dao.RecepcionistaDaoJDBC import RecepcionistaDaoJDBC
from src.modelo.dao.ContableDaoJDBC      import ContableDaoJDBC
from src.modelo.dao.ClaseDaoJDBC         import ClaseDaoJDBC
from src.modelo.dao.InscripcionDaoJDBC   import InscripcionDaoJDBC
from src.modelo.dao.AsistenciaDaoJDBC    import AsistenciaDaoJDBC
from src.modelo.dao.PagoDaoJDBC          import PagoDaoJDBC
from src.modelo.dao.RegistroAccesoDaoJDBC import RegistroAccesoDaoJDBC
from src.modelo.dao.TarifaDaoJDBC        import TarifaDaoJDBC
from src.modelo.dao.InformeDaoJDBC       import InformeDaoJDBC

from src.modelo.VO.UsuarioVO        import UsuarioVO
from src.modelo.VO.ClientesVO       import ClientesVO
from src.modelo.VO.EmpleadosVO      import EmpleadoVO
from src.modelo.VO.AdminitradorVO   import AdminitradorVO
from src.modelo.VO.EntrenadorVO     import EntrenadorVO
from src.modelo.VO.RecepcionistaVO  import RecepcionistaVO
from src.modelo.VO.ContableVO       import ContableVO
from src.modelo.VO.ClaseVO          import ClaseVO
from src.modelo.VO.InscripcionVO    import InscripcionVO
from src.modelo.VO.AsistenciaVO     import AsistenciaVO
from src.modelo.VO.PagoVO           import PagoVO
from src.modelo.VO.Registro_accesoVO import RegistroAccesoVO
from src.modelo.VO.TarifaVO         import TarifaVO
from src.modelo.VO.InformeVO        import InformeVO
from src.modelo.conexion.Conexion   import Conexion


class ServicioProyectoDaoJDBC:
    """
    DAO/Fachada de persistencia del proyecto.
    Contiene las consultas SQL y coordina los DAO específicos.
    La capa Logica solo llama a estos métodos, por lo que las consultas no quedan en Logica.
    """

    def __init__(self):
        self._conexion = Conexion()
        # DAOs — se instancian una sola vez y reutilizan la misma conexión
        self._usuario_dao     = UsuarioDaoJDBC()
        self._cliente_dao     = ClienteDaoJDBC()
        self._empleado_dao    = EmpleadoDaoJDBC()
        self._admin_dao       = AdministradorDaoJDBC()
        self._entrenador_dao  = EntrenadorDaoJDBC()
        self._recep_dao       = RecepcionistaDaoJDBC()
        self._contable_dao    = ContableDaoJDBC()
        self._clase_dao       = ClaseDaoJDBC()
        self._inscripcion_dao = InscripcionDaoJDBC()
        self._asistencia_dao  = AsistenciaDaoJDBC()
        self._pago_dao        = PagoDaoJDBC()
        self._acceso_dao      = RegistroAccesoDaoJDBC()
        self._tarifa_dao      = TarifaDaoJDBC()
        self._informe_dao     = InformeDaoJDBC()

    # ── Helpers internos ────────────────────────────────────────────────────

    def _cifrar(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def consultar(self, sql, parametros=()):
        """Consulta SQL directa (solo para queries complejas con JOINs)."""
        cursor = self._conexion.getCursor()
        try:
            cursor.execute(sql, parametros)
            return cursor.fetchall()
        finally:
            cursor.close()

    def ejecutar(self, sql, parametros=()):
        """Ejecución SQL directa (solo para updates complejos con JOINs)."""
        cursor = self._conexion.getCursor()
        try:
            cursor.execute(sql, parametros)
            try:
                self._conexion.conexion.commit()
            except Exception:
                pass
            return cursor.rowcount
        finally:
            cursor.close()

    # ── AUTENTICACIÓN ───────────────────────────────────────────────────────

    def iniciar_sesion(self, username: str, password: str) -> dict | None:
        """
        Busca el usuario por username mediante el DAO y comprueba la contraseña.
        Devuelve un dict con los datos de sesión o None si falla.
        """
        vo = self._usuario_dao.selectByUsername(username)
        if vo is None:
            return None

        password_cifrada = self._cifrar(password)
        if vo.password_hash != password and vo.password_hash != password_cifrada:
            return None

        # Obtener nombre del rol
        datos_rol = self.consultar(
            "SELECT nombre_rol FROM roles WHERE id_rol = ?", (vo.id_rol,)
        )
        rol = datos_rol[0][0] if datos_rol else "cliente"

        return {
            "id_usuario": vo.id_usuario,
            "nombre":     vo.nombre,
            "username":   vo.username,
            "rol":        rol,
        }

    # ── USUARIOS ────────────────────────────────────────────────────────────

    def registrar_usuario(self, dni, nombre, telefono, email, username,
                          password, id_rol, direccion, fecha_nacimiento) -> int:
        """Crea un UsuarioVO y lo inserta mediante el DAO."""
        vo = UsuarioVO(
            id_usuario=None,
            dni=dni,
            nombre=nombre,
            telefono=telefono,
            email=email,
            username=username,
            password_hash=self._cifrar(password),
            id_rol=id_rol,
            direccion=direccion,
            fecha_registro=None,
            fecha_nacimiento=fecha_nacimiento,
        )
        return self._usuario_dao.insert(vo)

    def registrar_cliente(self, id_cliente: int):
        """Crea un ClientesVO e inserta el cliente mediante el DAO."""
        vo = ClientesVO(id_cliente=id_cliente, estado_pagado="pendiente",
                        calorias_acumuladas=0)
        return self._cliente_dao.insert(vo)

    def registrar_empleado(self, id_empleado: int, salario: float = 0.0):
        """Crea un EmpleadosVO e inserta el empleado mediante el DAO."""
        vo = EmpleadoVO(id_empleado=id_empleado, salario=salario)
        return self._empleado_dao.insert(vo)

    def registrar_entrenador(self, id_entrenador: int, especialidad: str,
                             id_admin: int):
        vo = EntrenadorVO(id_entrenador=id_entrenador,
                          especialidad=especialidad,
                          id_administrador_registra=id_admin)
        return self._entrenador_dao.insert(vo)

    def registrar_recepcionista(self, id_recep: int, turno: str, id_admin: int):
        vo = RecepcionistaVO(id_recepcionista=id_recep, turno=turno,
                             id_administrador_registra=id_admin)
        return self._recep_dao.insert(vo)

    def registrar_contable(self, id_contable: int, titulacion: str, id_admin: int):
        vo = ContableVO(id_contable=id_contable, titulacion=titulacion,
                        id_administrador_registra=id_admin)
        return self._contable_dao.insert(vo)

    def registrar_administrador(self, id_admin: int):
        vo = AdminitradorVO(id_administrador=id_admin)
        return self._admin_dao.insert(vo)

    def modificar_usuario(self, id_usuario: int, telefono: str,
                          email: str, direccion: str):
        """Recupera el VO actual, lo modifica y lo actualiza mediante el DAO."""
        vo = self._usuario_dao.selectById(id_usuario)
        if vo is None:
            raise ValueError(f"Usuario {id_usuario} no encontrado")
        vo_actualizado = UsuarioVO(
            id_usuario=vo.id_usuario,
            dni=vo.dni,
            nombre=vo.nombre,
            telefono=telefono,
            email=email,
            username=vo.username,
            password_hash=vo.password_hash,
            id_rol=vo.id_rol,
            direccion=direccion,
            fecha_registro=vo.fecha_registro,
            fecha_nacimiento=vo.fecha_nacimiento,
        )
        return self._usuario_dao.update(vo_actualizado)

    def eliminar_usuario(self, id_usuario: int):
        return self._usuario_dao.delete(id_usuario)

    def buscar_usuario(self, id_usuario: int) -> UsuarioVO | None:
        return self._usuario_dao.selectById(id_usuario)

    def listar_usuarios(self) -> list:
        """Devuelve lista de tuplas para rellenar tablas en la vista."""
        vos = self._usuario_dao.select()
        return [(v.id_usuario, v.dni, v.nombre, v.telefono, v.email,
                 v.username, v.id_rol, v.direccion, v.fecha_nacimiento)
                for v in vos]

    # ── CLIENTES ────────────────────────────────────────────────────────────

    def contar_usuarios(self) -> int:
        return len(self._cliente_dao.select())

    def listar_clientes(self) -> list:
        vos = self._cliente_dao.select()
        return [(v.id_cliente, v.estado_pagado, v.calorias_acumuladas)
                for v in vos]

    def listar_clientes_completo(self) -> list:
        return self.consultar("""
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, c.estado_pagado, u.direccion, u.fecha_nacimiento
            FROM usuarios u JOIN clientes c ON u.id_usuario = c.id_cliente
            ORDER BY u.nombre
        """)

    def buscar_clientes(self, texto: str) -> list:
        t = texto.lower()
        return self.consultar(f"""
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, c.estado_pagado, u.direccion, u.fecha_nacimiento
            FROM usuarios u JOIN clientes c ON u.id_usuario = c.id_cliente
            WHERE LOWER(u.nombre) LIKE '%{t}%' OR LOWER(u.username) LIKE '%{t}%'
               OR LOWER(u.dni) LIKE '%{t}%'
            ORDER BY u.nombre
        """)

    def buscar_clientes_estado(self, estado: str) -> list:
        return self.consultar(f"""
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, c.estado_pagado, u.direccion, u.fecha_nacimiento
            FROM usuarios u JOIN clientes c ON u.id_usuario = c.id_cliente
            WHERE LOWER(c.estado_pagado) = '{estado.lower()}'
            ORDER BY u.nombre
        """)

    def perfil_usuario(self, id_usuario: int):
        return self._usuario_dao.selectById(id_usuario)

    def datos_inicio_cliente(self, id_cliente: int):
        """Delega en ClienteDaoJDBC.selectInicioCliente que devuelve ClienteInicioVO."""
        return self._cliente_dao.selectInicioCliente(id_cliente)

    # ── TRABAJADORES ────────────────────────────────────────────────────────

    def contar_trabajadores(self) -> int:
        return len(self._empleado_dao.select())

    def contar_por_rol(self, nombre_rol: str) -> int:
        datos = self.consultar(f"""
            SELECT COUNT(*) FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol
            WHERE LOWER(r.nombre_rol) = '{nombre_rol.lower()}'
        """)
        return datos[0][0] if datos else 0

    def listar_trabajadores_completo(self) -> list:
        return self.consultar("""
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, r.nombre_rol, u.direccion, u.fecha_nacimiento
            FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol
            WHERE r.nombre_rol IN ('entrenador','recepcionista','contable','administrador')
            ORDER BY r.nombre_rol, u.nombre
        """)

    def buscar_trabajadores(self, texto: str) -> list:
        t = texto.lower()
        return self.consultar(f"""
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, r.nombre_rol, u.direccion, u.fecha_nacimiento
            FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol
            WHERE r.nombre_rol IN ('entrenador','recepcionista','contable','administrador')
            AND (LOWER(u.nombre) LIKE '%{t}%' OR LOWER(u.username) LIKE '%{t}%'
                 OR LOWER(u.dni) LIKE '%{t}%')
            ORDER BY u.nombre
        """)

    def buscar_trabajadores_rol(self, rol: str) -> list:
        return self.consultar(f"""
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, r.nombre_rol, u.direccion, u.fecha_nacimiento
            FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol
            WHERE LOWER(r.nombre_rol) = '{rol.lower()}'
            ORDER BY u.nombre
        """)

    def listar_empleados(self) -> list:
        vos = self._empleado_dao.select()
        return [(v.id_empleado, v.salario) for v in vos]

    def guardar_cambios_trabajador(self, id_usuario, nombre, telefono, email, direccion):
        self.modificar_usuario(id_usuario, telefono, email, direccion)

    # ── CLASES ──────────────────────────────────────────────────────────────

    def contar_clases(self) -> int:
        return len(self._clase_dao.select())

    def listar_clases(self) -> list:
        vos = self._clase_dao.select()
        return [(v.id_clase, v.nombre_actividad, v.dia_semana, v.hora_inicio,
                 v.hora_fin, v.aforo_maximo, v.nivel_intensidad, v.calorias_estimadas)
                for v in vos]

    def clases_de_entrenador(self, id_entrenador: int) -> list:
        vos = self._clase_dao.selectByEntrenador(id_entrenador)
        return [(v.id_clase, v.nombre_actividad, v.dia_semana, v.hora_inicio,
                 v.hora_fin, v.aforo_maximo, v.nivel_intensidad)
                for v in vos]

    def registrar_clase(self, id_entrenador, id_sala, nombre_actividad,
                        calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                        duracion, aforo_maximo, nivel_intensidad):
        vo = ClaseVO(None, id_entrenador, id_sala, nombre_actividad,
                     calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                     duracion, aforo_maximo, nivel)
        return self._clase_dao.insert(vo)

    def modificar_clase(self, id_clase, id_entrenador, id_sala, nombre_actividad,
                        calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                        duracion, aforo_maximo, nivel_intensidad):
        vo = ClaseVO(id_clase, id_entrenador, id_sala, nombre_actividad,
                     calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                     duracion, aforo_maximo, nivel)
        return self._clase_dao.update(vo)

    def eliminar_clase(self, id_clase: int):
        return self._clase_dao.delete(id_clase)

    def buscar_clases(self, texto: str) -> list:
        t = texto.lower()
        return self.consultar(f"""
            SELECT id_clase, nombre_actividad, dia_semana, hora_inicio,
                   hora_fin, aforo_maximo, nivel_intensidad, calorias_estimadas
            FROM clase WHERE LOWER(nombre_actividad) LIKE '%{t}%'
            ORDER BY nombre_actividad
        """)

    def ocupacion_clases(self) -> list:
        return self.consultar("""
            SELECT c.id_clase, c.nombre_actividad,
                   COUNT(i.id_inscripcion) AS inscritos, c.aforo_maximo,
                   ROUND(COUNT(i.id_inscripcion)*100.0/c.aforo_maximo,1) AS pct
            FROM clase c
            LEFT JOIN inscripcion i ON c.id_clase=i.id_clase AND i.estado='inscrito'
            GROUP BY c.id_clase, c.nombre_actividad, c.aforo_maximo
            ORDER BY pct DESC
        """)

    # ── INSCRIPCIONES ───────────────────────────────────────────────────────

    def contar_inscripciones(self) -> int:
        vos = self._inscripcion_dao.select()
        return sum(1 for v in vos if v.estado == "inscrito")

    def contar_inscripciones_clase(self, nombre_actividad: str) -> int:
        t = nombre_actividad.lower()
        datos = self.consultar(f"""
            SELECT COUNT(*) FROM inscripcion i
            JOIN clase c ON i.id_clase = c.id_clase
            WHERE LOWER(c.nombre_actividad) LIKE '%{t}%' AND i.estado = 'inscrito'
        """)
        return datos[0][0] if datos else 0

    def inscribirse_clase(self, id_cliente: int, id_clase: int):
        # Verificar que no esté ya inscrito
        vos = self._inscripcion_dao.selectByCliente(id_cliente)
        for v in vos:
            if v.id_clase == id_clase and v.estado == "inscrito":
                raise ValueError("Ya estás inscrito en esta clase")
        vo = InscripcionVO(None, id_cliente, id_clase, None, "inscrito")
        return self._inscripcion_dao.insert(vo)

    def desapuntarse_clase(self, id_cliente: int, id_clase: int):
        vos = self._inscripcion_dao.selectByCliente(id_cliente)
        for v in vos:
            if v.id_clase == id_clase and v.estado == "inscrito":
                return self._inscripcion_dao.updateEstado(v.id_inscripcion, "cancelado")
        raise ValueError("No estás inscrito en esa clase")

    def clases_inscritas_cliente(self, id_cliente: int) -> list:
        return self.consultar(f"""
            SELECT c.id_clase, c.nombre_actividad, c.dia_semana,
                   c.hora_inicio, c.hora_fin, c.nivel_intensidad
            FROM inscripcion i JOIN clase c ON i.id_clase = c.id_clase
            WHERE i.id_cliente = {id_cliente} AND i.estado = 'inscrito'
            ORDER BY c.dia_semana
        """)

    def clientes_inscritos_clase(self, id_clase: int) -> list:
        return self.consultar(f"""
            SELECT u.id_usuario, u.nombre, u.email, u.telefono
            FROM inscripcion i JOIN usuarios u ON i.id_cliente = u.id_usuario
            WHERE i.id_clase = {id_clase} AND i.estado = 'inscrito'
        """)

    def listar_inscripciones_resumen(self) -> list:
        return self.consultar("""
            SELECT u.nombre, c.nombre_actividad, i.fecha_inscripcion, i.estado
            FROM inscripcion i
            JOIN usuarios u ON i.id_cliente = u.id_usuario
            JOIN clase c ON i.id_clase = c.id_clase
            WHERE i.estado = 'inscrito'
            ORDER BY i.fecha_inscripcion DESC LIMIT 50
        """)

    def estadisticas_inscripciones(self) -> dict:
        total_r = self.consultar(
            "SELECT COUNT(*) FROM inscripcion WHERE estado='inscrito'")
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
            "total":       total_r[0][0]  if total_r  else 0,
            "clase_mas":   mas_r[0][0]    if mas_r    else "-",
            "num_mas":     mas_r[0][1]    if mas_r    else 0,
            "clase_menos": menos_r[0][0]  if menos_r  else "-",
            "num_menos":   menos_r[0][1]  if menos_r  else 0,
            "ocupacion":   ocup_r[0][0]   if ocup_r and ocup_r[0][0] else 0,
        }

    # ── ASISTENCIA ──────────────────────────────────────────────────────────

    def registrar_asistencia_lista(self, id_clase: int, fecha: str,
                                   ids_presentes: list):
        """Registra asistencia para una clase usando el DAO de Asistencia."""
        inscritos = self._inscripcion_dao.selectByClase(id_clase)
        for ins in inscritos:
            presente = "si" if ins.id_cliente in ids_presentes else "no"
            vo = AsistenciaVO(None, ins.id_cliente, id_clase, fecha, presente)
            self._asistencia_dao.insert(vo)

    def calcular_calorias_cliente(self, id_cliente: int) -> int:
        datos = self.consultar(f"""
            SELECT COALESCE(SUM(c.calorias_estimadas), 0)
            FROM asistencia a JOIN clase c ON a.id_clase = c.id_clase
            WHERE a.id_cliente = {id_cliente} AND a.presente = 'si'
        """)
        return int(datos[0][0]) if datos else 0

    def estadisticas_cliente(self, id_cliente: int) -> list:
        return self.consultar(f"""
            SELECT c.nombre_actividad, COUNT(*) as asistencias,
                   SUM(c.calorias_estimadas) as calorias
            FROM asistencia a JOIN clase c ON a.id_clase = c.id_clase
            WHERE a.id_cliente = {id_cliente} AND a.presente = 'si'
            GROUP BY c.nombre_actividad
        """)

    def historial_cliente(self, id_cliente: int) -> list:
        vos = self._asistencia_dao.selectByCliente(id_cliente)
        return [(v.id_asistencia, v.id_clase, v.fecha, v.presente)
                for v in vos]

    def ranking_clientes_activos(self) -> list:
        return self.consultar("""
            SELECT u.nombre, COUNT(*) as asistencias
            FROM asistencia a JOIN usuarios u ON a.id_cliente = u.id_usuario
            WHERE a.presente = 'si'
            GROUP BY u.id_usuario, u.nombre
            ORDER BY asistencias DESC LIMIT 20
        """)

    # ── PAGOS ───────────────────────────────────────────────────────────────

    def registrar_pago(self, id_cliente, id_contable, id_tarifa,
                       importe, metodo_pago, tipo_cuota):
        from datetime import datetime
        vo = PagoVO(None, id_cliente, id_contable, id_tarifa,
                    importe, metodo_pago,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "pendiente", tipo_cuota)
        return self._pago_dao.insert(vo)

    def marcar_pago_abonado(self, id_pago: int):
        return self._pago_dao.updateEstado(id_pago, "abonado")

    def listar_pagos(self) -> list:
        vos = self._pago_dao.select()
        return [(v.id_pago, v.id_cliente, v.id_contable, v.id_tarifa,
                 v.importe, v.metodo_pago, v.fecha_pago, v.estado, v.tipo_cuota)
                for v in vos]

    def pagos_pendientes(self) -> list:
        # Busca en tabla pago primero
        datos = self.consultar("""
            SELECT p.id_pago, u.nombre, t.nombre, p.importe,
                   p.fecha_pago, p.tipo_cuota
            FROM pago p
            JOIN usuarios u ON p.id_cliente = u.id_usuario
            JOIN tarifa t ON p.id_tarifa = t.id_tarifa
            WHERE p.estado = 'pendiente' ORDER BY p.fecha_pago
        """)
        if datos:
            return datos
        # Fallback: clientes con estado_pagado pendiente
        return self.consultar("""
            SELECT c.id_cliente, u.nombre, 'Sin tarifa', 0,
                   u.fecha_registro, 'mensual'
            FROM clientes c JOIN usuarios u ON c.id_cliente = u.id_usuario
            WHERE c.estado_pagado = 'pendiente'
        """)

    def pagos_cliente(self, id_cliente: int) -> list:
        vos = self._pago_dao.selectByCliente(id_cliente)
        return [(v.id_pago, v.importe, v.metodo_pago,
                 v.fecha_pago, v.estado, v.tipo_cuota)
                for v in vos]

    def informe_pagos_realizados(self) -> list:
        return self.consultar("""
            SELECT u.nombre, t.nombre, p.importe, p.fecha_pago, p.metodo_pago
            FROM pago p
            JOIN usuarios u ON p.id_cliente = u.id_usuario
            JOIN tarifa t ON p.id_tarifa = t.id_tarifa
            WHERE p.estado = 'abonado' ORDER BY p.fecha_pago DESC
        """)

    def informe_pagos_por_mes(self) -> list:
        return self.ingresos_por_mes()

    def informe_salarios(self) -> list:
        return self.consultar("""
            SELECT u.nombre, r.nombre_rol, e.salario
            FROM empleados e
            JOIN usuarios u ON e.id_empleado = u.id_usuario
            JOIN roles r ON u.id_rol = r.id_rol
            ORDER BY e.salario DESC
        """)

    def total_ingresos(self):
        datos = self.consultar(
            "SELECT COALESCE(SUM(importe),0) FROM pago WHERE estado='abonado'")
        return datos[0][0] if datos else 0

    def ingresos_por_mes(self) -> list:
        return self.consultar("""
            SELECT YEAR(fecha_pago) anio, MONTH(fecha_pago) mes, SUM(importe) total
            FROM pago WHERE estado='abonado'
            GROUP BY YEAR(fecha_pago), MONTH(fecha_pago)
            ORDER BY anio DESC, mes DESC LIMIT 6
        """)

    def contar_clientes_tarifa(self, nombre_tarifa: str) -> int:
        t = nombre_tarifa.lower()
        datos = self.consultar(f"""
            SELECT COUNT(*) FROM cliente_tarifa ct
            JOIN tarifa t ON ct.id_tarifa = t.id_tarifa
            WHERE LOWER(t.nombre) LIKE '%{t}%' AND ct.estado = 'activa'
        """)
        return datos[0][0] if datos else 0

    def generar_informe(self, id_contable: int, tipo: str):
        vo = InformeVO(None, id_contable, tipo, None)
        return self._informe_dao.insert(vo)

    def listar_informes(self) -> list:
        vos = self._informe_dao.select()
        return [(v.id_informe, v.id_contable, v.tipo_informe, v.fecha_generacion)
                for v in vos]

    # ── REGISTRO DE ACCESO ──────────────────────────────────────────────────

    def registrar_acceso(self, id_usuario: int, tipo_acceso: str):
        from datetime import datetime
        vo = RegistroAccesoVO(
            id_registro=None,
            id_usuario=id_usuario,
            fecha_hora_registro=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tipo_acceso=tipo_acceso,
        )
        return self._acceso_dao.insert(vo)

    def listar_accesos(self) -> list:
        vos = self._acceso_dao.select()
        return [(v.id_registro, v.id_usuario,
                 v.fecha_hora_registro, v.tipo_acceso)
                for v in vos]

    # ── TARIFAS ─────────────────────────────────────────────────────────────

    def listar_tarifas(self) -> list:
        vos = self._tarifa_dao.select()
        return [(v.id_tarifa, v.nombre, v.precio_mensual,
                 v.servicios_incluidos, v.fecha_inicio, v.fecha_fin)
                for v in vos]


    def consultar_asistencia_clase(self, id_clase: int) -> list:
        """Devuelve las asistencias de una clase. Usado por el panel del entrenador."""
        return self.consultar("""
            SELECT u.nombre, a.fecha, a.presente
            FROM asistencia a
            JOIN usuarios u ON a.id_cliente = u.id_usuario
            WHERE a.id_clase = ?
            ORDER BY a.fecha DESC, u.nombre
        """, (id_clase,))

    def crear_relacion_usuario_por_rol(self, id_usuario: int, id_rol: int, id_admin: int):
        """Crea el registro asociado al rol tras insertar el usuario base."""
        if id_rol == 1:
            return self.registrar_cliente(id_usuario)
        self.registrar_empleado(id_usuario, 0.00)
        if id_rol == 2:
            return self.registrar_entrenador(id_usuario, "General", id_admin)
        if id_rol == 3:
            return self.registrar_recepcionista(id_usuario, "mañana", id_admin)
        if id_rol == 4:
            return self.registrar_administrador(id_usuario)
        if id_rol == 5:
            return self.registrar_contable(id_usuario, "ADE", id_admin)
        raise ValueError("Rol no reconocido")

    def crear_usuario_completo(self, dni, nombre, telefono, email, username,
                               password, id_rol, direccion, fecha_nacimiento,
                               id_admin_registra=None):
        """Alta completa de usuario y su tabla específica de rol."""
        self.registrar_usuario(dni, nombre, telefono, email, username,
                               password, id_rol, direccion, fecha_nacimiento)
        usuario_vo = self._usuario_dao.selectByUsername(username)
        if usuario_vo is None:
            raise ValueError("No se pudo obtener el usuario recién creado")
        self.crear_relacion_usuario_por_rol(
            usuario_vo.id_usuario,
            id_rol,
            id_admin_registra if id_admin_registra is not None else usuario_vo.id_usuario
        )
        return usuario_vo.id_usuario

    def guardar_cambios_clase_tabla(self, id_clase, nombre, dia, hora_ini, hora_fin, aforo, nivel):
        """Actualización simplificada desde la tabla editable de clases."""
        clase = self._clase_dao.selectById(int(id_clase))
        if clase is None:
            raise ValueError("Clase no encontrada")
        vo = ClaseVO(
            clase.id_clase,
            clase.id_entrenador,
            clase.id_sala,
            nombre,
            dia,
            hora_ini,
            hora_fin,
            int(aforo),
            nivel,
            clase.calorias_estimadas,
        )
        return self._clase_dao.update(vo)

    # ── CAMBIO DE CONTRASEÑA ────────────────────────────────────────────────

    def cambiar_password(self, id_usuario: int, nueva_password: str):
        vo = self._usuario_dao.selectById(id_usuario)
        if vo is None:
            raise ValueError("Usuario no encontrado")
        vo_nuevo = UsuarioVO(
            vo.id_usuario, vo.dni, vo.nombre, vo.telefono, vo.email,
            vo.username, self._cifrar(nueva_password), vo.id_rol,
            vo.direccion, vo.fecha_registro, vo.fecha_nacimiento,
        )
        return self._usuario_dao.update(vo_nuevo)
