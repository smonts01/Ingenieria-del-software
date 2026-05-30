import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox


class VentanaCliente:

    def __init__(self, ruta_ui: str):
        self.ventana = uic.loadUi(os.path.join(ruta_ui, "interfaz_cliente_clases_reservas.ui"))

        self._pagina_actual = 0

    # ============================================================
    # CONEXIONES
    # ============================================================

    def conectar_navegacion(self, callback_pagina, callback_cerrar_sesion):
        v = self.ventana

        if hasattr(v, "btnInicio"):
            v.btnInicio.clicked.connect(lambda: callback_pagina(0))

        if hasattr(v, "btnClases"):
            v.btnClases.clicked.connect(lambda: callback_pagina(1))

        if hasattr(v, "btnEstadisticas"):
            v.btnEstadisticas.clicked.connect(lambda: callback_pagina(2))

        if hasattr(v, "btnPerfil"):
            v.btnPerfil.clicked.connect(lambda: callback_pagina(3))

        if hasattr(v, "btnInformacion"):
            v.btnInformacion.clicked.connect(lambda: callback_pagina(4))

        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(callback_cerrar_sesion)

    def conectar_reservar(self, callback):
        """
        Esta interfaz antigua no tiene botones btnReservar1, btnReservar2...
        Por eso lo dejamos preparado, pero sin romper el programa.
        """
        for i in range(1, 5):
            btn = getattr(self.ventana, f"btnReservar{i}", None)
            if btn:
                btn.clicked.connect(lambda checked, n=i: callback(n))

    def conectar_guardar_perfil(self, callback):
        """
        Esta pantalla antigua no tiene btnGuardarCambios.
        Lo comprobamos para que no dé error.
        """
        if hasattr(self.ventana, "btnGuardarCambios"):
            self.ventana.btnGuardarCambios.clicked.connect(callback)

    # ============================================================
    # NAVEGACIÓN
    # ============================================================

    def cambiar_pagina(self, indice: int):
        self._pagina_actual = indice

        # Esta UI antigua no tiene stackedWidget.
        # De momento solo dejamos que no se rompa.
        if indice != 1:
            QMessageBox.information(
                self.ventana,
                "Pantalla no disponible",
                "De momento solo está recuperada la pantalla de clases y reservas."
            )

    def pagina_actual(self) -> int:
        return self._pagina_actual

    # ============================================================
    # CARGAR DATOS DEL CLIENTE
    # ============================================================

    def inicializar(self, vo):
        v = self.ventana

        # Header
        if hasattr(v, "lblNombreCliente"):
            v.lblNombreCliente.setText(f"Hola, {vo.nombre}")

        if hasattr(v, "lblFechaAltaCliente"):
            v.lblFechaAltaCliente.setText(f"Cliente desde {vo.fecha_registro}")

        # Rellenar tarjetas de reservas/clases
        self._rellenar_reservas(vo)

    def _rellenar_reservas(self, vo):
        """
        Rellena las cards de clases usando los datos que llegan del VO.
        Si no llegan suficientes clases, deja textos por defecto.
        """

        clases = []

        if hasattr(vo, "proximas_clases") and vo.proximas_clases:
            clases = vo.proximas_clases

        for i in range(1, 5):
            lbl_nombre = getattr(self.ventana, f"lblReservaClase{i}", None)
            lbl_desc = getattr(self.ventana, f"lblReservaDesc{i}", None)
            lbl_fecha = getattr(self.ventana, f"lblReservaFecha{i}", None)
            lbl_plazas = getattr(self.ventana, f"lblPlazasReserva{i}", None)

            if i <= len(clases):
                clase = clases[i - 1]

                nombre = clase.get("nombre_actividad", "Clase")
                fecha = clase.get("fecha", "")
                hora = clase.get("hora_inicio", "")
                sala = clase.get("nombre_sala", "")

                if lbl_nombre:
                    lbl_nombre.setText(str(nombre))

                if lbl_desc:
                    lbl_desc.setText(str(sala))

                if lbl_fecha:
                    lbl_fecha.setText(f"{fecha} {hora}")

                if lbl_plazas:
                    lbl_plazas.setText("Reservada")

            else:
                if lbl_nombre:
                    lbl_nombre.setText("Clase disponible")

                if lbl_desc:
                    lbl_desc.setText("Consulta disponibilidad")

                if lbl_fecha:
                    lbl_fecha.setText("Sin fecha")

                if lbl_plazas:
                    lbl_plazas.setText("Disponible")

    # ============================================================
    # GETTERS
    # ============================================================

    def get_datos_perfil(self) -> dict:
        return {
            "telefono": "",
            "email": "",
            "direccion": "",
        }

    def get_nombre_clase_card(self, numero_card: int) -> str:
        lbl = getattr(self.ventana, f"lblReservaClase{numero_card}", None)
        return lbl.text() if lbl else "Clase"

    # ============================================================
    # MOSTRAR / CERRAR
    # ============================================================

    def show(self):
        self.ventana.show()

    def close(self):
        self.ventana.close()