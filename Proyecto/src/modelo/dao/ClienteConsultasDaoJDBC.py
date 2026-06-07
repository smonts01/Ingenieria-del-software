# Importamos la clase base DaoJDBCBase.
# Esta clase ya tiene métodos comunes como consultar() y ejecutar()
from src.modelo.dao.DaoJDBCBase import DaoJDBCBase

# Importamos el VO que representa un resumen de cliente.
from src.modelo.VO.ClienteResumenVO import ClienteResumenVO


class ClienteConsultasDaoJDBC(DaoJDBCBase):
    """
    DAO de consultas específicas de clientes.
    Responsabilidad:
    - Consultar información de clientes.
    - Buscar clientes por nombre, usuario, DNI o estado de pago.
    - Obtener datos para la pantalla de recepción.
    - Actualizar datos básicos del cliente y su estado de pago.
    """

    # Consultas SQL al inicio 

    # Lista todos los clientes con sus datos principales.
    SQL_LISTAR_CLIENTES_COMPLETO = (
        "SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email, "
        "u.username, c.estado_pagado, u.direccion, u.fecha_nacimiento "
        "FROM usuarios u JOIN clientes c ON u.id_usuario = c.id_cliente "
        "ORDER BY u.nombre"
    )

    # Busca clientes por nombre, username o DNI.
    SQL_BUSCAR_CLIENTES = (
        "SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email, "
        "u.username, c.estado_pagado, u.direccion, u.fecha_nacimiento "
        "FROM usuarios u JOIN clientes c ON u.id_usuario = c.id_cliente "
        "WHERE LOWER(u.nombre) LIKE ? OR LOWER(u.username) LIKE ? "
        "OR LOWER(u.dni) LIKE ? "
        "ORDER BY u.nombre"
    )

    # Busca clientes según su estado de pago.
    SQL_BUSCAR_CLIENTES_ESTADO = (
        "SELECT u.id_usuario, u.dni, u.nombre, u.telefono, u.email, "
        "u.username, c.estado_pagado, u.direccion, u.fecha_nacimiento "
        "FROM usuarios u JOIN clientes c ON u.id_usuario = c.id_cliente "
        "WHERE LOWER(c.estado_pagado) = ? "
        "ORDER BY u.nombre"
    )

    # Cuenta el número total de clientes.
    SQL_TOTAL_CLIENTES = (
        "SELECT COUNT(*) FROM clientes"
    )

    # Lista los últimos clientes registrados.
    # Se usa en el panel de inicio de recepción.
    SQL_CLIENTES_RECIENTES = (
        "SELECT u.nombre, u.dni, u.telefono, u.fecha_registro "
        "FROM usuarios u "
        "JOIN clientes c ON u.id_usuario = c.id_cliente "
        "ORDER BY u.fecha_registro DESC "
        "LIMIT 8"
    )

    # Cuenta los clientes nuevos registrados durante el mes actual.
    SQL_NUEVOS_CLIENTES_MES = (
        "SELECT COUNT(*) "
        "FROM usuarios u "
        "INNER JOIN clientes c ON u.id_usuario = c.id_cliente "
        "WHERE YEAR(u.fecha_registro) = YEAR(CURRENT_DATE) "
        "AND MONTH(u.fecha_registro) = MONTH(CURRENT_DATE)"
    )

    # Actualiza los datos personales del usuario asociado al cliente.
    SQL_UPDATE_USUARIO = (
        "UPDATE usuarios "
        "SET dni = ?, nombre = ?, telefono = ?, email = ?, "
        "direccion = ?, fecha_nacimiento = ? "
        "WHERE id_usuario = ?"
    )

    # Actualiza el estado de pago del cliente.
    SQL_UPDATE_ESTADO_PAGADO = (
        "UPDATE clientes SET estado_pagado = ? WHERE id_cliente = ?"
    )

    # Busca un cliente por ID para la pantalla de control de acceso.
    SQL_BUSCAR_ACCESO_POR_ID = (
        "SELECT u.id_usuario, u.dni, u.nombre, c.estado_pagado "
        "FROM usuarios u "
        "INNER JOIN clientes c ON u.id_usuario = c.id_cliente "
        "WHERE u.id_usuario = ? "
        "LIMIT 1"
    )

    # Busca un cliente por DNI para la pantalla de control de acceso.
    SQL_BUSCAR_ACCESO_POR_DNI = (
        "SELECT u.id_usuario, u.dni, u.nombre, c.estado_pagado "
        "FROM usuarios u "
        "INNER JOIN clientes c ON u.id_usuario = c.id_cliente "
        "WHERE LOWER(u.dni) = LOWER(?) "
        "LIMIT 1"
    )

    # Consulta base para listar clientes filtrados desde recepción.
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
        """
        Convierte una fila de la base de datos en un ClienteResumenVO
        """
        return ClienteResumenVO(
            row[0],  # id_usuario
            row[1],  # dni
            row[2],  # nombre
            row[3],  # telefono
            row[4],  # email
            row[5],  # username
            row[6],  # estado_pagado
            row[7],  # direccion
            row[8],  # fecha_nacimiento
        )

    def listar_clientes_completo(self):
        """
        Devuelve todos los clientes con sus datos principales.
        """
        filas = self.consultar(self.SQL_LISTAR_CLIENTES_COMPLETO)
        return [self._rowToVO(f) for f in filas]

    def buscar_clientes(self, texto: str):
        """
        Busca clientes por nombre, usuario o DNI.
        """
        t = f"%{texto.lower().strip()}%"
        filas = self.consultar(self.SQL_BUSCAR_CLIENTES, (t, t, t))
        return [self._rowToVO(f) for f in filas]

    def buscar_clientes_estado(self, estado: str):
        """
        Busca clientes por estado de pago
        """
        filas = self.consultar(self.SQL_BUSCAR_CLIENTES_ESTADO, (estado.lower(),))
        return [self._rowToVO(f) for f in filas]

    def recepcion_total_clientes(self):
        """
        Devuelve el número total de clientes.
        """
        datos = self.consultar(self.SQL_TOTAL_CLIENTES)
        return datos[0][0] if datos else 0

    def recepcion_total_clientes_lista(self):
        """
        Devuelve el total de clientes para la pantalla de listado.
        """
        return self.recepcion_total_clientes()

    def recepcion_clientes_recientes(self):
        """
        Devuelve los últimos clientes registrados.

        Aquí se devuelven tuplas porque la vista las usa directamente
        para rellenar una tabla sencilla.
        """
        filas = self.consultar(self.SQL_CLIENTES_RECIENTES)
        return filas

    def recepcion_nuevos_clientes_mes(self):
        """
        Devuelve cuántos clientes se han registrado en el mes actual.
        """
        datos = self.consultar(self.SQL_NUEVOS_CLIENTES_MES)
        return datos[0][0] if datos else 0

    def recepcion_listar_clientes_filtrados(self, dni="", tipo="Todos", plan="Todos"):
        """
        Lista clientes aplicando filtros .
        """
        condiciones = []
        parametros = []

        # Filtro por DNI.
        if dni:
            condiciones.append("LOWER(u.dni) LIKE LOWER(?)")
            parametros.append(f"%{dni}%")

        # Filtro por tipo de cliente.
        if tipo and tipo.lower() != "todos":
            if tipo.lower() == "menor":
                condiciones.append("m.id_cliente IS NOT NULL")
            elif tipo.lower() == "adulto":
                condiciones.append("m.id_cliente IS NULL")

        # Filtro por plan/tarifa.
        if plan and plan.lower() != "todos":
            condiciones.append("LOWER(t.nombre) LIKE LOWER(?)")
            parametros.append(f"%{plan}%")


        sql = self.SQL_LISTAR_CLIENTES_FILTRADOS

        # Si hay filtros, añadimos WHERE con las condiciones.
        if condiciones:
            sql += "WHERE " + " AND ".join(condiciones) + " "

        # Ordenamos el resultado por nombre.
        sql += "ORDER BY u.nombre"

        # Ejecutamos la consulta con parámetros.
        filas = self.consultar(sql, tuple(parametros))

        # Devolvemos solo las columnas que la vista necesita mostrar.
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

    def recepcion_guardar_cambios_cliente(
        self,
        id_cliente,
        dni,
        nombre,
        telefono,
        email,
        direccion,
        fecha_nacimiento,
        estado_pagado
    ):
        """
        Guarda los cambios realizados sobre un cliente desde recepción.
        """
        self.ejecutar(
            self.SQL_UPDATE_USUARIO,
            (dni, nombre, telefono, email, direccion, fecha_nacimiento, id_cliente)
        )

        self.ejecutar(
            self.SQL_UPDATE_ESTADO_PAGADO,
            (estado_pagado, id_cliente)
        )

        return True

    def buscar_cliente_acceso_por_dni_o_id(self, texto):
        """
        Busca un cliente para el control de acceso.
        """
        texto = str(texto).strip()

        if texto.isdigit():
            return self._buscar_cliente_acceso_por_id(int(texto))

        return self._buscar_cliente_acceso_por_dni(texto)

    def _buscar_cliente_acceso_por_id(self, id_usuario):
        """
        Busca un cliente por ID para registrar entrada o salida.
        """
        datos = self.consultar(self.SQL_BUSCAR_ACCESO_POR_ID, (id_usuario,))
        return datos[0] if datos else None

    def _buscar_cliente_acceso_por_dni(self, dni):
        """
        Busca un cliente por DNI para registrar entrada o salida.
        """
        datos = self.consultar(self.SQL_BUSCAR_ACCESO_POR_DNI, (dni,))
        return datos[0] if datos else None