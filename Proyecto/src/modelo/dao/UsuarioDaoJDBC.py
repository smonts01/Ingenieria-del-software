from src.modelo.conexion.Conexion import Conexion
from src.modelo.VO.UsuarioVO import UsuarioVO
from src.modelo.dao.UsuarioDao import UsuarioDao

class UsuarioDaoJDBC(UsuarioDao, Conexion):
    SQL_SELECT             = "SELECT id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_registro, fecha_nacimiento FROM usuarios"
    SQL_SELECT_BY_ID       = "SELECT id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_registro, fecha_nacimiento FROM usuarios WHERE id_usuario = ?"
    SQL_SELECT_BY_USERNAME = "SELECT id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_registro, fecha_nacimiento FROM usuarios WHERE username = ?"
    SQL_INSERT             = "INSERT INTO usuarios (dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_nacimiento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    SQL_UPDATE             = "UPDATE usuarios SET dni=?, nombre=?, telefono=?, email=?, username=?, password_hash=?, id_rol=?, direccion=?, fecha_nacimiento=? WHERE id_usuario=?"
    SQL_DELETE             = "DELETE FROM usuarios WHERE id_usuario = ?"

    def select(self) -> list[UsuarioVO]:
        cursor = self.getCursor()
        usuarios = []
        try:
            cursor.execute(self.SQL_SELECT)
            rows = cursor.fetchall()
            for row in rows:
                id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_registro, fecha_nacimiento = row
                usuarios.append(UsuarioVO(id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_registro, fecha_nacimiento))
        except Exception as e:
            print("Error al seleccionar usuarios:", e)
        finally:
            if cursor: cursor.close()
            self.closeConnection()
        return usuarios

    def selectById(self, id_usuario: int) -> UsuarioVO:
        cursor = self.getCursor()
        usuario = None
        try:
            cursor.execute(self.SQL_SELECT_BY_ID, (id_usuario,))
            row = cursor.fetchone()
            if row:
                usuario = UsuarioVO(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        except Exception as e:
            print("Error al seleccionar usuario por ID:", e)
        finally:
            if cursor: cursor.close()
            self.closeConnection()
        return usuario

    def selectByUsername(self, username: str) -> UsuarioVO:
        cursor = self.getCursor()
        usuario = None
        try:
            cursor.execute(self.SQL_SELECT_BY_USERNAME, (username,))
            row = cursor.fetchone()
            if row:
                usuario = UsuarioVO(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        except Exception as e:
            print("Error al seleccionar usuario por username:", e)
        finally:
            if cursor: cursor.close()
            self.closeConnection()
        return usuario

    def insert(self, usuario: UsuarioVO) -> int:
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_INSERT, (
                usuario._dni, usuario._nombre, usuario._telefono,
                usuario._email, usuario._username, usuario._password_hash,
                usuario._id_rol, usuario._direccion, usuario._fecha_nacimiento
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al insertar usuario:", e)
        finally:
            if cursor: cursor.close()
            self.closeConnection()
        return rows

    def update(self, usuario: UsuarioVO) -> int:
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_UPDATE, (
                usuario._dni, usuario._nombre, usuario._telefono,
                usuario._email, usuario._username, usuario._password_hash,
                usuario._id_rol, usuario._direccion, usuario._fecha_nacimiento,
                usuario._id_usuario
            ))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al actualizar usuario:", e)
        finally:
            if cursor: cursor.close()
            self.closeConnection()
        return rows

    def delete(self, id_usuario: int) -> int:
        cursor = self.getCursor()
        rows = 0
        try:
            cursor.execute(self.SQL_DELETE, (id_usuario,))
            rows = cursor.rowcount
        except Exception as e:
            print("Error al eliminar usuario:", e)
        finally:
            if cursor: cursor.close()
            self.closeConnection()
        return rows