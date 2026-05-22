"""
Vistas de informes del contable
  - VistaContableInformes               (interfaz_contable_informes.ui)
  - VistaContableInformeBalanceMensual  (interfaz_contable_informes_balance_mensual.ui)
  - VistaContableInformeDePagos         (interfaz_contable_informes_de_pagos.ui)
  - VistaContableInformeGestionEconomica(interfaz_contable_informes_gestion_económica.ui)
  - VistaContableInformePagosPendientes (interfaz_contable_informes_pagos_pendientes.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi


def _conectar_menu_contable(vista, ctrl):
    vista.btnInicio.clicked.connect(ctrl.ir_inicio)
    vista.btnClases_2.clicked.connect(ctrl.ir_gestion_economica)
    vista.btnInscritos.clicked.connect(ctrl.ir_pagos_pendientes)
    vista.btnOcupacion.clicked.connect(ctrl.ir_registrar_pago)
    vista.btnInformacion.clicked.connect(ctrl.ir_informacion)
    vista.btnPerfil.clicked.connect(ctrl.ir_perfil)
    vista.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)


# ---------------------------------------------------------------------------
class VistaContableInformes(QMainWindow):
    """Vista del hub de informes del contable."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_contable_informes.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_num_asistencias(self, valor: str):
        self.labelNumAsistencias.setText(valor)

    def set_num_clases(self, valor: str):
        self.labelNumClases.setText(valor)

    def cargar_tabla(self, datos: list[list], cabeceras: list[str]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(datos))
        self._tabla.setColumnCount(len(cabeceras))
        self._tabla.setHorizontalHeaderLabels(cabeceras)
        for fi, fila in enumerate(datos):
            for ci, val in enumerate(fila):
                self._tabla.setItem(fi, ci, QTableWidgetItem(str(val)))

    def conectar_senales(self, ctrl):
        # Botones de acceso rápido a cada informe
        self.btnOcupacion_2.clicked.connect(ctrl.ir_informe_balance_mensual)
        self.btnOcupacion_3.clicked.connect(ctrl.ir_informe_de_pagos)
        self.btnOcupacion_5.clicked.connect(ctrl.ir_informe_gestion_economica)
        self.btnOcupacion_6.clicked.connect(ctrl.ir_informe_pagos_pendientes)
        _conectar_menu_contable(self, ctrl)


# ---------------------------------------------------------------------------
class _VistaBaseInformeContable(QMainWindow):
    """Base común para las vistas de informe individuales."""

    UI_FILE = ""

    def __init__(self):
        super().__init__()
        loadUi(f"ui/{self.UI_FILE}", self)

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_bienvenida(self, texto: str):
        self.lblBienvenida.setText(texto)

    def conectar_senales(self, ctrl):
        _conectar_menu_contable(self, ctrl)


class VistaContableInformeBalanceMensual(_VistaBaseInformeContable):
    """Informe de balance mensual."""
    UI_FILE = "interfaz_contable_informes_balance_mensual.ui"


class VistaContableInformeDePagos(_VistaBaseInformeContable):
    """Informe de pagos realizados."""
    UI_FILE = "interfaz_contable_informes_de_pagos.ui"


class VistaContableInformeGestionEconomica(_VistaBaseInformeContable):
    """Informe de gestión económica."""
    UI_FILE = "interfaz_contable_informes_gestion_económica.ui"


class VistaContableInformePagosPendientes(_VistaBaseInformeContable):
    """Informe de pagos pendientes."""
    UI_FILE = "interfaz_contable_informes_pagos_pendientes.ui"
