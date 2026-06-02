from src.modelo.dao.DaoJDBCBase import DaoJDBCBase


class PagoConsultasDaoJDBC(DaoJDBCBase):

    def marcar_pago_abonado(self, id_pago: int):
        datos = self.consultar("""
            SELECT id_cliente
            FROM pago
            WHERE id_pago = ?
        """, (id_pago,))
        if not datos:
            raise ValueError("No existe ningún pago con ese ID.")
        id_cliente = datos[0][0]
        self.ejecutar("""
            UPDATE pago
            SET estado = 'abonado',
                fecha_pago = CURRENT_TIMESTAMP
            WHERE id_pago = ?
        """, (id_pago,))
        self.ejecutar("""
            UPDATE clientes
            SET estado_pagado = 'abonado'
            WHERE id_cliente = ?
        """, (id_cliente,))
        return True

    def pagos_pendientes(self):
        return self.consultar("""
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
        """)

    def informe_pagos_realizados(self):
        return self.consultar("""
            SELECT u.nombre, t.nombre, p.importe, p.fecha_pago, p.metodo_pago
            FROM pago p
            JOIN usuarios u ON p.id_cliente = u.id_usuario
            JOIN tarifa t ON p.id_tarifa = t.id_tarifa
            WHERE p.estado = 'abonado'
            ORDER BY p.fecha_pago DESC
        """)

    def total_ingresos(self):
        datos = self.consultar("SELECT COALESCE(SUM(importe),0) FROM pago WHERE estado='abonado'")
        return datos[0][0] if datos else 0

    def ingresos_por_mes(self):
        return self.consultar("""
            SELECT YEAR(fecha_pago) anio, MONTH(fecha_pago) mes, SUM(importe) total
            FROM pago
            WHERE estado='abonado'
            GROUP BY YEAR(fecha_pago), MONTH(fecha_pago)
            ORDER BY anio DESC, mes DESC LIMIT 6
        """)

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
        
    def clientes_pendientes_admin(self):
        return self.consultar("""
            SELECT 
                u.id_usuario,
                u.nombre,
                COALESCE(t.nombre, 'Sin tarifa') AS tarifa,
                c.estado_pagado
            FROM clientes c
            INNER JOIN usuarios u 
                ON c.id_cliente = u.id_usuario
            LEFT JOIN cliente_tarifa ct 
                ON c.id_cliente = ct.id_cliente
            AND ct.estado = 'activa'
            LEFT JOIN tarifa t 
                ON ct.id_tarifa = t.id_tarifa
            WHERE c.estado_pagado = 'pendiente'
            ORDER BY u.nombre
            LIMIT 10
        """)

    def buscar_pago_pendiente_por_dni(self, dni):
        d = f"%{dni.lower().strip()}%"
        return self.consultar("""
            SELECT u.nombre,
                   u.dni,
                   t.nombre,
                   p.importe,
                   p.fecha_pago,
                   p.estado
            FROM pago p
            JOIN usuarios u ON p.id_cliente = u.id_usuario
            JOIN tarifa t ON p.id_tarifa = t.id_tarifa
            WHERE p.estado = 'pendiente'
              AND LOWER(u.dni) LIKE ?
            ORDER BY p.fecha_pago DESC
        """, (d,))

    # ── Contable: pantalla de inicio ─────────────────────────────────────
    def cobros_hoy_contable(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM pago
            WHERE estado = 'abonado'
              AND DATE(fecha_pago) = CURRENT_DATE
        """)
        return datos[0][0] if datos else 0

    def ultimos_pagos_inicio_contable(self):
        return self.consultar("""
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
        """)


    def pagos_pendientes_inicio_contable(self):
        return self.consultar("""
            SELECT u.nombre AS cliente,
                   CONCAT(SUM(p.importe), ' €') AS importe_pendiente,
                   MIN(DATE(p.fecha_pago)) AS fecha_limite
            FROM pago p
            INNER JOIN usuarios u ON p.id_cliente = u.id_usuario
            WHERE p.estado = 'pendiente'
            GROUP BY p.id_cliente, u.nombre
            ORDER BY fecha_limite ASC
            LIMIT 10
        """)

    def num_pagos_pendientes_contable(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM pago
            WHERE estado = 'pendiente'
        """)
        return datos[0][0] if datos else 0

    def ingresos_mes_contable(self):
        datos = self.consultar("""
            SELECT COALESCE(SUM(importe), 0)
            FROM pago
            WHERE estado = 'abonado'
              AND YEAR(fecha_pago) = YEAR(CURRENT_DATE)
              AND MONTH(fecha_pago) = MONTH(CURRENT_DATE)
        """)
        return datos[0][0] if datos else 0

    # ── Contable: pagos pendientes ───────────────────────────────────────
    def contable_clientes_con_deuda(self):
        datos = self.consultar("""
            SELECT COUNT(DISTINCT id_cliente)
            FROM pago
            WHERE estado = 'pendiente'
        """)
        return datos[0][0] if datos else 0

    def contable_importe_pendiente(self):
        datos = self.consultar("""
            SELECT COALESCE(SUM(importe), 0)
            FROM pago
            WHERE estado = 'pendiente'
        """)
        return datos[0][0] if datos else 0

    def contable_pagos_vencidos(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM pago
            WHERE estado = 'pendiente'
              AND DATE(fecha_pago) < CURRENT_DATE
        """)
        return datos[0][0] if datos else 0

    def contable_pagos_vencen_semana(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM pago
            WHERE estado = 'pendiente'
              AND DATE(fecha_pago) BETWEEN CURRENT_DATE AND DATE_ADD(CURRENT_DATE, INTERVAL 7 DAY)
        """)
        return datos[0][0] if datos else 0

    # ── Contable: registrar pago ─────────────────────────────────────────
    def buscar_cliente_tarifa_por_dni(self, dni):
        datos = self.consultar("""
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
        """, (dni,))
        return datos[0] if datos else None

    def registrar_pago_contable(self, dni_cliente, id_contable, metodo_pago, fecha_pago):
        cliente = self.buscar_cliente_tarifa_por_dni(dni_cliente)

        if not cliente:
            return False, "No se ha encontrado ningún cliente con ese DNI o no tiene tarifa activa."

        id_cliente = cliente[0]
        nombre_cliente = cliente[1]
        id_tarifa = cliente[3]
        nombre_tarifa = cliente[4]
        importe = cliente[5]

        ya_abonado = self.consultar("""
            SELECT id_pago
            FROM pago
            WHERE id_cliente = ?
              AND estado = 'abonado'
              AND YEAR(fecha_pago) = YEAR(?)
              AND MONTH(fecha_pago) = MONTH(?)
            LIMIT 1
        """, (id_cliente, fecha_pago, fecha_pago))

        if ya_abonado:
            return False, f"El cliente {nombre_cliente} ya tiene un pago abonado en ese mes."

        pendiente = self.consultar("""
            SELECT id_pago
            FROM pago
            WHERE id_cliente = ?
              AND estado = 'pendiente'
            ORDER BY fecha_pago DESC
            LIMIT 1
        """, (id_cliente,))

        if pendiente:
            id_pago = pendiente[0][0]
            self.ejecutar("""
                UPDATE pago
                SET estado = 'abonado',
                    metodo_pago = ?,
                    fecha_pago = ?,
                    id_contable = ?
                WHERE id_pago = ?
            """, (metodo_pago, fecha_pago, id_contable, id_pago))
        else:
            self.ejecutar("""
                INSERT INTO pago
                (id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago, estado, tipo_cuota)
                VALUES (?, ?, ?, ?, ?, ?, 'abonado', 'mensual')
            """, (id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago))

        self.ejecutar("""
            UPDATE clientes
            SET estado_pagado = 'abonado'
            WHERE id_cliente = ?
        """, (id_cliente,))

        mensaje = f"Pago registrado correctamente para {nombre_cliente}.\nTarifa: {nombre_tarifa}\nImporte: {importe} €"
        return True, mensaje

    # ── Contable: gestión económica ──────────────────────────────────────
    def contable_total_nominas(self):
        datos = self.consultar("""
            SELECT COALESCE(SUM(salario), 0)
            FROM empleados
        """)
        return datos[0][0] if datos else 0

    def contable_balance_economico(self):
        ingresos = self.total_ingresos()
        gastos = self.contable_total_nominas()
        return ingresos, gastos, ingresos - gastos

    # ── Contable: informes/perfil ────────────────────────────────────────
    def contable_gastos_mes(self):
        return self.contable_total_nominas()

    def contable_balance_mes(self):
        return self.ingresos_mes_contable() - self.contable_gastos_mes()

    def contable_pagos_registrados(self, id_contable):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM pago
            WHERE id_contable = ?
              AND estado = 'abonado'
        """, (id_contable,))
        return datos[0][0] if datos else 0

    def contable_pendientes_revisados(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM pago
            WHERE estado = 'pendiente'
        """)
        return datos[0][0] if datos else 0

    def contable_importe_gestionado(self, id_contable):
        datos = self.consultar("""
            SELECT COALESCE(SUM(importe), 0)
            FROM pago
            WHERE id_contable = ?
              AND estado = 'abonado'
        """, (id_contable,))
        return datos[0][0] if datos else 0
