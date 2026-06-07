from src.modelo.dao.DaoJDBCBase import DaoJDBCBase
from src.modelo.VO.ClienteResumenVO import ClienteResumenVO


class ClienteConsultasDaoJDBC(DaoJDBCBase):

    SQL_LISTAR_CLIENTES_COMPLETO = (
        "SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email, "
        "u.username, c.estado_pagado, u.direccion, u.fecha_nacimiento "
        "FROM usuarios u JOIN clientes c ON u.id_usuario = c.id_cliente "
        "ORDER BY u.nombre"
    )

    SQL_BUSCAR_CLIENTES = (
        "SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email, "
        "u.username, c.estado_pagado, u.direccion, u.fecha_nacimiento "
        "FROM usuarios u JOIN clientes c ON u.id_usuario = c.id_cliente "
        "WHERE LOWER(u.nombre) LIKE ? OR LOWER(u.username) LIKE ? "
        "OR LOWER(u.dni) LIKE ? "
        "ORDER BY u.nombre"
    )

    SQL_BUSCAR_CLIENTES_ESTADO = (
        "SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email, "
        "u.username, c.estado_pagado, u.direccion, u.fecha_nacimiento "
        "FROM usuarios u JOIN clientes c ON u.id_usuario = c.id_cliente "
        "WHERE LOWER(c.estado_pagado) = ? "
        "ORDER BY u.nombre"
    )

    SQL_TOTAL_CLIENTES = (
        "SELECT COUNT(*) FROM clientes"
    )

    SQL_CLIENTES_RECIENTES = (
        "SELECT u.nombre, u.dni, u.telefono, u.fecha_registro "
        "FROM usuarios u "
        "JOIN clientes c ON u.id_usuario = c.id_cliente "
        "ORDER BY u.fecha_registro DESC "
        "LIMIT 8"
    )

    SQL_NUEVOS_CLIENTES_MES = (
        "SELECT COUNT(*) "
        "FROM usuarios u "
        "INNER JOIN clientes c ON u.id_usuario = c.id_cliente "
        "WHERE YEAR(u.fecha_registro) = YEAR(CURRENT_DATE) "
        "AND MONTH(u.fecha_registro) = MONTH(CURRENT_DATE)"
    )

    SQL_UPDATE_USUARIO = (
        "UPDATE usuarios "
        "SET dni = ?, nombre = ?, telefono = ?, email = ?, "
        "direccion = ?, fecha_nacimiento = ? "
        "WHERE id_usuario = ?"
    )

    SQL_UPDATE_ESTADO_PAGADO = (
        "UPDATE clientes SET estado_pagado = ? WHERE id_cliente = ?"
    )

    SQL_BUSCAR_ACCESO_POR_ID = (
        "SELECT u.id_usuario, u.dni, u.nombre, c.estado_pagado "
        "FROM usuarios u "
        "INNER JOIN clientes c ON u.id_usuario = c.id_cliente "
        "WHERE u.id_usuario = ? "
        "LIMIT 1"
    )

    SQL_BUSCAR_ACCESO_POR_DNI = (
        "SELECT u.id_usuario, u.dni, u.nombre, c.estado_pagado "
        "FROM usuarios u "
        "INNER JOIN clientes c ON u.id_usuario = c.id_cliente "
        "WHERE LOWER(u.dni) = LOWER(?) "
        "LIMIT 1"
    )

    SQL_LISTAR_CLIENTES_FILTRADOS = (
        "SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email, "
        "u.direccion, u.fecha_nacimiento, c.estado_pagado, "
        "CASE WHEN m.id_cliente IS NOT NULL THEN 'Menor' ELSE 'Adulto' END AS tipo_cliente, "
        "COALESCE(t.nombre, 'Sin plan') AS plan "
        "FROM usuarios u "
        "INNER JOIN clientes c ON u.id_usuario = c.id_cliente "
        "LEFT JOIN menor m ON c.id_cliente = m.id_cliente "
        "LEFT JOIN cliente_tarifa ct ON c.id_cliente = ct.id_cliente AND ct.estado = 'activa' "
        "LEFT JOIN tarifa t ON ct.id_tarifa = t.id_tarifa "
    )

    def _rowToVO(self, row) -> ClienteResumenVO:
        return ClienteResumenVO(row[0], row[1], row[2], row[3], row[4],
                                row[5], row[6], row[7], row[8])

    def listar_clientes_completo(self):
        filas = self.consultar(self.SQL_LISTAR_CLIENTES_COMPLETO)
        return [self._rowToVO(f) for f in filas]

    def buscar_clientes(self, texto: str):
        t = f"%{texto.lower().strip()}%"
        filas = self.consultar(self.SQL_BUSCAR_CLIENTES, (t, t, t))
        return [self._rowToVO(f) for f in filas]

    def buscar_clientes_estado(self, estado: str):
        filas = self.consultar(self.SQL_BUSCAR_CLIENTES_ESTADO, (estado.lower(),))
        return [self._rowToVO(f) for f in filas]

    def recepcion_total_clientes(self):
        datos = self.consultar(self.SQL_TOTAL_CLIENTES)
        return datos[0][0] if datos else 0

    def recepcion_total_clientes_lista(self):
        return self.recepcion_total_clientes()

    def recepcion_clientes_recientes(self):
        filas = self.consultar(self.SQL_CLIENTES_RECIENTES)
        # Devuelve tuplas (nombre, dni, telefono, fecha_registro) — usadas directamente en tabla
        return filas

    def recepcion_nuevos_clientes_mes(self):
        datos = self.consultar(self.SQL_NUEVOS_CLIENTES_MES)
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

        sql = self.SQL_LISTAR_CLIENTES_FILTRADOS
        if condiciones:
            sql += "WHERE " + " AND ".join(condiciones) + " "
        sql += "ORDER BY u.nombre"

        filas = self.consultar(sql, tuple(parametros))

        return [
            (
                f[0],  # ID
                f[1],  # DNI
                f[2],  # Nombre
                f[3],  # Teléfono
                f[4],  # Email
                f[5],  # Dirección
                f[6],  # Nacimiento
                f[7],  # Estado pago
            )
            for f in filas
        ]

    def recepcion_guardar_cambios_cliente(self, id_cliente, dni, nombre, telefono,
                                           email, direccion, fecha_nacimiento, estado_pagado):
        self.ejecutar(self.SQL_UPDATE_USUARIO,
                      (dni, nombre, telefono, email, direccion, fecha_nacimiento, id_cliente))
        self.ejecutar(self.SQL_UPDATE_ESTADO_PAGADO, (estado_pagado, id_cliente))
        return True

    def buscar_cliente_acceso_por_dni_o_id(self, texto):
        texto = str(texto).strip()
        if texto.isdigit():
            return self._buscar_cliente_acceso_por_id(int(texto))
        return self._buscar_cliente_acceso_por_dni(texto)

    def _buscar_cliente_acceso_por_id(self, id_usuario):
        datos = self.consultar(self.SQL_BUSCAR_ACCESO_POR_ID, (id_usuario,))
        return datos[0] if datos else None

    def _buscar_cliente_acceso_por_dni(self, dni):
        datos = self.consultar(self.SQL_BUSCAR_ACCESO_POR_DNI, (dni,))
        return datos[0] if datos else None