"""
Vista de gestión de clases del administrador (interfaz_admin_clases.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox


class VistaAdminClases(QMainWindow):
    """Vista de administración de clases del gimnasio."""

    CABECERAS = ["ID", "Clase", "Entrenador", "Horario", "Sala", "Plazas", "Estado"]

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_admin_clases.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    # --- Filtros ---
    def get_filtro_categoria(self) -> str:
        return self.cmbCategorias.currentText()

    def get_filtro_estado(self) -> str:
        return self.cmbEstados.currentText()

    def get_filtro_horario(self) -> str:
        return self.cmbHorarios.currentText()

    def poblar_combo_categorias(self, categorias: list[str]):
        self.cmbCategorias.clear()
        self.cmbCategorias.addItems(["Todas"] + categorias)

    def poblar_combo_estados(self, estados: list[str]):
        self.cmbEstados.clear()
        self.cmbEstados.addItems(["Todos"] + estados)

    def poblar_combo_horarios(self, horarios: list[str]):
        self.cmbHorarios.clear()
        self.cmbHorarios.addItems(["Todos"] + horarios)

    # --- Tabla de clases ---
    def cargar_tabla(self, clases: list[list]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(clases))
        self._tabla.setColumnCount(len(self.CABECERAS))
        self._tabla.setHorizontalHeaderLabels(self.CABECERAS)
        for fila_idx, fila in enumerate(clases):
            for col_idx, valor in enumerate(fila):
                item = QTableWidgetItem(str(valor))
                self._tabla.setItem(fila_idx, col_idx, item)

    def get_fila_seleccionada(self) -> int | None:
        """Devuelve el índice de la fila seleccionada o None."""
        filas = self._tabla.selectedItems()
        if not filas:
            return None
        return self._tabla.currentRow()

    def get_id_clase_seleccionada(self) -> str | None:
        fila = self.get_fila_seleccionada()
        if fila is None:
            return None
        item = self._tabla.item(fila, 0)
        return item.text() if item else None

    def set_total_clases(self, total: int):
        self.lblTotalClases.setText(str(total))
        self.lblClasesTotales.setText(f"{total} clases registradas")

    def set_texto_mostrando(self, texto: str):
        self.lblMostrando.setText(texto)

    # --- Feedback ---
    def mostrar_mensaje(self, titulo: str, mensaje: str):
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, mensaje: str):
        QMessageBox.critical(self, "Error", mensaje)

    def confirmar_accion(self, pregunta: str) -> bool:
        resp = QMessageBox.question(self, "Confirmar", pregunta)
        return resp == QMessageBox.Yes

    # --- Conexión con el controlador ---
    def conectar_senales(self, ctrl):
        self.btnNuevaClase.clicked.connect(ctrl.nueva_clase)
        self.btnGuardarCambios.clicked.connect(ctrl.guardar_cambios)
        self.cmbCategorias.currentIndexChanged.connect(ctrl.aplicar_filtros)
        self.cmbEstados.currentIndexChanged.connect(ctrl.aplicar_filtros)
        self.cmbHorarios.currentIndexChanged.connect(ctrl.aplicar_filtros)
        # Navegación
        self.btnInicio.clicked.connect(ctrl.ir_inicio)
        self.btnUsuarios.clicked.connect(ctrl.ir_usuarios)
        self.btnInscripciones.clicked.connect(ctrl.ir_inscripciones)
        self.btnPagos.clicked.connect(ctrl.ir_pagos)
        self.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
        self.btnConfiguracion.clicked.connect(ctrl.ir_configuracion)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
