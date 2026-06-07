from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi

#- Cargar el .ui en __init__
# Conectar sus propios botones en set_controlador()
#Exponer métodos set_xxx() / get_xxx() para que el controlador actualice la UI sin tocar widgets directamente

# MENÚ LATERAL
# Conecta los botones comunes del menú lateral con métodos del controlador.
# v = vista actual
# ctrl = controlador contable
def _menu_contable(v, ctrl):
    v.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
    v.btnInicio.clicked.connect(ctrl.ir_inicio)
    v.btnRegistrarPago.clicked.connect(ctrl.ir_registrar_pago)
    v.btnPagosPendientes.clicked.connect(ctrl.ir_pagos_pendientes)
    v.btnGestionEconomica.clicked.connect(ctrl.ir_gestion_economica)
    v.btnInformes.clicked.connect(ctrl.ir_informes)
    v.btnPerfil.clicked.connect(ctrl.ir_perfil)
    v.btnInformacion.clicked.connect(ctrl.ir_informacion)


# Rellenar tablas con tuplas

def _extraer(vo, n):
    if isinstance(vo, (list, tuple)):
        return [str(x) if x is not None else '' for x in list(vo)[:n]]
    props = [k for k,v in type(vo).__dict__.items() if isinstance(v, property)]
    return [str(getattr(vo, k, '')) for k in props[:n]]

# Recibe la tabla, las cabeceras y los datos.
def _rellenar(tabla, cabeceras, datos):
    tabla.clear()
    tabla.setColumnCount(len(cabeceras))
    tabla.setHorizontalHeaderLabels(cabeceras)
    tabla.setRowCount(len(datos))
    for fi, fila in enumerate(datos):
        vals = _extraer(fila, len(cabeceras))
        for ci, val in enumerate(vals):
            tabla.setItem(fi, ci, QTableWidgetItem(val))
    tabla.resizeColumnsToContents()

# Lee una tabla ya pintada en pantalla y devuelve sus cabeceras y filas.
# Lo usa exportar_pdf() para mandar al modelo los datos que se van a guardar en PDF.
def _obtener_datos_tabla(tabla):
    cabeceras = [
        tabla.horizontalHeaderItem(col).text()
        if tabla.horizontalHeaderItem(col) else ''
        for col in range(tabla.columnCount())
    ]

    filas = []

    for fi in range(tabla.rowCount()):
        fila = [
            tabla.item(fi, ci).text() if tabla.item(fi, ci) else ''
            for ci in range(tabla.columnCount())
        ]
        filas.append(fila)

    return cabeceras, filas


# INICIO DEL CONTABLE
# Pantalla principal del contable.
# Muestra resumen: pagos pendientes, ingresos, tarifas, informes,
# últimos pagos y pagos pendientes.
class VistaContableInicio(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__() # Inicializa la ventana.
        loadUi(ruta_ui, self) #carga el archivo .ui de esa ventana
        self.controlador = None #se asigna despues en set_contrlador()

    # Métodos set_: el controlador los usa para actualizar labels de la pantalla.
    
    def set_controlador(self, ctrl):
        self.controlador = ctrl #guarda el controlador
        _menu_contable(self, ctrl) #conecta el menu lateral

    def set_num_pagos_pendientes(self, v): 
        self.labelNumPagosPend.setText(v)
    def set_ingresos_mes(self, v):         
        self.labelIngresosMes.setText(v)
    def set_num_tarifas(self, v):          
        self.labelNumTarifas.setText(v)
    def set_num_informes(self, v):
        if hasattr(self, 'lblInformesGen'): 
            self.lblInformesGen.setText(v)



    # Rellena la tabla de últimos pagos recibidos desde el controlador
    def cargar_tabla_ultimos_pagos(self, datos):
        tabla = self.tablaUltimosPagos
        cabeceras = ['Cliente', 'Tarifa', 'Importe', 'Fecha', 'Estado']
        tabla.clear(); tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras); tabla.setRowCount(len(datos))
        for fi, vo in enumerate(datos):
            for ci, val in enumerate([vo.cliente, vo.tarifa, vo.importe, vo.fecha, vo.estado]):
                tabla.setItem(fi, ci, QTableWidgetItem(str(val) if val is not None else ''))
        tabla.resizeColumnsToContents()

    # Rellena la tabla resumen de pagos pendientes.
    def cargar_tabla_pagos_pendientes(self, datos):
        tabla = self.tablaClientesPagosPendientes
        cabeceras = ['Cliente', 'Importe Pendiente', 'Fecha límite']
        tabla.clear(); tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras); tabla.setRowCount(len(datos))
        for fi, vo in enumerate(datos):
            for ci, val in enumerate([vo.cliente, vo.importe_pendiente, vo.fecha_limite]):
                tabla.setItem(fi, ci, QTableWidgetItem(str(val) if val is not None else ''))
        tabla.resizeColumnsToContents()

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)

    def mostrar_exito(self, msg): 
        QMessageBox.information(self, 'Correcto', msg)


# VISTA REGISTRAR PAGO

# Pantalla para registrar pagos.
# Permite buscar un cliente por DNI, mostrar su pago pendiente y registrar el pago.

class VistaContableRegistrarPago(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)

        # Al pulsar Enter en el DNI, se busca el cliente/pago pendiente.
        self.lineEdit.returnPressed.connect(ctrl.buscar_cliente_registrar_pago)

        #boton que confirma el registro del pago
        self.btnInicio_2.clicked.connect(ctrl.registrar_pago)

    # Getters 
    #el controlador los usa para LEER DATOS ESCRITOS O SELECCIONADOS EN LA VISTA
    def get_dni(self):          
        return self.lineEdit.text().strip().upper()
    
    def get_metodo_pago(self):  
        return self.comboBox.currentText().strip().lower()
    
    def get_fecha_texto(self):  
        return self.lineEdit_2.text().strip() if hasattr(self, 'lineEdit_2') else ''

    # — Setters para mostrar el pago encontrado —

    #MUESTRA EN PANTALLA el pago pendiente encontrado por dni
    def set_cliente(self, nombre, dni, id_cliente, estado, tarifa, importe, fecha):
        
        self.lblNombreCliente_8.setText(str(nombre))
        self.lblNombreCliente_9.setText(f'DNI: {dni}')
        self.lblNombreCliente_10.setText(f'ID:{id_cliente}')
        
        
        if hasattr(self, 'btnCalorias_2'):  
            self.btnCalorias_2.setText(str(estado).capitalize())
        if hasattr(self, 'lblSubAs_3'):     
            self.lblSubAs_3.setText(str(tarifa))
        if hasattr(self, 'lblSubAs_5'):     
            self.lblSubAs_5.setText(f'{float(importe):.2f}€')
        if hasattr(self, 'lblSubAs_4'):     
            self.lblSubAs_4.setText(str(fecha))

    # deja la pantalla en estado sin pago pendiente
    def set_sin_pago(self, dni=''):
        self.lblNombreCliente_8.setText('Sin pago pendiente')
        self.lblNombreCliente_9.setText(f'DNI: {dni}')
        self.lblNombreCliente_10.setText('ID: -')
        
        if hasattr(self, 'btnCalorias_2'):  
            self.btnCalorias_2.setText('Al corriente')
        if hasattr(self, 'lblSubAs_3'):     
            self.lblSubAs_3.setText('-')
        if hasattr(self, 'lblSubAs_5'):     
            self.lblSubAs_5.setText('0.00€')
        if hasattr(self, 'lblSubAs_4'):     
            self.lblSubAs_4.setText('-')

    def set_num_pendientes(self, v):
        if hasattr(self, 'labelPagosPendientesRegistro'): 
            self.labelPagosPendientesRegistro.setText(v)

    def set_cobros_hoy(self, v):
        if hasattr(self, 'labelCobrosHoyRegistro'): 
            self.labelCobrosHoyRegistro.setText(v)

    def set_num_informes(self, v):
        if hasattr(self, 'labelInformesRegistro'): 
            self.labelInformesRegistro.setText(v)

    #limpia los campos despues de registrar un pago
    def limpiar_dni(self):
        self.lineEdit.clear()
        if hasattr(self, 'lineEdit_2'): self.lineEdit_2.clear()

    #cambia visualmente el esatdo de pago a abonado
    def set_estado_abonado(self):
        if hasattr(self, 'btnCalorias_2'): self.btnCalorias_2.setText('Abonado')

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)

    def mostrar_exito(self, msg): 
        QMessageBox.information(self, 'Correcto', msg)


# PAGOS PENDIENTES 
# Pantalla de pagos pendientes.
# Muestra resumen de deudas y una tabla de pagos pendientes filtrable.
class VistaContablePagosPendientes(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)

        # Cuando cambia el filtro, el controlador recarga la tabla.
        self.comboFiltroPagos.currentTextChanged.connect(ctrl.cargar_pagos_pendientes_filtrados)

        # Si existe el botón, permite marcar un pago como abonado.
        if hasattr(self, 'btnMarcarAbonado'):
            self.btnMarcarAbonado.clicked.connect(ctrl.marcar_abonado)

    # Devuelve el filtro seleccionado en el desplegable.
    def get_filtro(self): 
        return self.comboFiltroPagos.currentText().strip().lower()
    
    # Actualiza los indicadores/resumen de la pantalla de pagos pendientes.
    def set_resumen(self, clientes_deuda, importe_pendiente, vencidos, vencen_semana, total_pendientes):
        if hasattr(self, 'labelClientesDeuda'):     
            self.labelClientesDeuda.setText(str(clientes_deuda))
        if hasattr(self, 'labelImportePendiente'):  
            self.labelImportePendiente.setText(f'{float(importe_pendiente):.2f} €')
        if hasattr(self, 'labelPagosVencidos'):     
            self.labelPagosVencidos.setText(str(vencidos))
        if hasattr(self, 'labelVencenSemana'):     
            self.labelVencenSemana.setText(str(vencen_semana))
        if hasattr(self, 'label_Num_Pagos_Pend'):  
            self.label_Num_Pagos_Pend.setText(str(total_pendientes))
        if hasattr(self, 'label_Num_Vencidos'):     
            self.label_Num_Vencidos.setText(str(vencidos))
        if hasattr(self, 'label_ImporteTotal'):     
            self.label_ImporteTotal.setText(f'{float(importe_pendiente):.2f} €')

    # Rellena la tabla con los pagos pendientes recibidos desde el controlador.
    def cargar_tabla(self, datos):
        # datos = lista de PagoPendienteVO
        cabeceras = ['Cliente', 'Tarifa', 'Importe', 'Fecha']
        tabla = self.tableWidget
        tabla.clear(); tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras); tabla.setRowCount(len(datos))
        for fi, vo in enumerate(datos):
            for ci, val in enumerate([vo.nombre_cliente, vo.nombre_tarifa, vo.importe, vo.fecha]):
                tabla.setItem(fi, ci, QTableWidgetItem(str(val) if val is not None else ''))
        tabla.resizeColumnsToContents()
        return
        


# VISTA GESTIÓN ECONÓMICA
# Pantalla de gestión económica.
# Muestra tarifas, nóminas, pagos pendientes, balance y salarios.

class VistaContableGestionEconomica(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)

    
    # Actualiza en pantalla los datos de una tarifa concreta.
    # nombre indica si es básica o premium.
    def set_tarifa(self, nombre, precio, duracion):
        if nombre == 'basico':
            if hasattr(self, 'labelBasicoPrecio'):    
                self.labelBasicoPrecio.setText(precio)
            if hasattr(self, 'labelBasicoBuracion'):  
                self.labelBasicoBuracion.setText(duracion)
        elif nombre == 'premium':
            if hasattr(self, 'labelPremiumPrecio'):   
                self.labelPremiumPrecio.setText(precio)
            if hasattr(self, 'labelPremiumDuracion'): 
                self.labelPremiumDuracion.setText(duracion)

    def set_num_tarifas(self, v):
        if hasattr(self, 'labelTarifasActivasEco'): 
            self.labelTarifasActivasEco.setText(v)

    def set_nominas(self, v):
        if hasattr(self, 'labelNominasMesEco'): 
            self.labelNominasMesEco.setText(v)

    def set_pagos_pendientes(self, v):
        if hasattr(self, 'labelPagosPendientesEco'): 
            self.labelPagosPendientesEco.setText(v)

    # Muestra ingresos, gastos y balance económico.
    def set_balance(self, ingresos, gastos, balance):
        if hasattr(self, 'labelIngresosEco'): 
            self.labelIngresosEco.setText(ingresos)
        if hasattr(self, 'labelGastosEco'):   
            self.labelGastosEco.setText(gastos)
        if hasattr(self, 'labelBalanceEco'):  
            self.labelBalanceEco.setText(balance)
    
    # Rellena la tabla de salarios del personal.
    def cargar_tabla_salarios(self, datos):
        tabla = self.tablaSalariosEconomica
        cabeceras = ['Empleado', 'Rol', 'Salario']
        tabla.clear(); tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras); tabla.setRowCount(len(datos))
        for fi, vo in enumerate(datos):
            for ci, val in enumerate([vo.nombre, vo.rol, vo.salario]):
                tabla.setItem(fi, ci, QTableWidgetItem(str(val) if val is not None else ''))
        tabla.resizeColumnsToContents()

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)

   

# VISTA INFORMES
# Pantalla principal de informes.
# Permite abrir los distintos tipos de informe y generar informes.

class VistaContableInformes(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)

        # Cada botón abre una pantalla de informe distinta.
        # El lambda sirve para pasar parámetros al método del controlador.

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
        if hasattr(self, 'labelInformesGeneradosInf'): 
            self.labelInformesGeneradosInf.setText(v)
    def set_ingresos_mes(self, v):
        if hasattr(self, 'labelIngresosMesInf'): 
            self.labelIngresosMesInf.setText(v)
    def set_gastos_mes(self, v):
        if hasattr(self, 'labelGastosMesInf'): 
            self.labelGastosMesInf.setText(v)
    def set_balance_mes(self, v):
        if hasattr(self, 'labelBalanceInf'): 
            self.labelBalanceInf.setText(v)

    # Rellena la tabla con el historial de informes generados.
    def cargar_tabla_historial(self, datos):
        tabla = self.tablaHistorialInformes
        cabeceras = ['ID', 'Contable', 'Tipo', 'Fecha']
        tabla.clear(); tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras); tabla.setRowCount(len(datos))
        for fi, vo in enumerate(datos):
            for ci, val in enumerate([vo.id_informe, vo.contable, vo.tipo_informe, vo.fecha]):
                tabla.setItem(fi, ci, QTableWidgetItem(str(val) if val is not None else ''))
        tabla.resizeColumnsToContents()

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)
    
    def mostrar_exito(self, msg): 
        QMessageBox.information(self, 'Correcto', msg)

   

# VISTA PERFIL CONTABLE
# Pantalla de perfil del contable.
# Muestra datos personales y estadísticas de trabajo.

class VistaContablePerfil(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)

    # Actualiza los labels con los datos personales del contable.
    def set_perfil(self, nombre, rol, email, telefono, direccion, fecha_alta):
        if hasattr(self, 'labelPerfilNombre'):    
            self.labelPerfilNombre.setText(nombre)
        if hasattr(self, 'labelPerfilRol'):       
            self.labelPerfilRol.setText(rol)
        if hasattr(self, 'labelPerfilEmail'):     
            self.labelPerfilEmail.setText(email)
        if hasattr(self, 'labelPerfilTelefono'):  
            self.labelPerfilTelefono.setText(telefono)
        if hasattr(self, 'labelPerfilDireccion'): 
            self.labelPerfilDireccion.setText(direccion)
        if hasattr(self, 'labelPerfilFechaAlta'): 
            self.labelPerfilFechaAlta.setText(fecha_alta)

    # Actualiza las estadísticas del perfil:
    # pagos registrados, pendientes revisados, informes generados e importe gestionado.

    def set_stats(self, pagos, pendientes, informes, importe):
        if hasattr(self, 'labelPerfilPagosRegistrados'):    
            self.labelPerfilPagosRegistrados.setText(str(pagos))
        if hasattr(self, 'labelPerfilPendientesRevisados'): 
            self.labelPerfilPendientesRevisados.setText(str(pendientes))
        if hasattr(self, 'labelPerfilInformesGenerados'):   
            self.labelPerfilInformesGenerados.setText(str(informes))
        if hasattr(self, 'labelPerfilImporteGestionado'):   
            self.labelPerfilImporteGestionado.setText(f'{float(importe):.2f} €')

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)


# VISTA INFORMACIÓN
# Pantalla de información general.
# Solo carga la interfaz y conecta el menú lateral.

class VistaContableInfo(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)


#  SUB INFORMES
# Vistas de informes concretos.
# Todas:
# - cargan su .ui
# - conectan el botón Exportar PDF
# - rellenan una tabla
# - devuelven los datos de la tabla para exportar a PDF

class VistaContableInformeGestionEconomica(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    # Botón que llama al controlador para exportar el informe a PDF.
    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_contable(self, ctrl)
        self.btnExportarPDF.clicked.connect(ctrl.exportar_pdf)

    # Rellena la tabla del informe con los datos que trae el controlador.
    def cargar_tabla(self, datos):
        _rellenar(self.tablaInformeGestionEconomica, ['Concepto', 'Valor'], datos)

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)
    
    def mostrar_exito(self, msg): 
        QMessageBox.information(self, 'PDF exportado', msg)

    # Devuelve cabeceras y filas de la tabla para que el controlador/modelo genere el PDF.
    def obtener_datos_tabla_informe(self):
        return _obtener_datos_tabla(self.tablaInformeGestionEconomica)


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

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): 
        QMessageBox.information(self, 'PDF exportado', msg)

    def obtener_datos_tabla_informe(self):
        return _obtener_datos_tabla(self.tablaInformePagos)


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

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)

    def mostrar_exito(self, msg): 
        QMessageBox.information(self, 'PDF exportado', msg)
    
    def obtener_datos_tabla_informe(self):
        return _obtener_datos_tabla(self.tablaInformePagosPendientes)


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

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)

    def mostrar_exito(self, msg): 
        QMessageBox.information(self, 'PDF exportado', msg)

    def obtener_datos_tabla_informe(self):
        return _obtener_datos_tabla(self.tablaInformeBalanceMensual)