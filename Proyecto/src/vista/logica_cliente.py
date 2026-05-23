"""
main_cliente.py
---------------
Ventana principal del cliente StayFit.
Carga la UI unificada (interfaz_cliente_unificada.ui) y conecta
los botones del menú lateral con el QStackedWidget central.

Estructura de páginas del stackedWidget:
  0 → Inicio
  1 → Clases
  2 → Estadísticas
  3 → Perfil
  4 → Información
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import uic


# Índice de cada página en el QStackedWidget
PAGE_INICIO       = 0
PAGE_CLASES       = 1
PAGE_ESTADISTICAS = 2
PAGE_PERFIL       = 3
PAGE_INFORMACION  = 4


class VentanaCliente(QMainWindow):

    def __init__(self):
        super().__init__()

        # ── Carga del .ui ───────────────────────────────────────────────
        uic.loadUi("interfaz_cliente_unificada.ui", self)

        # ── Lista de (botón, índice de página) para iterar ─────────────
        self._nav_buttons = [
            (self.btnInicio,       PAGE_INICIO),
            (self.btnClases,       PAGE_CLASES),
            (self.btnEstadisticas, PAGE_ESTADISTICAS),
            (self.btnPerfil,       PAGE_PERFIL),
            (self.btnInformacion,  PAGE_INFORMACION),
        ]

        # ── Conectar señales ────────────────────────────────────────────
        for btn, page_idx in self._nav_buttons:
            # Captura por valor con argumento predeterminado
            btn.clicked.connect(lambda checked, p=page_idx: self._cambiar_pagina(p))

        self.btnCerrarSesion.clicked.connect(self._cerrar_sesion)

        # ── Mostrar Inicio al arrancar ──────────────────────────────────
        self._cambiar_pagina(PAGE_INICIO)

    # ── Métodos privados ────────────────────────────────────────────────

    def _cambiar_pagina(self, indice: int):
        """Cambia la página visible y actualiza el estilo activo del menú."""
        self.stackedWidget.setCurrentIndex(indice)
        self._actualizar_estilo_menu(indice)

    def _actualizar_estilo_menu(self, indice_activo: int):
        """
        Aplica la propiedad CSS 'activo' al botón seleccionado y la
        elimina del resto, forzando el recalculo del estilo de Qt.
        """
        for btn, page_idx in self._nav_buttons:
            es_activo = (page_idx == indice_activo)
            btn.setProperty("activo", es_activo)
            # Forzar la actualización del stylesheet dinámico
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    def _cerrar_sesion(self):
        """Cierra la ventana (o navega a la pantalla de login)."""
        self.close()

    # ── API pública para rellenar datos del cliente ─────────────────────

    def set_datos_cliente(self, nombre: str, fecha_alta: str):
        """Actualiza nombre y fecha de alta en el header."""
        self.lblNombreCliente.setText(f"Hola, {nombre}")
        self.lblFechaAltaCliente.setText(fecha_alta)
        # También actualizar campos de perfil
        self.lblNombrePerfil.setText(nombre)
        self.lblBienvenida.setText(f"Bienvenida, {nombre}")

    def set_datos_perfil(self, nombre: str, email: str, telefono: str = "",
                         fecha_nac: str = "", genero: str = "",
                         direccion: str = "", peso: str = "", altura: str = ""):
        """Rellena los campos del formulario de perfil."""
        self.txtNombre.setText(nombre)
        self.txtEmail.setText(email)
        self.txtTelefono.setText(telefono)
        self.txtFecha.setText(fecha_nac)
        self.txtGenero.setText(genero)
        self.txtDireccion.setText(direccion)
        self.txtPeso.setText(peso)
        self.txtAltura.setText(altura)
        self.lblEmailPerfil.setText(email)


# ── Punto de entrada ────────────────────────────────────────────────────

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaCliente()

    # Ejemplo: cargar datos de un cliente
    ventana.set_datos_cliente("Ana García", "Cliente desde enero 2024")
    ventana.set_datos_perfil(
        nombre="Ana García",
        email="ana@email.com",
        telefono="611 222 333",
        fecha_nac="10/03/1992",
        genero="Femenino",
        direccion="Calle Mayor 45, Madrid",
        peso="65",
        altura="168",
    )

    ventana.show()
    sys.exit(app.exec_())