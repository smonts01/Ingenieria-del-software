"""
Vista de gestión de pagos del administrador (interfaz_admin_pagos.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi


class VistaAdminPagos(QMainWindow):
    """Vista de control de pagos del gimnasio."""

    CABECERAS = ["ID", "Cliente", "Concepto", "Importe", "Fecha", "Estado"]

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_admin_pagos.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    # --- KPIs ---
    def set_importe_total(self, importe: str):
        self.label_ImporteTotal.setText(importe)

    def set_num_pagos_pendientes(self, n: str):
        self.label_Num_Pagos_Pend.setText(n)

    def set_num_vencidos(self, n: str):
        self.label_Num_Vencidos.setText(n)

    # --- Tabla ---
    def cargar_tabla(self, pagos: list[list]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(pagos))
        self._tabla.setColumnCount(len(self.CABECERAS))
        self._tabla.setHorizontalHeaderLabels(self.CABECERAS)
        for fila_idx, fila in enumerate(pagos):
            for col_idx, valor in enumerate(fila):
                self._tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def get_id_pago_seleccionado(self) -> str | None:
        if self._tabla is None:
            return None
        fila = self._tabla.currentRow()
        if fila < 0:
            return None
        item = self._tabla.item(fila, 0)
        return item.text() if item else None

    # --- Feedback ---
    def mostrar_error(self, mensaje: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", mensaje)

    def mostrar_mensaje(self, titulo: str, mensaje: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, titulo, mensaje)

    def confirmar_accion(self, pregunta: str) -> bool:
        from PyQt5.QtWidgets import QMessageBox
        resp = QMessageBox.question(self, "Confirmar", pregunta)
        return resp == QMessageBox.Yes

    # --- Señales ---
    def conectar_senales(self, ctrl):
        # Navegación
        self.btnInicio.clicked.connect(ctrl.ir_inicio)
        self.btnUsuarios.clicked.connect(ctrl.ir_usuarios)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnInscripciones.clicked.connect(ctrl.ir_inscripciones)
        self.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
        self.btnConfiguracion.clicked.connect(ctrl.ir_configuracion)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
