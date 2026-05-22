"""
Vistas del rol Contable
  - VistaContableInicio           (interfaz_contable.ui)
  - VistaContableGestionEconomica (interfaz_contable_gestion_económica.ui)
  - VistaContablePagosPendientes  (interfaz_contable_pagos_pendientes.ui)
  - VistaContableRegistrarPago    (interfaz_contable_registrar pago.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi


# ---------------------------------------------------------------------------
# Navegación compartida del menú lateral del contable
# ---------------------------------------------------------------------------
def _conectar_menu_contable(vista, ctrl):
    vista.btnInicio.clicked.connect(ctrl.ir_inicio)
    vista.btnClases_2.clicked.connect(ctrl.ir_gestion_economica)
    vista.btnInscritos.clicked.connect(ctrl.ir_pagos_pendientes)
    vista.btnOcupacion.clicked.connect(ctrl.ir_registrar_pago)
    vista.btnInformacion.clicked.connect(ctrl.ir_informacion)
    vista.btnPerfil.clicked.connect(ctrl.ir_perfil)
    vista.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)


# ---------------------------------------------------------------------------
class VistaContableInicio(QMainWindow):
    """Dashboard principal del contable."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_contable.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    def set_bienvenida(self, nombre: str):
        self.lblBienvenida.setText(f"¡Hola, {nombre}!")

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_ingresos_mes(self, valor: str):
        self.labelIngresosMes.setText(valor)

    def set_num_pagos_pendientes(self, valor: str):
        self.labelNumPagosPend.setText(valor)

    def set_num_tarifas(self, valor: str):
        self.labelNumTarifas.setText(valor)

    def cargar_tabla(self, datos: list[list], cabeceras: list[str]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(datos))
        self._tabla.setColumnCount(len(cabeceras))
        self._tabla.setHorizontalHeaderLabels(cabeceras)
        for fi, fila in enumerate(datos):
            for ci, valor in enumerate(fila):
                self._tabla.setItem(fi, ci, QTableWidgetItem(str(valor)))

    def conectar_senales(self, ctrl):
        _conectar_menu_contable(self, ctrl)


# ---------------------------------------------------------------------------
class VistaContableGestionEconomica(QMainWindow):
    """Vista de gestión económica del contable."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_contable_gestion_económica.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_num_asistencias(self, valor: str):
        self.labelNumAsistencias.setText(valor)

    def set_num_clases(self, valor: str):
        self.labelNumClases.setText(valor)

    def set_kpi(self, sufijo: str, valor: str):
        """Actualiza un KPI por su sufijo de widget (p.ej. '_3', '_4', '_5')."""
        lbl = getattr(self, f"labelNumAsistencias{sufijo}", None)
        if lbl:
            lbl.setText(valor)

    def cargar_tabla(self, datos: list[list], cabeceras: list[str]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(datos))
        self._tabla.setColumnCount(len(cabeceras))
        self._tabla.setHorizontalHeaderLabels(cabeceras)
        for fi, fila in enumerate(datos):
            for ci, valor in enumerate(fila):
                self._tabla.setItem(fi, ci, QTableWidgetItem(str(valor)))

    def conectar_senales(self, ctrl):
        _conectar_menu_contable(self, ctrl)


# ---------------------------------------------------------------------------
class VistaContablePagosPendientes(QMainWindow):
    """Vista de pagos pendientes del contable."""

    CABECERAS = ["ID", "Cliente", "Concepto", "Importe", "Vencimiento", "Estado"]

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_contable_pagos_pendientes.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_ingresos_mes(self, valor: str):
        self.labelIngresosMes.setText(valor)

    def set_num_pagos_pendientes(self, valor: str):
        self.labelNumPagosPend.setText(valor)

    def set_num_tarifas(self, valor: str):
        self.labelNumTarifas.setText(valor)

    def get_filtro_pagos(self) -> str:
        return self.comboFiltroPagos.currentText()

    def poblar_combo_filtro(self, opciones: list[str]):
        self.comboFiltroPagos.clear()
        self.comboFiltroPagos.addItems(opciones)

    def cargar_tabla(self, pagos: list[list]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(pagos))
        self._tabla.setColumnCount(len(self.CABECERAS))
        self._tabla.setHorizontalHeaderLabels(self.CABECERAS)
        for fi, fila in enumerate(pagos):
            for ci, valor in enumerate(fila):
                self._tabla.setItem(fi, ci, QTableWidgetItem(str(valor)))

    def get_id_pago_seleccionado(self) -> str | None:
        if self._tabla is None:
            return None
        fila = self._tabla.currentRow()
        if fila < 0:
            return None
        item = self._tabla.item(fila, 0)
        return item.text() if item else None

    def mostrar_error(self, msg: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", msg)

    def mostrar_mensaje(self, titulo: str, msg: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, titulo, msg)

    def conectar_senales(self, ctrl):
        self.comboFiltroPagos.currentIndexChanged.connect(ctrl.aplicar_filtro)
        _conectar_menu_contable(self, ctrl)


# ---------------------------------------------------------------------------
class VistaContableRegistrarPago(QMainWindow):
    """Vista para registrar un nuevo pago."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_contable_registrar pago.ui", self)

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    # --- Formulario ---
    def get_combo_cliente(self) -> str:
        return self.comboBox.currentText()

    def poblar_combo_clientes(self, clientes: list[str]):
        self.comboBox.clear()
        self.comboBox.addItems(clientes)

    def get_datos_pago(self) -> dict:
        """Recoge todos los campos del formulario de pago."""
        from PyQt5.QtWidgets import QLineEdit, QComboBox, QDateEdit
        datos = {}
        for w in self.findChildren(QLineEdit):
            datos[w.objectName()] = w.text().strip()
        for w in self.findChildren(QComboBox):
            datos[w.objectName()] = w.currentText()
        for w in self.findChildren(QDateEdit):
            datos[w.objectName()] = w.date().toString("yyyy-MM-dd")
        return datos

    # --- Feedback ---
    def mostrar_error(self, msg: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", msg)

    def mostrar_exito(self, msg: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Pago registrado", msg)

    def limpiar_formulario(self):
        from PyQt5.QtWidgets import QLineEdit
        for w in self.findChildren(QLineEdit):
            w.clear()

    def conectar_senales(self, ctrl):
        self.btnInicio_2.clicked.connect(ctrl.guardar_pago)
        self.btnCalorias_2.clicked.connect(ctrl.cancelar)
        _conectar_menu_contable(self, ctrl)
