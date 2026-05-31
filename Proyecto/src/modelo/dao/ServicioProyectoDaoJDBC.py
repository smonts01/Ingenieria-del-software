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
from src.modelo.dao.MenorDaoJDBC import MenorDaoJDBC
from src.modelo.VO.MenorVO import MenorVO


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
        self._menor_dao = MenorDaoJDBC()
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

    #  Helpers internos 

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
        """
        Devuelve el perfil de usuario en formato tupla para que los controladores
        puedan usar índices como perfil[2], perfil[3], etc.
        """
        sql = """
            SELECT u.id_usuario,
                   u.dni,
                   u.nombre,
                   u.telefono,
                   u.email,
                   u.username,
                   r.nombre_rol,
                   u.direccion,
                   u.fecha_registro,
                   u.fecha_nacimiento
            FROM usuarios u
            INNER JOIN roles r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = ?
        """
        datos = self.consultar(sql, (id_usuario,))
        return datos[0] if datos else None

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


    def buscar_inscripciones(self, texto: str) -> list:
        t = texto.lower()

        return self.consultar(f"""
            SELECT 
                u.nombre,
                c.nombre_actividad,
                i.fecha_inscripcion,
                i.estado
            FROM inscripcion i
            JOIN usuarios u ON i.id_cliente = u.id_usuario
            JOIN clase c ON i.id_clase = c.id_clase
            WHERE i.estado = 'inscrito'
            AND (
                    LOWER(u.nombre) LIKE '%{t}%'
                OR LOWER(c.nombre_actividad) LIKE '%{t}%'
                OR LOWER(i.estado) LIKE '%{t}%'
            )
            ORDER BY i.fecha_inscripcion DESC
        """)

    def clases_de_entrenador(self, id_entrenador: int) -> list:
        vos = self._clase_dao.selectByEntrenador(id_entrenador)
        return [(v.id_clase, v.nombre_actividad, v.dia_semana, v.hora_inicio,
                 v.hora_fin, v.aforo_maximo, v.nivel_intensidad)
                for v in vos]

    def registrar_clase(self, id_entrenador, id_sala, nombre_actividad,
                        calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                        duracion, aforo_maximo, nivel_intensidad):
        vo = ClaseVO(
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
        return self._clase_dao.insert(vo)

    def modificar_clase(self, id_clase, id_entrenador, id_sala, nombre_actividad,
                        calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                        duracion, aforo_maximo, nivel_intensidad):
        vo = ClaseVO(
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
        """
        Devuelve los clientes inscritos en una clase.
        Formato esperado por ControladorEntrenador:
        id_cliente, nombre, telefono, email
        """
        sql = """
            SELECT u.id_usuario,
                   u.nombre,
                   u.telefono,
                   u.email
            FROM inscripcion i
            INNER JOIN usuarios u ON i.id_cliente = u.id_usuario
            WHERE i.id_clase = ?
              AND i.estado = 'inscrito'
            ORDER BY u.nombre
        """
        return self.consultar(sql, (id_clase,))

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
        """
        Marca un pago pendiente como abonado y actualiza también el estado del cliente.
        """

        # Primero buscamos el cliente de ese pago
        sql_buscar = """
            SELECT id_cliente
            FROM pago
            WHERE id_pago = ?
        """
        datos = self.consultar(sql_buscar, (id_pago,))

        if not datos:
            raise ValueError("No existe ningún pago con ese ID.")

        id_cliente = datos[0][0]

        # Marcamos el pago como abonado
        sql_pago = """
            UPDATE pago
            SET estado = 'abonado',
                fecha_pago = CURRENT_TIMESTAMP
            WHERE id_pago = ?
        """
        self.ejecutar(sql_pago, (id_pago,))

        # Marcamos el cliente como abonado
        sql_cliente = """
            UPDATE clientes
            SET estado_pagado = 'abonado'
            WHERE id_cliente = ?
        """
        self.ejecutar(sql_cliente, (id_cliente,))

        return True

    def listar_pagos(self) -> list:
        vos = self._pago_dao.select()
        return [(v.id_pago, v.id_cliente, v.id_contable, v.id_tarifa,
                 v.importe, v.metodo_pago, v.fecha_pago, v.estado, v.tipo_cuota)
                for v in vos]

    def pagos_pendientes(self) -> list:
        """
        Devuelve solo pagos reales pendientes.
        La primera columna SIEMPRE es id_pago, porque el controlador la usa
        para marcar el pago como abonado.
        """
        sql = """
            SELECT p.id_pago,
                u.nombre AS cliente,
                t.nombre AS tarifa,
                CONCAT(p.importe, ' €') AS importe,
                DATE(p.fecha_pago) AS fecha,
                p.tipo_cuota
            FROM pago p
            INNER JOIN usuarios u ON p.id_cliente = u.id_usuario
            INNER JOIN tarifa t ON p.id_tarifa = t.id_tarifa
            WHERE p.estado = 'pendiente'
            ORDER BY p.fecha_pago ASC
        """
        return self.consultar(sql)
    
    #-----------
       

    def contable_clientes_con_deuda(self):
        sql = """
            SELECT COUNT(DISTINCT id_cliente)
            FROM pago
            WHERE estado = 'pendiente'
        """
        datos = self.consultar(sql)
        return datos[0][0] if datos else 0

    def contable_importe_pendiente(self):
        sql = """
            SELECT COALESCE(SUM(importe), 0)
            FROM pago
            WHERE estado = 'pendiente'
        """
        datos = self.consultar(sql)
        return datos[0][0] if datos else 0

    def contable_pagos_vencidos(self):
        sql = """
            SELECT COUNT(*)
            FROM pago
            WHERE estado = 'pendiente'
              AND DATE(fecha_pago) < CURRENT_DATE
        """
        datos = self.consultar(sql)
        return datos[0][0] if datos else 0

    def contable_pagos_vencen_semana(self):
        sql = """
            SELECT COUNT(*)
            FROM pago
            WHERE estado = 'pendiente'
              AND DATE(fecha_pago) BETWEEN CURRENT_DATE AND DATE_ADD(CURRENT_DATE, INTERVAL 7 DAY)
        """
        datos = self.consultar(sql)
        return datos[0][0] if datos else 0
    #----------

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
        t = f"%{nombre_tarifa.lower()}%"
        datos = self.consultar(
            """
            SELECT COUNT(*) FROM cliente_tarifa ct
            JOIN tarifa t ON ct.id_tarifa = t.id_tarifa
            WHERE LOWER(t.nombre) LIKE ? AND ct.estado = 'activa'
            """,
            (t,)
        )
        return datos[0][0] if datos else 0

    def generar_informe(self, id_contable: int, tipo: str):
        """
        Genera un informe guardándolo con fecha y hora actuales.
        """
        sql = """
            INSERT INTO informe (id_contable, tipo_informe, fecha_generacion)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """
        return self.ejecutar(sql, (id_contable, tipo))
    
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
        clase = self._clase_dao.selectById(int(id_clase))
        if clase is None:
            raise ValueError("Clase no encontrada")

        vo = ClaseVO(
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

    def ingresos_mes_actual(self):
        datos = self.consultar("""
            SELECT COALESCE(SUM(importe), 0)
            FROM pago
            WHERE estado = 'abonado'
            AND YEAR(fecha_pago) = YEAR(CURDATE())
            AND MONTH(fecha_pago) = MONTH(CURDATE())
        """)
        return datos[0][0] if datos else 0


    def ingresos_anio_actual(self):
        datos = self.consultar("""
            SELECT COALESCE(SUM(importe), 0)
            FROM pago
            WHERE estado = 'abonado'
            AND YEAR(fecha_pago) = YEAR(CURDATE())
        """)
        return datos[0][0] if datos else 0


    def numero_clientes_pendientes_pago(self):
        datos = self.consultar("""
            SELECT COUNT(DISTINCT p.id_cliente)
            FROM pago p
            WHERE p.estado = 'pendiente'
        """)
        return datos[0][0] if datos else 0


    def importe_pendiente_cobrar(self):
        datos = self.consultar("""
            SELECT COALESCE(SUM(importe), 0)
            FROM pago
            WHERE estado = 'pendiente'
        """)
        return datos[0][0] if datos else 0


    def listar_pagos_pendientes_admin(self):
        return self.consultar("""
            SELECT 
                u.nombre,
                u.dni,
                t.nombre,
                p.importe,
                p.fecha_pago,
                p.estado
            FROM pago p
            JOIN usuarios u ON p.id_cliente = u.id_usuario
            JOIN tarifa t ON p.id_tarifa = t.id_tarifa
            WHERE p.estado = 'pendiente'
            ORDER BY p.fecha_pago DESC
        """)


    def buscar_pago_pendiente_por_dni(self, dni):
        d = dni.lower().strip()

        return self.consultar(f"""
            SELECT 
                u.nombre,
                u.dni,
                t.nombre,
                p.importe,
                p.fecha_pago,
                p.estado
            FROM pago p
            JOIN usuarios u ON p.id_cliente = u.id_usuario
            JOIN tarifa t ON p.id_tarifa = t.id_tarifa
            WHERE p.estado = 'pendiente'
            AND LOWER(u.dni) LIKE '%{d}%'
            ORDER BY p.fecha_pago DESC
        """)

    def estadisticas_admin(self):
        clientes_activos = self.consultar("""
            SELECT COUNT(*)
            FROM clientes
        """)

        reservas = self.consultar("""
            SELECT COUNT(*)
            FROM inscripcion
            WHERE estado = 'inscrito'
        """)

        asistencias = self.consultar("""
            SELECT COUNT(*)
            FROM asistencia
            WHERE presente = 'si'
        """)

        clases_activas = self.consultar("""
            SELECT COUNT(*)
            FROM clase
        """)

        entrenadores = self.consultar("""
            SELECT COUNT(*)
            FROM entrenador
        """)

        salas = self.consultar("""
            SELECT COUNT(DISTINCT id_sala)
            FROM clase
        """)

        ocupacion = self.consultar("""
            SELECT COALESCE(ROUND(
                (COUNT(i.id_inscripcion) / NULLIF(SUM(c.aforo_maximo), 0)) * 100
            ), 0)
            FROM clase c
            LEFT JOIN inscripcion i 
                ON c.id_clase = i.id_clase 
            AND i.estado = 'inscrito'
        """)

        return {
            "clientes_activos": clientes_activos[0][0] if clientes_activos else 0,
            "reservas": reservas[0][0] if reservas else 0,
            "asistencias": asistencias[0][0] if asistencias else 0,
            "clases_activas": clases_activas[0][0] if clases_activas else 0,
            "entrenadores": entrenadores[0][0] if entrenadores else 0,
            "salas": salas[0][0] if salas else 0,
            "ocupacion": ocupacion[0][0] if ocupacion else 0
        }


    def ranking_usuarios_activos_estadisticas(self):
        return self.consultar("""
            SELECT 
                u.nombre,
                COUNT(a.id_asistencia) AS asistencias,
                COALESCE(MAX(c.nombre_actividad), '-') AS ultima_clase,
                'Activo' AS estado
            FROM usuarios u
            JOIN clientes cli ON u.id_usuario = cli.id_cliente
            LEFT JOIN asistencia a 
                ON cli.id_cliente = a.id_cliente
            AND a.presente = 'si'
            LEFT JOIN clase c 
                ON a.id_clase = c.id_clase
            GROUP BY u.id_usuario, u.nombre
            ORDER BY asistencias DESC, u.nombre ASC
            LIMIT 8
        """)


    def ocupacion_por_clase_estadisticas(self):
        return self.consultar("""
            SELECT 
                c.nombre_actividad,
                COALESCE(ROUND(
                    (COUNT(i.id_inscripcion) / NULLIF(c.aforo_maximo, 0)) * 100
                ), 0) AS ocupacion
            FROM clase c
            LEFT JOIN inscripcion i 
                ON c.id_clase = i.id_clase 
            AND i.estado = 'inscrito'
            GROUP BY c.id_clase, c.nombre_actividad, c.aforo_maximo
            ORDER BY ocupacion DESC
            LIMIT 4
        """)
    

    def clases_entrenador_tabla(self, id_entrenador):
        """
        Devuelve las clases de un entrenador en formato preparado para tablas:
        Clase, Sala, Horario, Día y Capacidad.
        """
        sql = """
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
        """
        return self.consultar(sql, (id_entrenador,))

    def ocupacion_clases_entrenador(self, id_entrenador):
        """
        Devuelve la ocupación de las clases de un entrenador.
        Formato:
        id_clase, nombre_actividad, inscritos, aforo_maximo, ocupacion
        """
        sql = """
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
        """
        return self.consultar(sql, (id_entrenador,))

    def informacion_clase_con_sala(self, id_clase):
        """
        Devuelve la información completa de una clase junto con la sala.
        Se usa en Clientes inscritos para actualizar la tarjeta superior.
        """
        sql = """
            SELECT c.nombre_actividad,
                   s.nombre,
                   c.dia_semana,
                   c.hora_inicio,
                   c.hora_fin,
                   c.aforo_maximo
            FROM clase c
            INNER JOIN sala s ON c.id_sala = s.id_sala
            WHERE c.id_clase = ?
        """
        datos = self.consultar(sql, (id_clase,))
        return datos[0] if datos else None

    def buscar_clase(self, id_clase):
        """
        Busca una clase por ID.
        Devuelve SELECT * para mantener los índices que usa ControladorEntrenador:
        clase[3] = nombre_actividad
        clase[5] = dia_semana
        clase[6] = hora_inicio
        clase[7] = hora_fin
        """
        sql = """
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
        """
        datos = self.consultar(sql, (id_clase,))
        return datos[0] if datos else None

    def asistencia_clase_fecha(self, id_clase, fecha):
        """
        Devuelve la asistencia registrada de una clase en una fecha concreta.
        Sirve para que al volver a abrir la pantalla aparezca si/no y no Pendiente.
        """
        sql = """
            SELECT id_cliente,
                   presente
            FROM asistencia
            WHERE id_clase = ?
              AND fecha = ?
            ORDER BY id_asistencia
        """
        return self.consultar(sql, (id_clase, fecha))

    def registrar_asistencia(self, id_cliente, id_clase, fecha, presente):
        """
        Registra o actualiza la asistencia de un cliente para una clase y fecha.
        Primero borra la asistencia previa de ese día para evitar duplicados.
        """
        sql_delete = """
            DELETE FROM asistencia
            WHERE id_cliente = ?
              AND id_clase = ?
              AND fecha = ?
        """
        self.ejecutar(sql_delete, (id_cliente, id_clase, fecha))

        sql_insert = """
            INSERT INTO asistencia (id_cliente, id_clase, fecha, presente)
            VALUES (?, ?, ?, ?)
        """
        return self.ejecutar(sql_insert, (id_cliente, id_clase, fecha, presente))

    
    #CONTABLE

    def cobros_hoy_contable(self):
        """
        Cuenta los pagos abonados registrados hoy.
        """
        sql = """
            SELECT COUNT(*)
            FROM pago
            WHERE estado = 'abonado'
              AND DATE(fecha_pago) = CURRENT_DATE
        """
        datos = self.consultar(sql)
        return datos[0][0] if datos else 0

    def ultimos_pagos_inicio_contable(self):
        """
        Devuelve los últimos pagos para la tabla de inicio del contable.
        Formato:
        Cliente, Tarifa, Importe, Fecha, Estado
        """
        sql = """
            SELECT u.nombre AS cliente,
                   t.nombre AS tarifa,
                   CONCAT(p.importe, ' €') AS importe,
                   DATE(p.fecha_pago) AS fecha,
                   p.estado
            FROM pago p
            INNER JOIN usuarios u ON p.id_cliente = u.id_usuario
            INNER JOIN tarifa t ON p.id_tarifa = t.id_tarifa
            ORDER BY p.fecha_pago DESC
            LIMIT 10
        """
        return self.consultar(sql)

    def pagos_pendientes_inicio_contable(self):
        """
        Devuelve los clientes con pagos pendientes para la tabla de inicio.
        Formato:
        Cliente, Importe pendiente, Fecha límite
        """
        sql = """
            SELECT u.nombre AS cliente,
                   CONCAT(p.importe, ' €') AS importe_pendiente,
                   DATE(p.fecha_pago) AS fecha_limite
            FROM pago p
            INNER JOIN usuarios u ON p.id_cliente = u.id_usuario
            WHERE p.estado = 'pendiente'
            ORDER BY p.fecha_pago ASC
        """
        return self.consultar(sql)

    def num_pagos_pendientes_contable(self):
        """
        Cuenta los pagos pendientes registrados.
        """
        sql = """
            SELECT COUNT(*)
            FROM pago
            WHERE estado = 'pendiente'
        """
        datos = self.consultar(sql)
        return datos[0][0] if datos else 0

    def ingresos_mes_contable(self):
        """
        Calcula los ingresos abonados del mes actual.
        """
        sql = """
            SELECT COALESCE(SUM(importe), 0)
            FROM pago
            WHERE estado = 'abonado'
              AND YEAR(fecha_pago) = YEAR(CURRENT_DATE)
              AND MONTH(fecha_pago) = MONTH(CURRENT_DATE)
        """
        datos = self.consultar(sql)
        return datos[0][0] if datos else 0

    def num_tarifas_activas_contable(self):
        """
        Cuenta las tarifas activas.
        """
        sql = """
            SELECT COUNT(*)
            FROM tarifa
            WHERE fecha_fin IS NULL OR fecha_fin >= CURRENT_DATE
        """
        datos = self.consultar(sql)
        return datos[0][0] if datos else 0

    def num_informes_mes_contable(self):
        """
        Cuenta los informes generados durante el mes actual.
        """
        sql = """
            SELECT COUNT(*)
            FROM informe
            WHERE YEAR(fecha_generacion) = YEAR(CURRENT_DATE)
              AND MONTH(fecha_generacion) = MONTH(CURRENT_DATE)
        """
        datos = self.consultar(sql)
        return datos[0][0] if datos else 0
    


    def buscar_cliente_tarifa_por_dni(self, dni):
        """
        Busca un cliente por DNI y devuelve su tarifa activa.
        Formato:
        id_cliente, nombre, dni, id_tarifa, nombre_tarifa, precio_mensual
        """
        sql = """
            SELECT u.id_usuario,
                   u.nombre,
                   u.dni,
                   t.id_tarifa,
                   t.nombre,
                   t.precio_mensual
            FROM usuarios u
            INNER JOIN clientes c ON u.id_usuario = c.id_cliente
            INNER JOIN cliente_tarifa ct ON c.id_cliente = ct.id_cliente
            INNER JOIN tarifa t ON ct.id_tarifa = t.id_tarifa
            WHERE u.dni = ?
              AND ct.estado = 'activa'
            LIMIT 1
        """
        datos = self.consultar(sql, (dni,))
        return datos[0] if datos else None

    def registrar_pago_contable(self, dni_cliente, id_contable, metodo_pago, fecha_pago):
        """
        Registra el pago de un cliente usando su DNI.
        Si ya existe un pago pendiente, lo actualiza a abonado.
        Si no existe pago pendiente, crea un pago nuevo.
        """
        cliente = self.buscar_cliente_tarifa_por_dni(dni_cliente)

        if not cliente:
            return False, "No se ha encontrado ningún cliente con ese DNI o no tiene tarifa activa."

        id_cliente = cliente[0]
        nombre_cliente = cliente[1]
        id_tarifa = cliente[3]
        nombre_tarifa = cliente[4]
        importe = cliente[5]

        # Comprobar si ya existe un pago abonado de ese cliente en el mismo mes
        sql_ya_abonado = """
            SELECT id_pago
            FROM pago
            WHERE id_cliente = ?
              AND estado = 'abonado'
              AND YEAR(fecha_pago) = YEAR(?)
              AND MONTH(fecha_pago) = MONTH(?)
            LIMIT 1
        """
        ya_abonado = self.consultar(sql_ya_abonado, (id_cliente, fecha_pago, fecha_pago))

        if ya_abonado:
            return False, f"El cliente {nombre_cliente} ya tiene un pago abonado en ese mes."

        # Buscar si ya existe un pago pendiente de ese cliente
        sql_pendiente = """
            SELECT id_pago
            FROM pago
            WHERE id_cliente = ?
              AND estado = 'pendiente'
            ORDER BY fecha_pago DESC
            LIMIT 1
        """
        pendiente = self.consultar(sql_pendiente, (id_cliente,))

        if pendiente:
            id_pago = pendiente[0][0]

            sql_update = """
                UPDATE pago
                SET estado = 'abonado',
                    metodo_pago = ?,
                    fecha_pago = ?,
                    id_contable = ?
                WHERE id_pago = ?
            """
            self.ejecutar(sql_update, (metodo_pago, fecha_pago, id_contable, id_pago))

        else:
            sql_insert = """
                INSERT INTO pago
                (id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago, estado, tipo_cuota)
                VALUES (?, ?, ?, ?, ?, ?, 'abonado', 'mensual')
            """
            self.ejecutar(sql_insert, (id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago))

        # Actualizar estado del cliente
        sql_cliente = """
            UPDATE clientes
            SET estado_pagado = 'abonado'
            WHERE id_cliente = ?
        """
        self.ejecutar(sql_cliente, (id_cliente,))

        mensaje = f"Pago registrado correctamente para {nombre_cliente}.\nTarifa: {nombre_tarifa}\nImporte: {importe} €"
        return True, mensaje
    
    def contable_tarifas_economica(self):
        """
        Devuelve las tarifas activas para la pantalla Gestión económica.
        Formato: Plan, Precio, Duración
        """
        sql = """
            SELECT nombre,
                   CONCAT(precio_mensual, ' €') AS precio,
                   'Mensual' AS duracion
            FROM tarifa
            WHERE fecha_fin IS NULL OR fecha_fin >= CURRENT_DATE
            ORDER BY precio_mensual ASC
        """
        return self.consultar(sql)

    def contable_salarios_personal(self):
        """
        Devuelve los salarios del personal.
        Formato: Empleado, Rol, Salario
        """
        sql = """
            SELECT u.nombre,
                   r.nombre_rol,
                   CONCAT(e.salario, ' €') AS salario
            FROM empleados e
            INNER JOIN usuarios u ON e.id_empleado = u.id_usuario
            INNER JOIN roles r ON u.id_rol = r.id_rol
            ORDER BY r.nombre_rol, u.nombre
        """
        return self.consultar(sql)

    def contable_total_nominas(self):
        """
        Suma todos los salarios del personal.
        """
        sql = """
            SELECT COALESCE(SUM(salario), 0)
            FROM empleados
        """
        datos = self.consultar(sql)
        return datos[0][0] if datos else 0

    def contable_balance_economico(self):
        """
        Calcula ingresos, gastos y balance.
        Ingresos: pagos abonados.
        Gastos: salarios del personal.
        """
        ingresos = self.consultar("""
            SELECT COALESCE(SUM(importe), 0)
            FROM pago
            WHERE estado = 'abonado'
        """)

        gastos = self.consultar("""
            SELECT COALESCE(SUM(salario), 0)
            FROM empleados
        """)

        total_ingresos = ingresos[0][0] if ingresos else 0
        total_gastos = gastos[0][0] if gastos else 0
        balance = total_ingresos - total_gastos

        return total_ingresos, total_gastos, balance
    
    def informe_balance_mensual_contable(self):
        sql = """
            SELECT YEAR(fecha_pago) AS anio,
                MONTH(fecha_pago) AS mes,
                COALESCE(SUM(importe), 0) AS ingresos
            FROM pago
            WHERE estado = 'abonado'
            GROUP BY YEAR(fecha_pago), MONTH(fecha_pago)
            ORDER BY anio DESC, mes DESC
        """

        ingresos_mensuales = self.consultar(sql)

        # Gasto mensual estimado = suma total de salarios / 12
        # Es una estimación razonable mientras no haya tabla de gastos por mes
        total_nominas = self.contable_total_nominas()
        gasto_mensual = total_nominas / 12 if total_nominas else 0

        resultado = []

        for fila in ingresos_mensuales:
            anio = fila[0]
            mes = fila[1]
            ingresos = fila[2]
            balance = ingresos - gasto_mensual  # ahora el gasto es proporcional

            resultado.append((
                anio,
                mes,
                f"{float(ingresos):.2f} €",
                f"{float(gasto_mensual):.2f} €",
                f"{float(balance):.2f} €"
            ))

        return resultado
    
    def informe_gestion_economica_contable(self):
        """
        Devuelve un resumen económico general para el informe de gestión económica.
        Formato: Concepto, Valor
        """

        ingresos, gastos, balance = self.contable_balance_economico()
        pendiente = self.contable_importe_pendiente()
        tarifas_activas = self.num_tarifas_activas_contable()
        nominas = self.contable_total_nominas()

        return [
            ("Ingresos abonados", f"{float(ingresos):.2f} €"),
            ("Gastos / nóminas", f"{float(gastos):.2f} €"),
            ("Balance", f"{float(balance):.2f} €"),
            ("Pagos pendientes", f"{float(pendiente):.2f} €"),
            ("Tarifas activas", str(tarifas_activas)),
            ("Total nóminas", f"{float(nominas):.2f} €"),
        ]

    def contable_gastos_mes(self):
        """
        Calcula los gastos del mes.
        De momento usamos la suma de salarios como gasto mensual.
        """
        sql = """
            SELECT COALESCE(SUM(salario), 0)
            FROM empleados
        """
        datos = self.consultar(sql)
        return datos[0][0] if datos else 0

    def contable_balance_mes(self):
        """
        Calcula el balance del mes:
        ingresos abonados del mes - gastos del mes.
        """
        ingresos = self.ingresos_mes_contable()
        gastos = self.contable_gastos_mes()
        return ingresos - gastos

    def historial_informes_contable(self):
        """
        Devuelve el historial de informes generados.
        """
        sql = """
            SELECT i.id_informe,
                   u.nombre AS contable,
                   i.tipo_informe,
                   DATE(i.fecha_generacion) AS fecha
            FROM informe i
            INNER JOIN usuarios u ON i.id_contable = u.id_usuario
            ORDER BY i.fecha_generacion DESC
        """
        return self.consultar(sql)
    
    def contable_pagos_registrados(self, id_contable):
        """
        Cuenta los pagos abonados registrados por este contable.
        """
        sql = """
            SELECT COUNT(*)
            FROM pago
            WHERE id_contable = ?
              AND estado = 'abonado'
        """
        datos = self.consultar(sql, (id_contable,))
        return datos[0][0] if datos else 0


    def contable_pendientes_revisados(self):
        """
        Cuenta los pagos pendientes actuales.
        """
        sql = """
            SELECT COUNT(*)
            FROM pago
            WHERE estado = 'pendiente'
        """
        datos = self.consultar(sql)
        return datos[0][0] if datos else 0


    def contable_informes_generados_usuario(self, id_contable):
        """
        Cuenta los informes generados por este contable.
        """
        sql = """
            SELECT COUNT(*)
            FROM informe
            WHERE id_contable = ?
        """
        datos = self.consultar(sql, (id_contable,))
        return datos[0][0] if datos else 0


    def contable_importe_gestionado(self, id_contable):
        """
        Suma el importe abonado gestionado por este contable.
        """
        sql = """
            SELECT COALESCE(SUM(importe), 0)
            FROM pago
            WHERE id_contable = ?
              AND estado = 'abonado'
        """
        datos = self.consultar(sql, (id_contable,))
        return datos[0][0] if datos else 0

    #-----------------------



    def recepcion_total_clientes(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM clientes
        """)
        return datos[0][0] if datos else 0


    def recepcion_entradas_hoy(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM registro_acceso
            WHERE tipo_acceso = 'entrada'
            AND DATE(fecha_hora_registro) = CURDATE()
        """)
        return datos[0][0] if datos else 0


    def recepcion_nuevos_usuarios_hoy(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM usuarios
            WHERE DATE(fecha_registro) = CURDATE()
        """)
        return datos[0][0] if datos else 0


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


    def recepcion_ultimos_registros_acceso(self):
        return self.consultar("""
            SELECT 
                u.nombre,
                u.dni,
                r.tipo_acceso,
                r.fecha_hora_registro
            FROM registro_acceso r
            JOIN usuarios u ON r.id_usuario = u.id_usuario
            ORDER BY r.fecha_hora_registro DESC
            LIMIT 8
        """)


    def recepcion_clientes_recientes(self):
        return self.consultar("""
            SELECT 
                u.nombre,
                u.dni,
                u.telefono,
                u.fecha_registro
            FROM usuarios u
            JOIN clientes c ON u.id_usuario = c.id_cliente
            ORDER BY u.fecha_registro DESC
            LIMIT 8
        """)

    def crear_cliente_desde_recepcion(
        self,
        dni,
        nombre,
        telefono,
        email,
        username,
        password,
        direccion,
        fecha_nacimiento,
        es_menor=False,
        dni_tutor="",
        nombre_tutor=""
    ):
        usuario_existente = self._usuario_dao.selectByUsername(username)
        if usuario_existente is not None:
            raise ValueError("Ya existe un usuario con ese nombre de usuario")

        id_cliente = self.crear_usuario_completo(
            dni=dni,
            nombre=nombre,
            telefono=telefono,
            email=email,
            username=username,
            password=password,
            id_rol=1,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            id_admin_registra=None
        )

        if es_menor:
            menor_vo = MenorVO(
                id_cliente=id_cliente,
                dni_tutor=dni_tutor,
                nombre_tutor=nombre_tutor
            )
            self._menor_dao.insert(menor_vo)

        return id_cliente
    
        

    def buscar_cliente_acceso_por_dni_o_id(self, texto):
        texto = str(texto).strip()

        if texto.isdigit():
            sql = """
                SELECT u.id_usuario,
                    u.dni,
                    u.nombre,
                    c.estado_pagado
                FROM usuarios u
                INNER JOIN clientes c ON u.id_usuario = c.id_cliente
                WHERE u.id_usuario = ?
                LIMIT 1
            """
            datos = self.consultar(sql, (int(texto),))
        else:
            sql = """
                SELECT u.id_usuario,
                    u.dni,
                    u.nombre,
                    c.estado_pagado
                FROM usuarios u
                INNER JOIN clientes c ON u.id_usuario = c.id_cliente
                WHERE LOWER(u.dni) = LOWER(?)
                LIMIT 1
            """
            datos = self.consultar(sql, (texto,))

        return datos[0] if datos else None


    def ultimo_acceso_cliente(self, id_usuario):
        sql = """
            SELECT tipo_acceso
            FROM registro_acceso
            WHERE id_usuario = ?
            ORDER BY fecha_hora_registro DESC
            LIMIT 1
        """
        datos = self.consultar(sql, (id_usuario,))
        return datos[0][0] if datos else None


    def registrar_acceso_cliente_control(self, id_usuario, tipo_acceso):
        tipo_acceso = tipo_acceso.lower().strip()

        if tipo_acceso not in ("entrada", "salida"):
            raise ValueError("Tipo de acceso no válido")

        ultimo = self.ultimo_acceso_cliente(id_usuario)

        if tipo_acceso == "salida" and ultimo != "entrada":
            raise ValueError("No se puede registrar una salida sin una entrada previa")

        if tipo_acceso == "entrada" and ultimo == "entrada":
            raise ValueError("Este cliente ya tiene una entrada registrada sin salida")

        return self.registrar_acceso(id_usuario, tipo_acceso)


    def listar_ultimos_accesos_control(self):
        return self.consultar("""
            SELECT u.nombre,
                u.dni,
                r.tipo_acceso,
                r.fecha_hora_registro
            FROM registro_acceso r
            INNER JOIN usuarios u ON r.id_usuario = u.id_usuario
            ORDER BY r.fecha_hora_registro DESC
            LIMIT 20
        """)

    def recepcion_total_clientes_lista(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM clientes
        """)
        return datos[0][0] if datos else 0


    def recepcion_nuevos_clientes_mes(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM usuarios u
            INNER JOIN clientes c ON u.id_usuario = c.id_cliente
            WHERE YEAR(u.fecha_registro) = YEAR(CURRENT_DATE)
            AND MONTH(u.fecha_registro) = MONTH(CURRENT_DATE)
        """)
        return datos[0][0] if datos else 0


    def recepcion_listar_clientes_filtrados(self, dni="", tipo="Todos", plan="Todos"):
        condiciones = []
        parametros = []

        if dni:
            condiciones.append("LOWER(u.dni) LIKE LOWER(?)")
            parametros.append(f"%{dni}%")

        if tipo and tipo.lower() != "todos":
            if tipo.lower() == "menor":
                condiciones.append("m.id_cliente IS NOT NULL")
            elif tipo.lower() == "adulto":
                condiciones.append("m.id_cliente IS NULL")

        if plan and plan.lower() != "todos":
            condiciones.append("LOWER(t.nombre) LIKE LOWER(?)")
            parametros.append(f"%{plan}%")

        where = ""
        if condiciones:
            where = "WHERE " + " AND ".join(condiciones)

        sql = f"""
            SELECT 
                u.id_usuario,
                u.dni,
                u.nombre,
                u.telefono,
                u.email,
                u.direccion,
                u.fecha_nacimiento,
                c.estado_pagado,
                CASE 
                    WHEN m.id_cliente IS NOT NULL THEN 'Menor'
                    ELSE 'Adulto'
                END AS tipo_cliente,
                COALESCE(t.nombre, 'Sin plan') AS plan
            FROM usuarios u
            INNER JOIN clientes c ON u.id_usuario = c.id_cliente
            LEFT JOIN menor m ON c.id_cliente = m.id_cliente
            LEFT JOIN cliente_tarifa ct 
                ON c.id_cliente = ct.id_cliente 
            AND ct.estado = 'activa'
            LEFT JOIN tarifa t ON ct.id_tarifa = t.id_tarifa
            {where}
            ORDER BY u.nombre
        """

        return self.consultar(sql, tuple(parametros))


    def recepcion_guardar_cambios_cliente(self, id_cliente, dni, nombre, telefono, email, direccion, fecha_nacimiento, estado_pagado):
        sql_usuario = """
            UPDATE usuarios
            SET dni = ?,
                nombre = ?,
                telefono = ?,
                email = ?,
                direccion = ?,
                fecha_nacimiento = ?
            WHERE id_usuario = ?
        """
        self.ejecutar(sql_usuario, (
            dni,
            nombre,
            telefono,
            email,
            direccion,
            fecha_nacimiento,
            id_cliente
        ))

        sql_cliente = """
            UPDATE clientes
            SET estado_pagado = ?
            WHERE id_cliente = ?
        """
        self.ejecutar(sql_cliente, (estado_pagado, id_cliente))

        return True