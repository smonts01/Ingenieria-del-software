"""
Vista de ocupación de clases del entrenador (interfaz_entrenador_ocupacionClases.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi


class VistaEntrenadorOcupacion(QMainWindow):
    """Vista de métricas de ocupación de clases del entrenador."""

    CABECERAS = ["Clase", "Fecha", "Inscritos", "Plazas", "% Ocupación"]

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_entrenador_ocupacionClases.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    # --- Cabecera ---
    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    # --- Filtro ---
    def poblar_combo_clase(self, clases: list[str]):
        self.comboBox.clear()
        self.comboBox.addItems(["Todas"] + clases)

    def get_filtro_clase(self) -> str:
        return self.comboBox.currentText()

    # --- KPIs de ocupación ---
    def set_clase_mas_llena(self, nombre: str):
        self.label_Clase_masLlena.setText(nombre)

    def set_ocupacion_media(self, idx: int, valor: str):
        """Actualiza uno de los indicadores de ocupación media (idx 1-3)."""
        frame = getattr(self, f"frameOcupacionMedia{'' if idx == 1 else f'_{idx}'}", None)
        if frame:
            from PyQt5.QtWidgets import QLabel
            lbl = frame.findChild(QLabel)
            if lbl:
                lbl.setText(valor)

    # --- Tabla ---
    def cargar_tabla(self, datos: list[list]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(datos))
        self._tabla.setColumnCount(len(self.CABECERAS))
        self._tabla.setHorizontalHeaderLabels(self.CABECERAS)
        for fila_idx, fila in enumerate(datos):
            for col_idx, valor in enumerate(fila):
                self._tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.comboBox.currentIndexChanged.connect(ctrl.aplicar_filtro)
        self.btnInicio_2.clicked.connect(ctrl.ir_inicio)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnInscritos.clicked.connect(ctrl.ir_inscritos)
        self.btnRegistroAsistencia.clicked.connect(ctrl.ir_registro_asistencia)
        self.btnInformacion.clicked.connect(ctrl.ir_informacion)
        self.btnPerfil.clicked.connect(ctrl.ir_perfil)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
