from src.modelo.dao.DaoJDBCBase import DaoJDBCBase
from src.modelo.VO.ClientePendienteAdminVO import ClientePendienteAdminVO
from src.modelo.VO.IngresoMesVO import IngresoMesVO
from src.modelo.VO.InformePagoVO import InformePagoVO
from src.modelo.VO.PagoPendienteInicioVO import PagoPendienteInicioVO
from src.modelo.VO.UltimoPagoVO import UltimoPagoVO
from src.modelo.VO.PagoPendienteVO import PagoPendienteVO


class PagoConsultasDaoJDBC(DaoJDBCBase):
    """DAO de consultas y operaciones sobre pagos.
    """

    # Cambio de estado

    # Marca a un cliente como abonado tras registrar su pago
    SQL_MARCAR_CLIENTE_ABONADO = """
        UPDATE clientes
        SET estado_pagado = 'abonado'
        WHERE id_cliente = ?
    """

    # Inserta un nuevo registro de pago en la tabla pago
    SQL_INSERT_PAGO_ABONADO = """
        INSERT INTO pago 
            (id_cliente, id_contable, id_tarifa, importe, metodo_pago, fecha_pago)
        VALUES 
            (?, ?, ?, ?, ?, ?)
    """

    # Consultas pagos pendientes

    # Primer cliente con pago pendiente 
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

    # Lista de pagos pendientes para la pantalla de pagos del contable
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

    # Lista de clientes con pago pendiente para la pantalla del administrador
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

    # Clientes pendientes de pago con fecha límite (tabla admin pagos)
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

    # Busca clientes pendientes filtrando por DNI 
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

    # Busca el pago pendiente de un cliente por DNI exacto 
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

    # Datos del cliente y su tarifa activa por DNI (para validar antes de registrar pago)
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

    # Comprueba si el cliente ya tiene un pago registrado en el mismo mes
    SQL_PAGO_YA_ABONADO_MES = """
        SELECT id_pago 
        FROM pago
        WHERE id_cliente = ?
          AND YEAR(fecha_pago) = YEAR(?) 
          AND MONTH(fecha_pago) = MONTH(?)
        LIMIT 1
    """

    # Consultas sobre ingresos

    # Suma total de todos los pagos registrados
    SQL_TOTAL_INGRESOS = """
        SELECT COALESCE(SUM(importe), 0)
        FROM pago
    """

    # Ingresos agrupados por año y mes (últimos 6 meses, para el gráfico del admin)
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

    # Ingresos del mes en curso
    SQL_INGRESOS_MES_ACTUAL = """
        SELECT COALESCE(SUM(importe), 0)
        FROM pago
        WHERE YEAR(fecha_pago) = YEAR(CURDATE())
          AND MONTH(fecha_pago) = MONTH(CURDATE())
    """

    # Ingresos del año en curso
    SQL_INGRESOS_ANIO_ACTUAL = """
        SELECT COALESCE(SUM(importe), 0)
        FROM pago
        WHERE YEAR(fecha_pago) = YEAR(CURDATE())
    """

    # Ingresos del mes en curso (alias usado por el contable)
    SQL_INGRESOS_MES_CONTABLE = """
        SELECT COALESCE(SUM(importe), 0)
        FROM pago
        WHERE YEAR(fecha_pago) = YEAR(CURDATE())
          AND MONTH(fecha_pago) = MONTH(CURDATE())
    """

    # Consulta totales

    # Número de clientes con pago pendiente (para el admin)
    SQL_NUM_CLIENTES_PENDIENTES = """
        SELECT COUNT(*)
        FROM clientes
        WHERE LOWER(estado_pagado) = 'pendiente'
    """

    # Importe total pendiente de cobrar (suma de cuotas de clientes no abonados)
    SQL_IMPORTE_PENDIENTE = """
        SELECT COALESCE(SUM(t.precio_mensual), 0)
        FROM clientes c
        LEFT JOIN cliente_tarifa ct
            ON c.id_cliente = ct.id_cliente
           AND ct.estado = 'activa'
        LEFT JOIN tarifa t
            ON ct.id_tarifa = t.id_tarifa
        WHERE LOWER(c.estado_pagado) = 'pendiente'
    """

    # Número de clientes con pago pendiente (para el contable)
    SQL_NUM_PAGOS_PENDIENTES = """
        SELECT COUNT(*)
        FROM clientes c
        LEFT JOIN cliente_tarifa ct
            ON c.id_cliente = ct.id_cliente
           AND ct.estado = 'activa'
        WHERE LOWER(c.estado_pagado) = 'pendiente'
    """

    # Número de clientes con deuda 
    SQL_CLIENTES_CON_DEUDA = """
        SELECT COUNT(*)
        FROM clientes
        WHERE LOWER(estado_pagado) = 'pendiente'
    """

    # Pagos vencidos: clientes con fecha de contratación anterior a hoy y sin abonar
    SQL_PAGOS_VENCIDOS = """
        SELECT COUNT(*)
        FROM clientes c
        INNER JOIN cliente_tarifa ct
            ON c.id_cliente = ct.id_cliente
           AND ct.estado = 'activa'
        WHERE LOWER(c.estado_pagado) = 'pendiente'
          AND DATE(ct.fecha_contratacion) < CURRENT_DATE
    """

    # Pagos que vencen en los próximos 7 días
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

    # Cobros realizados hoy
    SQL_COBROS_HOY = """
        SELECT COUNT(*)
        FROM pago
        WHERE DATE(fecha_pago) = CURDATE()
    """

    # ─Consultas contable

    # Últimos 10 pagos registrados (para la tabla de inicio del contable)
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

    # Primeros 10 clientes con pago pendiente (para la tabla de inicio del contable)
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

    # Total de nóminas (suma de salarios de todos los empleados)
    SQL_TOTAL_NOMINAS = """
        SELECT COALESCE(SUM(salario), 0) 
        FROM empleados
    """

    # Número de pagos registrados por un contable concreto
    SQL_PAGOS_REGISTRADOS_CONTABLE = """
        SELECT COUNT(*)
        FROM pago p
        WHERE p.id_contable = ?
    """

    # Número de clientes con pago pendiente 
    SQL_PENDIENTES_REVISADOS = """
        SELECT COUNT(*)
        FROM clientes
        WHERE LOWER(estado_pagado) = 'pendiente'
    """

    # Importe total gestionado por un contable concreto
    SQL_IMPORTE_GESTIONADO = """
        SELECT COALESCE(SUM(importe), 0)
        FROM pago
        WHERE id_contable = ?
    """

    # Informe completo de pagos realizados (para el informe de pagos del contable)
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

    # Funciones

    def primer_pago_pendiente(self):
        """Devuelve los datos del primer cliente con pago pendiente como tupla,
        o None si no hay ninguno."""
        datos = self.consultar(self.SQL_PRIMER_PAGO_PENDIENTE)
        return datos[0] if datos else None

    def listar_pagos_pendientes_admin(self):
        """Devuelve todos los clientes con pago pendiente
        como lista de ClientePendienteAdminVO, para la tabla del administrador."""
        filas = self.consultar(self.SQL_LISTAR_PAGOS_PENDIENTES_ADMIN)
        return [ClientePendienteAdminVO(f[2], f[1], f[3], f[4], f[5]) for f in filas]


    def pagos_pendientes(self):
        """Devuelve todos los pagos pendientes como lista de PagoPendienteVO.
        Usada en la pantalla de pagos pendientes del contable."""
        filas = self.consultar(self.SQL_PAGOS_PENDIENTES)
        return [PagoPendienteVO(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    def informe_pagos_realizados(self):
        """Devuelve todos los pagos realizados como lista de InformePagoVO,
        ordenados del más reciente al más antiguo."""
        filas = self.consultar(self.SQL_INFORME_PAGOS_REALIZADOS)
        return [InformePagoVO(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    def total_ingresos(self):
        """Devuelve la suma total de todos los pagos registrados en la BD."""
        datos = self.consultar(self.SQL_TOTAL_INGRESOS)
        return datos[0][0] if datos else 0

    def ingresos_por_mes(self):
        """Devuelve los ingresos de los últimos 6 meses como lista de IngresoMesVO.
        Usada para el gráfico de ingresos del administrador."""
        filas = self.consultar(self.SQL_INGRESOS_POR_MES)
        return [IngresoMesVO(f[0], f[1], f[2]) for f in filas]

    def ingresos_mes_actual(self):
        """Devuelve el total de ingresos del mes en curso."""
        datos = self.consultar(self.SQL_INGRESOS_MES_ACTUAL)
        return datos[0][0] if datos else 0

    def ingresos_anio_actual(self):
        """Devuelve el total de ingresos del año en curso."""
        datos = self.consultar(self.SQL_INGRESOS_ANIO_ACTUAL)
        return datos[0][0] if datos else 0

    def numero_clientes_pendientes_pago(self):
        """Devuelve el número de clientes con estado de pago pendiente."""
        datos = self.consultar(self.SQL_NUM_CLIENTES_PENDIENTES)
        return datos[0][0] if datos else 0

    def importe_pendiente_cobrar(self):
        """Devuelve el importe total pendiente de cobrar
        (suma de cuotas de todos los clientes no abonados)."""
        datos = self.consultar(self.SQL_IMPORTE_PENDIENTE)
        return datos[0][0] if datos else 0

    def clientes_pendientes_admin(self):
        """Devuelve los clientes con pago pendiente como lista de ClientePendienteAdminVO,
        con nombre, DNI, tarifa, importe y fecha límite."""
        filas = self.consultar(self.SQL_CLIENTES_PENDIENTES_ADMIN)
        return [ClientePendienteAdminVO(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    def buscar_cliente_pendiente_por_dni_admin(self, dni):
        """Busca clientes con pago pendiente cuyo DNI contenga el texto indicado.
        Devuelve lista de ClientePendienteAdminVO."""
        d = f"%{dni.lower().strip()}%"
        filas = self.consultar(self.SQL_BUSCAR_CLIENTE_PENDIENTE_DNI_ADMIN, (d,))
        return [ClientePendienteAdminVO(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    def buscar_pago_pendiente_por_dni(self, dni):
        """Busca el pago pendiente de un cliente por DNI exacto.
        Devuelve la fila como tupla, o None si no hay pago pendiente."""
        d = dni.strip().upper()
        datos = self.consultar(self.SQL_BUSCAR_PAGO_PENDIENTE_DNI, (d,))
        return datos[0] if datos else None

    def cobros_hoy_contable(self):
        """Devuelve el número de pagos registrados hoy."""
        datos = self.consultar(self.SQL_COBROS_HOY)
        return datos[0][0] if datos else 0

    def ultimos_pagos_inicio_contable(self):
        """Devuelve los últimos 10 pagos registrados como lista de UltimoPagoVO,
        para la tabla de inicio del contable."""
        filas = self.consultar(self.SQL_ULTIMOS_PAGOS_CONTABLE)
        return [UltimoPagoVO(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    def pagos_pendientes_inicio_contable(self):
        """Devuelve los primeros 10 clientes con pago pendiente como lista de
        PagoPendienteInicioVO, para la tabla de inicio del contable."""
        filas = self.consultar(self.SQL_PAGOS_PENDIENTES_CONTABLE)
        return [PagoPendienteInicioVO(f[0], f[1], f[2]) for f in filas]

    def num_pagos_pendientes_contable(self):
        """Devuelve el número total de clientes con pago pendiente."""
        datos = self.consultar(self.SQL_NUM_PAGOS_PENDIENTES)
        return datos[0][0] if datos else 0

    def ingresos_mes_contable(self):
        """Devuelve los ingresos del mes en curso ."""
        datos = self.consultar(self.SQL_INGRESOS_MES_CONTABLE)
        return datos[0][0] if datos else 0

    def contable_clientes_con_deuda(self):
        """Devuelve el número de clientes con deuda pendiente."""
        datos = self.consultar(self.SQL_CLIENTES_CON_DEUDA)
        return datos[0][0] if datos else 0

    def contable_importe_pendiente(self):
        """Devuelve el importe total pendiente de cobrar."""
        datos = self.consultar(self.SQL_IMPORTE_PENDIENTE)
        return datos[0][0] if datos else 0

    def contable_pagos_vencidos(self):
        """Devuelve el número de pagos cuya fecha de contratación ya ha pasado
        y siguen sin abonar."""
        datos = self.consultar(self.SQL_PAGOS_VENCIDOS)
        return datos[0][0] if datos else 0

    def contable_pagos_vencen_semana(self):
        """Devuelve el número de pagos que vencen en los próximos 7 días."""
        datos = self.consultar(self.SQL_PAGOS_VENCEN_SEMANA)
        return datos[0][0] if datos else 0

    def buscar_cliente_tarifa_por_dni(self, dni):
        """Devuelve los datos del cliente y su tarifa activa por DNI exacto,
        o None si no existe o no tiene tarifa activa."""
        datos = self.consultar(self.SQL_BUSCAR_CLIENTE_TARIFA_DNI, (dni,))
        return datos[0] if datos else None

    def registrar_pago_contable(self, dni_cliente, id_contable, metodo_pago, fecha_pago):
        """Registra el pago de un cliente identificado por DNI.

        Pasos:
        1. Busca al cliente y su tarifa activa por DNI.
        2. Comprueba que no tenga ya un pago registrado en el mismo mes.
        3. Inserta el pago en la tabla pago.
        4. Actualiza el estado del cliente a 'abonado'.
        """
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
        """Devuelve la suma total de salarios de todos los empleados."""
        datos = self.consultar(self.SQL_TOTAL_NOMINAS)
        return datos[0][0] if datos else 0

    def contable_balance_economico(self):
        """Devuelve una tupla (ingresos, gastos, balance) con el balance económico global."""
        ingresos = self.total_ingresos()
        gastos   = self.contable_total_nominas()
        return ingresos, gastos, ingresos - gastos

    def contable_gastos_mes(self):
        """Devuelve los gastos del mes actual ."""
        return self.contable_total_nominas()

    def contable_balance_mes(self):
        """Devuelve el balance del mes actual: ingresos del mes menos nóminas."""
        return self.ingresos_mes_contable() - self.contable_gastos_mes()

    def contable_pagos_registrados(self, id_contable):
        """Devuelve el número de pagos registrados por un contable concreto."""
        datos = self.consultar(self.SQL_PAGOS_REGISTRADOS_CONTABLE, (id_contable,))
        return datos[0][0] if datos else 0

    def contable_pendientes_revisados(self):
        """Devuelve el número de clientes con pago pendiente
        (métrica del perfil del contable)."""
        datos = self.consultar(self.SQL_PENDIENTES_REVISADOS)
        return datos[0][0] if datos else 0

    def contable_importe_gestionado(self, id_contable):
        """Devuelve el importe total de pagos gestionados por un contable concreto."""
        datos = self.consultar(self.SQL_IMPORTE_GESTIONADO, (id_contable,))
        return datos[0][0] if datos else 0