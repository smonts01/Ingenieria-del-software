import hashlib
from datetime import datetime

from src.modelo.dao.UsuarioDaoJDBC import UsuarioDaoJDBC
from src.modelo.dao.UsuarioConsultasDaoJDBC import UsuarioConsultasDaoJDBC
from src.modelo.dao.ClienteDaoJDBC import ClienteDaoJDBC
from src.modelo.dao.EmpleadoDaoJDBC import EmpleadoDaoJDBC
from src.modelo.dao.EmpleadoConsultasDaoJDBC import EmpleadoConsultasDaoJDBC
from src.modelo.dao.AdministradorDaoJDBC import AdministradorDaoJDBC
from src.modelo.dao.EntrenadorDaoJDBC import EntrenadorDaoJDBC
from src.modelo.dao.RecepcionistaDaoJDBC import RecepcionistaDaoJDBC
from src.modelo.dao.ContableDaoJDBC import ContableDaoJDBC

from src.modelo.VO.UsuarioVO import UsuarioVO
from src.modelo.VO.ClientesVO import ClientesVO
from src.modelo.VO.EmpleadosVO import EmpleadoVO
from src.modelo.VO.AdminitradorVO import AdminitradorVO
from src.modelo.VO.EntrenadorVO import EntrenadorVO
from src.modelo.VO.RecepcionistaVO import RecepcionistaVO
from src.modelo.VO.ContableVO import ContableVO


class LogicaUsuarios:
    """
    Lógica de negocio para la gestión de usuarios y sus roles.
    Al crear un usuario también registra su fila en la tabla específica
    de su rol (clientes, empleados, entrenadores, etc.).
    Las contraseñas se cifran con SHA-256 antes de almacenarse.
    """

    def __init__(self):
        # DAOs de usuario
        self._usuario_dao = UsuarioDaoJDBC()
        self._usuario_consultas_dao = UsuarioConsultasDaoJDBC()
        # DAO de cliente
        self._cliente_dao  = ClienteDaoJDBC()
        # DAOs de empleado
        self._empleado_dao  = EmpleadoDaoJDBC()
        self._empleado_consultas_dao = EmpleadoConsultasDaoJDBC()
        # DAOs de roles específicos
        self._administrador_dao = AdministradorDaoJDBC()
        self._entrenador_dao  = EntrenadorDaoJDBC()
        self._recepcionista_dao = RecepcionistaDaoJDBC()
        self._contable_dao = ContableDaoJDBC()

    # Cifrar contraseña

    def _cifrar(self, password: str) -> str:
        """Devuelve el hash SHA-256 de la contraseña en hexadecimal."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    # Usuarios

    def registrar_usuario(self, dni, nombre, telefono, email, username,
                          password, id_rol, direccion, fecha_nacimiento):
        """Inserta un nuevo usuario en la tabla usuarios con la contraseña cifrada.
        Lanza ValueError si faltan campos obligatorios.
        Devuelve el número de filas afectadas."""
        if not dni or not nombre or not username or not password:
            raise ValueError("DNI, nombre, usuario y contraseña son obligatorios")

        usuario_vo = UsuarioVO(
            None, dni, nombre, telefono, email,
            username, self._cifrar(password),
            id_rol, direccion, None, fecha_nacimiento
        )
        return self._usuario_dao.insert(usuario_vo)

    def crear_usuario_completo(self, dni, nombre, telefono, email, username,
                               password, id_rol, direccion, fecha_nacimiento,
                               id_admin_registra=None):
        """
        Crea un usuario completo: inserta en usuarios y en la tabla de su rol.

        Pasos:
        1. Valida que el username no esté ya en uso.
        2. Inserta el usuario en la tabla usuarios.
        3. Crea la fila correspondiente en la tabla del rol (cliente, empleado, etc.).

        Devuelve el id del usuario creado.
        Lanza ValueError si el username ya existe o si el usuario no se pudo crear.
        """
        if not username:
            raise ValueError("El nombre de usuario es obligatorio")

        # Comprobar que el username no esté ya en uso
        if self._usuario_dao.selectByUsername(username) is not None:
            raise ValueError("Ya existe un usuario con ese nombre de usuario")

        # Insertar en la tabla usuarios
        self.registrar_usuario(
            dni, nombre, telefono, email, username,
            password, id_rol, direccion, fecha_nacimiento
        )

        # Recuperar el usuario recién creado para obtener su id
        usuario_vo = self._usuario_dao.selectByUsername(username)
        if usuario_vo is None:
            raise ValueError("No se pudo obtener el usuario recién creado")

        id_admin = id_admin_registra if id_admin_registra is not None else usuario_vo.id_usuario

        # Crear la fila correspondiente según el rol
        self.crear_relacion_usuario_por_rol(usuario_vo.id_usuario, id_rol, id_admin)

        return usuario_vo.id_usuario

    def modificar_usuario(self, id_usuario, telefono, email, direccion):
        """Actualiza el teléfono, email y dirección de un usuario.
        Mantiene el resto de campos sin cambios.
        Lanza ValueError si el usuario no existe."""
        usuario_vo = self._usuario_dao.selectById(id_usuario)
        if usuario_vo is None:
            raise ValueError(f"Usuario {id_usuario} no encontrado")

        usuario_actualizado = UsuarioVO(
            usuario_vo.id_usuario, usuario_vo.dni, usuario_vo.nombre,
            telefono, email, usuario_vo.username, usuario_vo.password_hash,
            usuario_vo.id_rol, direccion,
            usuario_vo.fecha_registro, usuario_vo.fecha_nacimiento
        )
        return self._usuario_dao.update(usuario_actualizado)

    def perfil_usuario(self, id_usuario):
        """Devuelve los datos de perfil de un usuario .
        Lanza ValueError si no se indica el id."""
        if not id_usuario:
            raise ValueError("Debe indicarse el usuario")
        return self._usuario_consultas_dao.perfil_usuario(id_usuario)

    def eliminar_usuario(self, id_usuario):
        """Elimina un usuario por su ID.
        Lanza ValueError si no se indica el id."""
        if not id_usuario:
            raise ValueError("Debe indicarse el usuario")
        return self._usuario_dao.delete(id_usuario)

    def buscar_usuario(self, id_usuario):
        """Devuelve el UsuarioVO del usuario con el ID indicado, o None si no existe.
        Lanza ValueError si no se indica el id."""
        if not id_usuario:
            raise ValueError("Debe indicarse el usuario")
        return self._usuario_dao.selectById(id_usuario)

    def listar_usuarios(self):
        """Devuelve todos los usuarios como lista de UsuarioVO."""
        return self._usuario_dao.select()

    def cambiar_password(self, id_usuario, nueva_password):
        """Cambia la contraseña de un usuario cifrándola con SHA-256.
        Lanza ValueError si la contraseña está vacía o el usuario no existe."""
        if not nueva_password:
            raise ValueError("La nueva contraseña no puede estar vacía")

        usuario_vo = self._usuario_dao.selectById(id_usuario)
        if usuario_vo is None:
            raise ValueError("Usuario no encontrado")

        usuario_actualizado = UsuarioVO(
            usuario_vo.id_usuario, usuario_vo.dni, usuario_vo.nombre,
            usuario_vo.telefono, usuario_vo.email, usuario_vo.username,
            self._cifrar(nueva_password), usuario_vo.id_rol,
            usuario_vo.direccion, usuario_vo.fecha_registro,
            usuario_vo.fecha_nacimiento
        )
        return self._usuario_dao.update(usuario_actualizado)

    # Reigistra teniendo en cuenta el rol

    def registrar_cliente(self, id_cliente):
        """Inserta la fila de cliente con estado de pago pendiente y calorías a 0."""
        cliente_vo = ClientesVO(
            id_cliente=id_cliente,
            estado_pagado="pendiente",
            calorias_acumuladas=0
        )
        return self._cliente_dao.insert(cliente_vo)

    def registrar_empleado(self, id_empleado, salario=0.0):
        """Inserta la fila de empleado con el salario indicado."""
        empleado_vo = EmpleadoVO(id_empleado=id_empleado, salario=salario)
        return self._empleado_dao.insert(empleado_vo)

    def registrar_entrenador(self, id_entrenador, id_admin=1):
        """Inserta la fila de entrenador indicando el administrador que lo registró."""
        entrenador_vo = EntrenadorVO(
            id_entrenador=id_entrenador,
            id_administrador_registra=id_admin
        )
        return self._entrenador_dao.insert(entrenador_vo)

    def registrar_recepcionista(self, id_recepcionista, id_admin=1):
        """Inserta la fila de recepcionista indicando el administrador que lo registró."""
        recepcionista_vo = RecepcionistaVO(
            id_recepcionista=id_recepcionista,
            id_administrador_registra=id_admin
        )
        return self._recepcionista_dao.insert(recepcionista_vo)

    def registrar_contable(self, id_contable, id_admin=1):
        """Inserta la fila de contable indicando el administrador que lo registró."""
        contable_vo = ContableVO(
            id_contable=id_contable,
            id_administrador_registra=id_admin
        )
        return self._contable_dao.insert(contable_vo)

    def registrar_administrador(self, id_administrador):
        """Inserta la fila de administrador."""
        administrador_vo = AdminitradorVO(id_administrador=id_administrador)
        return self._administrador_dao.insert(administrador_vo)

    def crear_relacion_usuario_por_rol(self, id_usuario, id_rol, id_admin):
        """Crea la fila específica del rol del usuario recién creado.

        Para clientes solo inserta en la tabla clientes.
        Para empleados inserta primero en empleados (con salario base)
        y luego en la tabla específica del rol (entrenador, recepcionista, etc.).
        Lanza ValueError si el id_rol no es reconocido.
        """
        # Rol 1 → cliente
        if id_rol == 1:
            return self.registrar_cliente(id_usuario)

        # Roles 2-5 → empleado (con salario base según rol)
        salario = self._salario_base_por_rol(id_rol)
        self.registrar_empleado(id_usuario, salario)

        if id_rol == 2: return self.registrar_entrenador(id_usuario, id_admin)
        if id_rol == 3: return self.registrar_recepcionista(id_usuario, id_admin)
        if id_rol == 4: return self.registrar_administrador(id_usuario)
        if id_rol == 5: return self.registrar_contable(id_usuario, id_admin)

        raise ValueError("Rol no reconocido")

    # Empleados

    def contar_trabajadores(self):
        """Devuelve el número total de empleados registrados."""
        return len(self._empleado_dao.select())

    def contar_por_rol(self, rol):
        """Devuelve el número de empleados con el rol indicado."""
        return self._empleado_consultas_dao.contar_por_rol(rol)

    def listar_trabajadores_completo(self):
        """Devuelve todos los trabajadores con sus datos completos como lista de VOs."""
        return self._empleado_consultas_dao.listar_trabajadores_completo()

    def buscar_trabajadores(self, texto):
        """Busca trabajadores cuyo nombre contenga el texto indicado."""
        return self._empleado_consultas_dao.buscar_trabajadores(texto)

    def buscar_trabajadores_rol(self, rol):
        """Devuelve los trabajadores que tienen el rol indicado."""
        return self._empleado_consultas_dao.buscar_trabajadores_rol(rol)

    def listar_empleados(self):
        """Devuelve todos los empleados como lista de EmpleadoVO."""
        return self._empleado_dao.select()

    def guardar_cambios_trabajador(self, id_usuario, nombre, telefono, email, direccion):
        """Actualiza nombre, teléfono, email y dirección de un trabajador.
        Lanza ValueError si el trabajador no existe."""
        usuario_vo = self._usuario_dao.selectById(id_usuario)
        if usuario_vo is None:
            raise ValueError("Trabajador no encontrado")

        usuario_actualizado = UsuarioVO(
            usuario_vo.id_usuario, usuario_vo.dni, nombre,
            telefono, email, usuario_vo.username, usuario_vo.password_hash,
            usuario_vo.id_rol, direccion,
            usuario_vo.fecha_registro, usuario_vo.fecha_nacimiento
        )
        return self._usuario_dao.update(usuario_actualizado)

    def resumen_trabajadores_por_rol(self, trabajadores):
        """Devuelve un diccionario con el total de trabajadores desglosado por rol.
        """
        resumen = {
            "total": len(trabajadores),
            "entrenadores": 0,
            "recepcionistas": 0,
            "contables": 0,
            "administradores": 0
        }
        for trabajador in trabajadores:
            # Obtener el nombre del rol del VO 
            if hasattr(trabajador, "nombre_rol"):
                rol = str(trabajador.nombre_rol).lower().strip()
            elif hasattr(trabajador, "rol"):
                rol = str(trabajador.rol).lower().strip()
            else:
                continue

            if "entrenador" in rol:
                resumen["entrenadores"] += 1
            elif "recepcionista" in rol or "recepción" in rol or "recepcion" in rol:
                resumen["recepcionistas"] += 1
            elif "contable" in rol:
                resumen["contables"] += 1
            elif "administrador" in rol or "admin" in rol:
                resumen["administradores"] += 1

        return resumen

    # Validar

    def validar_nuevo_usuario(self, dni, nombre, telefono, email,
                               username, password, confirmar, fecha_texto):
        """Valida los datos del formulario de registro de usuario.
        Comprueba que todos los campos estén rellenos, que las contraseñas
        coincidan, que tengan al menos 4 caracteres y que la fecha tenga
        el formato DD/MM/YYYY.
        Devuelve la fecha convertida a formato BD (YYYY-MM-DD).
        Lanza ValueError si alguna validación falla."""
        if not all([dni, nombre, telefono, email, username, password]):
            raise ValueError("Todos los campos son obligatorios")
        if password != confirmar:
            raise ValueError("Las contraseñas no coinciden")
        if len(password) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres")
        try:
            fecha_bd = datetime.strptime(fecha_texto, '%d/%m/%Y').strftime('%Y-%m-%d')
        except ValueError:
            raise ValueError("Formato de fecha incorrecto. Usa DD/MM/YYYY")
        return fecha_bd

    def rol_texto_a_id(self, rol_texto):
        """Convierte el nombre del rol tal como aparece en el combo de la vista
        al id_rol correspondiente de la base de datos.
        Devuelve 1 (Cliente) si el texto no coincide con ningún rol conocido."""
        roles_map = {
            'Cliente': 1, 'Entrenador': 2, 'Recepcionista': 3,
            'Administrador': 4, 'Contable': 5
        }
        return roles_map.get(rol_texto, 1)

    # Segun rol sueldo

    def _salario_base_por_rol(self, id_rol):
        """Devuelve el salario base para el rol indicado.
        Primero intenta obtenerlo de la BD; si no hay datos usa valores por defecto:
        entrenador 1600€, recepcionista 1200€, administrador 2000€, contable 1800€."""
        salarios_por_defecto = {
            2: 1600.00,   # entrenador
            3: 1200.00,   # recepcionista
            4: 2000.00,   # administrador
            5: 1800.00,   # contable
        }
        try:
            salario = self._empleado_consultas_dao.obtener_salario_base_por_rol(id_rol)
            if salario is not None:
                return float(salario)
            return salarios_por_defecto.get(id_rol, 0.0)
        except Exception as e:
            print("Error al obtener salario base:", e)
            return salarios_por_defecto.get(id_rol, 0.0)