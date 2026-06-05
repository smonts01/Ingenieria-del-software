"""
Vista de gestión de trabajadores del administrador (interfaz_admin_usuarios_trabajadores.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox


class VistaAdminUsuariosTrabajadores(QMainWindow):
    """Vista de la lista de trabajadores del gimnasio."""

    CABECERAS = ["ID", "Nombre", "Rol", "Email", "Teléfono", "Estado"]

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_admin_usuarios_trabajadores.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    # --- Resumen ---
    def set_total_trabajadores(self, total: int):
        self.lblNumTrabajadores.setText(str(total))

    def set_num_entrenadores(self, n: int):
        self.lblEntrenadores.setText(str(n))

    def set_num_contables(self, n: int):
        self.lblContables.setText(str(n))

    def set_num_recepcionistas(self, n: int):
        self.lblRecepcion.setText(str(n))

    # --- Filtro de rol ---
    def get_filtro_rol(self) -> str:
        return self.cmbRoles.currentText()

    def poblar_combo_roles(self, roles: list[str]):
        self.cmbRoles.clear()
        self.cmbRoles.addItems(["Todos"] + roles)

    # --- Tabla ---
    def cargar_tabla(self, trabajadores: list[list]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(trabajadores))
        self._tabla.setColumnCount(len(self.CABECERAS))
        self._tabla.setHorizontalHeaderLabels(self.CABECERAS)
        for fila_idx, fila in enumerate(trabajadores):
            for col_idx, valor in enumerate(fila):
                self._tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def get_id_trabajador_seleccionado(self) -> str | None:
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
        
        QMessageBox.critical(self, "Error", mensaje)

    def mostrar_mensaje(self, titulo: str, mensaje: str):
    
        QMessageBox.information(self, titulo, mensaje)

    def confirmar_accion(self, pregunta: str) -> bool:
    
        resp = QMessageBox.question(self, "Confirmar", pregunta)
        return resp == QMessageBox.Yes

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.btnNuevoUsuario.clicked.connect(ctrl.nuevo_usuario)
        self.btnGuardarCambios_2.clicked.connect(ctrl.guardar_cambios)
        self.cmbRoles.currentIndexChanged.connect(ctrl.aplicar_filtros)
        self.lblTabClientes.mousePressEvent = lambda _: ctrl.ir_clientes()
        # Navegación
        self.btnInicio.clicked.connect(ctrl.ir_inicio)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnInscripciones.clicked.connect(ctrl.ir_inscripciones)
        self.btnPagos.clicked.connect(ctrl.ir_pagos)
        self.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
        self.btnConfiguracion.clicked.connect(ctrl.ir_configuracion)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
