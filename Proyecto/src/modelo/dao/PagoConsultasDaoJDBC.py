from src.modelo.dao.DaoJDBCBase import DaoJDBCBase
from src.modelo.VO.ClientePendienteAdminVO import ClientePendienteAdminVO
from src.modelo.VO.IngresoMesVO import IngresoMesVO
from src.modelo.VO.InformePagoVO import InformePagoVO
from src.modelo.VO.PagoPendienteInicioVO import PagoPendienteInicioVO
from src.modelo.VO.UltimoPagoVO import UltimoPagoVO
from src.modelo.VO.PagoPendienteVO import PagoPendienteVO


class PagoConsultasDaoJDBC(DaoJDBCBase):

    SQL_MARCAR_CLIENTE_ABONADO = """
        UPDATE clientes
        SET estado_pagado = 'abonado'
        WHERE id_cliente = ?
    """

    SQL_LISTAR_PAGOS_PENDIENTES_ADMIN = """
        SELECT 
            0 AS id_pago,
            u.dni,
            u.nombre,
            COALESCE(t.nombre, 'Sin tarifa') AS tarifa,
            COALESCE(t.precio_mensual, 0) AS precio,
            COALESCE(ct.fecha_contratacion, CURDATE()) AS fecha_pago,
            c.estado_pagado AS estado
        FROM clientes c
        INNER JOIN usuarios u 
            ON c.id_cliente = u.id_usuario
        LEFT JOIN cliente_tarifa ct 
            ON c.id_cliente = ct.id_cliente
           AND ct.estado = 'activa'
        LEFT JOIN tarifa t 
            ON ct.id_tarifa = t.id_tarifa
        WHERE LOWER(c.estado_pagado) = 'pendiente'
        ORDER BY ct.fecha_contratacion DESC
    """

    SQL_PAGOS_PENDIENTES = """
        SELECT 
            0 AS id_pago,
            u.nombre AS cliente,
            COALESCE(t.nombre, 'Sin tarifa') AS tarifa,
            CONCAT(COALESCE(t.precio_mensual, 0), ' €') AS importe,
            COALESCE(ct.fecha_contratacion, CURDATE()) AS fecha,
            'mensual' AS tipo_cuota
        FROM clientes c
        INNER JOIN usuarios u 
            ON c.id_cliente = u.id_usuario
        LEFT JOIN cliente_tarifa ct
            ON c.id_cliente = ct.id_cliente
        AND ct.estado = 'activa'
        LEFT JOIN tarifa t 
            ON ct.id_tarifa = t.id_tarifa
        WHERE LOWER(c.estado_pagado) = 'pendiente'
        ORDER BY ct.fecha_contratacion ASC
    """

    SQL_INFORME_PAGOS_REALIZADOS = """
        SELECT 
            u.nombre, 
            t.nombre, 
            p.importe, 
            p.fecha_pago, 
            p.metodo_pago
        FROM pago p
        INNER JOIN usuarios u 
            ON p.id_cliente = u.id_usuario
        INNER JOIN tarifa t 
            ON p.id_tarifa = t.id_tarifa
        ORDER BY p.fecha_pago DESC
    """

    SQL_TOTAL_INGRESOS = """
        SELECT COALESCE(SUM(importe), 0)
        FROM pago
    """

    SQL_INGRESOS_POR_MES = """
        SELECT 
            YEAR(fecha_pago) AS anio,
            MONTH(fecha_pago) AS mes,
            COALESCE(SUM(importe), 0) AS total
        FROM pago
        GROUP BY YEAR(fecha_pago), MONTH(fecha_pago)
        ORDER BY anio DESC, mes DESC
        LIMIT 6
    """

    SQL_INGRESOS_MES_ACTUAL = """
        SELECT COALESCE(SUM(importe), 0)
        FROM pago
        WHERE YEAR(fecha_pago) = YEAR(CURDATE())
          AND MONTH(fecha_pago) = MONTH(CURDATE())
    """

    SQL_INGRESOS_ANIO_ACTUAL = """
        SELECT COALESCE(SUM(importe), 0)
        FROM pago
        WHERE YEAR(fecha_pago) = YEAR(CURDATE())
    """

    SQL_NUM_CLIENTES_PENDIENTES = """
        SELECT COUNT(*)
        FROM clientes
        WHERE LOWER(estado_pagado) = 'pendiente'
    """

    SQL_IMPORTE_PENDIENTE = """
        SELECT 
            COALESCE(SUM(t.precio_mensual), 0)
        FROM clientes c
        LEFT JOIN cliente_tarifa ct
            ON c.id_cliente = ct.id_cliente
           AND ct.estado = 'activa'
        LEFT JOIN tarifa t
            ON ct.id_tarifa = t.id_tarifa
        WHERE LOWER(c.estado_pagado) = 'pendiente'
    """

    SQL_CLIENTES_PENDIENTES_ADMIN = """
        SELECT 
            u.nombre AS cliente,
            u.dni AS dni,
            COALESCE(t.nombre, 'Sin tarifa') AS tarifa,
            COALESCE(t.precio_mensual, 0) AS importe_pendiente,
            COALESCE(DATE_ADD(ct.fecha_contratacion, INTERVAL 30 DAY), CURDATE()) AS fecha_limite
        FROM clientes c
        INNER JOIN usuarios u 
            ON c.id_cliente = u.id_usuario
        LEFT JOIN cliente_tarifa ct 
            ON c.id_cliente = ct.id_cliente
           AND ct.estado = 'activa'
        LEFT JOIN tarifa t 
            ON ct.id_tarifa = t.id_tarifa
        WHERE LOWER(c.estado_pagado) = 'pendiente'
        ORDER BY u.nombre
    """

    SQL_BUSCAR_CLIENTE_PENDIENTE_DNI_ADMIN = """
        SELECT 
            u.nombre AS cliente,
            u.dni AS dni,
            COALESCE(t.nombre, 'Sin tarifa') AS tarifa,
            COALESCE(t.precio_mensual, 0) AS importe_pendiente,
            COALESCE(DATE_ADD(ct.fecha_contratacion, INTERVAL 30 DAY), CURDATE()) AS fecha_limite
        FROM clientes c
        INNER JOIN usuarios u 
            ON c.id_cliente = u.id_usuario
        LEFT JOIN cliente_tarifa ct 
            ON c.id_cliente = ct.id_cliente
           AND ct.estado = 'activa'
        LEFT JOIN tarifa t 
            ON ct.id_tarifa = t.id_tarifa
        WHERE LOWER(c.estado_pagado) = 'pendiente'
          AND LOWER(u.dni) LIKE ?
        ORDER BY u.nombre
    """

    SQL_COBROS_HOY = """
        SELECT COUNT(*)
        FROM pago
        WHERE DATE(fecha_pago) = CURDATE()
    """

    SQL_ULTIMOS_PAGOS_CONTABLE = """
        SELECT 
            u.nombre AS cliente,
            COALESCE(t.nombre, 'Sin tarifa') AS tarifa,
            p.importe,
            DATE(p.fecha_pago) AS fecha,
            'abonado' AS estado
        FROM pago p
        INNER JOIN usuarios u 
            ON p.id_cliente = u.id_usuario
        LEFT JOIN tarifa t
            ON p.id_tarifa = t.id_tarifa
        ORDER BY p.fecha_pago DESC
        LIMIT 10
    """

    SQL_PAGOS_PENDIENTES_CONTABLE = """
        SELECT 
            u.nombre AS cliente,
            CONCAT(COALESCE(t.precio_mensual, 0), ' €') AS importe_pendiente,
            COALESCE(DATE_ADD(ct.fecha_contratacion, INTERVAL 30 DAY), CURDATE()) AS fecha_limite
        FROM clientes c
        INNER JOIN usuarios u 
            ON c.id_cliente = u.id_usuario
        LEFT JOIN cliente_tarifa ct
            ON c.id_cliente = ct.id_cliente
           AND ct.estado = 'activa'
        LEFT JOIN tarifa t
            ON ct.id_tarifa = t.id_tarifa
        WHERE LOWER(c.estado_pagado) = 'pendiente'
        ORDER BY fecha_limite ASC
        LIMIT 10
    """

    SQL_NUM_PAGOS_PENDIENTES = """
        SELECT COUNT(*)
        FROM clientes c
        INNER JOIN cliente_tarifa ct
            ON c.id_cliente = ct.id_cliente
        AND ct.estado = 'activa'
        WHERE LOWER(c.estado_pagado) = 'pendiente'
        AND DATE(ct.fecha_contratacion) >= CURRENT_DATE
    """

    SQL_INGRESOS_MES_CONTABLE = """
        SELECT COALESCE(SUM(importe), 0)
        FROM pago
        WHERE YEAR(fecha_pago) = YEAR(CURDATE())
          AND MONTH(fecha_pago) = MONTH(CURDATE())
    """

    SQL_CLIENTES_CON_DEUDA = """
        SELECT COUNT(*)
        FROM clientes
        WHERE LOWER(estado_pagado) = 'pendiente'
    """

    SQL_PAGOS_VENCIDOS = """
        SELECT COUNT(*)
        FROM clientes c
        INNER JOIN cliente_tarifa ct
            ON c.id_cliente = ct.id_cliente
        AND ct.estado = 'activa'
        WHERE LOWER(c.estado_pagado) = 'pendiente'
        AND DATE(ct.fecha_contratacion) < CURRENT_DATE
    """

    SQL_PAGOS_VENCEN_SEMANA = """
        SELECT COUNT(*)
        FROM clientes c
        INNER JOIN cliente_tarifa ct
            ON c.id_cliente = ct.id_cliente
        AND ct.estado = 'activa'
        WHERE LOWER(c.estado_pagado) = 'pendiente'
        AND DATE(ct.fecha_contratacion) >= CURRENT_DATE
        AND DATE(ct.fecha_contratacion) <= DATE_ADD(CURRENT_DATE, INTERVAL 7 DAY)
    """

    SQL_BUSCAR_PAGO_PENDIENTE_DNI = """
        SELECT 
            0 AS id_pago,
            u.id_usuario,
            u.nombre,
            u.dni,
            t.id_tarifa,
            t.nombre,
            t.precio_mensual AS importe,
            COALESCE(ct.fecha_contratacion, CURDATE()) AS fecha_pago
        FROM clientes c
        INNER JOIN usuarios u 
            ON c.id_cliente = u.id_usuario
        INNER JOIN cliente_tarifa ct
            ON c.id_cliente = ct.id_cliente
           AND ct.estado = 'activa'
        INNER JOIN tarifa t 
            ON ct.id_tarifa = t.id_tarifa
        WHERE LOWER(c.estado_pagado) = 'pendiente'
          AND UPPER(u.dni) = UPPER(?)
        ORDER BY ct.fecha_contratacion DESC
        LIMIT 1
    """

    SQL_BUSCAR_CLIENTE_TARIFA_DNI = """
        SELECT 
            u.id_usuario, 
            u.nombre, 
            u.dni,
            t.id_tarifa, 
            t.nombre, 
            t.precio_mensual
        FROM usuarios u
        INNER JOIN clientes c 
            ON u.id_usuario = c.id_cliente
        INNER JOIN cliente_tarifa ct 
            ON c.id_cliente = ct.id_cliente
           AND ct.estado = 'activa'
        INNER JOIN tarifa t 
            ON ct.id_tarifa = t.id_tarifa
        WHERE UPPER(u.dni) = UPPER(?)
        LIMIT 1
    """

    SQL_PAGO_YA_ABONADO_MES = """
        SELECT id_pago 
        FROM pago
        WHERE id_cliente = ?
          AND YEAR(fecha_pago) = YEAR(?) 
          AND MONTH(fecha_pago) = MONTH(?)
        LIMIT 1
    """

    SQL_INSERT_PAGO_ABONADO = """
        INSERT INTO pago 
            (id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago)
        VALUES 
            (?, ?, ?, ?, ?, ?)
    """

    SQL_TOTAL_NOMINAS = """
        SELECT COALESCE(SUM(salario), 0) 
        FROM empleados
    """

    SQL_PAGOS_REGISTRADOS_CONTABLE = """
        SELECT COUNT(*)
        FROM pago p
        WHERE p.id_contable = ?
    """

    SQL_PENDIENTES_REVISADOS = """
        SELECT COUNT(*)
        FROM clientes
        WHERE LOWER(estado_pagado) = 'pendiente'
    """

    SQL_IMPORTE_GESTIONADO = """
        SELECT COALESCE(SUM(importe), 0)
        FROM pago
        WHERE id_contable = ?
    """

    SQL_PRIMER_PAGO_PENDIENTE = """
        SELECT 
            0 AS id_pago,
            u.id_usuario,
            u.nombre,
            u.dni,
            t.id_tarifa,
            t.nombre,
            t.precio_mensual AS importe,
            COALESCE(ct.fecha_contratacion, CURDATE()) AS fecha_pago
        FROM clientes c
        INNER JOIN usuarios u 
            ON c.id_cliente = u.id_usuario
        INNER JOIN cliente_tarifa ct
            ON c.id_cliente = ct.id_cliente
           AND ct.estado = 'activa'
        INNER JOIN tarifa t 
            ON ct.id_tarifa = t.id_tarifa
        WHERE LOWER(c.estado_pagado) = 'pendiente'
        ORDER BY ct.fecha_contratacion DESC
        LIMIT 1
    """

    def primer_pago_pendiente(self):
        datos = self.consultar(self.SQL_PRIMER_PAGO_PENDIENTE)
        return datos[0] if datos else None

    def listar_pagos_pendientes_admin(self):
        return self.consultar(self.SQL_LISTAR_PAGOS_PENDIENTES_ADMIN)  # tuplas para uso interno

    def marcar_pago_abonado(self, id_pago: int):
        raise ValueError("Con la base nueva no se actualiza pago.estado. Se registra el pago y se marca el cliente como abonado.")

    def pagos_pendientes(self):
        filas = self.consultar(self.SQL_PAGOS_PENDIENTES)
        return [PagoPendienteVO(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    def informe_pagos_realizados(self):
        filas = self.consultar(self.SQL_INFORME_PAGOS_REALIZADOS)
        return [InformePagoVO(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    def total_ingresos(self):
        datos = self.consultar(self.SQL_TOTAL_INGRESOS)
        return datos[0][0] if datos else 0

    def ingresos_por_mes(self):
        filas = self.consultar(self.SQL_INGRESOS_POR_MES)
        return [IngresoMesVO(f[0], f[1], f[2]) for f in filas]

    def ingresos_mes_actual(self):
        datos = self.consultar(self.SQL_INGRESOS_MES_ACTUAL)
        return datos[0][0] if datos else 0

    def ingresos_anio_actual(self):
        datos = self.consultar(self.SQL_INGRESOS_ANIO_ACTUAL)
        return datos[0][0] if datos else 0

    def numero_clientes_pendientes_pago(self):
        datos = self.consultar(self.SQL_NUM_CLIENTES_PENDIENTES)
        return datos[0][0] if datos else 0

    def importe_pendiente_cobrar(self):
        datos = self.consultar(self.SQL_IMPORTE_PENDIENTE)
        return datos[0][0] if datos else 0

    def clientes_pendientes_admin(self):
        filas = self.consultar(self.SQL_CLIENTES_PENDIENTES_ADMIN)
        return [ClientePendienteAdminVO(f[0],f[1],f[2],f[3],f[4]) for f in filas]

    def buscar_cliente_pendiente_por_dni_admin(self, dni):
        d = f"%{dni.lower().strip()}%"
        filas = self.consultar(self.SQL_BUSCAR_CLIENTE_PENDIENTE_DNI_ADMIN, (d,))
        return [ClientePendienteAdminVO(f[0],f[1],f[2],f[3],f[4]) for f in filas]

    def buscar_pago_pendiente_por_dni(self, dni):
        d = dni.strip().upper()
        datos = self.consultar(self.SQL_BUSCAR_PAGO_PENDIENTE_DNI, (d,))
        return datos[0] if datos else None

    def cobros_hoy_contable(self):
        datos = self.consultar(self.SQL_COBROS_HOY)
        return datos[0][0] if datos else 0

    def ultimos_pagos_inicio_contable(self):
        filas = self.consultar(self.SQL_ULTIMOS_PAGOS_CONTABLE)
        return [UltimoPagoVO(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    def pagos_pendientes_inicio_contable(self):
        filas = self.consultar(self.SQL_PAGOS_PENDIENTES_CONTABLE)
        return [PagoPendienteInicioVO(f[0], f[1], f[2]) for f in filas]

    def num_pagos_pendientes_contable(self):
        datos = self.consultar(self.SQL_NUM_PAGOS_PENDIENTES)
        return datos[0][0] if datos else 0

    def ingresos_mes_contable(self):
        datos = self.consultar(self.SQL_INGRESOS_MES_CONTABLE)
        return datos[0][0] if datos else 0

    def contable_clientes_con_deuda(self):
        datos = self.consultar(self.SQL_CLIENTES_CON_DEUDA)
        return datos[0][0] if datos else 0

    def contable_importe_pendiente(self):
        datos = self.consultar(self.SQL_IMPORTE_PENDIENTE)
        return datos[0][0] if datos else 0

    def contable_pagos_vencidos(self):
        datos = self.consultar(self.SQL_PAGOS_VENCIDOS)
        return datos[0][0] if datos else 0

    def contable_pagos_vencen_semana(self):
        datos = self.consultar(self.SQL_PAGOS_VENCEN_SEMANA)
        return datos[0][0] if datos else 0

    def buscar_cliente_tarifa_por_dni(self, dni):
        datos = self.consultar(self.SQL_BUSCAR_CLIENTE_TARIFA_DNI, (dni,))
        return datos[0] if datos else None

    def registrar_pago_contable(self, dni_cliente, id_contable, metodo_pago, fecha_pago):
        cliente = self.buscar_cliente_tarifa_por_dni(dni_cliente)

        if not cliente:
            return False, "No se ha encontrado ningún cliente con ese DNI o no tiene tarifa activa."

        id_cliente, nombre_cliente, dni, id_tarifa, nombre_tarifa, importe = cliente

        if self.consultar(self.SQL_PAGO_YA_ABONADO_MES, (id_cliente, fecha_pago, fecha_pago)):
            return False, f"El cliente {nombre_cliente} ya tiene un pago registrado en ese mes."

        self.ejecutar(
            self.SQL_INSERT_PAGO_ABONADO,
            (id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago)
        )

        self.ejecutar(self.SQL_MARCAR_CLIENTE_ABONADO, (id_cliente,))

        return True, (
            f"Pago registrado correctamente para {nombre_cliente}.\n"
            f"Tarifa: {nombre_tarifa}\n"
            f"Importe: {importe} €"
        )

    def contable_total_nominas(self):
        datos = self.consultar(self.SQL_TOTAL_NOMINAS)
        return datos[0][0] if datos else 0

    def contable_balance_economico(self):
        ingresos = self.total_ingresos()
        gastos = self.contable_total_nominas()
        return ingresos, gastos, ingresos - gastos

    def contable_gastos_mes(self):
        return self.contable_total_nominas()

    def contable_balance_mes(self):
        return self.ingresos_mes_contable() - self.contable_gastos_mes()

    def contable_pagos_registrados(self, id_contable):
        datos = self.consultar(self.SQL_PAGOS_REGISTRADOS_CONTABLE, (id_contable,))
        return datos[0][0] if datos else 0

    def contable_pendientes_revisados(self):
        datos = self.consultar(self.SQL_PENDIENTES_REVISADOS)
        return datos[0][0] if datos else 0

    def contable_importe_gestionado(self, id_contable):
        datos = self.consultar(self.SQL_IMPORTE_GESTIONADO, (id_contable,))
        return datos[0][0] if datos else 0