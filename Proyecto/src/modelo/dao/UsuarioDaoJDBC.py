from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuarioVO import UsuarioVO


class UsuarioDaoJDBC(Conexion):

    SQL_SELECT             = "SELECT id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_registro, fecha_nacimiento FROM usuarios"
    SQL_SELECT_BY_ID       = "SELECT id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_registro, fecha_nacimiento FROM usuarios WHERE id_usuario = ?"
    SQL_SELECT_BY_USERNAME = "SELECT id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_registro, fecha_nacimiento FROM usuarios WHERE username = ?"
    SQL_CHECK_LOGIN        = "SELECT id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_registro, fecha_nacimiento FROM usuarios WHERE username = ? AND password_hash = ?"
    SQL_INSERT             = "INSERT INTO usuarios (dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_nacimiento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    SQL_UPDATE             = "UPDATE usuarios SET dni=?, nombre=?, telefono=?, email=?, username=?, password_hash=?, id_rol=?, direccion=?, fecha_nacimiento=? WHERE id_usuario=?"
    SQL_DELETE             = "DELETE FROM usuarios WHERE id_usuario = ?"

    def _rowToVO(self, row) -> UsuarioVO:
        id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_registro, fecha_nacimiento = row
        return UsuarioVO(id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_registro, fecha_nacimiento)

    def select(self) -> list[UsuarioVO]:
        """Recupera todos los usuarios."""
        cursor = self.getCursor()
        usuarios = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                usuarios.append(self._rowToVO(row))
        except Exception as e:
            print("Error al seleccionar usuarios:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return usuarios

    def selectById(self, id_usuario: int) -> UsuarioVO:
        """Recupera un usuario por su ID."""
        cursor = self.getCursor()
        usuario = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_usuario,))
            row = cursor.fetchone()
            if row:
                usuario = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar usuario por ID:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return usuario

    def selectByUsername(self, username: str) -> UsuarioVO:
        """Recupera un usuario por su username."""
        cursor = self.getCursor()
        usuario = None
        try:
            cursor.execute(self.SQL_SELECT_BY_USERNAME, (username,))
            row = cursor.fetchone()
            if row:
                usuario = self._rowToVO(row)
        except Exception as e:
            print("Error al seleccionar usuario por username:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return usuario

    def checkLogin(self, username: str, password_hash: str) -> UsuarioVO:
        """Verifica credenciales. Retorna UsuarioVO si son correctas, None si no."""
        cursor = self.getCursor()
        usuario = None
        try:
            cursor.execute(self.SQL_CHECK_LOGIN, (username, password_hash))
            row = cursor.fetchone()
            if row:
                usuario = self._rowToVO(row)
        except Exception as e:
            print("Error al verificar login:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return usuario

    def insert(self, usuario: UsuarioVO) -> int:
        """Inserta un nuevo usuario. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (
                usuario.dni, usuario.nombre, usuario.telefono,
                usuario.email, usuario.username, usuario.password_hash,
                usuario.id_rol, usuario.direccion, usuario.fecha_nacimiento
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar usuario:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def update(self, usuario: UsuarioVO) -> int:
        """Actualiza un usuario existente. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (
                usuario.dni, usuario.nombre, usuario.telefono,
                usuario.email, usuario.username, usuario.password_hash,
                usuario.id_rol, usuario.direccion, usuario.fecha_nacimiento,
                usuario.id_usuario
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar usuario:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_usuario: int) -> int:
        """Elimina un usuario por su ID. Retorna filas afectadas."""
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_usuario,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar usuario:", e)
        finally:
            cursor.close()
            self.closeConnection()
        return rows
