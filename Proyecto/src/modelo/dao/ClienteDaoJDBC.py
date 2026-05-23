from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.ClientesVO import ClientesVO
from src.modelo.vo.ClienteInicioVO import ClienteInicioVO


class ClienteDaoJDBC(Conexion):

    SQL_SELECT = "SELECT id_cliente, estado_pagado, calorias_acumuladas FROM clientes"
    SQL_SELECT_BY_ID = "SELECT id_cliente, estado_pagado, calorias_acumuladas FROM clientes WHERE id_cliente = ?"
    SQL_INSERT = "INSERT INTO clientes (id_cliente, estado_pagado, calorias_acumuladas) VALUES (?, ?, ?)"
    SQL_UPDATE = "UPDATE clientes SET estado_pagado=?, calorias_acumuladas=? WHERE id_cliente=?"
    SQL_UPDATE_ESTADO = "UPDATE clientes SET estado_pagado=? WHERE id_cliente=?"
    SQL_UPDATE_CALORIAS = "UPDATE clientes SET calorias_acumuladas=? WHERE id_cliente=?"
    SQL_DELETE = "DELETE FROM clientes WHERE id_cliente = ?"

    # Consultas para ClienteInicioVO

    # Datos del usuario y del cliente en una sola consulta
    _SQL_INICIO_BASE = """
        SELECT
            u.id_usuario,
            u.nombre,
            u.email,
            u.telefono,
            u.direccion,
            DATE_FORMAT(u.fecha_nacimiento, '%d/%m/%Y')  AS fecha_nacimiento,
            DATE_FORMAT(u.fecha_registro,   '%M %Y')     AS fecha_registro,
            c.estado_pagado,
            c.calorias_acumuladas
        FROM clientes c
        JOIN usuarios u ON u.id_usuario = c.id_cliente
        WHERE c.id_cliente = ?
    """

    # Tarifa activa del cliente
    _SQL_TARIFA_ACTIVA = """
        SELECT t.nombre, t.precio_mensual
        FROM cliente_tarifa ct
        JOIN tarifa t ON t.id_tarifa = ct.id_tarifa
        WHERE ct.id_cliente = ?
          AND ct.estado = 'activa'
        ORDER BY ct.fecha_contratacion DESC
        LIMIT 1
    """

    # Último pago registrado
    _SQL_ULTIMO_PAGO = """
        SELECT
            p.importe,
            DATE_FORMAT(p.fecha_pago, '%M %Y') AS mes_pago,
            p.estado
        FROM pago p
        WHERE p.id_cliente = ?
        ORDER BY p.fecha_pago DESC
        LIMIT 1
    """

    # Asistencias con presente='si' en la semana en curso
    _SQL_CLASES_SEMANA = """
        SELECT COUNT(*) AS clases_semana
        FROM asistencia a
        WHERE a.id_cliente = ?
          AND a.presente = 'si'
          AND YEARWEEK(a.fecha, 1) = YEARWEEK(CURDATE(), 1)
    """

    # Calorías quemadas en la semana en curso (suma de calorias_estimadas de
    # las clases asistidas)
    _SQL_CALORIAS_SEMANA = """
        SELECT COALESCE(SUM(cl.calorias_estimadas), 0) AS calorias_semana
        FROM asistencia a
        JOIN clase cl ON cl.id_clase = a.id_clase
        WHERE a.id_cliente = ?
          AND a.presente = 'si'
          AND YEARWEEK(a.fecha, 1) = YEARWEEK(CURDATE(), 1)
    """

    # Asistencias e inscripciones del mes actual
    _SQL_ASISTENCIAS_MES = """
        SELECT
            (
                SELECT COUNT(*)
                FROM asistencia
                WHERE id_cliente = ?
                  AND presente = 'si'
                  AND MONTH(fecha) = MONTH(CURDATE())
                  AND YEAR(fecha)  = YEAR(CURDATE())
            ) AS asistencias_mes,
            (
                SELECT COUNT(*)
                FROM inscripcion
                WHERE id_cliente = ?
                  AND estado = 'inscrito'
                  AND MONTH(fecha_inscripcion) = MONTH(CURDATE())
                  AND YEAR(fecha_inscripcion)  = YEAR(CURDATE())
            ) AS inscripciones_mes
    """

    # Próximas clases inscritas (fecha >= hoy, ordenadas por día de semana
    # + hora; se traen las 20 primeras para llenar la tabla de la UI)
    _SQL_PROXIMAS_CLASES = """
        SELECT
            cl.nombre_actividad,
            cl.dia_semana           AS fecha,
            TIME_FORMAT(cl.hora_inicio, '%H:%i') AS hora_inicio,
            s.nombre                AS nombre_sala
        FROM inscripcion i
        JOIN clase cl ON cl.id_clase  = i.id_clase
        JOIN sala  s  ON s.id_sala    = cl.id_sala
        WHERE i.id_cliente = ?
          AND i.estado = 'inscrito'
        ORDER BY
            FIELD(cl.dia_semana,
                  'lunes','martes','miércoles','jueves',
                  'viernes','sábado','domingo'),
            cl.hora_inicio
        LIMIT 20
    """

    # Estadísticas semana en curso
    _SQL_STATS_SEMANA_ACTUAL = """
        SELECT
            COUNT(*)                              AS entrenos,
            COALESCE(SUM(cl.duracion), 0)         AS tiempo_min
        FROM asistencia a
        JOIN clase cl ON cl.id_clase = a.id_clase
        WHERE a.id_cliente = ?
          AND a.presente = 'si'
          AND YEARWEEK(a.fecha, 1) = YEARWEEK(CURDATE(), 1)
    """

    # Estadísticas semana anterior (para calcular deltas)
    _SQL_STATS_SEMANA_ANTERIOR = """
        SELECT
            COUNT(*)                              AS entrenos,
            COALESCE(SUM(cl.duracion), 0)         AS tiempo_min
        FROM asistencia a
        JOIN clase cl ON cl.id_clase = a.id_clase
        WHERE a.id_cliente = ?
          AND a.presente = 'si'
          AND YEARWEEK(a.fecha, 1) = YEARWEEK(CURDATE(), 1) - 1
    """

    # Racha: días consecutivos con al menos una asistencia hasta hoy.
    # Se calculan todas las fechas de asistencia del cliente y se evalúa
    # cuántos días seguidos hay hacia atrás desde hoy.
    _SQL_FECHAS_ASISTENCIA = """
        SELECT DISTINCT fecha
        FROM asistencia
        WHERE id_cliente = ?
          AND presente = 'si'
        ORDER BY fecha DESC
    """

    # Distribución por tipo de clase (especialidad del entrenador como proxy
    # del tipo de actividad). Se agrupan por nombre_actividad y se calcula
    # el porcentaje sobre el total de asistencias del cliente.
    _SQL_DISTRIBUCION = """
        SELECT
            cl.nombre_actividad AS tipo,
            COUNT(*)            AS total
        FROM asistencia a
        JOIN clase cl ON cl.id_clase = a.id_clase
        WHERE a.id_cliente = ?
          AND a.presente = 'si'
        GROUP BY cl.nombre_actividad
        ORDER BY total DESC
    """

    # Métodos originales

    def _rowToVO(self, row) -> ClientesVO:
        id_cliente, estado_pagado, calorias_acumuladas = row
        return ClientesVO(id_cliente, estado_pagado, calorias_acumuladas)

    def select(self) -> list[ClientesVO]:
        """Recupera todos los clientes."""
        cursor = self.getCursor()
        clientes = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                clientes.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar clientes:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return clientes

    def selectById(self, id_cliente: int) -> ClientesVO:
        """Recupera un cliente por su ID."""
        cursor = self.getCursor()
        cliente = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_cliente,))
            row = cursor.fetchone()
            if row:
                cliente = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar cliente por ID:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return cliente

    def insert(self, vo: ClientesVO) -> int:
        """Inserta un nuevo cliente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (
                vo.id_cliente, vo.estado_pagado, vo.calorias_acumuladas
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar cliente:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def update(self, vo: ClientesVO) -> int:
        """Actualiza un cliente existente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (
                vo.estado_pagado, vo.calorias_acumuladas, vo.id_cliente
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar cliente:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def updateEstadoPagado(self, id_cliente: int, estado_pagado: str) -> int:
        """Actualiza únicamente el estado de pago de un cliente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE_ESTADO, (estado_pagado, id_cliente))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar estado de pago:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def updateCalorias(self, id_cliente: int, calorias_acumuladas: int) -> int:
        """Actualiza únicamente las calorías acumuladas de un cliente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE_CALORIAS, (calorias_acumuladas, id_cliente))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar calorías:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_cliente: int) -> int:
        """Elimina un cliente por su ID. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_cliente,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar cliente:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    #  Nuevo método 

    def selectInicioCliente(self, id_cliente: int) -> ClienteInicioVO | None:
        """
        Recopila de la base de datos toda la información necesaria para
        inicializar la interfaz unificada del cliente y la devuelve
        encapsulada en un ClienteInicioVO.

        Realiza 11 consultas independientes agrupadas lógicamente:
            1. Datos base (usuario + cliente)
            2. Tarifa activa
            3. Último pago
            4. Clases asistidas esta semana
            5. Calorías quemadas esta semana
            6. Asistencias / inscripciones del mes
            7. Próximas clases inscritas (tabla Inicio)
            8. Estadísticas semana actual
            9. Estadísticas semana anterior (para deltas)
           10. Fechas de asistencia para calcular racha
           11. Distribución por tipo de actividad

        Retorna None si el cliente no existe.
        """
        cursor = self.getCursor()
        try:
            # 1. Datos base 
            cursor.execute(self._SQL_INICIO_BASE, (id_cliente,))
            row_base = cursor.fetchone()
            if not row_base:
                return None

            (id_usu, nombre, email, telefono, direccion,
             fecha_nacimiento, fecha_registro,
             estado_pagado, calorias_acumuladas) = row_base

            # 2. Tarifa activa 
            cursor.execute(self._SQL_TARIFA_ACTIVA, (id_cliente,))
            row_tarifa = cursor.fetchone()
            nombre_tarifa  = row_tarifa[0] if row_tarifa else "Sin tarifa"
            precio_tarifa  = float(row_tarifa[1]) if row_tarifa else 0.0

            # 3. Último pago
            cursor.execute(self._SQL_ULTIMO_PAGO, (id_cliente,))
            row_pago = cursor.fetchone()
            ultimo_pago_importe = float(row_pago[0]) if row_pago else 0.0
            ultimo_pago_fecha   = row_pago[1]        if row_pago else "—"
            ultimo_pago_estado  = row_pago[2]        if row_pago else "pendiente"

            # 4. Clases asistidas esta semana 
            cursor.execute(self._SQL_CLASES_SEMANA, (id_cliente,))
            clases_semana = cursor.fetchone()[0] or 0

            # 5. Calorías esta semana 
            cursor.execute(self._SQL_CALORIAS_SEMANA, (id_cliente,))
            calorias_semana = cursor.fetchone()[0] or 0

            # 6. Asistencias e inscripciones del mes 
            cursor.execute(self._SQL_ASISTENCIAS_MES, (id_cliente, id_cliente))
            row_mes = cursor.fetchone()
            asistencias_mes   = row_mes[0] if row_mes else 0
            inscripciones_mes = row_mes[1] if row_mes else 0

            # 7. Próximas clases inscritas 
            cursor.execute(self._SQL_PROXIMAS_CLASES, (id_cliente,))
            proximas_clases = [
                {
                    "nombre_actividad": r[0],
                    "fecha":            r[1],
                    "hora_inicio":      r[2],
                    "nombre_sala":      r[3],
                }
                for r in cursor.fetchall()
            ]

            # 8. Estadísticas semana actual 
            cursor.execute(self._SQL_STATS_SEMANA_ACTUAL, (id_cliente,))
            row_actual = cursor.fetchone()
            entrenos_semana    = row_actual[0] if row_actual else 0
            tiempo_semana_min  = int(row_actual[1]) if row_actual else 0

            # 9. Estadísticas semana anterior 
            cursor.execute(self._SQL_STATS_SEMANA_ANTERIOR, (id_cliente,))
            row_ant = cursor.fetchone()
            entrenos_semana_anterior    = row_ant[0] if row_ant else 0
            tiempo_semana_anterior_min  = int(row_ant[1]) if row_ant else 0

            # 10. Racha de días consecutivos 
            cursor.execute(self._SQL_FECHAS_ASISTENCIA, (id_cliente,))
            fechas = [r[0] for r in cursor.fetchall()]  # objetos date, DESC
            racha_dias = self._calcular_racha(fechas)

            # 11. Distribución por tipo de actividad 
            cursor.execute(self._SQL_DISTRIBUCION, (id_cliente,))
            rows_dist = cursor.fetchall()
            distribucion_tipos = self._calcular_distribucion(rows_dist)

            return ClienteInicioVO(
                id_cliente=id_usu,
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion,
                fecha_nacimiento=fecha_nacimiento,
                fecha_registro=fecha_registro,
                estado_pagado=estado_pagado,
                calorias_acumuladas=calorias_acumuladas,
                nombre_tarifa=nombre_tarifa,
                precio_tarifa=precio_tarifa,
                ultimo_pago_importe=ultimo_pago_importe,
                ultimo_pago_fecha=ultimo_pago_fecha,
                ultimo_pago_estado=ultimo_pago_estado,
                clases_semana=clases_semana,
                calorias_semana=calorias_semana,
                asistencias_mes=asistencias_mes,
                inscripciones_mes=inscripciones_mes,
                proximas_clases=proximas_clases,
                entrenos_semana=entrenos_semana,
                tiempo_semana_min=tiempo_semana_min,
                entrenos_semana_anterior=entrenos_semana_anterior,
                tiempo_semana_anterior_min=tiempo_semana_anterior_min,
                racha_dias=racha_dias,
                distribucion_tipos=distribucion_tipos,
            )

        except Exception as e:
            print("Error al obtener datos de inicio del cliente:", e)
            return None
        finally:
            cursor.close()
            self.closeConnection()

    #  Helpers privados 

    @staticmethod
    def _calcular_racha(fechas: list) -> int:
        """
        Dado un listado de objetos date ordenados de más reciente a más
        antiguo (sin duplicados), calcula cuántos días consecutivos hay
        hacia atrás desde hoy.
        """
        from datetime import date, timedelta

        if not fechas:
            return 0

        hoy = date.today()
        # Si el cliente no entrenó ni hoy ni ayer, la racha ya rompió
        if fechas[0] < hoy - timedelta(days=1):
            return 0

        racha = 0
        dia_esperado = fechas[0]  # empezamos desde la asistencia más reciente
        for fecha in fechas:
            if fecha == dia_esperado:
                racha += 1
                dia_esperado -= timedelta(days=1)
            else:
                break
        return racha

    @staticmethod
    def _calcular_distribucion(rows: list) -> dict:
        """
        Convierte las filas (tipo, total) en un dict {tipo: porcentaje_int}.
        Los porcentajes suman 100; el último tipo absorbe el redondeo.
        """
        if not rows:
            return {}

        total_global = sum(r[1] for r in rows)
        if total_global == 0:
            return {}

        resultado = {}
        acumulado = 0
        tipos = list(rows)
        for i, (tipo, total) in enumerate(tipos):
            if i == len(tipos) - 1:
                # El último absorbe el residuo de redondeo
                resultado[tipo] = 100 - acumulado
            else:
                pct = round(total * 100 / total_global)
                resultado[tipo] = pct
                acumulado += pct
        return resultado
