"""
logica_cliente.py
-----------------
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
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
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

        # Carga del .ui 
        uic.loadUi("interfaz_cliente_unificada.ui", self)

        # ── Lista de (botón, índice de página) para iterar 
        self._nav_buttons = [
            (self.btnInicio,       PAGE_INICIO),
            (self.btnClases,       PAGE_CLASES),
            (self.btnEstadisticas, PAGE_ESTADISTICAS),
            (self.btnPerfil,       PAGE_PERFIL),
            (self.btnInformacion,  PAGE_INFORMACION),
        ]

        # Conectar señales 
        for btn, page_idx in self._nav_buttons:
            # Captura por valor con argumento predeterminado
            btn.clicked.connect(lambda checked, p=page_idx: self._cambiar_pagina(p))

        self.btnCerrarSesion.clicked.connect(self._cerrar_sesion)

        # Mostrar Inicio al arrancar 
        self._cambiar_pagina(PAGE_INICIO)

    # Métodos privados

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

    # API pública para rellenar datos del cliente

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

    def inicializar(self, vo) -> None:
        """Rellena todos los widgets de la interfaz con los datos del VO."""

        # Header
        self.lblNombreCliente.setText(f"Hola, {vo.nombre}")
        self.lblFechaAltaCliente.setText(f"Cliente desde {vo.fecha_registro}")
        self.lblBienvenida.setText(f"Bienvenida, {vo.nombre}")
        self.lblNombrePerfil.setText(vo.nombre)

        # Inicio — cards
        self.lblEstadoPago.setText(vo.estado_pagado.capitalize())
        self.lblCaloriasSemana.setText(f"{vo.calorias_semana:,} kcal".replace(",", "."))
        self.lblAsistencias.setText(vo.get_asistencias_str())

        # Inicio — cardPago
        self.lblCuota.setText(vo.nombre_tarifa)
        self.lblCantidadPago.setText(vo.get_precio_str())
        self.lblMesPago.setText(vo.ultimo_pago_fecha)
        self.lblPendientePago.setText(vo.ultimo_pago_estado.capitalize())

        # Inicio — tabla próximas clases
        self.tablaProximasClases.setRowCount(0)
        for fila in vo.proximas_clases:
            row = self.tablaProximasClases.rowCount()
            self.tablaProximasClases.insertRow(row)
            self.tablaProximasClases.setItem(row, 0, QTableWidgetItem(fila["nombre_actividad"]))
            self.tablaProximasClases.setItem(row, 1, QTableWidgetItem(fila["fecha"]))
            self.tablaProximasClases.setItem(row, 2, QTableWidgetItem(fila["hora_inicio"]))
            self.tablaProximasClases.setItem(row, 3, QTableWidgetItem(fila["nombre_sala"]))

        # Estadísticas
        self.lblNumEntrenos.setText(str(vo.entrenos_semana))
        self.lblSubEntrenos.setText(vo.get_delta_entrenos_str())
        self.lblNumTiempo.setText(vo.get_tiempo_semana_str())
        self.lblSubTiempo.setText(vo.get_delta_tiempo_str())
        self.lblNumRacha.setText(str(vo.racha_dias))
        self.lblTextoRacha.setText(f"Llevas {vo.racha_dias} días consecutivos entrenando.")

        # Perfil
        self.set_datos_perfil(
            nombre=vo.nombre,
            email=vo.email,
            telefono=vo.telefono,
            fecha_nac=vo.fecha_nacimiento,
            direccion=vo.direccion,
        )


# Punto de entrada

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