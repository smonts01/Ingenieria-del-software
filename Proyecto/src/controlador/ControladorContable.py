import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem


class ControladorContable:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None

    def abrir(self):
        self.abrir_pantalla("interfaz_contable.ui")

    def abrir_pantalla(self, archivo):
        if self.ventana:
            self.ventana.close()

        ruta = os.path.join(self.ruta_ui, archivo)
        self.ventana = uic.loadUi(ruta)
        self.conectar_botones()
        self.cargar_datos()
        self.ventana.show()

    def conectar_botones(self):
        v = self.ventana

        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(self.cerrar_sesion)

        if hasattr(v, "btnInicio"):
            v.btnInicio.clicked.connect(lambda: self.abrir_pantalla("interfaz_contable.ui"))

        if hasattr(v, "btnPerfil"):
            v.btnPerfil.clicked.connect(lambda: self.abrir_pantalla("interfaz_contable_perfil.ui"))

        if hasattr(v, "btnInformacion"):
            v.btnInformacion.clicked.connect(lambda: self.abrir_pantalla("interfaz_contable_info.ui"))

        if hasattr(v, "btnOcupacion"):
            v.btnOcupacion.clicked.connect(lambda: self.abrir_pantalla("interfaz_contable_pagos_pendientes.ui"))

        if hasattr(v, "btnInscritos"):
            v.btnInscritos.clicked.connect(lambda: self.abrir_pantalla("interfaz_contable_informes.ui"))

        if hasattr(v, "btnRegistroAsistencia"):
            v.btnRegistroAsistencia.clicked.connect(lambda: self.abrir_pantalla("interfaz_contable_registrar_pago.ui"))

        if hasattr(v, "btnClases_2"):
            v.btnClases_2.clicked.connect(lambda: self.abrir_pantalla("interfaz_contable_gestion_economica.ui"))

        if hasattr(v, "btnOcupacion_2"):
            v.btnOcupacion_2.clicked.connect(lambda: self.abrir_pantalla("interfaz_contable_informes_de_pagos.ui"))

        if hasattr(v, "btnOcupacion_3"):
            v.btnOcupacion_3.clicked.connect(lambda: self.abrir_pantalla("interfaz_contable_informes_pagos_pendientes.ui"))

        if hasattr(v, "btnOcupacion_5"):
            v.btnOcupacion_5.clicked.connect(lambda: self.abrir_pantalla("interfaz_contable_informes_balance_mensual.ui"))

        if hasattr(v, "btnOcupacion_6"):
            v.btnOcupacion_6.clicked.connect(lambda: self.abrir_pantalla("interfaz_contable_informes_gestion_economica.ui"))

        if hasattr(v, "btnCalorias_2"):
            v.btnCalorias_2.clicked.connect(self.registrar_pago)

        if hasattr(v, "btnMarcarAbonado"):
            v.btnMarcarAbonado.clicked.connect(self.marcar_abonado)

    def cargar_datos(self):
        v = self.ventana

        if hasattr(v, "tablaUltimosPagos"):
            datos = self.modelo.listar_pagos()
            self.rellenar_tabla(v.tablaUltimosPagos, datos)

        if hasattr(v, "tablaClientesPagosPendientes"):
            datos = self.modelo.pagos_pendientes()
            self.rellenar_tabla(v.tablaClientesPagosPendientes, datos)

        if hasattr(v, "tableWidget"):
            datos = self.modelo.pagos_pendientes()
            self.rellenar_tabla(v.tableWidget, datos)

        if hasattr(v, "tableWidget_2"):
            datos = self.modelo.informe_pagos_realizados()
            self.rellenar_tabla(v.tableWidget_2, datos)

        if hasattr(v, "tablaInformes"):
            datos = self.modelo.listar_informes()
            self.rellenar_tabla(v.tablaInformes, datos)

    def registrar_pago(self):
        v = self.ventana
        try:
            id_cliente = int(v.lineEdit.text())
            id_tarifa = 1
            if hasattr(v, "comboBox") and v.comboBox.count() > 0:
                id_tarifa = int(v.comboBox.currentText())
            importe = float(v.lineEdit_2.text()) if hasattr(v, "lineEdit_2") else 0.0

            self.modelo.registrar_pago(
                id_cliente,
                self.usuario["id_usuario"],
                id_tarifa,
                importe,
                "efectivo",
                "mensual"
            )
            QMessageBox.information(v, "Correcto", "Pago registrado correctamente")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def marcar_abonado(self):
        v = self.ventana
        try:
            if hasattr(v, "tableWidget"):
                fila = v.tableWidget.currentRow()
                if fila >= 0:
                    id_pago = int(v.tableWidget.item(fila, 0).text())
                    self.modelo.marcar_pago_abonado(id_pago)
                    QMessageBox.information(v, "Correcto", "Pago marcado como abonado")
                    self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def rellenar_tabla(self, tabla, datos):
        tabla.setRowCount(len(datos))
        if datos:
            tabla.setColumnCount(len(datos[0]))
        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                tabla.setItem(fila, columna, QTableWidgetItem(str(valor) if valor is not None else ""))

    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()
