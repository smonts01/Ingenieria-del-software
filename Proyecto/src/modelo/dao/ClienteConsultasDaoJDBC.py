from src.modelo.dao.DaoJDBCBase import DaoJDBCBase


class ClienteConsultasDaoJDBC(DaoJDBCBase):

    def listar_clientes_completo(self):
        return self.consultar("""
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, c.estado_pagado, u.direccion, u.fecha_nacimiento
            FROM usuarios u JOIN clientes c ON u.id_usuario = c.id_cliente
            ORDER BY u.nombre
        """)

    def buscar_clientes(self, texto: str):
        t = f"%{texto.lower().strip()}%"
        return self.consultar("""
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, c.estado_pagado, u.direccion, u.fecha_nacimiento
            FROM usuarios u JOIN clientes c ON u.id_usuario = c.id_cliente
            WHERE LOWER(u.nombre) LIKE ? OR LOWER(u.username) LIKE ?
               OR LOWER(u.dni) LIKE ?
            ORDER BY u.nombre
        """, (t, t, t))

    def buscar_clientes_estado(self, estado: str):
        return self.consultar("""
            SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email,
                   u.username, c.estado_pagado, u.direccion, u.fecha_nacimiento
            FROM usuarios u JOIN clientes c ON u.id_usuario = c.id_cliente
            WHERE LOWER(c.estado_pagado) = ?
            ORDER BY u.nombre
        """, (estado.lower(),))

    def recepcion_total_clientes(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM clientes
        """)
        return datos[0][0] if datos else 0

    def recepcion_total_clientes_lista(self):
        return self.recepcion_total_clientes()

    def recepcion_clientes_recientes(self):
        return self.consultar("""
            SELECT u.nombre,
                   u.dni,
                   u.telefono,
                   u.fecha_registro
            FROM usuarios u
            JOIN clientes c ON u.id_usuario = c.id_cliente
            ORDER BY u.fecha_registro DESC
            LIMIT 8
        """)

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
            SELECT u.id_usuario,
                   u.dni,
                   u.nombre,
                   u.telefono,
                   u.email,
                   u.direccion,
                   u.fecha_nacimiento,
                   c.estado_pagado,
                   CASE WHEN m.id_cliente IS NOT NULL THEN 'Menor'
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
        self.ejecutar("""
            UPDATE usuarios
            SET dni = ?,
                nombre = ?,
                telefono = ?,
                email = ?,
                direccion = ?,
                fecha_nacimiento = ?
            WHERE id_usuario = ?
        """, (dni, nombre, telefono, email, direccion, fecha_nacimiento, id_cliente))

        self.ejecutar("""
            UPDATE clientes
            SET estado_pagado = ?
            WHERE id_cliente = ?
        """, (estado_pagado, id_cliente))
        return True

    def buscar_cliente_acceso_por_dni_o_id(self, texto):
        texto = str(texto).strip()
        if texto.isdigit():
            return self._buscar_cliente_acceso_por_id(int(texto))
        return self._buscar_cliente_acceso_por_dni(texto)

    def _buscar_cliente_acceso_por_id(self, id_usuario):
        datos = self.consultar("""
            SELECT u.id_usuario,
                   u.dni,
                   u.nombre,
                   c.estado_pagado
            FROM usuarios u
            INNER JOIN clientes c ON u.id_usuario = c.id_cliente
            WHERE u.id_usuario = ?
            LIMIT 1
        """, (id_usuario,))
        return datos[0] if datos else None

    def _buscar_cliente_acceso_por_dni(self, dni):
        datos = self.consultar("""
            SELECT u.id_usuario,
                   u.dni,
                   u.nombre,
                   c.estado_pagado
            FROM usuarios u
            INNER JOIN clientes c ON u.id_usuario = c.id_cliente
            WHERE LOWER(u.dni) = LOWER(?)
            LIMIT 1
        """, (dni,))
        return datos[0] if datos else None
