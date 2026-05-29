import os
from src.vista.componentes import CargadorVista, MensajeView, TablaView


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
        self.ventana = CargadorVista.cargar(ruta)
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
        # Registrar pago
        if hasattr(v, "btnCalorias_2") or hasattr(v, "btnRegistrarPago"):
            btn = getattr(v, "btnCalorias_2", None) or getattr(v, "btnRegistrarPago", None)
            btn.clicked.connect(self.registrar_pago)
        # Marcar abonado
        if hasattr(v, "btnMarcarAbonado"):
            v.btnMarcarAbonado.clicked.connect(self.marcar_abonado)
        # Generar informe
        if hasattr(v, "btnGenerarInforme"):
            v.btnGenerarInforme.clicked.connect(self.generar_informe)

    def cargar_datos(self):
        v = self.ventana

        if hasattr(v, "tablaUltimosPagos"):
            self.rellenar_tabla(v.tablaUltimosPagos, self.modelo.listar_pagos())
        if hasattr(v, "tablaClientesPagosPendientes"):
            self.rellenar_tabla(v.tablaClientesPagosPendientes, self.modelo.pagos_pendientes())
        if hasattr(v, "tableWidget"):
            self.rellenar_tabla(v.tableWidget, self.modelo.pagos_pendientes())
        if hasattr(v, "tableWidget_2"):
            self.rellenar_tabla(v.tableWidget_2, self.modelo.informe_pagos_realizados())
        if hasattr(v, "tableWidget_3"):
            self.rellenar_tabla(v.tableWidget_3, self.modelo.informe_pagos_por_mes())
        if hasattr(v, "tablaInformes"):
            self.rellenar_tabla(v.tablaInformes, self.modelo.listar_informes())
        if hasattr(v, "tablaSalarios"):
            self.rellenar_tabla(v.tablaSalarios, self.modelo.informe_salarios())

    def registrar_pago(self):
        v = self.ventana
        try:
            # Try named fields first, then fallback to lineEdits
            campo_cliente = getattr(v, "txtIdCliente", None) or getattr(v, "lineEdit", None)
            campo_tarifa  = getattr(v, "txtIdTarifa",  None) or getattr(v, "lineEdit_3", None)
            campo_importe = getattr(v, "txtImporte",   None) or getattr(v, "lineEdit_2", None)
            campo_metodo  = getattr(v, "cmbMetodo",    None) or getattr(v, "comboBox",   None)

            if not campo_cliente or not campo_cliente.text().strip():
                MensajeView.warning(v, "Error", "Introduce el ID del cliente")
                return

            id_cliente = int(campo_cliente.text().strip())
            id_tarifa  = int(campo_tarifa.text().strip()) if campo_tarifa and campo_tarifa.text().strip() else 1
            importe    = float(campo_importe.text().strip()) if campo_importe and campo_importe.text().strip() else 0.0
            metodo     = campo_metodo.currentText() if campo_metodo and hasattr(campo_metodo, "currentText") else "efectivo"

            if importe <= 0:
                MensajeView.warning(v, "Error", "El importe debe ser mayor que 0")
                return

            self.modelo.registrar_pago(
                id_cliente, self.usuario["id_usuario"],
                id_tarifa, importe, metodo, "mensual"
            )
            MensajeView.information(v, "Correcto", "Pago registrado correctamente")
            self.cargar_datos()
        except ValueError:
            MensajeView.warning(v, "Error", "Los valores numéricos no son válidos")
        except Exception as e:
            MensajeView.warning(v, "Error", str(e))

    def marcar_abonado(self):
        v = self.ventana
        try:
            for tabla_name in ("tableWidget", "tablaClientesPagosPendientes"):
                if hasattr(v, tabla_name):
                    tabla = getattr(v, tabla_name)
                    fila = tabla.currentRow()
                    if fila >= 0 and tabla.item(fila, 0):
                        id_pago = int(tabla.item(fila, 0).text())
                        self.modelo.marcar_pago_abonado(id_pago)
                        MensajeView.information(v, "Correcto", "Pago marcado como abonado")
                        self.cargar_datos()
                        return
            MensajeView.warning(v, "Error", "Selecciona un pago primero")
        except Exception as e:
            MensajeView.warning(v, "Error", str(e))

    def generar_informe(self):
        v = self.ventana
        try:
            tipo = "general"
            if hasattr(v, "cmbTipoInforme"):
                tipo = v.cmbTipoInforme.currentText()
            self.modelo.generar_informe(self.usuario["id_usuario"], tipo)
            MensajeView.information(v, "Correcto", f"Informe '{tipo}' generado correctamente")
            self.cargar_datos()
        except Exception as e:
            MensajeView.warning(v, "Error", str(e))

    def rellenar_tabla(self, tabla, datos):
        tabla.setRowCount(len(datos))
        if datos:
            tabla.setColumnCount(len(datos[0]))
        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro):
                tabla.setItem(fila, col, TablaView.crear_item(str(valor) if valor is not None else ""))

    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()
