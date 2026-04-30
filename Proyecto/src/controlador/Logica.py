"""
Logica.py — Capa Modelo de StayFit
Gestiona la conexión con SQL Server y expone los métodos
que los controladores necesitan según los 16 casos de uso.
"""

import hashlib
import pyodbc
from datetime import date, datetime


# ──────────────────────────────────────────────────────────────────────
# Configuración de conexión  (ajustar según entorno)
# ──────────────────────────────────────────────────────────────────────
DRIVER   = "ODBC Driver 17 for SQL Server"
SERVER   = "localhost"
DATABASE = "Stayfit"
UID      = "sa"
PWD      = "tu_contraseña"      # Cambiar por la contraseña real


def _hash_password(password: str) -> str:
    """SHA-256 simple. En producción usar bcrypt."""
    return hashlib.sha256(password.encode()).hexdigest()


class Logica:
    """
    Interfaz entre los controladores y la base de datos SQL Server.
    Cada método devuelve datos como lista de dicts o tuplas (ok, mensaje).
    """

    # ------------------------------------------------------------------
    # Conexión
    # ------------------------------------------------------------------
    def _conectar(self):
        conn_str = (
            f"DRIVER={{{DRIVER}}};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"UID={UID};"
            f"PWD={PWD};"
            "TrustServerCertificate=yes;"
        )
        return pyodbc.connect(conn_str)

    def _ejecutar_consulta(self, sql, params=()):
        """Devuelve lista de dicts o [] en caso de error."""
        try:
            with self._conectar() as conn:
                cur = conn.cursor()
                cur.execute(sql, params)
                cols = [c[0] for c in cur.description]
                return [dict(zip(cols, row)) for row in cur.fetchall()]
        except Exception as e:
            print(f"[ERROR consulta] {e}")
            return []

    def _ejecutar_comando(self, sql, params=()):
        """Ejecuta INSERT/UPDATE/DELETE. Devuelve (True, msg) o (False, msg)."""
        try:
            with self._conectar() as conn:
                cur = conn.cursor()
                cur.execute(sql, params)
                conn.commit()
                return True, "Operación realizada correctamente."
        except pyodbc.IntegrityError as e:
            return False, f"Error de integridad: {e}"
        except Exception as e:
            return False, f"Error en la base de datos: {e}"

    # ==================================================================
    # UC1 · Autenticación
    # ==================================================================
    def autenticar_usuario(self, username: str, password: str):
        """
        Devuelve dict con datos del usuario si las credenciales son correctas,
        o None si no coinciden.
        """
        pw_hash = _hash_password(password)
        sql = """
            SELECT u.id_usuario, u.nombre, u.email, u.username,
                   r.nombre_rol
            FROM   usuarios u
            JOIN   roles    r ON u.id_rol = r.id_rol
            WHERE  u.username = ? AND u.password_hash = ?
        """
        resultado = self._ejecutar_consulta(sql, (username, pw_hash))
        return resultado[0] if resultado else None

    # ==================================================================
    # UC2 · Registrar nuevo usuario
    # ==================================================================
    def registrar_nuevo_cliente(self, datos: dict):
        """Registra un cliente (recepcionista) con rol 'cliente'."""
        sql_usuario = """
            INSERT INTO usuarios
                (dni, nombre, telefono, email, username,
                 password_hash, id_rol, direccion, fecha_nacimiento)
            VALUES (?, ?, ?, ?, ?, ?,
                    (SELECT id_rol FROM roles WHERE nombre_rol = 'cliente'),
                    ?, ?)
        """
        pw_hash = _hash_password(datos["password"])
        ok, msg = self._ejecutar_comando(
            sql_usuario,
            (datos["dni"], datos["nombre"], datos["telefono"],
             datos["email"], datos["username"], pw_hash,
             datos["direccion"], datos["fecha_nacimiento"])
        )
        if not ok:
            return False, msg
        # Insertar en la tabla clientes (el trigger clasifica menor/adulto)
        sql_id = "SELECT id_usuario FROM usuarios WHERE username = ?"
        fila = self._ejecutar_consulta(sql_id, (datos["username"],))
        if not fila:
            return False, "No se pudo recuperar el ID del usuario recién creado."
        id_nuevo = fila[0]["id_usuario"]
        ok2, msg2 = self._ejecutar_comando(
            "INSERT INTO clientes (id_cliente) VALUES (?)", (id_nuevo,)
        )
        return ok2, msg2

    def registrar_nuevo_trabajador(self, datos: dict, id_administrador: int):
        """Registra un empleado con el rol indicado en datos['rol']."""
        pw_hash = _hash_password(datos["password"])
        sql_usuario = """
            INSERT INTO usuarios
                (dni, nombre, telefono, email, username,
                 password_hash, id_rol, direccion, fecha_nacimiento)
            VALUES (?, ?, ?, ?, ?, ?,
                    (SELECT id_rol FROM roles WHERE nombre_rol = ?),
                    ?, ?)
        """
        ok, msg = self._ejecutar_comando(
            sql_usuario,
            (datos["dni"], datos["nombre"], datos["telefono"],
             datos["email"], datos["username"], pw_hash,
             datos["rol"], datos["direccion"], datos["fecha_nacimiento"])
        )
        if not ok:
            return False, msg

        sql_id = "SELECT id_usuario FROM usuarios WHERE username = ?"
        fila = self._ejecutar_consulta(sql_id, (datos["username"],))
        if not fila:
            return False, "No se pudo recuperar el ID del trabajador."
        id_nuevo = fila[0]["id_usuario"]

        # Insertar en empleados
        salario = float(datos.get("salario", 0))
        ok2, msg2 = self._ejecutar_comando(
            "INSERT INTO empleados (id_empleado, salario) VALUES (?, ?)",
            (id_nuevo, salario)
        )
        if not ok2:
            return False, msg2

        # Insertar en tabla específica del rol
        rol = datos["rol"]
        if rol == "entrenador":
            ok3, msg3 = self._ejecutar_comando(
                "INSERT INTO entrenador (id_entrenador, especialidad, id_administrador_registra) VALUES (?, ?, ?)",
                (id_nuevo, datos.get("especialidad", ""), id_administrador)
            )
        elif rol == "recepcionista":
            ok3, msg3 = self._ejecutar_comando(
                "INSERT INTO recepcionista (id_recepcionista, turno, id_administrador_registra) VALUES (?, ?, ?)",
                (id_nuevo, datos.get("turno", ""), id_administrador)
            )
        elif rol == "contable":
            ok3, msg3 = self._ejecutar_comando(
                "INSERT INTO contable (id_contable, titulacion, id_administrador_registra) VALUES (?, ?, ?)",
                (id_nuevo, datos.get("titulacion", ""), id_administrador)
            )
        elif rol == "administrador":
            ok3, msg3 = self._ejecutar_comando(
                "INSERT INTO administrador (id_administrador) VALUES (?)",
                (id_nuevo,)
            )
        else:
            return False, f"Rol '{rol}' no soportado para trabajadores."

        return ok3, msg3

    # ==================================================================
    # UC3 · Inscribirse a una clase
    # ==================================================================
    def obtener_clases_disponibles(self, id_cliente: int):
        """
        Clases con plazas libres, que el cliente no tenga ya inscrita.
        """
        sql = """
            SELECT c.id_clase,
                   c.nombre_actividad,
                   c.dia_semana,
                   CONVERT(VARCHAR(5), c.hora_inicio, 108) AS hora_inicio,
                   CONVERT(VARCHAR(5), c.hora_fin,    108) AS hora_fin,
                   u.nombre   AS entrenador,
                   s.nombre   AS sala,
                   c.nivel_intensidad,
                   c.aforo_maximo
                   - (SELECT COUNT(*) FROM inscripcion i2
                      WHERE i2.id_clase = c.id_clase
                        AND i2.estado = 'inscrito') AS plazas_libres
            FROM   clase       c
            JOIN   entrenador  e ON c.id_entrenador = e.id_entrenador
            JOIN   usuarios    u ON e.id_entrenador = u.id_usuario
            JOIN   sala        s ON c.id_sala = s.id_sala
            WHERE  c.aforo_maximo > (
                       SELECT COUNT(*) FROM inscripcion i3
                       WHERE i3.id_clase = c.id_clase
                         AND i3.estado = 'inscrito'
                   )
              AND  c.id_clase NOT IN (
                       SELECT id_clase FROM inscripcion
                       WHERE id_cliente = ? AND estado = 'inscrito'
                   )
        """
        return self._ejecutar_consulta(sql, (id_cliente,))

    def inscribir_cliente_clase(self, id_cliente: int, id_clase: int):
        # Verificar tarifa activa
        sql_tarifa = """
            SELECT 1 FROM cliente_tarifa
            WHERE id_cliente = ? AND estado = 'activa'
        """
        if not self._ejecutar_consulta(sql_tarifa, (id_cliente,)):
            return False, "No tienes una tarifa activa. Contacta con recepción."

        # Verificar pagos pendientes
        sql_pago = """
            SELECT 1 FROM pago
            WHERE id_cliente = ? AND estado = 'pendiente'
        """
        if self._ejecutar_consulta(sql_pago, (id_cliente,)):
            return False, "Tienes pagos pendientes. Regulariza tu situación antes de inscribirte."

        # Verificar que no esté ya inscrito
        sql_dup = """
            SELECT 1 FROM inscripcion
            WHERE id_cliente = ? AND id_clase = ? AND estado = 'inscrito'
        """
        if self._ejecutar_consulta(sql_dup, (id_cliente, id_clase)):
            return False, "Ya estás inscrito en esta clase."

        # Verificar aforo
        sql_aforo = """
            SELECT c.aforo_maximo - COUNT(i.id_inscripcion) AS libres
            FROM clase c
            LEFT JOIN inscripcion i ON c.id_clase = i.id_clase AND i.estado = 'inscrito'
            WHERE c.id_clase = ?
            GROUP BY c.aforo_maximo
        """
        res = self._ejecutar_consulta(sql_aforo, (id_clase,))
        if not res or res[0]["libres"] <= 0:
            return False, "La clase está completa. No quedan plazas disponibles."

        # Insertar inscripción
        sql_ins = """
            INSERT INTO inscripcion (id_cliente, id_clase)
            VALUES (?, ?)
        """
        return self._ejecutar_comando(sql_ins, (id_cliente, id_clase))

    def obtener_inscripciones_cliente(self, id_cliente: int):
        sql = """
            SELECT c.nombre_actividad,
                   c.dia_semana,
                   CONVERT(VARCHAR(5), c.hora_inicio, 108) AS hora_inicio,
                   s.nombre AS sala,
                   i.estado,
                   CONVERT(VARCHAR(16), i.fecha_inscripcion, 120) AS fecha_inscripcion
            FROM   inscripcion i
            JOIN   clase       c ON i.id_clase = c.id_clase
            JOIN   sala        s ON c.id_sala  = s.id_sala
            WHERE  i.id_cliente = ?
            ORDER  BY i.fecha_inscripcion DESC
        """
        return self._ejecutar_consulta(sql, (id_cliente,))

    # ==================================================================
    # UC4 · Registrar asistencia
    # ==================================================================
    def obtener_clases_entrenador(self, id_entrenador: int):
        sql = """
            SELECT c.id_clase,
                   c.nombre_actividad,
                   c.dia_semana,
                   CONVERT(VARCHAR(5), c.hora_inicio, 108) AS hora_inicio,
                   CONVERT(VARCHAR(5), c.hora_fin,    108) AS hora_fin,
                   s.nombre AS sala,
                   (SELECT COUNT(*) FROM inscripcion i
                    WHERE i.id_clase = c.id_clase AND i.estado = 'inscrito') AS total_inscritos
            FROM   clase c
            JOIN   sala  s ON c.id_sala = s.id_sala
            WHERE  c.id_entrenador = ?
            ORDER  BY c.dia_semana, c.hora_inicio
        """
        return self._ejecutar_consulta(sql, (id_entrenador,))

    def obtener_inscritos_clase(self, id_clase: int):
        sql = """
            SELECT u.id_usuario AS id_cliente,
                   u.nombre,
                   u.dni,
                   u.email,
                   CONVERT(VARCHAR(16), i.fecha_inscripcion, 120) AS fecha_inscripcion
            FROM   inscripcion i
            JOIN   usuarios    u ON i.id_cliente = u.id_usuario
            WHERE  i.id_clase = ? AND i.estado = 'inscrito'
            ORDER  BY u.nombre
        """
        return self._ejecutar_consulta(sql, (id_clase,))

    def registrar_asistencia(self, id_clase: int, lista_asistencia: list):
        """
        lista_asistencia = [(id_cliente, 'si'|'no'), ...]
        Inserta o actualiza registros de asistencia para la fecha de hoy.
        """
        hoy = date.today().isoformat()
        errores = []
        for id_cliente, presente in lista_asistencia:
            # Si ya existe para hoy, actualizar; si no, insertar
            sql_exists = """
                SELECT id_asistencia FROM asistencia
                WHERE id_cliente = ? AND id_clase = ? AND fecha = ?
            """
            existe = self._ejecutar_consulta(sql_exists, (id_cliente, id_clase, hoy))
            if existe:
                sql = "UPDATE asistencia SET presente = ? WHERE id_asistencia = ?"
                ok, msg = self._ejecutar_comando(
                    sql, (presente, existe[0]["id_asistencia"])
                )
            else:
                sql = """
                    INSERT INTO asistencia (id_cliente, id_clase, fecha, presente)
                    VALUES (?, ?, ?, ?)
                """
                ok, msg = self._ejecutar_comando(
                    sql, (id_cliente, id_clase, hoy, presente)
                )
            if not ok:
                errores.append(str(id_cliente))

        if errores:
            return False, f"Error al guardar asistencia de: {', '.join(errores)}"

        # Actualizar calorías acumuladas para los que asistieron
        self._actualizar_calorias_por_clase(id_clase, lista_asistencia)
        return True, "Asistencia registrada correctamente."

    def _actualizar_calorias_por_clase(self, id_clase: int, lista_asistencia: list):
        sql_cal = "SELECT calorias_estimadas FROM clase WHERE id_clase = ?"
        res = self._ejecutar_consulta(sql_cal, (id_clase,))
        if not res:
            return
        calorias = res[0]["calorias_estimadas"]
        for id_cliente, presente in lista_asistencia:
            if presente == "si":
                self._ejecutar_comando(
                    "UPDATE clientes SET calorias_acumuladas = calorias_acumuladas + ? WHERE id_cliente = ?",
                    (calorias, id_cliente)
                )

    # ==================================================================
    # UC6 · Registrar pago
    # ==================================================================
    def registrar_pago(self, id_pago: int, id_contable: int, metodo_pago: str):
        # Verificar que el pago existe y está pendiente
        sql_check = "SELECT estado FROM pago WHERE id_pago = ?"
        res = self._ejecutar_consulta(sql_check, (id_pago,))
        if not res:
            return False, "El pago indicado no existe en el sistema."
        if res[0]["estado"] == "abonado":
            return False, "Este pago ya ha sido registrado anteriormente."

        sql = """
            UPDATE pago
            SET estado = 'abonado',
                id_contable  = ?,
                metodo_pago  = ?,
                fecha_pago   = GETDATE()
            WHERE id_pago = ?
        """
        ok, msg = self._ejecutar_comando(sql, (id_contable, metodo_pago, id_pago))
        if ok:
            # Actualizar estado_pagado del cliente si no quedan pendientes
            self._sincronizar_estado_pago_cliente(id_pago)
        return ok, msg

    def _sincronizar_estado_pago_cliente(self, id_pago: int):
        sql_cliente = "SELECT id_cliente FROM pago WHERE id_pago = ?"
        res = self._ejecutar_consulta(sql_cliente, (id_pago,))
        if not res:
            return
        id_cliente = res[0]["id_cliente"]
        sql_pend = "SELECT 1 FROM pago WHERE id_cliente = ? AND estado = 'pendiente'"
        pendientes = self._ejecutar_consulta(sql_pend, (id_cliente,))
        nuevo_estado = "pendiente" if pendientes else "abonado"
        self._ejecutar_comando(
            "UPDATE clientes SET estado_pagado = ? WHERE id_cliente = ?",
            (nuevo_estado, id_cliente)
        )

    def obtener_pagos_pendientes_cliente(self, id_cliente: int):
        sql = """
            SELECT p.id_pago,
                   t.nombre,
                   p.importe,
                   p.tipo_cuota,
                   CONVERT(VARCHAR(10), p.fecha_pago, 23) AS fecha_pago
            FROM   pago   p
            JOIN   tarifa t ON p.id_tarifa = t.id_tarifa
            WHERE  p.id_cliente = ? AND p.estado = 'pendiente'
            ORDER  BY p.fecha_pago
        """
        return self._ejecutar_consulta(sql, (id_cliente,))

    def obtener_historial_pagos(self, id_cliente: int):
        sql = """
            SELECT CONVERT(VARCHAR(16), p.fecha_pago, 120) AS fecha_pago,
                   p.importe,
                   p.estado,
                   p.tipo_cuota,
                   t.nombre AS tarifa
            FROM   pago   p
            JOIN   tarifa t ON p.id_tarifa = t.id_tarifa
            WHERE  p.id_cliente = ?
            ORDER  BY p.fecha_pago DESC
        """
        return self._ejecutar_consulta(sql, (id_cliente,))

    # ==================================================================
    # UC7 · Consultar información del cliente
    # ==================================================================
    def obtener_estado_pago(self, id_cliente: int):
        res = self._ejecutar_consulta(
            "SELECT estado_pagado FROM clientes WHERE id_cliente = ?",
            (id_cliente,)
        )
        return res[0]["estado_pagado"] if res else None

    def obtener_calorias_quemadas(self, id_cliente: int):
        res = self._ejecutar_consulta(
            "SELECT calorias_acumuladas FROM clientes WHERE id_cliente = ?",
            (id_cliente,)
        )
        return res[0]["calorias_acumuladas"] if res else 0

    # ==================================================================
    # UC8 · Registro de entradas y salidas
    # ==================================================================
    def registrar_acceso(self, id_usuario: int, tipo_acceso: str):
        # Verificar que el usuario existe
        res = self._ejecutar_consulta(
            "SELECT id_usuario FROM usuarios WHERE id_usuario = ?",
            (id_usuario,)
        )
        if not res:
            return False, f"No existe ningún usuario con ID {id_usuario}."

        # Impedir salida sin entrada previa
        if tipo_acceso == "salida":
            sql_ult = """
                SELECT TOP 1 tipo_acceso
                FROM registro_acceso
                WHERE id_usuario = ?
                ORDER BY fecha_hora_registro DESC
            """
            ult = self._ejecutar_consulta(sql_ult, (id_usuario,))
            if not ult or ult[0]["tipo_acceso"] != "entrada":
                return False, "No se puede registrar una salida sin entrada previa."

        sql = """
            INSERT INTO registro_acceso (id_usuario, tipo_acceso)
            VALUES (?, ?)
        """
        return self._ejecutar_comando(sql, (id_usuario, tipo_acceso))

    def obtener_historial_accesos(self, limite: int = 50):
        sql = """
            SELECT TOP (?) r.id_registro,
                   u.nombre,
                   r.tipo_acceso,
                   CONVERT(VARCHAR(16), r.fecha_hora_registro, 120) AS fecha_hora_registro
            FROM   registro_acceso r
            JOIN   usuarios        u ON r.id_usuario = u.id_usuario
            ORDER  BY r.fecha_hora_registro DESC
        """
        return self._ejecutar_consulta(sql, (limite,))

    # ==================================================================
    # UC9 · Consultar y actualizar información de clientes
    # ==================================================================
    def obtener_todos_los_clientes(self):
        sql = """
            SELECT u.id_usuario, u.nombre, u.dni, u.telefono,
                   u.email, u.direccion,
                   c.estado_pagado,
                   t.nombre AS tarifa
            FROM   usuarios      u
            JOIN   clientes      c  ON u.id_usuario = c.id_cliente
            LEFT JOIN cliente_tarifa ct ON c.id_cliente = ct.id_cliente
                  AND ct.estado = 'activa'
            LEFT JOIN tarifa     t  ON ct.id_tarifa = t.id_tarifa
            WHERE  u.id_rol = (SELECT id_rol FROM roles WHERE nombre_rol = 'cliente')
            ORDER  BY u.nombre
        """
        return self._ejecutar_consulta(sql)

    def buscar_clientes(self, texto: str):
        like = f"%{texto}%"
        sql = """
            SELECT u.id_usuario, u.nombre, u.dni, u.telefono,
                   u.email, u.direccion, c.estado_pagado,
                   t.nombre AS tarifa
            FROM   usuarios      u
            JOIN   clientes      c  ON u.id_usuario = c.id_cliente
            LEFT JOIN cliente_tarifa ct ON c.id_cliente = ct.id_cliente
                  AND ct.estado = 'activa'
            LEFT JOIN tarifa     t  ON ct.id_tarifa = t.id_tarifa
            WHERE  u.id_rol = (SELECT id_rol FROM roles WHERE nombre_rol = 'cliente')
              AND  (u.nombre LIKE ? OR u.dni LIKE ? OR u.email LIKE ?)
            ORDER  BY u.nombre
        """
        return self._ejecutar_consulta(sql, (like, like, like))

    def obtener_cliente_por_id(self, id_usuario: int):
        sql = """
            SELECT u.id_usuario, u.nombre, u.telefono, u.email,
                   u.direccion, u.dni, c.estado_pagado
            FROM   usuarios u
            JOIN   clientes c ON u.id_usuario = c.id_cliente
            WHERE  u.id_usuario = ?
        """
        res = self._ejecutar_consulta(sql, (id_usuario,))
        return res[0] if res else None

    def actualizar_cliente(self, id_usuario: int, datos: dict):
        sql = """
            UPDATE usuarios
            SET nombre    = ?,
                telefono  = ?,
                email     = ?,
                direccion = ?
            WHERE id_usuario = ?
        """
        return self._ejecutar_comando(
            sql,
            (datos["nombre"], datos["telefono"],
             datos["email"], datos["direccion"], id_usuario)
        )

    # ==================================================================
    # UC10 · Gestionar clases
    # ==================================================================
    def obtener_todas_las_clases(self):
        sql = """
            SELECT c.id_clase, c.nombre_actividad, c.dia_semana,
                   CONVERT(VARCHAR(5), c.hora_inicio, 108) AS hora_inicio,
                   CONVERT(VARCHAR(5), c.hora_fin,    108) AS hora_fin,
                   u.nombre AS entrenador,
                   s.nombre AS sala,
                   c.aforo_maximo, c.nivel_intensidad,
                   c.calorias_estimadas, c.duracion
            FROM   clase      c
            JOIN   entrenador e ON c.id_entrenador = e.id_entrenador
            JOIN   usuarios   u ON e.id_entrenador = u.id_usuario
            JOIN   sala       s ON c.id_sala = s.id_sala
            ORDER  BY c.dia_semana, c.hora_inicio
        """
        return self._ejecutar_consulta(sql)

    def obtener_clase_por_id(self, id_clase: int):
        sql = """
            SELECT id_clase, nombre_actividad, dia_semana,
                   hora_inicio, hora_fin, aforo_maximo,
                   calorias_estimadas, duracion, nivel_intensidad,
                   id_entrenador, id_sala
            FROM clase WHERE id_clase = ?
        """
        res = self._ejecutar_consulta(sql, (id_clase,))
        return res[0] if res else None

    def crear_clase(self, datos: dict):
        sql = """
            INSERT INTO clase
                (id_entrenador, id_sala, nombre_actividad,
                 calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                 duracion, aforo_maximo, nivel_intensidad)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self._ejecutar_comando(
            sql,
            (datos["id_entrenador"], datos["id_sala"],
             datos["nombre_actividad"],
             int(datos.get("calorias_estimadas") or 0),
             datos["dia_semana"], datos["hora_inicio"], datos["hora_fin"],
             int(datos["duracion"]), int(datos["aforo_maximo"]),
             datos["nivel_intensidad"])
        )

    def modificar_clase(self, id_clase: int, datos: dict):
        sql = """
            UPDATE clase
            SET nombre_actividad   = ?,
                dia_semana         = ?,
                hora_inicio        = ?,
                hora_fin           = ?,
                aforo_maximo       = ?,
                calorias_estimadas = ?,
                duracion           = ?,
                nivel_intensidad   = ?
            WHERE id_clase = ?
        """
        return self._ejecutar_comando(
            sql,
            (datos["nombre_actividad"], datos["dia_semana"],
             datos["hora_inicio"], datos["hora_fin"],
             int(datos["aforo_maximo"]),
             int(datos.get("calorias_estimadas") or 0),
             int(datos["duracion"]),
             datos["nivel_intensidad"],
             id_clase)
        )

    # ==================================================================
    # UC11 · Gestión de recursos económicos
    # ==================================================================
    def obtener_tarifas(self):
        sql = """
            SELECT id_tarifa, nombre, precio_mensual,
                   servicios_incluidos,
                   CONVERT(VARCHAR(10), fecha_inicio, 23) AS fecha_inicio,
                   CONVERT(VARCHAR(10), fecha_fin,    23) AS fecha_fin
            FROM tarifa
            ORDER BY nombre
        """
        return self._ejecutar_consulta(sql)

    def actualizar_precio_tarifa(self, id_tarifa: int, nuevo_precio: float):
        return self._ejecutar_comando(
            "UPDATE tarifa SET precio_mensual = ? WHERE id_tarifa = ?",
            (nuevo_precio, id_tarifa)
        )

    def obtener_salarios_empleados(self):
        sql = """
            SELECT e.id_empleado, u.nombre, r.nombre_rol, e.salario
            FROM   empleados e
            JOIN   usuarios  u ON e.id_empleado = u.id_usuario
            JOIN   roles     r ON u.id_rol = r.id_rol
            ORDER  BY u.nombre
        """
        return self._ejecutar_consulta(sql)

    def actualizar_salario(self, id_empleado: int, nuevo_salario: float):
        return self._ejecutar_comando(
            "UPDATE empleados SET salario = ? WHERE id_empleado = ?",
            (nuevo_salario, id_empleado)
        )

    def obtener_resumen_economico(self):
        sql = """
            SELECT
                SUM(CASE WHEN estado = 'abonado'   THEN importe ELSE 0 END) AS total_recaudado,
                SUM(CASE WHEN estado = 'pendiente' THEN importe ELSE 0 END) AS total_pendiente
            FROM pago
        """
        res = self._ejecutar_consulta(sql)
        return res[0] if res else {"total_recaudado": 0, "total_pendiente": 0}

    # ==================================================================
    # UC12 · Generar informes
    # ==================================================================
    def generar_informe(self, tipo_informe: str, id_contable: int):
        """
        Devuelve (datos, cabeceras, campos) según el tipo solicitado.
        Registra también el informe generado en la tabla `informe`.
        """
        try:
            self._ejecutar_comando(
                "INSERT INTO informe (id_contable, tipo_informe) VALUES (?, ?)",
                (id_contable, tipo_informe)
            )
        except Exception:
            pass  # El registro del informe es secundario

        consultas = {
            "pagos_realizados": (
                """
                SELECT CONVERT(VARCHAR(10), p.fecha_pago, 23) AS fecha_pago,
                       u.nombre AS cliente,
                       t.nombre AS tarifa,
                       p.importe, p.metodo_pago, p.tipo_cuota
                FROM pago p
                JOIN usuarios u ON p.id_cliente = u.id_usuario
                JOIN tarifa   t ON p.id_tarifa  = t.id_tarifa
                WHERE p.estado = 'abonado'
                ORDER BY p.fecha_pago DESC
                """,
                ["Fecha", "Cliente", "Tarifa", "Importe (€)", "Método", "Tipo cuota"],
                ["fecha_pago", "cliente", "tarifa", "importe", "metodo_pago", "tipo_cuota"],
            ),
            "pagos_pendientes": (
                """
                SELECT u.nombre AS cliente, u.email,
                       t.nombre AS tarifa,
                       p.importe,
                       CONVERT(VARCHAR(10), p.fecha_pago, 23) AS fecha_vencimiento
                FROM pago p
                JOIN usuarios u ON p.id_cliente = u.id_usuario
                JOIN tarifa   t ON p.id_tarifa  = t.id_tarifa
                WHERE p.estado = 'pendiente'
                ORDER BY p.fecha_pago
                """,
                ["Cliente", "Email", "Tarifa", "Importe (€)", "Fecha vencimiento"],
                ["cliente", "email", "tarifa", "importe", "fecha_vencimiento"],
            ),
            "tarifas": (
                """
                SELECT nombre,
                       precio_mensual,
                       servicios_incluidos,
                       CONVERT(VARCHAR(10), fecha_inicio, 23) AS fecha_inicio,
                       ISNULL(CONVERT(VARCHAR(10), fecha_fin, 23), 'Vigente') AS fecha_fin,
                       (SELECT COUNT(*) FROM cliente_tarifa ct
                        WHERE ct.id_tarifa = t.id_tarifa AND ct.estado = 'activa') AS clientes_activos
                FROM tarifa t
                ORDER BY nombre
                """,
                ["Nombre", "Precio/mes (€)", "Servicios", "Desde", "Hasta", "Clientes activos"],
                ["nombre", "precio_mensual", "servicios_incluidos",
                 "fecha_inicio", "fecha_fin", "clientes_activos"],
            ),
            "salarios": (
                """
                SELECT u.nombre, r.nombre_rol AS rol, e.salario
                FROM empleados e
                JOIN usuarios  u ON e.id_empleado = u.id_usuario
                JOIN roles     r ON u.id_rol = r.id_rol
                ORDER BY e.salario DESC
                """,
                ["Nombre", "Rol", "Salario (€)"],
                ["nombre", "rol", "salario"],
            ),
        }

        if tipo_informe not in consultas:
            return None, [], []

        sql, cabeceras, campos = consultas[tipo_informe]
        datos = self._ejecutar_consulta(sql)
        return datos, cabeceras, campos

    # ==================================================================
    # UC13 · Ranking de clientes más activos
    # ==================================================================
    def obtener_ranking_clientes(self):
        sql = """
            SELECT ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS posicion,
                   u.nombre,
                   u.dni,
                   COUNT(*) AS total_asistencias
            FROM   asistencia a
            JOIN   usuarios   u ON a.id_cliente = u.id_usuario
            WHERE  a.presente = 'si'
            GROUP  BY u.id_usuario, u.nombre, u.dni
            ORDER  BY total_asistencias DESC
        """
        return self._ejecutar_consulta(sql)

    # ==================================================================
    # UC14 · Detectar clientes con pagos pendientes
    # ==================================================================
    def obtener_clientes_con_pagos_pendientes(self):
        sql = """
            SELECT u.nombre,
                   u.dni,
                   u.email,
                   p.importe,
                   t.nombre AS nombre_tarifa,
                   CONVERT(VARCHAR(10), p.fecha_pago, 23) AS fecha_pago
            FROM   pago     p
            JOIN   usuarios u ON p.id_cliente = u.id_usuario
            JOIN   tarifa   t ON p.id_tarifa  = t.id_tarifa
            WHERE  p.estado = 'pendiente'
            ORDER  BY p.fecha_pago, u.nombre
        """
        return self._ejecutar_consulta(sql)

    # ==================================================================
    # UC15 · Consultar ocupación de clases
    # ==================================================================
    def obtener_ocupacion_clases(self, id_entrenador: int = None):
        filtro = "WHERE c.id_entrenador = ?" if id_entrenador else ""
        params = (id_entrenador,) if id_entrenador else ()
        sql = f"""
            SELECT c.nombre_actividad,
                   c.dia_semana,
                   c.aforo_maximo,
                   COUNT(i.id_inscripcion) AS inscritos,
                   CAST(
                       100.0 * COUNT(i.id_inscripcion) / NULLIF(c.aforo_maximo, 0)
                   AS DECIMAL(5,1)) AS porcentaje
            FROM clase c
            LEFT JOIN inscripcion i ON c.id_clase = i.id_clase
                  AND i.estado = 'inscrito'
            {filtro}
            GROUP BY c.id_clase, c.nombre_actividad, c.dia_semana, c.aforo_maximo
            ORDER BY porcentaje DESC
        """
        return self._ejecutar_consulta(sql, params)
