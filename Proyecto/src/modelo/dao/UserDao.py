from src.modelo.vo.UsuarioVO import UsuarioVO

class UsuarioDao:
    def select(self) -> list[UsuarioVO]:
        """Recupera todos los usuarios de la base de datos."""
        raise NotImplementedError("Método select() no implementado")

    def selectById(self, id_usuario: int) -> UsuarioVO:
        """Recupera un usuario por su ID."""
        raise NotImplementedError("Método selectById() no implementado")

    def selectByUsername(self, username: str) -> UsuarioVO:
        """Recupera un usuario por su username."""
        raise NotImplementedError("Método selectByUsername() no implementado")

    def insert(self, usuario: UsuarioVO) -> int:
        """Inserta un nuevo usuario. Retorna filas afectadas."""
        raise NotImplementedError("Método insert() no implementado")

    def update(self, usuario: UsuarioVO) -> int:
        """Actualiza un usuario existente. Retorna filas afectadas."""
        raise NotImplementedError("Método update() no implementado")

    def delete(self, id_usuario: int) -> int:
        """Elimina un usuario por su ID. Retorna filas afectadas."""
        raise NotImplementedError("Método delete() no implementado")