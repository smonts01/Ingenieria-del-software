"""
Vistas del rol Cliente — Patrón MVC según ejemplo de la profesora.

La Vista:
- Carga el .ui en __init__
- Conecta sus botones en set_controlador()
- Expone métodos set_xxx() para que el controlador actualice la UI
- Nunca contiene lógica de negocio
"""
from datetime import date, timedelta
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi


_DESCRIPCIONES = {
    'yoga': 'Flexibilidad y relajación.',
    'pilates': 'Core y postura.',
    'spinning': 'Cardio de alta intensidad.',
    'zumba': 'Baile y cardio.',
    'crossfit': 'Fuerza y resistencia.',
}


def _menu_cliente(v, ctrl):
    v.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
    v.btnInicio.clicked.connect(ctrl.ir_inicio)
    v.btnClases.clicked.connect(ctrl.ir_clases)
    v.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
    v.btnPerfil.clicked.connect(ctrl.ir_perfil)
    v.btnInformacion.clicked.connect(ctrl.ir_informacion)


# ── Vista inicio ──────────────────────────────────────────────────────────────

class VistaClienteInicio(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_cliente(self, ctrl)

    # — Cabecera —
    def set_nombre_cliente(self, v): self.lblNombreCliente.setText(v)
    def set_fecha_alta(self, v):     self.lblFechaAltaCliente.setText(v)

    # — Cuerpo —
    def set_bienvenida(self, v):     self.lblBienvenida.setText(v)
    def set_num_clases(self, v):     self.lblNumClases.setText(v)
    def set_estado_pago(self, v):    self.lblEstadoPago.setText(v)
    def set_sub_pago(self, v):       self.lblSubPago.setText(v)
    def set_calorias_semana(self, v):self.lblCaloriasSemana.setText(v)
    def set_asistencias(self, v):
        if hasattr(self, 'lblAsistencias'): self.lblAsistencias.setText(v)
    def set_cuota(self, v):
        if hasattr(self, 'lblCuota'): self.lblCuota.setText(v)
    def set_cantidad_pago(self, v):
        if hasattr(self, 'lblCantidadPago'): self.lblCantidadPago.setText(v)
    def set_mes_pago(self, v):
        if hasattr(self, 'lblMesPago'): self.lblMesPago.setText(v)
    def set_pendiente_pago(self, v):
        if hasattr(self, 'lblPendientePago'): self.lblPendientePago.setText(v)

    def cargar_tabla_proximas(self, datos):
        from src.vista.componentes import TablaView
        tabla = self.tablaProximasClases
        cabeceras = ['Clase', 'Fecha', 'Hora', 'Sala']
        TablaView.configurar_columnas(tabla, cabeceras)
        tabla.setRowCount(len(datos))
        for fi, reg in enumerate(datos):
            vals = [reg.get('nombre_actividad',''), reg.get('fecha',''),
                    reg.get('hora_inicio',''), reg.get('nombre_sala','')]
            for ci, val in enumerate(vals):
                tabla.setItem(fi, ci, TablaView.crear_item(str(val), editable=False))

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)


# ── Vista clases todas ────────────────────────────────────────────────────────

class VistaClienteClasesTodas(QMainWindow):

    _LABELS_CLASE  = {1:'lblClase1',  2:'lblClase2',  3:'lblClase3',  4:'lblClase4',  5:'lblClase4_2'}
    _LABELS_DESC   = {1:'lblDesc1',   2:'lblDesc2',   3:'lblDesc3',   4:'lblDesc4',   5:'lblDesc4_2'}
    _LABELS_FECHA  = {1:'lblFecha1',  2:'lblFecha2',  3:'lblFecha3',  4:'lblFecha4',  5:'lblFecha4_2'}
    _LABELS_PLAZAS = {1:'lblPlazas1', 2:'lblPlazas2', 3:'lblPlazas3', 4:'lblPlazas4', 5:'lblPlazas4_2'}
    _CARDS         = {1:'cardClase1', 2:'cardClase2', 3:'cardClase3', 4:'cardClase4', 5:'cardClase4_2'}

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None
        self._cards_clases = []

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_cliente(self, ctrl)
        # Tabs
        if hasattr(self, 'lblTabRes'):
            self.lblTabRes.mousePressEvent = lambda e: ctrl.ir_reservas()
        if hasattr(self, 'lblTabTodas'):
            self.lblTabTodas.mousePressEvent = lambda e: ctrl.ir_clases()
        # Botones de reserva
        for i in range(1, 6):
            btn = getattr(self, f'btnReservar{i}', None)
            if btn:
                btn.clicked.connect(lambda checked=False, n=i: ctrl.reservar_clase_card(n))
        # Filtros
        if hasattr(self, 'txtBuscarClases'):
            self.txtBuscarClases.textChanged.connect(ctrl.filtrar_clases)
        if hasattr(self, 'cmbTipo'):
            self.cmbTipo.currentIndexChanged.connect(ctrl.filtrar_clases)
        if hasattr(self, 'cmbHorario'):
            self.cmbHorario.currentIndexChanged.connect(ctrl.filtrar_clases)

    # — Cabecera —
    def set_nombre_cliente(self, v): self.lblNombreCliente.setText(v)
    def set_fecha_alta(self, v):     self.lblFechaAltaCliente.setText(v)

    def poblar_combo_tipo(self, nombres):
        self.cmbTipo.blockSignals(True)
        self.cmbTipo.clear()
        self.cmbTipo.addItems(['Todas las categorías'] + nombres)
        self.cmbTipo.blockSignals(False)

    def poblar_combo_horario(self, horarios):
        self.cmbHorario.blockSignals(True)
        self.cmbHorario.clear()
        self.cmbHorario.addItems(['Todos los horarios'] + horarios)
        self.cmbHorario.blockSignals(False)

    def set_periodo(self, texto):
        if hasattr(self, 'btnPeriodo'): 
            self.btnPeriodo.setText(texto)

    def cargar_cards(self, clases, ids_inscritas, asistidas):
        self._cards_clases = []
        for i, clase in enumerate(clases[:5], start=1):
            id_clase    = clase[0]
            nombre      = str(clase[1])
            dia         = clase[2]
            hora_inicio = str(clase[3])[:5]
            hora_fin    = str(clase[4])[:5]
            sala        = clase[5]
            inscritos   = clase[6]
            aforo       = clase[7]
            horario     = f'{hora_inicio} - {hora_fin}'

            lbl_c = getattr(self, self._LABELS_CLASE.get(i,''), None)
            lbl_d = getattr(self, self._LABELS_DESC.get(i,''), None)
            lbl_f = getattr(self, self._LABELS_FECHA.get(i,''), None)
            lbl_p = getattr(self, self._LABELS_PLAZAS.get(i,''), None)
            btn   = getattr(self, f'btnReservar{i}', None)
            card  = getattr(self, self._CARDS.get(i,''), None)

            if lbl_c: lbl_c.setText(nombre)
            if lbl_d: lbl_d.setText(_DESCRIPCIONES.get(nombre.strip().lower(), 'Clase disponible para reservar.'))
            if lbl_f: lbl_f.setText(f'{dia}\n{hora_inicio} - {hora_fin}\n{sala}')
            if lbl_p: lbl_p.setText(f'{inscritos} / {aforo}')
            if btn:
                if id_clase in asistidas:
                    btn.setText('Realizada'); btn.setEnabled(False)
                elif id_clase in ids_inscritas:
                    btn.setText('Cancelar'); btn.setEnabled(True)
                else:
                    btn.setText('Reservar'); btn.setEnabled(True)

            self._cards_clases.append({'card': card, 'nombre': nombre.lower(), 'horario': horario})

    def set_prox_datos(self, texto):
        if hasattr(self, 'lblProxDatos'): self.lblProxDatos.setText(texto)

    def get_texto_buscar(self):
        return self.txtBuscarClases.text().strip().lower() if hasattr(self, 'txtBuscarClases') else ''
    def get_filtro_tipo(self):
        return self.cmbTipo.currentText().strip().lower() if hasattr(self, 'cmbTipo') else 'todas las categorías'
    def get_filtro_horario(self):
        return self.cmbHorario.currentText().strip().lower() if hasattr(self, 'cmbHorario') else 'todos los horarios'
    def get_nombre_clase_card(self, n):
        lbl = getattr(self, self._LABELS_CLASE.get(n,''), None)
        return lbl.text().strip() if lbl else ''
    def get_accion_boton_card(self, n):
        btn = getattr(self, f'btnReservar{n}', None)
        return btn.text().strip().lower() if btn else 'reservar'

    def aplicar_filtro_cards(self, texto, tipo, horario):
        for item in self._cards_clases:
            card = item['card']
            if card is None:
                continue
            coincide_texto   = texto == '' or texto in item['nombre']
            coincide_tipo    = tipo == 'todas las categorías' or tipo == item['nombre']
            coincide_horario = horario == 'todos los horarios' or horario == item['horario'].lower()
            card.setVisible(coincide_texto and coincide_tipo and coincide_horario)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'Reserva', msg)


# ── Vista reservas ────────────────────────────────────────────────────────────

class VistaClienteReservas(QMainWindow):

    _CARDS         = {1:'cardReserva1',    2:'cardReserva2',    3:'cardReserva3',    4:'cardReserva4'}
    _LABELS_CLASE  = {1:'lblReservaClase1',2:'lblReservaClase2',3:'lblReservaClase3',4:'lblReservaClase4'}
    _LABELS_DESC   = {1:'lblReservaDesc1', 2:'lblReservaDesc2', 3:'lblReservaDesc3', 4:'lblReservaDesc4'}
    _LABELS_FECHA  = {1:'lblReservaFecha1',2:'lblReservaFecha2',3:'lblReservaFecha3',4:'lblReservaFecha4'}
    _LABELS_PLAZAS = {1:'lblPlazasReserva1',2:'lblPlazasReserva2',3:'lblPlazasReserva3',4:'lblPlazasReserva4'}
    _LABELS_ESTADO = {1:'lblEstadoReserva1',2:'lblEstadoReserva2',3:'lblEstadoReserva3',4:'lblEstadoReserva4'}

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_cliente(self, ctrl)
        if hasattr(self, 'lblTabTodas'):
            self.lblTabTodas.mousePressEvent = lambda e: ctrl.ir_clases()
        if hasattr(self, 'lblTabRes'):
            self.lblTabRes.mousePressEvent = lambda e: ctrl.ir_reservas()

    def set_nombre_cliente(self, v): self.lblNombreCliente.setText(v)
    def set_fecha_alta(self, v):     self.lblFechaAltaCliente.setText(v)

    def cargar_cards(self, reservas, ocupacion_por_nombre):
        # Ocultar todas primero
        for i in range(1, 5):
            card = getattr(self, self._CARDS.get(i,''), None)
            if card: card.setVisible(False)

        for i, reserva in enumerate(reservas[:4], start=1):
            nombre      = reserva.get('nombre_actividad', '')
            dia         = reserva.get('fecha', '')
            hora_inicio = str(reserva.get('hora_inicio', ''))[:5]
            sala        = reserva.get('nombre_sala', '')
            ins, afo    = ocupacion_por_nombre.get(str(nombre).lower(), (0, 0))

            card    = getattr(self, self._CARDS.get(i,''), None)
            lbl_c   = getattr(self, self._LABELS_CLASE.get(i,''), None)
            lbl_d   = getattr(self, self._LABELS_DESC.get(i,''), None)
            lbl_f   = getattr(self, self._LABELS_FECHA.get(i,''), None)
            lbl_p   = getattr(self, self._LABELS_PLAZAS.get(i,''), None)
            lbl_e   = getattr(self, self._LABELS_ESTADO.get(i,''), None)

            if card:  card.setVisible(True)
            if lbl_c: lbl_c.setText(str(nombre))
            if lbl_d: lbl_d.setText(_DESCRIPCIONES.get(str(nombre).strip().lower(), 'Clase reservada.'))
            if lbl_f: lbl_f.setText(f'{dia}\n{hora_inicio}\n{sala}')
            if lbl_p: lbl_p.setText(f'Plazas: {ins} / {afo}')
            if lbl_e: lbl_e.setText('Reserva confirmada')

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)


# ── Vista estadísticas ────────────────────────────────────────────────────────

class VistaClienteEstadisticas(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_cliente(self, ctrl)

    def set_nombre_cliente(self, v): self.lblNombreCliente.setText(v)
    def set_fecha_alta(self, v):     self.lblFechaAltaCliente.setText(v)

    def set_entrenos(self, num, sub):
        if hasattr(self, 'lblNumEntrenos'):  self.lblNumEntrenos.setText(num)
        if hasattr(self, 'lblSubEntrenos'):  self.lblSubEntrenos.setText(sub)
    def set_tiempo(self, num, sub):
        if hasattr(self, 'lblNumTiempo'):    self.lblNumTiempo.setText(num)
        if hasattr(self, 'lblSubTiempo'):    self.lblSubTiempo.setText(sub)
    def set_calorias(self, v):
        if hasattr(self, 'lblNumCalorias'):  self.lblNumCalorias.setText(v)
    def set_objetivo(self, pct, texto):
        if hasattr(self, 'lblNumObjetivo'):  self.lblNumObjetivo.setText(pct)
        if hasattr(self, 'lblTextoObjetivo'):self.lblTextoObjetivo.setText(texto)
    def set_mini(self, v):
        if hasattr(self, 'btnMini'):         self.btnMini.setText(v)
    def set_racha(self, dias):
        if hasattr(self, 'lblNumEntrenos_2'):self.lblNumEntrenos_2.setText(str(dias))
        if hasattr(self, 'lblSigueRacha'):   self.lblSigueRacha.setText(f'Llevas {dias} días consecutivos entrenando.')
    def set_total_calorias(self, v):
        if hasattr(self, 'lblTotalCalorias'):self.lblTotalCalorias.setText(v)
    def set_dias_label(self, v):
        if hasattr(self, 'dias'): self.dias.setText(v)

    def actualizar_barras(self, calorias_dias):
        barras = {
            'lunes':    getattr(self, 'barLun', None),
            'martes':   getattr(self, 'barMar', None),
            'miercoles':getattr(self, 'barMie', None),
            'jueves':   getattr(self, 'barJue', None),
            'viernes':  getattr(self, 'barVie', None),
            'sabado':   getattr(self, 'barSab', None),
            'domingo':  getattr(self, 'barDom', None),
        }
        

        max_kcal = 400
        altura_maxima = 80
        
        for dia, barra in barras.items():
            if barra:
                kcal = calorias_dias.get(dia, 0)
                altura = int((kcal / max_kcal) * altura_maxima)
                if kcal == 0: altura = 0
                elif altura < 8: altura = 8
                geo = barra.geometry()
                bottom = geo.y() + geo.height()
                barra.setGeometry(geo.x(), bottom - altura, geo.width(), altura)

    def set_leyendas_distribucion(self, distribucion):
        labels = [getattr(self, f'lblLeyenda{i}', None) for i in range(1, 5)]
        items = list(distribucion.items()) if isinstance(distribucion, dict) else []
        for i, lbl in enumerate(labels):
            if lbl is None: continue
            if i < len(items):
                tipo, pct = items[i]
                lbl.setText(f'● {tipo} {pct}%')
            else:
                lbl.setText('')

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)


# ── Vista perfil ──────────────────────────────────────────────────────────────

class VistaClientePerfil(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_cliente(self, ctrl)
        if hasattr(self, 'btnGuardarCambios'):
            self.btnGuardarCambios.clicked.connect(ctrl.guardar_perfil)

    def set_nombre_cliente(self, v): self.lblNombreCliente.setText(v)
    def set_fecha_alta(self, v):     self.lblFechaAltaCliente.setText(v)

    def set_perfil(self, nombre, email, telefono, fecha_nac, direccion, asistencias_str):
        if hasattr(self, 'lblNombreCompleto'):    self.lblNombreCompleto.setText(nombre)
        if hasattr(self, 'lblEmailPerfil'):       self.lblEmailPerfil.setText(email)
        if hasattr(self, 'txtNombre'):            self.txtNombre.setText(nombre)
        if hasattr(self, 'lblNumTelefono'):       self.lblNumTelefono.setText(telefono)
        if hasattr(self, 'lblCorreoElectronico'): self.lblCorreoElectronico.setText(email)
        if hasattr(self, 'lblFechaNacimiento'):   self.lblFechaNacimiento.setText(fecha_nac)
        if hasattr(self, 'lblDireccion'):         self.lblDireccion.setText(direccion)
        if hasattr(self, 'lblAsistenciasValor'):  self.lblAsistenciasValor.setText(asistencias_str)

    def set_objetivo(self, pct_texto):
        if hasattr(self, 'lblPorcentaje'): self.lblPorcentaje.setText(pct_texto)

    def set_barra_progreso(self, porcentaje):
        if hasattr(self, 'barraProgresoValor') and hasattr(self, 'barraProgresoFondo'):
            ancho = self.barraProgresoFondo.width()
            self.barraProgresoValor.setFixedWidth(int(ancho * porcentaje / 100))

    def get_telefono(self):  return self.txtTelefono.text().strip() if hasattr(self, 'txtTelefono') else ''
    def get_email(self):     return self.txtEmail.text().strip() if hasattr(self, 'txtEmail') else ''
    def get_direccion(self): return self.txtDireccion.text().strip() if hasattr(self, 'txtDireccion') else ''

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'Perfil actualizado', msg)


# ── Vista información ─────────────────────────────────────────────────────────

class VistaClienteInformacion(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_cliente(self, ctrl)

    def set_nombre_cliente(self, v): self.lblNombreCliente.setText(v)
    def set_fecha_alta(self, v):     self.lblFechaAltaCliente.setText(v)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)