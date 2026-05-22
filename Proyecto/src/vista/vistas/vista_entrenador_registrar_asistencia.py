"""
Vista de registro de asistencia del entrenador (interfaz_entrenador_registrar_asistencia.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi


class VistaEntrenadorRegistrarAsistencia(QMainWindow):
    """Vista para marcar asistencia en una clase."""

    CABECERAS = ["ID", "Nombre", "Email", "Asistencia"]

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_entrenador_registrar_asistencia.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    # --- Cabecera ---
    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaEntrenador.setText(fecha)

    # --- Selector de clase ---
    def poblar_combo_clases(self, clases: list[str]):
        self.comboSeleccionarClase.clear()
        self.comboSeleccionarClase.addItems(clases)

    def get_clase_seleccionada(self) -> str:
        return self.comboSeleccionarClase.currentText()

    # --- Resumen de la clase ---
    def set_nombre_clase(self, nombre: str):
        self.label_nombreclase.setText(nombre)

    def set_fecha_clase(self, fecha: str):
        self.label_fecha.setText(fecha)

    def set_total_inscritos(self, valor: str):
        self.label_TotalInscritos.setText(valor)
        self.label_numInscritos.setText(valor)

    def set_num_asistentes(self, valor: str):
        self.label_numAsist.setText(valor)

    def set_num_ausentes(self, valor: str):
        self.label_numAus.setText(valor)

    def set_num_pendientes(self, valor: str):
        self.label_numPend.setText(valor)

    def set_resumen_visible(self, visible: bool):
        self.frameResumenAsistencia.setVisible(visible)

    # --- Tabla de alumnos ---
    def cargar_tabla(self, alumnos: list[list]):
        """
        Carga la lista de inscritos en la tabla.
        Columna 'Asistencia' usa checkboxes gestionados por el controlador.
        """
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(alumnos))
        self._tabla.setColumnCount(len(self.CABECERAS))
        self._tabla.setHorizontalHeaderLabels(self.CABECERAS)
        for fila_idx, fila in enumerate(alumnos):
            for col_idx, valor in enumerate(fila):
                self._tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def get_datos_tabla(self) -> list[dict]:
        """Devuelve los datos de la tabla incluyendo el estado de asistencia."""
        if self._tabla is None:
            return []
        resultado = []
        for fila in range(self._tabla.rowCount()):
            fila_data = {}
            for col, nombre in enumerate(self.CABECERAS):
                item = self._tabla.item(fila, col)
                fila_data[nombre.lower()] = item.text() if item else ""
            resultado.append(fila_data)
        return resultado

    # --- Feedback ---
    def mostrar_mensaje(self, titulo: str, mensaje: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, mensaje: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", mensaje)

    def confirmar_guardar(self) -> bool:
        from PyQt5.QtWidgets import QMessageBox
        resp = QMessageBox.question(self, "Guardar asistencia",
                                    "¿Confirmas el registro de asistencia?")
        return resp == QMessageBox.Yes

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.comboSeleccionarClase.currentIndexChanged.connect(ctrl.cargar_clase)
        self.btnInicio_2.clicked.connect(ctrl.ir_inicio)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnInscritos.clicked.connect(ctrl.ir_inscritos)
        self.btnOcupacion.clicked.connect(ctrl.ir_ocupacion)
        self.btnInformacion.clicked.connect(ctrl.ir_informacion)
        self.btnPerfil.clicked.connect(ctrl.ir_perfil)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
