import hashlib
from src.modelo.dao.UsuarioDaoJDBC import UsuarioDaoJDBC
from src.modelo.dao.RolesDaoJDBC import RolesDaoJDBC


class LogicaAutenticacion:
    """
    Lógica de negocio para la autenticación de usuarios.
    Gestiona el inicio de sesión comprobando las credenciales
    contra la base de datos. Las contraseñas se almacenan cifradas
    con SHA-256, para mantener confidencialidad
    """

    def __init__(self):
        self._usuario_dao = UsuarioDaoJDBC()
        self._roles_dao   = RolesDaoJDBC()

    def _cifrar(self, password: str) -> str:
        """Devuelve el hash SHA-256 de la contraseña en hexadecimal."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def iniciar_sesion(self, username: str, password: str):
        """Valida las credenciales del usuario y devuelve sus datos si son correctas.

        Proceso:
        1. Comprueba que username y password no estén vacíos.
        2. Busca al usuario en la BD por su nombre de usuario.
        3. Compara la contraseña introducida con el hash almacenado,
           aceptando tanto texto  como SHA-256.
        4. Consulta el nombre del rol asociado al usuario.

        Devuelve un diccionario con id_usuario, nombre, username y rol
        si las credenciales son correctas, o None si no lo son.
        """
        # Validar que los campos no estén vacíos
        if not username or not password:
            return None

        username = username.strip()
        password = password.strip()

        # Buscar el usuario por nombre de usuario
        usuario_vo = self._usuario_dao.selectByUsername(username)
        if usuario_vo is None:
            return None

        # Verificar contraseña: se acepta texto y hash SHA-256
        password_cifrada = self._cifrar(password)
        if usuario_vo.password_hash != password and usuario_vo.password_hash != password_cifrada:
            return None

        # Obtener el nombre del rol (por defecto 'cliente' si no se encuentra)
        rol = self._roles_dao.nombre_rol_por_id(usuario_vo.id_rol) or "cliente"

        return {
            "id_usuario": usuario_vo.id_usuario,
            "nombre":     usuario_vo.nombre,
            "username":   usuario_vo.username,
            "rol":        rol,
        }