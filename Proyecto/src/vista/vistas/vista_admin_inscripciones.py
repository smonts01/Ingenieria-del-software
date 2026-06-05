"""
Vista de gestión de inscripciones del administrador (interfaz_admin_inscripciones.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox


class VistaAdminInscripciones(QMainWindow):
    """Vista de inscripciones a clases."""

    CABECERAS = ["ID", "Cliente", "Clase", "Fecha", "Estado"]

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_admin_inscripciones.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    # --- Resumen KPIs ---
    def set_clase_solicitada(self, texto: str):
        self.Clasesolicitada.setText(texto)

    def set_clase_menos_solicitada(self, texto: str):
        self.ClaseMenosSoli.setText(texto)

    def set_inscripciones_canceladas(self, texto: str):
        self.InsCanceladas.setText(texto)

    def set_ocupacion_media(self, texto: str):
        self.OcupMedia.setText(texto)

    # --- Alertas visuales ---
    def mostrar_alerta_aforo(self, visible: bool):
        self.frameAlertaAforo.setVisible(visible)

    def mostrar_alerta_baja_inscripcion(self, visible: bool):
        self.frameAlertaBajaInscripcion.setVisible(visible)

    def mostrar_alerta_cancelaciones(self, visible: bool):
        self.frameAlertaCancelaciones.setVisible(visible)

    # --- Filtros ---
    def get_filtro_clase(self) -> str:
        return self.cmbClase.currentText()

    def get_filtro_estado(self) -> str:
        return self.cmbEstado.currentText()

    def get_filtro_fecha(self) -> str:
        return self.cmbFecha.currentText()

    def poblar_combo_clases(self, clases: list[str]):
        self.cmbClase.clear()
        self.cmbClase.addItems(["Todas"] + clases)

    # --- Tabla ---
    def cargar_tabla(self, inscripciones: list[list]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(inscripciones))
        self._tabla.setColumnCount(len(self.CABECERAS))
        self._tabla.setHorizontalHeaderLabels(self.CABECERAS)
        for fila_idx, fila in enumerate(inscripciones):
            for col_idx, valor in enumerate(fila):
                self._tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def get_id_inscripcion_seleccionada(self) -> str | None:
        if self._tabla is None:
            return None
        fila = self._tabla.currentRow()
        if fila < 0:
            return None
        item = self._tabla.item(fila, 0)
        return item.text() if item else None

    # --- Feedback ---
    def mostrar_error(self, mensaje: str):
        
        QMessageBox.critical(self, "Error", mensaje)

    def mostrar_mensaje(self, titulo: str, mensaje: str):
   
        QMessageBox.information(self, titulo, mensaje)

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.cmbClase.currentIndexChanged.connect(ctrl.aplicar_filtros)
        self.cmbEstado.currentIndexChanged.connect(ctrl.aplicar_filtros)
        self.cmbFecha.currentIndexChanged.connect(ctrl.aplicar_filtros)
        # Navegación
        self.btnInicio.clicked.connect(ctrl.ir_inicio)
        self.btnUsuarios.clicked.connect(ctrl.ir_usuarios)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnPagos.clicked.connect(ctrl.ir_pagos)
        self.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
        self.btnConfiguracion.clicked.connect(ctrl.ir_configuracion)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
