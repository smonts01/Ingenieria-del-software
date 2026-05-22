"""
Vista de gestión de usuarios/clientes del administrador (interfaz_admin_usuarios_clientes.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi


class VistaAdminUsuariosClientes(QMainWindow):
    """Vista de la lista de clientes del gimnasio."""

    CABECERAS = ["ID", "Nombre", "Email", "Teléfono", "Tarifa", "Estado", "Alta"]

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_admin_usuarios_clientes.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    # --- Resumen numérico ---
    def set_total_usuarios(self, total: int):
        self.lblNumUsuarios.setText(str(total))

    def set_num_clientes(self, n: int):
        self.lblClientes.setText(str(n))

    def set_num_entrenadores(self, n: int):
        self.lblEntrenadores.setText(str(n))

    def set_num_admins(self, n: int):
        self.lblAdmins.setText(str(n))

    def set_nuevos_mes(self, n: int):
        self.lblNuevos.setText(str(n))

    # --- Filtros ---
    def get_filtro_estado(self) -> str:
        return self.cmbEstado_2.currentText()

    def get_filtro_tarifa(self) -> str:
        return self.cmbTarifa.currentText()

    def poblar_combo_tarifas(self, tarifas: list[str]):
        self.cmbTarifa.clear()
        self.cmbTarifa.addItems(["Todas"] + tarifas)

    # --- Tabla ---
    def cargar_tabla(self, clientes: list[list]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(clientes))
        self._tabla.setColumnCount(len(self.CABECERAS))
        self._tabla.setHorizontalHeaderLabels(self.CABECERAS)
        for fila_idx, fila in enumerate(clientes):
            for col_idx, valor in enumerate(fila):
                self._tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def get_id_cliente_seleccionado(self) -> str | None:
        if self._tabla is None:
            return None
        fila = self._tabla.currentRow()
        if fila < 0:
            return None
        item = self._tabla.item(fila, 0)
        return item.text() if item else None

    def set_texto_mostrando(self, texto: str):
        self.lblMostrando_2.setText(texto)

    # --- Feedback ---
    def mostrar_error(self, mensaje: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", mensaje)

    def mostrar_mensaje(self, titulo: str, mensaje: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, titulo, mensaje)

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.cmbEstado_2.currentIndexChanged.connect(ctrl.aplicar_filtros)
        self.cmbTarifa.currentIndexChanged.connect(ctrl.aplicar_filtros)
        self.lblTabTrabajadores.mousePressEvent = lambda _: ctrl.ir_trabajadores()
        # Navegación
        self.btnInicio.clicked.connect(ctrl.ir_inicio)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnInscripciones.clicked.connect(ctrl.ir_inscripciones)
        self.btnPagos.clicked.connect(ctrl.ir_pagos)
        self.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
        self.btnConfiguracion.clicked.connect(ctrl.ir_configuracion)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
