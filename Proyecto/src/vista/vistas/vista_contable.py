"""
Vistas del rol Contable — Patrón MVC según ejemplo de la profesora.

Responsabilidad de la Vista:
- Cargar el .ui en __init__
- Conectar sus propios botones en set_controlador()
- Exponer métodos set_xxx() / get_xxx() para que el controlador
  actualice la UI sin tocar widgets directamente
- Nunca contiene lógica de negocio
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi


# ── Helper: menú lateral común ────────────────────────────────────────────────

def _menu_contable(v, ctrl):
    v.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
    v.btnInicio.clicked.connect(ctrl.ir_inicio)
    v.btnRegistrarPago.clicked.connect(ctrl.ir_registrar_pago)
    v.btnPagosPendientes.clicked.connect(ctrl.ir_pagos_pendientes)
    v.btnGestionEconomica.clicked.connect(ctrl.ir_gestion_economica)
    v.btnInformes.clicked.connect(ctrl.ir_informes)
    v.btnPerfil.clicked.connect(ctrl.ir_perfil)
    v.btnInformacion.clicked.connect(ctrl.ir_informacion)


# ── Helper: rellenar tabla con tuplas ─────────────────────────────────────────

def _rellenar(tabla, cabeceras, datos):
    tabla.clear()
    tabla.setColumnCount(len(cabeceras))
    tabla.setHorizontalHeaderLabels(cabeceras)
    tabla.setRowCount(len(datos))
    for fi, fila in enumerate(datos):
        for ci, val in enumerate(list(fila)[:len(cabeceras)]):
            tabla.setItem(fi, ci, QTableWidgetItem(str(val) if val is not None else ''))
    tabla.resizeColumnsToContents()


# ── Vista inicio ──────────────────────────────────────────────────────────────

class VistaContableInicio(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)

    def set_num_pagos_pendientes(self, v): self.labelNumPagosPend.setText(v)
    def set_ingresos_mes(self, v):         self.labelIngresosMes.setText(v)
    def set_num_tarifas(self, v):          self.labelNumTarifas.setText(v)
    def set_num_informes(self, v):
        if hasattr(self, 'lblInformesGen'): self.lblInformesGen.setText(v)

    def cargar_tabla_ultimos_pagos(self, datos):
        _rellenar(self.tablaUltimosPagos,
                  ['Cliente', 'Tarifa', 'Importe', 'Fecha', 'Estado'], datos)

    def cargar_tabla_pagos_pendientes(self, datos):
        _rellenar(self.tablaClientesPagosPendientes,
                  ['Cliente', 'Importe Pendiente', 'Fecha límite'], datos)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'Correcto', msg)


# ── Vista registrar pago ──────────────────────────────────────────────────────

class VistaContableRegistrarPago(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)
        self.lineEdit.returnPressed.connect(ctrl.buscar_cliente_registrar_pago)
        self.btnInicio_2.clicked.connect(ctrl.registrar_pago)

    # — Getters —
    def get_dni(self):          return self.lineEdit.text().strip().upper()
    def get_metodo_pago(self):  return self.comboBox.currentText().strip().lower()
    def get_fecha_texto(self):  return self.lineEdit_2.text().strip() if hasattr(self, 'lineEdit_2') else ''

    # — Setters para mostrar el pago encontrado —
    def set_cliente(self, nombre, dni, id_cliente, estado, tarifa, importe, fecha):
        self.lblNombreCliente_8.setText(str(nombre))
        self.lblNombreCliente_9.setText(f'DNI: {dni}')
        self.lblNombreCliente_10.setText(f'ID:{id_cliente}')
        if hasattr(self, 'btnCalorias_2'):  self.btnCalorias_2.setText(str(estado).capitalize())
        if hasattr(self, 'lblSubAs_3'):     self.lblSubAs_3.setText(str(tarifa))
        if hasattr(self, 'lblSubAs_5'):     self.lblSubAs_5.setText(f'{float(importe):.2f}€')
        if hasattr(self, 'lblSubAs_4'):     self.lblSubAs_4.setText(str(fecha))

    def set_sin_pago(self, dni=''):
        self.lblNombreCliente_8.setText('Sin pago pendiente')
        self.lblNombreCliente_9.setText(f'DNI: {dni}')
        self.lblNombreCliente_10.setText('ID: -')
        if hasattr(self, 'btnCalorias_2'):  self.btnCalorias_2.setText('Al corriente')
        if hasattr(self, 'lblSubAs_3'):     self.lblSubAs_3.setText('-')
        if hasattr(self, 'lblSubAs_5'):     self.lblSubAs_5.setText('0.00€')
        if hasattr(self, 'lblSubAs_4'):     self.lblSubAs_4.setText('-')

    def set_num_pendientes(self, v):
        if hasattr(self, 'labelPagosPendientesRegistro'): self.labelPagosPendientesRegistro.setText(v)
    def set_cobros_hoy(self, v):
        if hasattr(self, 'labelCobrosHoyRegistro'): self.labelCobrosHoyRegistro.setText(v)
    def set_num_informes(self, v):
        if hasattr(self, 'labelInformesRegistro'): self.labelInformesRegistro.setText(v)

    def limpiar_dni(self):
        self.lineEdit.clear()
        if hasattr(self, 'lineEdit_2'): self.lineEdit_2.clear()

    def set_estado_abonado(self):
        if hasattr(self, 'btnCalorias_2'): self.btnCalorias_2.setText('Abonado')

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'Correcto', msg)


# ── Vista pagos pendientes ────────────────────────────────────────────────────

class VistaContablePagosPendientes(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)
        self.comboFiltroPagos.currentTextChanged.connect(ctrl.cargar_pagos_pendientes_filtrados)
        if hasattr(self, 'btnMarcarAbonado'):
            self.btnMarcarAbonado.clicked.connect(ctrl.marcar_abonado)

    def get_filtro(self): return self.comboFiltroPagos.currentText().strip().lower()

    def set_resumen(self, clientes_deuda, importe_pendiente, vencidos, vencen_semana, total_pendientes):
        if hasattr(self, 'labelClientesDeuda'):     self.labelClientesDeuda.setText(str(clientes_deuda))
        if hasattr(self, 'labelImportePendiente'):  self.labelImportePendiente.setText(f'{float(importe_pendiente):.2f} €')
        if hasattr(self, 'labelPagosVencidos'):     self.labelPagosVencidos.setText(str(vencidos))
        if hasattr(self, 'labelVencenSemana'):      self.labelVencenSemana.setText(str(vencen_semana))
        if hasattr(self, 'label_Num_Pagos_Pend'):   self.label_Num_Pagos_Pend.setText(str(total_pendientes))
        if hasattr(self, 'label_Num_Vencidos'):     self.label_Num_Vencidos.setText(str(vencidos))
        if hasattr(self, 'label_ImporteTotal'):     self.label_ImporteTotal.setText(f'{float(importe_pendiente):.2f} €')

    def cargar_tabla(self, datos):
        cabeceras = ['Cliente', 'Tarifa', 'Importe', 'Fecha']
        tabla = self.tableWidget
        tabla.clear()
        tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras)
        tabla.setRowCount(len(datos))
        for fi, fila in enumerate(datos):
            # fila = (id_pago, nombre, tarifa, importe, fecha)
            # saltamos fila[0] porque id_pago siempre es 0
            vals = [fila[1], fila[2], fila[3], fila[4]]
            for ci, val in enumerate(vals):
                tabla.setItem(fi, ci, QTableWidgetItem(str(val) if val is not None else ''))
        tabla.resizeColumnsToContents()


# ── Vista gestión económica ───────────────────────────────────────────────────

class VistaContableGestionEconomica(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)

    def set_tarifa(self, nombre, precio, duracion):
        if nombre == 'basico':
            if hasattr(self, 'labelBasicoPrecio'):    self.labelBasicoPrecio.setText(precio)
            if hasattr(self, 'labelBasicoBuracion'):  self.labelBasicoBuracion.setText(duracion)
        elif nombre == 'premium':
            if hasattr(self, 'labelPremiumPrecio'):   self.labelPremiumPrecio.setText(precio)
            if hasattr(self, 'labelPremiumDuracion'): self.labelPremiumDuracion.setText(duracion)

    def set_num_tarifas(self, v):
        if hasattr(self, 'labelTarifasActivasEco'): self.labelTarifasActivasEco.setText(v)
    def set_nominas(self, v):
        if hasattr(self, 'labelNominasMesEco'): self.labelNominasMesEco.setText(v)
    def set_pagos_pendientes(self, v):
        if hasattr(self, 'labelPagosPendientesEco'): self.labelPagosPendientesEco.setText(v)
    def set_balance(self, ingresos, gastos, balance):
        if hasattr(self, 'labelIngresosEco'): self.labelIngresosEco.setText(ingresos)
        if hasattr(self, 'labelGastosEco'):   self.labelGastosEco.setText(gastos)
        if hasattr(self, 'labelBalanceEco'):  self.labelBalanceEco.setText(balance)

    def cargar_tabla_salarios(self, datos):
        _rellenar(self.tablaSalariosEconomica, ['Empleado', 'Rol', 'Salario'], datos)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)


# ── Vista informes (menú de informes) ─────────────────────────────────────────

class VistaContableInformes(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)
        self.btnInformeGestionEconomica.clicked.connect(
            lambda: ctrl.generar_y_abrir_informe('Gestión económica',
                'interfaz_contable_informes_gestion_economica.ui'))
        self.btnInformePagos.clicked.connect(
            lambda: ctrl.generar_y_abrir_informe('Informe de pagos',
                'interfaz_contable_informes_de_pagos.ui'))
        self.btnInformePagosPendientes.clicked.connect(
            lambda: ctrl.generar_y_abrir_informe('Informe de pagos pendientes',
                'interfaz_contable_informes_pagos_pendientes.ui'))
        self.btnInformeBalanceMensual.clicked.connect(
            lambda: ctrl.generar_y_abrir_informe('Balance mensual',
                'interfaz_contable_informes_balance_mensual.ui'))
        if hasattr(self, 'btnGenerarInforme'):
            self.btnGenerarInforme.clicked.connect(ctrl.generar_informe)

    def set_num_informes(self, v):
        if hasattr(self, 'labelInformesGeneradosInf'): self.labelInformesGeneradosInf.setText(v)
    def set_ingresos_mes(self, v):
        if hasattr(self, 'labelIngresosMesInf'): self.labelIngresosMesInf.setText(v)
    def set_gastos_mes(self, v):
        if hasattr(self, 'labelGastosMesInf'): self.labelGastosMesInf.setText(v)
    def set_balance_mes(self, v):
        if hasattr(self, 'labelBalanceInf'): self.labelBalanceInf.setText(v)

    def cargar_tabla_historial(self, datos):
        _rellenar(self.tablaHistorialInformes, ['ID', 'Contable', 'Tipo', 'Fecha'], datos)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'Correcto', msg)


# ── Vista perfil contable ─────────────────────────────────────────────────────

class VistaContablePerfil(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)

    def set_perfil(self, nombre, rol, email, telefono, direccion, fecha_alta):
        if hasattr(self, 'labelPerfilNombre'):    self.labelPerfilNombre.setText(nombre)
        if hasattr(self, 'labelPerfilRol'):       self.labelPerfilRol.setText(rol)
        if hasattr(self, 'labelPerfilEmail'):     self.labelPerfilEmail.setText(email)
        if hasattr(self, 'labelPerfilTelefono'):  self.labelPerfilTelefono.setText(telefono)
        if hasattr(self, 'labelPerfilDireccion'): self.labelPerfilDireccion.setText(direccion)
        if hasattr(self, 'labelPerfilFechaAlta'): self.labelPerfilFechaAlta.setText(fecha_alta)

    def set_stats(self, pagos, pendientes, informes, importe):
        if hasattr(self, 'labelPerfilPagosRegistrados'):    self.labelPerfilPagosRegistrados.setText(str(pagos))
        if hasattr(self, 'labelPerfilPendientesRevisados'): self.labelPerfilPendientesRevisados.setText(str(pendientes))
        if hasattr(self, 'labelPerfilInformesGenerados'):   self.labelPerfilInformesGenerados.setText(str(informes))
        if hasattr(self, 'labelPerfilImporteGestionado'):   self.labelPerfilImporteGestionado.setText(f'{float(importe):.2f} €')

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)


# ── Vista información ─────────────────────────────────────────────────────────

class VistaContableInfo(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)


# ── Vistas sub-informes ───────────────────────────────────────────────────────

class VistaContableInformeGestionEconomica(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)
        self.btnExportarPDF.clicked.connect(ctrl.exportar_pdf)

    def cargar_tabla(self, datos):
        _rellenar(self.tablaInformeGestionEconomica, ['Concepto', 'Valor'], datos)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'PDF exportado', msg)


class VistaContableInformeDePagos(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)
        self.btnExportarPDF.clicked.connect(ctrl.exportar_pdf)

    def cargar_tabla(self, datos):
        _rellenar(self.tablaInformePagos,
                  ['Cliente', 'Tarifa', 'Importe', 'Fecha', 'Método'], datos)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'PDF exportado', msg)


class VistaContableInformePagosPendientes(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)
        self.btnExportarPDF.clicked.connect(ctrl.exportar_pdf)

    def cargar_tabla(self, datos):
        _rellenar(self.tablaInformePagosPendientes,
                  ['ID Pago', 'Cliente', 'Tarifa', 'Importe', 'Fecha', 'Cuota'], datos)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'PDF exportado', msg)


class VistaContableInformeBalanceMensual(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)
        self.btnExportarPDF.clicked.connect(ctrl.exportar_pdf)

    def cargar_tabla(self, datos):
        _rellenar(self.tablaInformeBalanceMensual,
                  ['Año', 'Mes', 'Ingresos', 'Gastos', 'Balance'], datos)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'PDF exportado', msg)