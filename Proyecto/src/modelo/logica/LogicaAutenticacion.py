import hashlib

from src.modelo.dao.UsuarioDaoJDBC import UsuarioDaoJDBC
from src.modelo.dao.RolesDaoJDBC import RolesDaoJDBC


class LogicaAutenticacion:

    def __init__(self):
        self._usuario_dao = UsuarioDaoJDBC()
        self._roles_dao = RolesDaoJDBC()

    def _cifrar(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def iniciar_sesion(self, username: str, password: str):
        if not username or not password:
            return None

        username = username.strip()
        password = password.strip()

        usuario_vo = self._usuario_dao.selectByUsername(username)

        if usuario_vo is None:
            return None

        password_cifrada = self._cifrar(password)

        if usuario_vo.password_hash != password and usuario_vo.password_hash != password_cifrada:
            return None

        rol = self._roles_dao.nombre_rol_por_id(usuario_vo.id_rol) or "cliente"

        return {
            "id_usuario": usuario_vo.id_usuario,
            "nombre": usuario_vo.nombre,
            "username": usuario_vo.username,
            "rol": rol,
        }