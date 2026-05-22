"""
Vista de clases asignadas al entrenador (interfaz_entrenador_clases.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi


class VistaEntrenadorClases(QMainWindow):
    """Vista con el listado de clases asignadas al entrenador."""

    CABECERAS = ["ID", "Clase", "Fecha", "Hora", "Sala", "Inscritos", "Estado"]

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_entrenador_clases.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    # --- Cabecera ---
    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaEntrenador.setText(fecha)

    # --- KPIs ---
    def set_clases_hoy(self, valor: str):
        self.labelClasesHoy.setText(valor)

    def set_total_clases_asignadas(self, valor: str):
        self.labelTotalClasesAsignadas.setText(valor)

    def set_proxima_clase(self, nombre: str):
        self.labelProximaClase.setText(nombre)

    def set_hora_proxima(self, hora: str):
        self.lblHoraProxClase.setText(hora)

    # --- Tabla ---
    def cargar_tabla(self, clases: list[list]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(clases))
        self._tabla.setColumnCount(len(self.CABECERAS))
        self._tabla.setHorizontalHeaderLabels(self.CABECERAS)
        for fila_idx, fila in enumerate(clases):
            for col_idx, valor in enumerate(fila):
                self._tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    def get_id_clase_seleccionada(self) -> str | None:
        if self._tabla is None:
            return None
        fila = self._tabla.currentRow()
        if fila < 0:
            return None
        item = self._tabla.item(fila, 0)
        return item.text() if item else None

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.btnInicio_2.clicked.connect(ctrl.ir_inicio)
        self.btnInscritos.clicked.connect(ctrl.ir_inscritos)
        self.btnOcupacion.clicked.connect(ctrl.ir_ocupacion)
        self.btnRegistroAsistencia.clicked.connect(ctrl.ir_registro_asistencia)
        self.btnInformacion.clicked.connect(ctrl.ir_informacion)
        self.btnPerfil.clicked.connect(ctrl.ir_perfil)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
