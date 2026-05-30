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
            v.btnInicio.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable.ui")
            )

        if hasattr(v, "btnRegistrarPago"):
            v.btnRegistrarPago.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_registrar_pago.ui")
            )

        if hasattr(v, "btnPagosPendientes"):
            v.btnPagosPendientes.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_pagos_pendientes.ui")
            )

        if hasattr(v, "btnGestionEconomica"):
            v.btnGestionEconomica.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_gestion_economica.ui")
            )

        if hasattr(v, "btnInformes"):
            v.btnInformes.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_contable_informes.ui")
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
        # Al pulsar una tarjeta, se guarda el informe y se abre su pantalla

        if hasattr(v, "btnInformeGestionEconomica"):
            v.btnInformeGestionEconomica.clicked.connect(
                lambda: self.generar_y_abrir_informe(
                    "Gestión económica",
                    "interfaz_contable_informes_gestion_economica.ui"
                )
            )

        if hasattr(v, "btnInformePagos"):
            v.btnInformePagos.clicked.connect(
                lambda: self.generar_y_abrir_informe(
                    "Informe de pagos",
                    "interfaz_contable_informes_de_pagos.ui"
                )
            )

        if hasattr(v, "btnInformePagosPendientes"):
            v.btnInformePagosPendientes.clicked.connect(
                lambda: self.generar_y_abrir_informe(
                    "Informe de pagos pendientes",
                    "interfaz_contable_informes_pagos_pendientes.ui"
                )
            )

        if hasattr(v, "btnInformeBalanceMensual"):
            v.btnInformeBalanceMensual.clicked.connect(
                lambda: self.generar_y_abrir_informe(
                    "Balance mensual",
                    "interfaz_contable_informes_balance_mensual.ui"
                )
            )
        

        # Botón real para registrar pago
        if hasattr(v, "btnConfirmarRegistrarPago"):
            v.btnConfirmarRegistrarPago.clicked.connect(self.registrar_pago)

        # En tu interfaz actual el botón grande se llama btnInicio_2
        if hasattr(v, "btnInicio_2"):
            v.btnInicio_2.clicked.connect(self.registrar_pago)

        # Botón para marcar pago pendiente como abonado
        if hasattr(v, "btnMarcarAbonado"):
            v.btnMarcarAbonado.clicked.connect(self.marcar_abonado)

        # Botón para generar informe
        if hasattr(v, "btnGenerarInforme"):
            v.btnGenerarInforme.clicked.connect(self.generar_informe)


        if hasattr(v, "comboFiltroPagos"):
            v.comboFiltroPagos.currentTextChanged.connect(
                self.cargar_pagos_pendientes_filtrados
            )

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
        # PANTALLA REGISTRAR PAGO
        # ============================================================

        if hasattr(v, "labelPagosPendientesRegistro"):
            total_pendientes = self.modelo.num_pagos_pendientes_contable()
            v.labelPagosPendientesRegistro.setText(str(total_pendientes))

        if hasattr(v, "labelCobrosHoyRegistro"):
            cobros_hoy = self.modelo.cobros_hoy_contable()
            v.labelCobrosHoyRegistro.setText(str(cobros_hoy))

        if hasattr(v, "labelInformesRegistro"):
            total_informes = self.modelo.num_informes_mes_contable()
            v.labelInformesRegistro.setText(str(total_informes))

        # ============================================================
        # PANTALLA PAGOS PENDIENTES
        # Esta pantalla se reconoce porque tiene txtBuscarClientePendiente
        # ============================================================

        if hasattr(v, "comboFiltroPagos"):
            self.cargar_pagos_pendientes_filtrados()

            clientes_deuda = self.modelo.contable_clientes_con_deuda()
            importe_pendiente = self.modelo.contable_importe_pendiente()
            vencidos = self.modelo.contable_pagos_vencidos()
            vencen_semana = self.modelo.contable_pagos_vencen_semana()
            total_pendientes = self.modelo.num_pagos_pendientes_contable()

            if hasattr(v, "labelClientesDeuda"):
                v.labelClientesDeuda.setText(str(clientes_deuda))

            if hasattr(v, "labelImportePendiente"):
                v.labelImportePendiente.setText(f"{float(importe_pendiente):.2f} €")

            if hasattr(v, "labelPagosVencidos"):
                v.labelPagosVencidos.setText(str(vencidos))

            if hasattr(v, "labelVencenSemana"):
                v.labelVencenSemana.setText(str(vencen_semana))

            if hasattr(v, "label_Num_Pagos_Pend"):
                v.label_Num_Pagos_Pend.setText(str(total_pendientes))

            if hasattr(v, "label_Num_Vencidos"):
                v.label_Num_Vencidos.setText(str(vencidos))

            if hasattr(v, "label_ImporteTotal"):
                v.label_ImporteTotal.setText(f"{float(importe_pendiente):.2f} €")


        # ============================================================
        # PANTALLA GESTIÓN ECONÓMICA
        # ============================================================

        if (
            hasattr(v, "labelBasicoPrecio")
            and hasattr(v, "labelBasicoDuracion")
            and hasattr(v, "labelPremiumPrecio")
            and hasattr(v, "labelPremiumDuracion")
        ):
            tarifas = self.modelo.contable_tarifas_economica()

            for tarifa in tarifas:
                nombre = str(tarifa[0]).lower()
                precio = str(tarifa[1])
                duracion = str(tarifa[2])

                if nombre == "basico":
                    v.labelBasicoPrecio.setText(precio)
                    v.labelBasicoDuracion.setText(duracion)

                elif nombre == "premium":
                    v.labelPremiumPrecio.setText(precio)
                    v.labelPremiumDuracion.setText(duracion)

        
        if hasattr(v, "tablaSalariosEconomica"):
            datos = self.modelo.contable_salarios_personal()
            self.rellenar_tabla(
                v.tablaSalariosEconomica,
                datos,
                ["Empleado", "Rol", "Salario"]
            )

        if hasattr(v, "labelTarifasActivasEco"):
            total_tarifas = self.modelo.num_tarifas_activas_contable()
            v.labelTarifasActivasEco.setText(str(total_tarifas))

        if hasattr(v, "labelNominasMesEco"):
            nominas = self.modelo.contable_total_nominas()
            v.labelNominasMesEco.setText(f"{float(nominas):.2f} €")

        if hasattr(v, "labelPagosPendientesEco"):
            pendiente = self.modelo.contable_importe_pendiente()
            v.labelPagosPendientesEco.setText(f"{float(pendiente):.2f} €")

        if (
            hasattr(v, "labelIngresosEco")
            and hasattr(v, "labelGastosEco")
            and hasattr(v, "labelBalanceEco")
        ):
            ingresos, gastos, balance = self.modelo.contable_balance_economico()

            v.labelIngresosEco.setText(f"{float(ingresos):.2f} €")
            v.labelGastosEco.setText(f"{float(gastos):.2f} €")
            v.labelBalanceEco.setText(f"{float(balance):.2f} €")

        # ============================================================
        # PANTALLA INFORMES
        # ============================================================

        if hasattr(v, "labelInformesGeneradosInf"):
            total_informes = self.modelo.num_informes_mes_contable()
            v.labelInformesGeneradosInf.setText(str(total_informes))

        if hasattr(v, "labelIngresosMesInf"):
            ingresos = self.modelo.ingresos_mes_contable()
            v.labelIngresosMesInf.setText(f"{float(ingresos):.2f} €")

        if hasattr(v, "labelGastosMesInf"):
            gastos = self.modelo.contable_gastos_mes()
            v.labelGastosMesInf.setText(f"{float(gastos):.2f} €")

        if hasattr(v, "labelBalanceInf"):
            balance = self.modelo.contable_balance_mes()
            v.labelBalanceInf.setText(f"{float(balance):.2f} €")

        if hasattr(v, "tablaHistorialInformes"):
            datos = self.modelo.historial_informes_contable()
            self.rellenar_tabla(
                v.tablaHistorialInformes,
                datos,
                ["ID", "Contable", "Tipo", "Fecha"]
            )

        # ============================================================
        # INFORME GESTIÓN ECONÓMICA
        # ============================================================

        if hasattr(v, "tablaInformeGestionEconomica"):
            datos = self.modelo.informe_gestion_economica_contable()
            self.rellenar_tabla(
                v.tablaInformeGestionEconomica,
                datos,
                ["Concepto", "Valor"]
            )

        # ============================================================
        # INFORME DE PAGOS
        # ============================================================

        if hasattr(v, "tablaInformePagos"):
            datos = self.modelo.informe_pagos_realizados()
            self.rellenar_tabla(
                v.tablaInformePagos,
                datos,
                ["Cliente", "Tarifa", "Importe", "Fecha", "Método"]
            )

        # ============================================================
        # INFORME DE PAGOS PENDIENTES
        # ============================================================

        if hasattr(v, "tablaInformePagosPendientes"):
            datos = self.modelo.pagos_pendientes()
            self.rellenar_tabla(
                v.tablaInformePagosPendientes,
                datos,
                ["ID Pago", "Cliente", "Tarifa", "Importe", "Fecha", "Cuota"]
            )

        # ============================================================
        # INFORME BALANCE MENSUAL
        # ============================================================

        if hasattr(v, "tablaInformeBalanceMensual"):
            datos = self.modelo.informe_balance_mensual_contable()
            self.rellenar_tabla(
                v.tablaInformeBalanceMensual,
                datos,
                ["Año", "Mes", "Ingresos", "Gastos", "Balance"]
            )

        # ============================================================
        # PANTALLA PERFIL CONTABLE
        # ============================================================

        if hasattr(v, "labelPerfilNombre"):
            perfil = self.modelo.perfil_usuario(self.usuario["id_usuario"])

            if perfil:
                # perfil_usuario devuelve:
                # 0 id_usuario
                # 1 dni
                # 2 nombre
                # 3 telefono
                # 4 email
                # 5 username
                # 6 rol
                # 7 direccion
                # 8 fecha_registro
                # 9 fecha_nacimiento

                v.labelPerfilNombre.setText(str(perfil[2]))
                v.labelPerfilRol.setText(str(perfil[6]).capitalize())
                v.labelPerfilEmail.setText(str(perfil[4]))
                v.labelPerfilTelefono.setText(str(perfil[3]))
                v.labelPerfilDireccion.setText(str(perfil[7]))

                if perfil[8]:
                    v.labelPerfilFechaAlta.setText(f"Miembro desde: {perfil[8]}")
                else:
                    v.labelPerfilFechaAlta.setText("Miembro desde: -")

            pagos_registrados = self.modelo.contable_pagos_registrados(
                self.usuario["id_usuario"]
            )

            pendientes_revisados = self.modelo.contable_pendientes_revisados()

            informes_generados = self.modelo.contable_informes_generados_usuario(
                self.usuario["id_usuario"]
            )

            importe_gestionado = self.modelo.contable_importe_gestionado(
                self.usuario["id_usuario"]
            )

            if hasattr(v, "labelPerfilPagosRegistrados"):
                v.labelPerfilPagosRegistrados.setText(str(pagos_registrados))

            if hasattr(v, "labelPerfilPendientesRevisados"):
                v.labelPerfilPendientesRevisados.setText(str(pendientes_revisados))

            if hasattr(v, "labelPerfilInformesGenerados"):
                v.labelPerfilInformesGenerados.setText(str(informes_generados))

            if hasattr(v, "labelPerfilImporteGestionado"):
                v.labelPerfilImporteGestionado.setText(f"{float(importe_gestionado):.2f} €")

        # ============================================================
        # OTRAS PANTALLAS DEL CONTABLE
        # ============================================================

        if hasattr(v, "tableWidget") and not hasattr(v, "comboFiltroPagos"):
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


    #filtrar en tabla de clientes x clientes con pagos pendientes, pendiente vencido y todos
    def cargar_pagos_pendientes_filtrados(self, *args):
        v = self.ventana

        if not hasattr(v, "tableWidget"):
            return

        if hasattr(v, "comboFiltroPagos"):
            filtro = v.comboFiltroPagos.currentText().strip().lower()
        else:
            filtro = "todos"

        datos = self.modelo.pagos_pendientes()
        datos_filtrados = []

        from datetime import date, datetime

        for fila in datos:
            id_pago = fila[0]
            cliente = fila[1]
            tarifa = fila[2]
            importe = fila[3]
            fecha_pago = fila[4]
            cuota = fila[5] if len(fila) > 5 else ""

            fecha_convertida = fecha_pago

            if isinstance(fecha_pago, str):
                try:
                    fecha_convertida = datetime.strptime(fecha_pago[:10], "%Y-%m-%d").date()
                except Exception:
                    fecha_convertida = None
            elif hasattr(fecha_pago, "date"):
                fecha_convertida = fecha_pago.date()

            es_vencido = False

            if fecha_convertida is not None:
                es_vencido = fecha_convertida < date.today()

            if filtro == "vencido" and not es_vencido:
                continue

            if filtro == "pendiente" and es_vencido:
                continue

            datos_filtrados.append((
                id_pago,
                cliente,
                tarifa,
                importe,
                fecha_pago,
                cuota
            ))

        self.rellenar_tabla(
            v.tableWidget,
            datos_filtrados,
            ["ID Pago", "Cliente", "Tarifa", "Importe", "Fecha", "Cuota"]
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

                self.cargar_datos()

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

                        MensajeView.information(
                            v,
                            "Correcto",
                            "Pago marcado como abonado"
                        )

                        self.cargar_datos()
                        return

            MensajeView.warning(v, "Error", "Selecciona un pago primero")

        except Exception as e:
            MensajeView.warning(v, "Error", str(e))


    def generar_y_abrir_informe(self, tipo_informe, archivo_ui):
        """
        Genera un informe en la base de datos y abre su pantalla correspondiente.
        """

        try:
            self.modelo.generar_informe(
                self.usuario["id_usuario"],
                tipo_informe
            )

            self.abrir_pantalla(archivo_ui)

        except Exception as e:
            MensajeView.warning(
                self.ventana,
                "Error",
                f"No se pudo generar el informe: {e}"
            )



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

        
        tabla.resizeColumnsToContents()
        tabla.resizeRowsToContents()



    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()
