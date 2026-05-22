"""
Vistas de perfil e información del contable
  - VistaContablePerfil (interfaz_contable_perfil.ui)
  - VistaContableInfo   (interfaz_contable_info.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5.uic import loadUi


def _conectar_menu_contable(vista, ctrl):
    vista.btnInicio.clicked.connect(ctrl.ir_inicio)
    vista.btnClases_2.clicked.connect(ctrl.ir_gestion_economica)
    vista.btnInscritos.clicked.connect(ctrl.ir_pagos_pendientes)
    vista.btnOcupacion.clicked.connect(ctrl.ir_registrar_pago)
    vista.btnInformacion.clicked.connect(ctrl.ir_informacion)
    vista.btnPerfil.clicked.connect(ctrl.ir_perfil)
    vista.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)


class VistaContablePerfil(QMainWindow):
    """Vista del perfil del contable."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_contable_perfil.ui", self)

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_ingresos_mes(self, valor: str):
        self.labelIngresosMes.setText(valor)

    def set_num_pagos_pendientes(self, valor: str):
        self.labelNumPagosPend.setText(valor)

    def set_num_tarifas(self, valor: str):
        self.labelNumTarifas.setText(valor)

    def get_campo(self, nombre: str) -> str:
        w = self.findChild(QLineEdit, nombre)
        return w.text().strip() if w else ""

    def set_campo(self, nombre: str, valor: str):
        w = self.findChild(QLineEdit, nombre)
        if w:
            w.setText(valor)

    def mostrar_aviso_perfil(self, visible: bool):
        self.frameAvisoPerfil_2.setVisible(visible)

    def mostrar_error(self, msg: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", msg)

    def mostrar_exito(self, msg: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Guardado", msg)

    def conectar_senales(self, ctrl):
        _conectar_menu_contable(self, ctrl)


class VistaContableInfo(QMainWindow):
    """Vista de información del gimnasio para el contable."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_contable_info.ui", self)

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def conectar_senales(self, ctrl):
        _conectar_menu_contable(self, ctrl)
