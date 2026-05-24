"""
logica_cliente.py
-----------------
Vista de la interfaz unificada del cliente.
Gestiona todo lo visual: carga del .ui, navegación entre páginas,
relleno de widgets y estilos. No accede nunca a la base de datos.
"""

import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


# Índice de cada página en el QStackedWidget
PAGE_INICIO       = 0
PAGE_CLASES       = 1
PAGE_ESTADISTICAS = 2
PAGE_PERFIL       = 3
PAGE_INFORMACION  = 4

# Colores para las 4 leyendas de distribución
_COLORES_LEYENDA = [
    "color:#1F2937;",
    "color:#FF9F2E;",
    "color:#8E6CFF;",
    "color:#9CA3AF;",
]


class VentanaCliente:

    def __init__(self, ruta_ui: str):
        self.ventana = uic.loadUi(os.path.join(ruta_ui, "interfaz_cliente_unificada.ui"))

        self._nav_buttons = [
            (self.ventana.btnInicio,       PAGE_INICIO),
            (self.ventana.btnClases,       PAGE_CLASES),
            (self.ventana.btnEstadisticas, PAGE_ESTADISTICAS),
            (self.ventana.btnPerfil,       PAGE_PERFIL),
            (self.ventana.btnInformacion,  PAGE_INFORMACION),
        ]

    # ── API para el controlador: conectar señales ───────────────────────────

    def conectar_navegacion(self, callback_pagina, callback_cerrar_sesion):
        """El controlador pasa las funciones que se ejecutarán al pulsar."""
        for btn, idx in self._nav_buttons:
            btn.clicked.connect(lambda checked, p=idx: callback_pagina(p))
        self.ventana.btnCerrarSesion.clicked.connect(callback_cerrar_sesion)

    def conectar_reservar(self, callback):
        """Conecta los botones btnReservar1-4 al callback del controlador."""
        for i in range(1, 5):
            btn = getattr(self.ventana, f"btnReservar{i}", None)
            if btn:
                btn.clicked.connect(lambda checked, n=i: callback(n))

    def conectar_guardar_perfil(self, callback):
        self.ventana.btnGuardarCambios.clicked.connect(callback)

    # ── Navegación ──────────────────────────────────────────────────────────

    def cambiar_pagina(self, indice: int):
        self.ventana.stackedWidget.setCurrentIndex(indice)
        self._actualizar_estilo_menu(indice)

    def pagina_actual(self) -> int:
        return self.ventana.stackedWidget.currentIndex()

    def _actualizar_estilo_menu(self, indice_activo: int):
        for btn, idx in self._nav_buttons:
            btn.setProperty("activo", idx == indice_activo)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    # ── Relleno de datos con el VO ──────────────────────────────────────────

    def inicializar(self, vo) -> None:
        """Rellena todos los widgets de la interfaz con los datos del VO."""
        v = self.ventana

        # ── Header ──────────────────────────────────────────────────────────
        v.lblNombreCliente.setText(f"Hola, {vo.nombre}")
        v.lblFechaAltaCliente.setText(f"Cliente desde {vo.fecha_registro}")

        # ── Inicio — bienvenida ──────────────────────────────────────────────
        v.lblBienvenida.setText(f"Bienvenida, {vo.nombre}")

        # ── Inicio — card1: clases esta semana ───────────────────────────────
        v.lblNumClases.setText(str(vo.clases_semana))

        # ── Inicio — card2: estado de pago ───────────────────────────────────
        v.lblEstadoPago.setText(vo.estado_pagado.capitalize())

        # ── Inicio — card3: calorías esta semana ─────────────────────────────
        v.lblCaloriasSemana.setText(f"{vo.calorias_semana:,} kcal".replace(",", "."))

        # ── Inicio — card4: asistencias este mes ─────────────────────────────
        v.lblAsistencias.setText(vo.get_asistencias_str())

        # ── Inicio — cardPago: último pago ───────────────────────────────────
        v.lblCuota.setText(vo.nombre_tarifa)
        v.lblCantidadPago.setText(vo.get_precio_str())
        v.lblMesPago.setText(vo.ultimo_pago_fecha)
        v.lblPendientePago.setText(vo.ultimo_pago_estado.capitalize())

        # ── Inicio — tabla: próximas clases inscritas ─────────────────────
        self._rellenar_tabla_proximas(vo.proximas_clases)

        # ── Estadísticas — cards ─────────────────────────────────────────────
        v.lblNumEntrenos.setText(str(vo.entrenos_semana))
        v.lblSubEntrenos.setText(vo.get_delta_entrenos_str())
        v.lblNumTiempo.setText(vo.get_tiempo_semana_str())
        v.lblSubTiempo.setText(vo.get_delta_tiempo_str())
        v.lblNumCalorias.setText(f"{vo.calorias_semana:,} kcal".replace(",", "."))

        objetivo = 5
        pct_obj = min(100, round(vo.entrenos_semana * 100 / objetivo)) if objetivo else 0
        v.lblNumObjetivo.setText(f"{pct_obj}%")

        # ── Estadísticas — gráfico calorías: resumen ─────────────────────────
        v.btnMini.setText(f"Total semanal: {vo.calorias_semana:,} kcal".replace(",", "."))

        # ── Estadísticas — distribución: leyendas ────────────────────────────
        self._rellenar_leyendas_distribucion(vo.distribucion_tipos)

        # ── Estadísticas — racha ─────────────────────────────────────────────
        v.lblNumRacha.setText(str(vo.racha_dias))
        v.lblTextoRacha.setText(f"Llevas {vo.racha_dias} días consecutivos entrenando.")

        # ── Perfil — card izquierdo ───────────────────────────────────────────
        v.lblNombrePerfil.setText(vo.nombre)
        v.lblEmailPerfil.setText(vo.email)

        # ── Perfil — campos editables ─────────────────────────────────────────
        v.txtNombre.setText(vo.nombre)
        v.txtTelefono.setText(vo.telefono)
        v.txtEmail.setText(vo.email)
        v.txtFecha.setText(vo.fecha_nacimiento)
        v.txtDireccion.setText(vo.direccion)

        # ── Perfil — barra de progreso y asistencias ──────────────────────────
        self._actualizar_barra_progreso(vo.asistencias_mes, vo.inscripciones_mes)
        v.lblAsistenciasValor.setText(
            f"{vo.asistencias_mes} / {vo.inscripciones_mes} clases"
        )

    # ── Getters de campos editables (para que el controlador los lea) ───────

    def get_datos_perfil(self) -> dict:
        """Devuelve los valores actuales de los campos del formulario de perfil."""
        v = self.ventana
        return {
            "telefono":  v.txtTelefono.text().strip(),
            "email":     v.txtEmail.text().strip(),
            "direccion": v.txtDireccion.text().strip(),
        }

    def get_nombre_clase_card(self, numero_card: int) -> str:
        """Devuelve el texto del label de nombre de la card de clase N."""
        lbl = getattr(self.ventana, f"lblClase{numero_card}", None)
        return lbl.text() if lbl else f"clase {numero_card}"

    # ── Mostrar / cerrar ────────────────────────────────────────────────────

    def show(self):
        self.ventana.show()

    def close(self):
        self.ventana.close()

    # ── Helpers visuales privados ───────────────────────────────────────────

    def _rellenar_tabla_proximas(self, proximas: list):
        tabla = self.ventana.tablaProximasClases
        tabla.setRowCount(0)
        for fila in proximas:
            row = tabla.rowCount()
            tabla.insertRow(row)
            tabla.setItem(row, 0, QTableWidgetItem(fila["nombre_actividad"]))
            tabla.setItem(row, 1, QTableWidgetItem(fila["fecha"]))
            tabla.setItem(row, 2, QTableWidgetItem(fila["hora_inicio"]))
            tabla.setItem(row, 3, QTableWidgetItem(fila["nombre_sala"]))

    def _rellenar_leyendas_distribucion(self, distribucion: dict):
        v      = self.ventana
        labels = [v.lblLeyenda1, v.lblLeyenda2, v.lblLeyenda3, v.lblLeyenda4]
        items  = list(distribucion.items())
        for i, lbl in enumerate(labels):
            if i < len(items):
                tipo, pct = items[i]
                lbl.setText(f"● {tipo:<12} {pct}%")
                lbl.setStyleSheet(_COLORES_LEYENDA[i] + ' font:8pt "Segoe UI";')
            else:
                lbl.setText("")

    def _actualizar_barra_progreso(self, asistencias: int, inscripciones: int):
        v         = self.ventana
        ancho_max = v.barraProgresoFondo.width()
        if inscripciones > 0:
            ancho = min(ancho_max, round(asistencias * ancho_max / inscripciones))
        else:
            ancho = 0
        v.barraProgresoValor.setFixedWidth(max(0, ancho))
        pct = round(asistencias * 100 / inscripciones) if inscripciones else 0
        v.lblPorcentaje.setText(f"{pct}%")