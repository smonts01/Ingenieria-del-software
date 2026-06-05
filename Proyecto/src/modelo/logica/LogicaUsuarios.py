import hashlib

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
    

    def __init__(self):
        self._usuario_dao = UsuarioDaoJDBC()
        self._usuario_consultas_dao = UsuarioConsultasDaoJDBC()

        self._cliente_dao = ClienteDaoJDBC()

        self._empleado_dao = EmpleadoDaoJDBC()
        self._empleado_consultas_dao = EmpleadoConsultasDaoJDBC()

        self._administrador_dao = AdministradorDaoJDBC()
        self._entrenador_dao = EntrenadorDaoJDBC()
        self._recepcionista_dao = RecepcionistaDaoJDBC()
        self._contable_dao = ContableDaoJDBC()

    def _cifrar(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    # ── USUARIOS ─────────────────────────────────────────────────────

    def registrar_usuario(self, dni, nombre, telefono, email, username,
                          password, id_rol, direccion, fecha_nacimiento):
        if not dni or not nombre or not username or not password:
            raise ValueError("DNI, nombre, usuario y contraseña son obligatorios")

        usuario_vo = UsuarioVO(
            None,
            dni,
            nombre,
            telefono,
            email,
            username,
            self._cifrar(password),
            id_rol,
            direccion,
            None,
            fecha_nacimiento
        )

        return self._usuario_dao.insert(usuario_vo)

    def crear_usuario_completo(self, dni, nombre, telefono, email, username,
                               password, id_rol, direccion, fecha_nacimiento,
                               id_admin_registra=None):
        if not username:
            raise ValueError("El nombre de usuario es obligatorio")

        usuario_existente = self._usuario_dao.selectByUsername(username)

        if usuario_existente is not None:
            raise ValueError("Ya existe un usuario con ese nombre de usuario")

        self.registrar_usuario(
            dni,
            nombre,
            telefono,
            email,
            username,
            password,
            id_rol,
            direccion,
            fecha_nacimiento
        )

        usuario_vo = self._usuario_dao.selectByUsername(username)

        if usuario_vo is None:
            raise ValueError("No se pudo obtener el usuario recién creado")

        id_admin = id_admin_registra if id_admin_registra is not None else usuario_vo.id_usuario

        self.crear_relacion_usuario_por_rol(
            usuario_vo.id_usuario,
            id_rol,
            id_admin
        )

        return usuario_vo.id_usuario

    def modificar_usuario(self, id_usuario, telefono, email, direccion):
        usuario_vo = self._usuario_dao.selectById(id_usuario)

        if usuario_vo is None:
            raise ValueError(f"Usuario {id_usuario} no encontrado")

        usuario_actualizado = UsuarioVO(
            usuario_vo.id_usuario,
            usuario_vo.dni,
            usuario_vo.nombre,
            telefono,
            email,
            usuario_vo.username,
            usuario_vo.password_hash,
            usuario_vo.id_rol,
            direccion,
            usuario_vo.fecha_registro,
            usuario_vo.fecha_nacimiento
        )

        return self._usuario_dao.update(usuario_actualizado)

    def perfil_usuario(self, id_usuario):
        if not id_usuario:
            raise ValueError("Debe indicarse el usuario")

        return self._usuario_consultas_dao.perfil_usuario(id_usuario)

    def eliminar_usuario(self, id_usuario):
        if not id_usuario:
            raise ValueError("Debe indicarse el usuario")

        return self._usuario_dao.delete(id_usuario)

    def buscar_usuario(self, id_usuario):
        if not id_usuario:
            raise ValueError("Debe indicarse el usuario")

        return self._usuario_dao.selectById(id_usuario)

    def listar_usuarios(self):
        usuarios = self._usuario_dao.select()

        return [
            (
                usuario.id_usuario,
                usuario.dni,
                usuario.nombre,
                usuario.telefono,
                usuario.email,
                usuario.username,
                usuario.id_rol,
                usuario.direccion,
                usuario.fecha_nacimiento
            )
            for usuario in usuarios
        ]

    def cambiar_password(self, id_usuario, nueva_password):
        if not nueva_password:
            raise ValueError("La nueva contraseña no puede estar vacía")

        usuario_vo = self._usuario_dao.selectById(id_usuario)

        if usuario_vo is None:
            raise ValueError("Usuario no encontrado")

        usuario_actualizado = UsuarioVO(
            usuario_vo.id_usuario,
            usuario_vo.dni,
            usuario_vo.nombre,
            usuario_vo.telefono,
            usuario_vo.email,
            usuario_vo.username,
            self._cifrar(nueva_password),
            usuario_vo.id_rol,
            usuario_vo.direccion,
            usuario_vo.fecha_registro,
            usuario_vo.fecha_nacimiento
        )

        return self._usuario_dao.update(usuario_actualizado)

    # ── TRABAJADORES ─────────────────────────────────────────────────

    def registrar_empleado(self, id_empleado, salario=0.0):
        empleado_vo = EmpleadoVO(
            id_empleado=id_empleado,
            salario=salario
        )

        return self._empleado_dao.insert(empleado_vo)

    def registrar_entrenador(self, id_entrenador, especialidad, id_admin):
        entrenador_vo = EntrenadorVO(
            id_entrenador=id_entrenador,
            especialidad=especialidad,
            id_administrador_registra=id_admin
        )

        return self._entrenador_dao.insert(entrenador_vo)

    def registrar_recepcionista(self, id_recepcionista, turno, id_admin):
        recepcionista_vo = RecepcionistaVO(
            id_recepcionista=id_recepcionista,
            turno=turno,
            id_administrador_registra=id_admin
        )

        return self._recepcionista_dao.insert(recepcionista_vo)

    def registrar_contable(self, id_contable, titulacion, id_admin):
        contable_vo = ContableVO(
            id_contable=id_contable,
            titulacion=titulacion,
            id_administrador_registra=id_admin
        )

        return self._contable_dao.insert(contable_vo)

    def registrar_administrador(self, id_administrador):
        administrador_vo = AdminitradorVO(
            id_administrador=id_administrador
        )

        return self._administrador_dao.insert(administrador_vo)

    def contar_trabajadores(self):
        return len(self._empleado_dao.select())

    def contar_por_rol(self, rol):
        return self._empleado_consultas_dao.contar_por_rol(rol)

    def listar_trabajadores_completo(self):
        return self._empleado_consultas_dao.listar_trabajadores_completo()

    def buscar_trabajadores(self, texto):
        return self._empleado_consultas_dao.buscar_trabajadores(texto)

    def buscar_trabajadores_rol(self, rol):
        return self._empleado_consultas_dao.buscar_trabajadores_rol(rol)

    def listar_empleados(self):
        empleados = self._empleado_dao.select()

        return [
            (
                empleado.id_empleado,
                empleado.salario
            )
            for empleado in empleados
        ]

    def guardar_cambios_trabajador(self, id_usuario, nombre, telefono, email, direccion):
        usuario_vo = self._usuario_dao.selectById(id_usuario)

        if usuario_vo is None:
            raise ValueError("Trabajador no encontrado")

        usuario_actualizado = UsuarioVO(
            usuario_vo.id_usuario,
            usuario_vo.dni,
            nombre,
            telefono,
            email,
            usuario_vo.username,
            usuario_vo.password_hash,
            usuario_vo.id_rol,
            direccion,
            usuario_vo.fecha_registro,
            usuario_vo.fecha_nacimiento
        )

        return self._usuario_dao.update(usuario_actualizado)

    # ── RELACIONES POR ROL ───────────────────────────────────────────

    def registrar_cliente(self, id_cliente):
        cliente_vo = ClientesVO(
            id_cliente=id_cliente,
            estado_pagado="pendiente",
            calorias_acumuladas=0
        )

        return self._cliente_dao.insert(cliente_vo)

    def crear_relacion_usuario_por_rol(self, id_usuario, id_rol, id_admin):
        if id_rol == 1:
            return self.registrar_cliente(id_usuario)

        self.registrar_empleado(id_usuario, 0.00)

        if id_rol == 2:
            return self.registrar_entrenador(id_usuario, "General", id_admin)

        if id_rol == 3:
            return self.registrar_recepcionista(id_usuario, "mañana", id_admin)

        if id_rol == 4:
            return self.registrar_administrador(id_usuario)

        if id_rol == 5:
            return self.registrar_contable(id_usuario, "ADE", id_admin)

        raise ValueError("Rol no reconocido")
    


    def resumen_trabajadores_por_rol(self, trabajadores):
        resumen = {
            "total": len(trabajadores),
            "entrenadores": 0,
            "recepcionistas": 0,
            "contables": 0,
            "administradores": 0
        }

        for trabajador in trabajadores:
            rol = str(trabajador[6]).lower().strip() if len(trabajador) > 6 else ""

            if "entrenador" in rol:
                resumen["entrenadores"] += 1
            elif "recepcionista" in rol or "recepción" in rol or "recepcion" in rol:
                resumen["recepcionistas"] += 1
            elif "contable" in rol:
                resumen["contables"] += 1
            elif "administrador" in rol or "admin" in rol:
                resumen["administradores"] += 1

        return resumen