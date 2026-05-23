import hashlib
from src.modelo.conexion.Conexion import Conexion


class Logica:

    def __init__(self):
        self.conexion = Conexion()

    def cifrar_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def consultar(self, sql, parametros=()):
        cursor = self.conexion.getCursor()
        try:
            cursor.execute(sql, parametros)
            return cursor.fetchall()
        finally:
            cursor.close()

    def ejecutar(self, sql, parametros=()):
        cursor = self.conexion.getCursor()
        try:
            cursor.execute(sql, parametros)

            try:
                self.conexion.conexion.commit()
            except Exception:
                pass

            return cursor.rowcount
        finally:
            cursor.close()

    def iniciar_sesion(self, username, password):
        sql = """
            SELECT u.id_usuario, u.nombre, u.username, u.password_hash, r.nombre_rol
            FROM usuarios u
            INNER JOIN roles r ON u.id_rol = r.id_rol
            WHERE u.username = ?
        """
        datos = self.consultar(sql, (username,))

        if not datos:
            return None

        id_usuario, nombre, usuario, password_bd, rol = datos[0]
        password_cifrada = self.cifrar_password(password)

        if password_bd == password or password_bd == password_cifrada:
            return {
                "id_usuario": id_usuario,
                "nombre": nombre,
                "username": usuario,
                "rol": rol
            }

        return None

    def listar_usuarios(self):
        sql = """
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, r.nombre_rol, u.direccion, u.fecha_nacimiento
            FROM usuarios u
            INNER JOIN roles r ON u.id_rol = r.id_rol
            ORDER BY u.nombre
        """
        return self.consultar(sql)

    def buscar_usuario(self, id_usuario):
        sql = """
            SELECT id_usuario, dni, nombre, telefono, email, username,
                   id_rol, direccion, fecha_nacimiento
            FROM usuarios
            WHERE id_usuario = ?
        """
        datos = self.consultar(sql, (id_usuario,))
        return datos[0] if datos else None

    def registrar_usuario(self, dni, nombre, telefono, email, username,
                          password, id_rol, direccion, fecha_nacimiento):
        password_cifrada = self.cifrar_password(password)

        sql = """
            INSERT INTO usuarios
            (dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_nacimiento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self.ejecutar(
            sql,
            (dni, nombre, telefono, email, username, password_cifrada,
             id_rol, direccion, fecha_nacimiento)
        )

    def modificar_usuario(self, id_usuario, telefono, email, direccion):
        sql = """
            UPDATE usuarios
            SET telefono = ?, email = ?, direccion = ?
            WHERE id_usuario = ?
        """
        return self.ejecutar(sql, (telefono, email, direccion, id_usuario))

    def eliminar_usuario(self, id_usuario):
        sql = "DELETE FROM usuarios WHERE id_usuario = ?"
        return self.ejecutar(sql, (id_usuario,))

    def registrar_cliente(self, id_cliente):
        sql = "INSERT INTO clientes (id_cliente) VALUES (?)"
        return self.ejecutar(sql, (id_cliente,))

    def listar_clientes(self):
        sql = """
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   c.estado_pagado, c.calorias_acumuladas
            FROM clientes c
            INNER JOIN usuarios u ON c.id_cliente = u.id_usuario
            ORDER BY u.nombre
        """
        return self.consultar(sql)

    def actualizar_cliente(self, id_cliente, telefono, email, direccion):
        return self.modificar_usuario(id_cliente, telefono, email, direccion)

    def historial_cliente(self, id_cliente):
        sql = """
            SELECT c.nombre_actividad, a.fecha, a.presente, c.calorias_estimadas
            FROM asistencia a
            INNER JOIN clase c ON a.id_clase = c.id_clase
            WHERE a.id_cliente = ?
            ORDER BY a.fecha DESC
        """
        return self.consultar(sql, (id_cliente,))

    def registrar_empleado(self, id_empleado, salario):
        sql = "INSERT INTO empleados (id_empleado, salario) VALUES (?, ?)"
        return self.ejecutar(sql, (id_empleado, salario))

    def listar_empleados(self):
        sql = """
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   r.nombre_rol, e.salario
            FROM empleados e
            INNER JOIN usuarios u ON e.id_empleado = u.id_usuario
            INNER JOIN roles r ON u.id_rol = r.id_rol
            ORDER BY u.nombre
        """
        return self.consultar(sql)

    def modificar_empleado(self, id_empleado, telefono, email, direccion, salario):
        self.modificar_usuario(id_empleado, telefono, email, direccion)

        sql = """
            UPDATE empleados
            SET salario = ?
            WHERE id_empleado = ?
        """
        return self.ejecutar(sql, (salario, id_empleado))

    def eliminar_empleado(self, id_empleado):
        return self.eliminar_usuario(id_empleado)

    def registrar_entrenador(self, id_entrenador, especialidad, id_admin):
        sql = """
            INSERT INTO entrenador
            (id_entrenador, especialidad, id_administrador_registra)
            VALUES (?, ?, ?)
        """
        return self.ejecutar(sql, (id_entrenador, especialidad, id_admin))

    def registrar_recepcionista(self, id_recepcionista, turno, id_admin):
        sql = """
            INSERT INTO recepcionista
            (id_recepcionista, turno, id_administrador_registra)
            VALUES (?, ?, ?)
        """
        return self.ejecutar(sql, (id_recepcionista, turno, id_admin))

    def registrar_contable(self, id_contable, titulacion, id_admin):
        sql = """
            INSERT INTO contable
            (id_contable, titulacion, id_administrador_registra)
            VALUES (?, ?, ?)
        """
        return self.ejecutar(sql, (id_contable, titulacion, id_admin))

    def registrar_acceso(self, id_usuario, tipo_acceso):
        if tipo_acceso not in ("entrada", "salida"):
            raise ValueError("Acceso no válido")

        if tipo_acceso == "salida":
            sql = """
                SELECT id_registro
                FROM registro_acceso
                WHERE id_usuario = ? AND tipo_acceso = 'entrada'
                ORDER BY fecha_hora_registro DESC
                LIMIT 1
            """
            datos = self.consultar(sql, (id_usuario,))

            if not datos:
                raise ValueError("No hay entrada previa")

        sql = """
            INSERT INTO registro_acceso (id_usuario, tipo_acceso)
            VALUES (?, ?)
        """
        return self.ejecutar(sql, (id_usuario, tipo_acceso))

    def listar_accesos(self):
        sql = """
            SELECT r.id_registro, u.nombre, r.fecha_hora_registro, r.tipo_acceso
            FROM registro_acceso r
            INNER JOIN usuarios u ON r.id_usuario = u.id_usuario
            ORDER BY r.fecha_hora_registro DESC
        """
        return self.consultar(sql)

    def listar_salas(self):
        sql = """
            SELECT id_sala, nombre, aforo_maximo, tipo_zona
            FROM sala
            ORDER BY nombre
        """
        return self.consultar(sql)

    def listar_clases(self):
        sql = """
            SELECT c.id_clase, c.nombre_actividad, u.nombre, s.nombre,
                   c.dia_semana, c.hora_inicio, c.hora_fin, c.duracion,
                   c.aforo_maximo, c.nivel_intensidad, c.calorias_estimadas
            FROM clase c
            INNER JOIN entrenador e ON c.id_entrenador = e.id_entrenador
            INNER JOIN usuarios u ON e.id_entrenador = u.id_usuario
            INNER JOIN sala s ON c.id_sala = s.id_sala
            ORDER BY c.dia_semana, c.hora_inicio
        """
        return self.consultar(sql)

    def buscar_clase(self, id_clase):
        sql = """
            SELECT id_clase, id_entrenador, id_sala, nombre_actividad,
                   calorias_estimadas, dia_semana, hora_inicio, hora_fin,
                   duracion, aforo_maximo, nivel_intensidad
            FROM clase
            WHERE id_clase = ?
        """
        datos = self.consultar(sql, (id_clase,))
        return datos[0] if datos else None

    def registrar_clase(self, id_entrenador, id_sala, nombre_actividad,
                        calorias_estimadas, dia_semana, hora_inicio,
                        hora_fin, duracion, aforo_maximo, nivel_intensidad):
        sql = """
            INSERT INTO clase
            (id_entrenador, id_sala, nombre_actividad, calorias_estimadas,
             dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self.ejecutar(
            sql,
            (id_entrenador, id_sala, nombre_actividad, calorias_estimadas,
             dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad)
        )

    def modificar_clase(self, id_clase, id_entrenador, id_sala, nombre_actividad,
                        calorias_estimadas, dia_semana, hora_inicio,
                        hora_fin, duracion, aforo_maximo, nivel_intensidad):
        sql = """
            UPDATE clase
            SET id_entrenador = ?, id_sala = ?, nombre_actividad = ?,
                calorias_estimadas = ?, dia_semana = ?, hora_inicio = ?,
                hora_fin = ?, duracion = ?, aforo_maximo = ?, nivel_intensidad = ?
            WHERE id_clase = ?
        """
        return self.ejecutar(
            sql,
            (id_entrenador, id_sala, nombre_actividad, calorias_estimadas,
             dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo,
             nivel_intensidad, id_clase)
        )

    def eliminar_clase(self, id_clase):
        sql = "DELETE FROM clase WHERE id_clase = ?"
        return self.ejecutar(sql, (id_clase,))

    def clases_de_entrenador(self, id_entrenador):
        sql = """
            SELECT id_clase, nombre_actividad, dia_semana, hora_inicio, hora_fin
            FROM clase
            WHERE id_entrenador = ?
            ORDER BY dia_semana, hora_inicio
        """
        return self.consultar(sql, (id_entrenador,))
    
    def clases_entrenador_tabla(self, id_entrenador):
        sql = """
            SELECT c.nombre_actividad,
                s.nombre AS sala,
                CONCAT(c.hora_inicio, ' - ', c.hora_fin) AS horario,
                c.dia_semana,
                CONCAT(
                    COUNT(i.id_inscripcion),
                    '/',
                    c.aforo_maximo
                ) AS capacidad
            FROM clase c
            INNER JOIN sala s ON c.id_sala = s.id_sala
            LEFT JOIN inscripcion i 
                ON c.id_clase = i.id_clase 
                AND i.estado = 'inscrito'
            WHERE c.id_entrenador = ?
            GROUP BY c.id_clase, c.nombre_actividad, s.nombre,
                    c.hora_inicio, c.hora_fin, c.dia_semana, c.aforo_maximo
            ORDER BY c.dia_semana, c.hora_inicio
        """
        return self.consultar(sql, (id_entrenador,))

    def inscribirse_clase(self, id_cliente, id_clase):
        aforo = self.consultar(
            "SELECT aforo_maximo FROM clase WHERE id_clase = ?",
            (id_clase,)
        )

        if not aforo:
            raise ValueError("Clase no encontrada")

        ocupacion = self.consultar(
            "SELECT COUNT(*) FROM inscripcion WHERE id_clase = ? AND estado = 'inscrito'",
            (id_clase,)
        )[0][0]

        if ocupacion >= aforo[0][0]:
            raise ValueError("Clase completa")

        repetido = self.consultar(
            "SELECT id_inscripcion FROM inscripcion WHERE id_cliente = ? AND id_clase = ?",
            (id_cliente, id_clase)
        )

        if repetido:
            sql = """
                UPDATE inscripcion
                SET estado = 'inscrito'
                WHERE id_cliente = ? AND id_clase = ?
            """
            return self.ejecutar(sql, (id_cliente, id_clase))

        sql = """
            INSERT INTO inscripcion (id_cliente, id_clase)
            VALUES (?, ?)
        """
        return self.ejecutar(sql, (id_cliente, id_clase))

    def desapuntarse_clase(self, id_cliente, id_clase):
        sql = """
            UPDATE inscripcion
            SET estado = 'cancelado'
            WHERE id_cliente = ? AND id_clase = ?
        """
        return self.ejecutar(sql, (id_cliente, id_clase))

    def clases_inscritas_cliente(self, id_cliente):
        sql = """
            SELECT c.id_clase, c.nombre_actividad, c.dia_semana,
                   c.hora_inicio, c.hora_fin, i.estado
            FROM inscripcion i
            INNER JOIN clase c ON i.id_clase = c.id_clase
            WHERE i.id_cliente = ?
            ORDER BY c.dia_semana, c.hora_inicio
        """
        return self.consultar(sql, (id_cliente,))

    def clientes_inscritos_clase(self, id_clase):
        sql = """
            SELECT u.id_usuario, u.nombre, u.telefono, u.email
            FROM inscripcion i
            INNER JOIN usuarios u ON i.id_cliente = u.id_usuario
            WHERE i.id_clase = ? AND i.estado = 'inscrito'
            ORDER BY u.nombre
        """
        return self.consultar(sql, (id_clase,))

    def registrar_asistencia(self, id_cliente, id_clase, fecha, presente="si"):
        existe = self.consultar(
            """
            SELECT id_asistencia
            FROM asistencia
            WHERE id_cliente = ? AND id_clase = ? AND fecha = ?
            """,
            (id_cliente, id_clase, fecha)
        )

        if existe:
            sql = """
                UPDATE asistencia
                SET presente = ?
                WHERE id_cliente = ? AND id_clase = ? AND fecha = ?
            """
            return self.ejecutar(sql, (presente, id_cliente, id_clase, fecha))

        sql = """
            INSERT INTO asistencia (id_cliente, id_clase, fecha, presente)
            VALUES (?, ?, ?, ?)
        """
        return self.ejecutar(sql, (id_cliente, id_clase, fecha, presente))

    def registrar_asistencia_lista(self, id_clase, fecha, lista_clientes_presentes):
        inscritos = self.clientes_inscritos_clase(id_clase)

        for cliente in inscritos:
            id_cliente = cliente[0]

            if id_cliente in lista_clientes_presentes:
                self.registrar_asistencia(id_cliente, id_clase, fecha, "si")
            else:
                self.registrar_asistencia(id_cliente, id_clase, fecha, "no")

        return True

    def consultar_asistencia_clase(self, id_clase):
        sql = """
            SELECT u.nombre, a.fecha, a.presente
            FROM asistencia a
            INNER JOIN usuarios u ON a.id_cliente = u.id_usuario
            WHERE a.id_clase = ?
            ORDER BY a.fecha DESC, u.nombre
        """
        return self.consultar(sql, (id_clase,))

    def listar_tarifas(self):
        sql = """
            SELECT id_tarifa, nombre, precio_mensual, servicios_incluidos,
                   fecha_inicio, fecha_fin
            FROM tarifa
            ORDER BY precio_mensual
        """
        return self.consultar(sql)

    def registrar_tarifa(self, nombre, precio_mensual, servicios_incluidos,
                         fecha_inicio, fecha_fin=None):
        sql = """
            INSERT INTO tarifa
            (nombre, precio_mensual, servicios_incluidos, fecha_inicio, fecha_fin)
            VALUES (?, ?, ?, ?, ?)
        """
        return self.ejecutar(
            sql,
            (nombre, precio_mensual, servicios_incluidos, fecha_inicio, fecha_fin)
        )

    def modificar_tarifa(self, id_tarifa, nombre, precio_mensual,
                         servicios_incluidos, fecha_inicio, fecha_fin=None):
        sql = """
            UPDATE tarifa
            SET nombre = ?, precio_mensual = ?, servicios_incluidos = ?,
                fecha_inicio = ?, fecha_fin = ?
            WHERE id_tarifa = ?
        """
        return self.ejecutar(
            sql,
            (nombre, precio_mensual, servicios_incluidos,
             fecha_inicio, fecha_fin, id_tarifa)
        )

    def asignar_tarifa_cliente(self, id_cliente, id_tarifa):
        sql = """
            INSERT INTO cliente_tarifa (id_cliente, id_tarifa)
            VALUES (?, ?)
        """
        return self.ejecutar(sql, (id_cliente, id_tarifa))

    def registrar_pago(self, id_cliente, id_contable, id_tarifa,
                       importe, metodo_pago, tipo_cuota):
        sql = """
            INSERT INTO pago
            (id_cliente, id_contable, id_tarifa, importe, metodo_pago, estado, tipo_cuota)
            VALUES (?, ?, ?, ?, ?, 'abonado', ?)
        """
        self.ejecutar(
            sql,
            (id_cliente, id_contable, id_tarifa, importe, metodo_pago, tipo_cuota)
        )

        sql_cliente = """
            UPDATE clientes
            SET estado_pagado = 'abonado'
            WHERE id_cliente = ?
        """
        return self.ejecutar(sql_cliente, (id_cliente,))

    def crear_pago_pendiente(self, id_cliente, id_contable, id_tarifa,
                             importe, metodo_pago, tipo_cuota):
        sql = """
            INSERT INTO pago
            (id_cliente, id_contable, id_tarifa, importe, metodo_pago, estado, tipo_cuota)
            VALUES (?, ?, ?, ?, ?, 'pendiente', ?)
        """
        return self.ejecutar(
            sql,
            (id_cliente, id_contable, id_tarifa, importe, metodo_pago, tipo_cuota)
        )

    def listar_pagos(self):
        sql = """
            SELECT p.id_pago, u.nombre, t.nombre, p.importe,
                   p.metodo_pago, p.fecha_pago, p.estado, p.tipo_cuota
            FROM pago p
            INNER JOIN usuarios u ON p.id_cliente = u.id_usuario
            INNER JOIN tarifa t ON p.id_tarifa = t.id_tarifa
            ORDER BY p.fecha_pago DESC
        """
        return self.consultar(sql)

    def pagos_cliente(self, id_cliente):
        sql = """
            SELECT p.id_pago, t.nombre, p.importe, p.metodo_pago,
                   p.fecha_pago, p.estado, p.tipo_cuota
            FROM pago p
            INNER JOIN tarifa t ON p.id_tarifa = t.id_tarifa
            WHERE p.id_cliente = ?
            ORDER BY p.fecha_pago DESC
        """
        return self.consultar(sql, (id_cliente,))

    def pagos_pendientes(self):
        sql = """
            SELECT p.id_pago, u.nombre, t.nombre, p.importe,
                   p.fecha_pago, p.tipo_cuota
            FROM pago p
            INNER JOIN usuarios u ON p.id_cliente = u.id_usuario
            INNER JOIN tarifa t ON p.id_tarifa = t.id_tarifa
            WHERE p.estado = 'pendiente'
            ORDER BY p.fecha_pago
        """
        return self.consultar(sql)

    def marcar_pago_abonado(self, id_pago):
        sql = """
            UPDATE pago
            SET estado = 'abonado'
            WHERE id_pago = ?
        """
        return self.ejecutar(sql, (id_pago,))

    def generar_informe(self, id_contable, tipo_informe):
        sql = """
            INSERT INTO informe (id_contable, tipo_informe)
            VALUES (?, ?)
        """
        return self.ejecutar(sql, (id_contable, tipo_informe))

    def listar_informes(self):
        sql = """
            SELECT i.id_informe, u.nombre, i.tipo_informe, i.fecha_generacion
            FROM informe i
            INNER JOIN usuarios u ON i.id_contable = u.id_usuario
            ORDER BY i.fecha_generacion DESC
        """
        return self.consultar(sql)

    def informe_pagos_realizados(self):
        sql = """
            SELECT u.nombre, t.nombre, p.importe, p.metodo_pago,
                   p.fecha_pago, p.tipo_cuota
            FROM pago p
            INNER JOIN usuarios u ON p.id_cliente = u.id_usuario
            INNER JOIN tarifa t ON p.id_tarifa = t.id_tarifa
            WHERE p.estado = 'abonado'
            ORDER BY p.fecha_pago DESC
        """
        return self.consultar(sql)

    def informe_pagos_por_mes(self):
        sql = """
            SELECT YEAR(fecha_pago) AS anio,
                   MONTH(fecha_pago) AS mes,
                   SUM(importe) AS total
            FROM pago
            WHERE estado = 'abonado'
            GROUP BY YEAR(fecha_pago), MONTH(fecha_pago)
            ORDER BY anio DESC, mes DESC
        """
        return self.consultar(sql)

    def informe_salarios(self):
        sql = """
            SELECT u.nombre, r.nombre_rol, e.salario
            FROM empleados e
            INNER JOIN usuarios u ON e.id_empleado = u.id_usuario
            INNER JOIN roles r ON u.id_rol = r.id_rol
            ORDER BY u.nombre
        """
        return self.consultar(sql)

    def ranking_clientes_activos(self):
        sql = """
            SELECT u.nombre, COUNT(a.id_asistencia) AS asistencias
            FROM asistencia a
            INNER JOIN usuarios u ON a.id_cliente = u.id_usuario
            WHERE a.presente = 'si'
            GROUP BY u.nombre
            ORDER BY asistencias DESC
        """
        return self.consultar(sql)

    def ocupacion_clases(self):
        sql = """
            SELECT c.id_clase, c.nombre_actividad,
                   COUNT(i.id_inscripcion) AS inscritos,
                   c.aforo_maximo,
                   CAST(COUNT(i.id_inscripcion) * 100.0 / c.aforo_maximo AS DECIMAL(5,2)) AS ocupacion
            FROM clase c
            LEFT JOIN inscripcion i
                ON c.id_clase = i.id_clase AND i.estado = 'inscrito'
            GROUP BY c.id_clase, c.nombre_actividad, c.aforo_maximo
            ORDER BY ocupacion DESC
        """
        return self.consultar(sql)
    
    #consultadar clases entrenador 
    def ocupacion_clases_entrenador(self, id_entrenador):
        sql = """
            SELECT c.id_clase, c.nombre_actividad,
                COUNT(i.id_inscripcion) AS inscritos,
                c.aforo_maximo,
                CAST(COUNT(i.id_inscripcion) * 100.0 / c.aforo_maximo AS DECIMAL(5,2)) AS ocupacion
            FROM clase c
            LEFT JOIN inscripcion i
                ON c.id_clase = i.id_clase AND i.estado = 'inscrito'
            WHERE c.id_entrenador = ?
            GROUP BY c.id_clase, c.nombre_actividad, c.aforo_maximo
            ORDER BY ocupacion DESC
        """
        return self.consultar(sql, (id_entrenador,))

    def calcular_calorias_cliente(self, id_cliente):
        sql = """
            SELECT SUM(c.calorias_estimadas)
            FROM asistencia a
            INNER JOIN clase c ON a.id_clase = c.id_clase
            WHERE a.id_cliente = ? AND a.presente = 'si'
        """
        datos = self.consultar(sql, (id_cliente,))

        total = datos[0][0]

        if total is None:
            total = 0

        sql_actualizar = """
            UPDATE clientes
            SET calorias_acumuladas = ?
            WHERE id_cliente = ?
        """
        self.ejecutar(sql_actualizar, (total, id_cliente))

        return total

    def estadisticas_cliente(self, id_cliente):
        sql = """
            SELECT c.nombre_actividad, COUNT(a.id_asistencia) AS veces,
                   SUM(c.calorias_estimadas) AS calorias
            FROM asistencia a
            INNER JOIN clase c ON a.id_clase = c.id_clase
            WHERE a.id_cliente = ? AND a.presente = 'si'
            GROUP BY c.nombre_actividad
            ORDER BY veces DESC
        """
        return self.consultar(sql, (id_cliente,))

    def perfil_usuario(self, id_usuario):
        sql = """
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, r.nombre_rol, u.direccion, u.fecha_registro,
                   u.fecha_nacimiento
            FROM usuarios u
            INNER JOIN roles r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = ?
        """
        datos = self.consultar(sql, (id_usuario,))
        return datos[0] if datos else None

    def cambiar_password(self, id_usuario, nueva_password):
        nueva_cifrada = self.cifrar_password(nueva_password)

        sql = """
            UPDATE usuarios
            SET password_hash = ?
            WHERE id_usuario = ?
        """
        return self.ejecutar(sql, (nueva_cifrada, id_usuario))

    def contar_usuarios(self):
        datos = self.consultar("SELECT COUNT(*) FROM clientes")
        return datos[0][0] if datos else 0

    def contar_clases(self):
        datos = self.consultar("SELECT COUNT(*) FROM clase")
        return datos[0][0] if datos else 0

    def contar_inscripciones(self):
        datos = self.consultar("SELECT COUNT(*) FROM inscripcion WHERE estado = 'inscrito'")
        return datos[0][0] if datos else 0


    def contar_inscripciones_clase(self, nombre_actividad):
        like = f"%{nombre_actividad.lower()}%"
        datos = self.consultar(f"""
            SELECT COUNT(*) FROM inscripcion i
            JOIN clase c ON i.id_clase = c.id_clase
            WHERE LOWER(c.nombre_actividad) LIKE '{like}' AND i.estado = 'inscrito'
        """)
        return datos[0][0] if datos else 0

    def contar_clientes_tarifa(self, nombre_tarifa):
        like = f"%{nombre_tarifa.lower()}%"
        datos = self.consultar(f"""
            SELECT COUNT(*) FROM cliente_tarifa ct
            JOIN tarifa t ON ct.id_tarifa = t.id_tarifa
            WHERE LOWER(t.nombre) LIKE '{like}' AND ct.estado = 'activa'
        """)
        return datos[0][0] if datos else 0

    def listar_inscripciones_resumen(self):
        return self.consultar("""
            SELECT u.nombre, c.nombre_actividad, i.fecha_inscripcion, i.estado
            FROM inscripcion i
            JOIN clientes cl ON i.id_cliente = cl.id_cliente
            JOIN usuarios u ON cl.id_cliente = u.id_usuario
            JOIN clase c ON i.id_clase = c.id_clase
            WHERE i.estado = 'inscrito'
            ORDER BY i.fecha_inscripcion DESC
            LIMIT 50
        """)

    def inscripciones_por_clase(self):
        return self.consultar("""
            SELECT c.nombre_actividad, COUNT(*) as total
            FROM inscripcion i
            JOIN clase c ON i.id_clase = c.id_clase
            WHERE i.estado = 'inscrito'
            GROUP BY c.nombre_actividad
            ORDER BY total DESC
        """)

    def ingresos_por_mes(self):
        return self.consultar("""
            SELECT DATE_FORMAT(fecha_pago, '%Y-%m') as mes,
                   SUM(importe) as total
            FROM pago
            WHERE estado = 'abonado'
            GROUP BY mes
            ORDER BY mes DESC
            LIMIT 6
        """)

