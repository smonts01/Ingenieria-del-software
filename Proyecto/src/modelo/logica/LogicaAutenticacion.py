class LogicaAutenticacion:
    """Reglas de negocio relacionadas con el inicio de sesión."""

    def __init__(self, servicio):
        self.servicio = servicio

    def iniciar_sesion(self, username, password):
        if not username or not password:
            return None
        return self.servicio.iniciar_sesion(username.strip(), password.strip())
