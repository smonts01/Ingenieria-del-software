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

        # Menú lateral principal
        if hasattr(v, "btnInicio"):
            v.btnInicio.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable.ui")
            )

        if hasattr(v, "btnInscritos"):
            v.btnInscritos.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_gestion_economica.ui")
            )

        if hasattr(v, "btnOcupacion"):
            v.btnOcupacion.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_informes.ui")
            )

        if hasattr(v, "btnRegistroAsistencia"):
            v.btnRegistroAsistencia.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_pagos_pendientes.ui")
            )

        if hasattr(v, "btnClases_2"):
            v.btnClases_2.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_registrar_pago.ui")
            )

        if hasattr(v, "btnPerfil"):
            v.btnPerfil.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_perfil.ui")
            )

        if hasattr(v, "btnInformacion"):
            v.btnInformacion.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_info.ui")
            )

        # Botones internos de la pantalla Informes
        if hasattr(v, "btnOcupacion_2"):
            v.btnOcupacion_2.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_informes_de_pagos.ui")
            )

        if hasattr(v, "btnOcupacion_3"):
            v.btnOcupacion_3.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_informes_pagos_pendientes.ui")
            )

        if hasattr(v, "btnOcupacion_5"):
            v.btnOcupacion_5.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_informes_balance_mensual.ui")
            )

        if hasattr(v, "btnOcupacion_6"):
            v.btnOcupacion_6.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_informes_gestion_economica.ui")
            )

        # Botón correcto de registrar pago
        if hasattr(v, "btnInicio_2"):
            v.btnInicio_2.clicked.connect(self.registrar_pago)

        # Marcar pago como abonado
        if hasattr(v, "btnMarcarAbonado"):
            v.btnMarcarAbonado.clicked.connect(self.marcar_abonado)

        # Generar informe
        if hasattr(v, "btnGenerarInforme"):
            v.btnGenerarInforme.clicked.connect(self.generar_informe)

    def cargar_datos(self):
        v = self.ventana

        # ============================================================
        # INICIO CONTABLE
        # ============================================================

        if hasattr(v, "tablaUltimosPagos"):
            datos = self.modelo.ultimos_pagos_inicio_contable()
            self.rellenar_tabla(
                v.tablaUltimosPagos,
                datos,
                ["Cliente", "Tarifa", "Importe", "Fecha", "Estado"]
            )

        if hasattr(v, "tablaClientesPagosPendientes"):
            datos = self.modelo.pagos_pendientes_inicio_contable()
            self.rellenar_tabla(
                v.tablaClientesPagosPendientes,
                datos,
                ["Cliente", "Importe Pendiente", "Fecha límite"]
            )

        if hasattr(v, "labelNumPagosPend"):
            total_pendientes = self.modelo.num_pagos_pendientes_contable()
            v.labelNumPagosPend.setText(str(total_pendientes))

        if hasattr(v, "labelIngresosMes"):
            ingresos = self.modelo.ingresos_mes_contable()
            v.labelIngresosMes.setText(f"{float(ingresos):.2f} €")

        if hasattr(v, "labelNumTarifas"):
            total_tarifas = self.modelo.num_tarifas_activas_contable()
            v.labelNumTarifas.setText(str(total_tarifas))

        if hasattr(v, "lblInformesGen"):
            total_informes = self.modelo.num_informes_mes_contable()
            v.lblInformesGen.setText(str(total_informes))

        # ============================================================
        # OTRAS PANTALLAS DEL CONTABLE
        # ============================================================

        if hasattr(v, "tableWidget"):
            self.rellenar_tabla(
                v.tableWidget,
                self.modelo.pagos_pendientes(),
                ["ID Pago", "Cliente", "Tarifa", "Importe", "Fecha", "Cuota"]
            )

        if hasattr(v, "tableWidget_2"):
            self.rellenar_tabla(
                v.tableWidget_2,
                self.modelo.informe_pagos_realizados(),
                ["Cliente", "Tarifa", "Importe", "Fecha", "Método"]
            )

        if hasattr(v, "tableWidget_3"):
            self.rellenar_tabla(
                v.tableWidget_3,
                self.modelo.informe_pagos_por_mes(),
                ["Año", "Mes", "Total"]
            )

        if hasattr(v, "tablaInformes"):
            self.rellenar_tabla(
                v.tablaInformes,
                self.modelo.listar_informes(),
                ["ID", "Contable", "Tipo", "Fecha"]
            )

        if hasattr(v, "tablaSalarios"):
            self.rellenar_tabla(
                v.tablaSalarios,
                self.modelo.informe_salarios(),
                ["Empleado", "Rol", "Salario"]
            )

    def registrar_pago(self):
        v = self.ventana

        try:
            # En tu pantalla, lineEdit es el DNI del cliente
            if not hasattr(v, "lineEdit"):
                MensajeView.warning(v, "Error", "No existe el campo para introducir el DNI.")
                return

            dni = v.lineEdit.text().strip().upper()

            if dni == "":
                MensajeView.warning(v, "Error", "Introduce el DNI del cliente.")
                return

            # comboBox es el método de pago
            if hasattr(v, "comboBox"):
                metodo_pago = v.comboBox.currentText().strip().lower()
            else:
                metodo_pago = "efectivo"

            # La base de datos solo acepta: efectivo, tarjeta, transferencia, bizum
            if metodo_pago == "tarjeta":
                metodo_pago = "tarjeta"
            elif metodo_pago == "efectivo":
                metodo_pago = "efectivo"
            elif metodo_pago == "transferencia":
                metodo_pago = "transferencia"
            elif metodo_pago == "bizum":
                metodo_pago = "bizum"
            else:
                MensajeView.warning(
                    v,
                    "Error",
                    "Método de pago no válido. Selecciona tarjeta, efectivo, transferencia o bizum."
                )
                return

            # lineEdit_2 es la fecha del pago
            if hasattr(v, "lineEdit_2"):
                fecha_texto = v.lineEdit_2.text().strip()
            else:
                fecha_texto = ""

            if fecha_texto == "":
                from datetime import datetime
                fecha_pago = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                # Escribe la fecha como: 2026-05-30
                fecha_pago = fecha_texto + " 00:00:00"

            correcto, mensaje = self.modelo.registrar_pago_contable(
                dni,
                self.usuario["id_usuario"],
                metodo_pago,
                fecha_pago
            )

            if correcto:
                MensajeView.information(v, "Correcto", mensaje)

                v.lineEdit.clear()

                if hasattr(v, "lineEdit_2"):
                    v.lineEdit_2.clear()

                if hasattr(v, "btnCalorias_2"):
                    v.btnCalorias_2.setText("Abonado")

            else:
                MensajeView.warning(v, "Error", mensaje)

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

    def rellenar_tabla(self, tabla, datos, cabeceras=None):
        tabla.clear()

        if cabeceras:
            tabla.setColumnCount(len(cabeceras))
            tabla.setHorizontalHeaderLabels(cabeceras)
        elif datos:
            tabla.setColumnCount(len(datos[0]))
        else:
            tabla.setColumnCount(0)

        tabla.setRowCount(len(datos))

        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro):
                texto = str(valor) if valor is not None else ""
                tabla.setItem(fila, col, TablaView.crear_item(texto))



    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()
