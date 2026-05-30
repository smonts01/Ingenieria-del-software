import os
from src.vista.componentes import MensajeView

from src.modelo.dao.ClienteDaoJDBC import ClienteDaoJDBC
from src.vista.logica_cliente import VentanaCliente


class ControladorCliente:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo      = modelo
        self.usuario     = usuario
        self.ruta_ui     = ruta_ui
        self.vista_login = vista_login
        self.vista       = None
        self._vo         = None


    def abrir(self):
        id_cliente = self.usuario["id_usuario"]

        dao = ClienteDaoJDBC()
        self._vo = dao.selectInicioCliente(id_cliente)

        if self._vo is None:
            MensajeView.critical(
                None, "Error",
                f"No se pudieron cargar los datos del cliente (id={id_cliente})."
            )
            self.vista_login.show()
            return

        self.vista = VentanaCliente(self.ruta_ui)
        self.vista.conectar_navegacion(self._cambiar_pagina, self._cerrar_sesion)
        self.vista.conectar_reservar(self._reservar_clase_card)
        self.vista.conectar_guardar_perfil(self._guardar_perfil)

        self.vista.inicializar(self._vo)
        self.vista.cambiar_pagina(1)
        self.vista.show()

    def _cambiar_pagina(self, indice: int):
        self.vista.cambiar_pagina(indice)


    def _reservar_clase_card(self, numero_card: int):
        nombre = self.vista.get_nombre_clase_card(numero_card)
        try:
            self.modelo.inscribirse_clase_por_nombre(
                self.usuario["id_usuario"], nombre
            )
            MensajeView.information(
                self.vista.ventana, "Reserva confirmada",
                f"Te has inscrito en {nombre}."
            )
            self._refrescar_datos()
        except Exception as e:
            MensajeView.warning(self.vista.ventana, "Error al reservar", str(e))


    def _guardar_perfil(self):
        datos = self.vista.get_datos_perfil()
        if not datos["email"]:
            MensajeView.warning(
                self.vista.ventana, "Error", "El email no puede estar vacío."
            )
            return
        try:
            self.modelo.modificar_usuario(
                self.usuario["id_usuario"],
                datos["telefono"],
                datos["email"],
                datos["direccion"],
            )
            MensajeView.information(
                self.vista.ventana, "Perfil actualizado",
                "Los cambios se han guardado correctamente."
            )
            self._refrescar_datos()
        except Exception as e:
            MensajeView.warning(self.vista.ventana, "Error al guardar", str(e))



    def _refrescar_datos(self):
        dao = ClienteDaoJDBC()
        vo_nuevo = dao.selectInicioCliente(self.usuario["id_usuario"])
        if vo_nuevo:
            self._vo = vo_nuevo
            pagina_actual = self.vista.pagina_actual()
            self.vista.inicializar(self._vo)
            self.vista.cambiar_pagina(pagina_actual)


    def _cerrar_sesion(self):
        self.vista.close()
        self.vista_login.show()