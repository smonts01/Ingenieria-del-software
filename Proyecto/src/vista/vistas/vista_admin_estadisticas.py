"""
Vista de estadísticas del administrador (interfaz_admin_estadisticas.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi


class VistaAdminEstadisticas(QMainWindow):
    """Vista de estadísticas y métricas del gimnasio."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_admin_estadisticas.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    # --- KPIs resumen ---
    def set_num_clases_activas(self, valor: str):
        self.lblNumClasesActivas.setText(valor)

    def set_num_entrenadores(self, valor: str):
        self.lblNumEntrenadores.setText(valor)

    def set_dato1(self, valor: str):
        self.lblDato1_2.setText(valor)

    def set_dato2(self, valor: str):
        self.lblDato2_2.setText(valor)

    def set_dato3(self, valor: str):
        self.lblDato3_2.setText(valor)

    # --- Gráfico de barras (representado como QFrames) ---
    def set_barras(self, alturas: list[int]):
        """
        Actualiza la altura visual de las barras del gráfico simulado.
        :param alturas: Lista de 7 valores (porcentaje 0-100, uno por día).
        """
        barras = [self.bar1, self.bar2, self.bar3, self.bar4,
                  self.bar5, self.bar6, self.bar7]
        max_h = 120  # px máximo según el diseño
        for barra, pct in zip(barras, alturas):
            h = max(4, int(pct * max_h / 100))
            barra.setFixedHeight(h)

    # --- Filtro de período ---
    def get_periodo(self) -> str:
        return self.cmbPeriodo.currentText()

    def poblar_combo_periodo(self, periodos: list[str]):
        self.cmbPeriodo.clear()
        self.cmbPeriodo.addItems(periodos)

    # --- Tabla de ranking ---
    def cargar_tabla_ranking(self, datos: list[list], cabeceras: list[str]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(datos))
        self._tabla.setColumnCount(len(cabeceras))
        self._tabla.setHorizontalHeaderLabels(cabeceras)
        for fila_idx, fila in enumerate(datos):
            for col_idx, valor in enumerate(fila):
                self._tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.btnActualizar.clicked.connect(ctrl.actualizar)
        self.cmbPeriodo.currentIndexChanged.connect(ctrl.cambiar_periodo)
        self.btnInformes.clicked.connect(ctrl.ir_informes)
        # Navegación
        self.btnInicio.clicked.connect(ctrl.ir_inicio)
        self.btnUsuarios.clicked.connect(ctrl.ir_usuarios)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnInscripciones.clicked.connect(ctrl.ir_inscripciones)
        self.btnPagos.clicked.connect(ctrl.ir_pagos)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
