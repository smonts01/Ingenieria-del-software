class UsuarioVO:
    def __init__(self, id_usuario, dni, nombre, telefono, email,
                 username, password_hash, id_rol, direccion,
                 fecha_registro, fecha_nacimiento):
        self._id_usuario = id_usuario
        self._dni = dni
        self._nombre = nombre
        self._telefono = telefono
        self._email = email
        self._username = username
        self._password_hash = password_hash
        self._id_rol = id_rol
        self._direccion = direccion
        self._fecha_registro = fecha_registro
        self._fecha_nacimiento = fecha_nacimiento
        

    @property
    def id_usuario(self): 
        return self._id_usuario
    
    @property
    def dni(self): 
        return self._dni
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def telefono(self):
        return self._telefono
    
    @property
    def email(self):
        return self._email
    
    @property
    def username(self):
        return self._username
    
    @property
    def password_hash(self):
        return self._password_hash
    
    @property
    def id_rol(self):
        return self._id_rol
    
    @property
    def direccion(self):
        return self._direccion
    
    @property
    def fecha_registro(self):
        return self._fecha_registro
    
    @property
    def fecha_nacimiento(self):
        return self._fecha_nacimiento