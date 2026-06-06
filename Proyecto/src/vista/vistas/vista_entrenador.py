"""
Vistas del rol Entrenador — Patrón MVC según ejemplo de la profesora.

La Vista:
- Carga el .ui en __init__
- Conecta sus botones en set_controlador()
- Expone métodos set_xxx() / get_xxx() para el controlador
- Nunca contiene lógica de negocio
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi


# ── Helper menú lateral ───────────────────────────────────────────────────────

def _menu_entrenador(v, ctrl):
    v.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
    # btnInicio puede llamarse btnInicio o btnInicio_2 según la pantalla
    if hasattr(v, 'btnInicio'):    v.btnInicio.clicked.connect(ctrl.ir_inicio)
    if hasattr(v, 'btnInicio_2'):  v.btnInicio_2.clicked.connect(ctrl.ir_inicio)
    # btnClases puede llamarse btnClases o btnClases_2
    if hasattr(v, 'btnClases'):    v.btnClases.clicked.connect(ctrl.ir_clases)
    if hasattr(v, 'btnClases_2'):  v.btnClases_2.clicked.connect(ctrl.ir_clases)
    if hasattr(v, 'btnInscritos'):         v.btnInscritos.clicked.connect(ctrl.ir_inscritos)
    if hasattr(v, 'btnOcupacion'):         v.btnOcupacion.clicked.connect(ctrl.ir_ocupacion)
    if hasattr(v, 'btnRegistroAsistencia'):v.btnRegistroAsistencia.clicked.connect(ctrl.ir_asistencia)
    if hasattr(v, 'btnPerfil'):            v.btnPerfil.clicked.connect(ctrl.ir_perfil)
    if hasattr(v, 'btnInformacion'):       v.btnInformacion.clicked.connect(ctrl.ir_informacion)


def _rellenar(tabla, cabeceras, datos):
    tabla.clear()
    tabla.setColumnCount(len(cabeceras))
    tabla.setHorizontalHeaderLabels(cabeceras)
    tabla.setRowCount(len(datos))
    for fi, fila in enumerate(datos):
        for ci, val in enumerate(list(fila)[:len(cabeceras)]):
            tabla.setItem(fi, ci, QTableWidgetItem(str(val) if val is not None else ''))


# ── Vista inicio ──────────────────────────────────────────────────────────────

class VistaEntrenadorInicio(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_entrenador(self, ctrl)

    def cargar_tabla_proximas(self, datos):
        _rellenar(self.tablaProximasClasesEntrenador,
                  ['Clase', 'Sala', 'Horario', 'Día', 'Capacidad'], datos)
        self.tablaProximasClasesEntrenador.verticalHeader().setVisible(False)

    def set_num_clases_hoy(self, v):
        if hasattr(self, 'labelNumClases'): self.labelNumClases.setText(v)

    def set_num_asistencias(self, v):
        if hasattr(self, 'labelNumAsistencias'): self.labelNumAsistencias.setText(v)

    def set_ocupacion_media(self, v):
        if hasattr(self, 'lblPorcentajeOcupacion'): self.lblPorcentajeOcupacion.setText(v)

    def set_proxima_clase(self, nombre, hora, sala):
        if hasattr(self, 'labelClase'): self.labelClase.setText(nombre)
        if hasattr(self, 'labelHora'):  self.labelHora.setText(hora)
        if hasattr(self, 'labelSala'):  self.labelSala.setText(sala)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)


# ── Vista mis clases ──────────────────────────────────────────────────────────

class VistaEntrenadorClases(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_entrenador(self, ctrl)

    def cargar_tabla(self, datos):
        _rellenar(self.tablaMisClases,
                  ['Clase', 'Sala', 'Horario', 'Día', 'Capacidad'], datos)
        self.tablaMisClases.verticalHeader().setVisible(False)

    def set_total_clases(self, v):
        if hasattr(self, 'labelTotalClasesAsignadas'): self.labelTotalClasesAsignadas.setText(v)

    def set_clases_hoy(self, v):
        if hasattr(self, 'labelClasesHoy'): self.labelClasesHoy.setText(v)

    def set_ocupacion_media(self, v):
        if hasattr(self, 'lblPorcentajeOcupacionClase'): self.lblPorcentajeOcupacionClase.setText(v)

    def set_proxima_clase(self, nombre, dia_hora):
        if hasattr(self, 'labelProximaClase'): self.labelProximaClase.setText(nombre)
        if hasattr(self, 'lblHoraProxClase'):  self.lblHoraProxClase.setText(dia_hora)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)


# ── Vista lista inscritos ─────────────────────────────────────────────────────

class VistaEntrenadorListaClientes(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_entrenador(self, ctrl)
        self.comboClasesInscritos.currentIndexChanged.connect(ctrl.cargar_clientes_inscritos)

    def poblar_combo_clases(self, clases):
        self.comboClasesInscritos.blockSignals(True)
        self.comboClasesInscritos.clear()
        for clase in clases:
            self.comboClasesInscritos.addItem(str(clase[1]), clase[0])
        self.comboClasesInscritos.blockSignals(False)

    def get_id_clase_seleccionada(self):
        return self.comboClasesInscritos.currentData()

    def cargar_tabla_inscritos(self, datos):
        _rellenar(self.tablaInscritos, ['Cliente', 'Teléfono', 'Email'], datos)

    def set_num_inscritos(self, v):
        if hasattr(self, 'label_numInscritos_ins'): self.label_numInscritos_ins.setText(v)
        if hasattr(self, 'label_total_inscritos'):  self.label_total_inscritos.setText(v)

    def set_info_clase(self, nombre, sala, dia, horario):
        if hasattr(self, 'label_nombreclase_ins'): self.label_nombreclase_ins.setText(nombre)
        if hasattr(self, 'lblSalaClase_ins'):       self.lblSalaClase_ins.setText(sala)
        if hasattr(self, 'label_fecha_ins'):        self.label_fecha_ins.setText(dia)
        if hasattr(self, 'lblHorarioClase_ins'):    self.lblHorarioClase_ins.setText(horario)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)


# ── Vista ocupación ───────────────────────────────────────────────────────────

class VistaEntrenadorOcupacion(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_entrenador(self, ctrl)

    def cargar_tabla(self, datos):
        _rellenar(self.tablaOcupacionClases,
                  ['ID', 'Clase', 'Inscritos', 'Aforo', 'Ocupación %'], datos)

    def set_resumen(self, clases_llenas, ocupacion_media,
                    nombre_mas_llena, inscritos_aforo, plazas_libres):
        if hasattr(self, 'label_Num_Clases'):           self.label_Num_Clases.setText(str(clases_llenas))
        if hasattr(self, 'label_Porcentaje_Ocupacion'):  self.label_Porcentaje_Ocupacion.setText(ocupacion_media)
        if hasattr(self, 'label_Porcentaje_Ocupacion_2'):self.label_Porcentaje_Ocupacion_2.setText(ocupacion_media)
        if hasattr(self, 'label_Clase_masLlena'):        self.label_Clase_masLlena.setText(nombre_mas_llena)
        if hasattr(self, 'label_inscritos'):             self.label_inscritos.setText(inscritos_aforo)
        if hasattr(self, 'label_plazasLibres'):          self.label_plazasLibres.setText(str(plazas_libres))

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)


# ── Vista registrar asistencia ────────────────────────────────────────────────

class VistaEntrenadorRegistrarAsistencia(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_entrenador(self, ctrl)
        self.comboSeleccionarClase.currentIndexChanged.connect(ctrl.cargar_inscritos_asistencia)
        self.pushButton_GuardarAsist.clicked.connect(ctrl.guardar_asistencia)

    def poblar_combo_clases(self, clases):
        self.comboSeleccionarClase.blockSignals(True)
        self.comboSeleccionarClase.clear()
        for clase in clases:
            self.comboSeleccionarClase.addItem(
                f"{clase[1]} - {clase[2]} {clase[3]} - {clase[4]}", clase[0]
            )
        self.comboSeleccionarClase.blockSignals(False)

    def get_id_clase_seleccionada(self):
        return self.comboSeleccionarClase.currentData()

    def cargar_tabla_asistencia(self, datos, mapa_asistencia):
        tabla = self.tablaInscritosAsistencia
        tabla.clear()
        tabla.setRowCount(len(datos))
        tabla.setColumnCount(3)
        tabla.setHorizontalHeaderLabels(['Cliente', 'Estado', 'Acción'])
        for fi, cliente in enumerate(datos):
            id_c, nombre = cliente[0], cliente[1]
            estado = mapa_asistencia.get(id_c, 'pendiente')
            estado_str = 'si' if estado == 'si' else ('no' if estado == 'no' else 'Pendiente')
            tabla.setItem(fi, 0, QTableWidgetItem(f'{id_c} - {nombre}'))
            tabla.setItem(fi, 1, QTableWidgetItem(estado_str))
            tabla.setItem(fi, 2, QTableWidgetItem('Escribe si o no'))

    def get_datos_asistencia(self):
        tabla = self.tablaInscritosAsistencia
        filas = []
        for fi in range(tabla.rowCount()):
            item_c = tabla.item(fi, 0)
            item_e = tabla.item(fi, 1)
            if item_c and item_e:
                filas.append((item_c.text(), item_e.text().strip().lower()))
        return filas

    def set_resumen_asistencia(self, total, presentes, ausentes, pendientes):
        if hasattr(self, 'label_TotalInscritos'): self.label_TotalInscritos.setText(str(total))
        if hasattr(self, 'label_numInscritos'):   self.label_numInscritos.setText(str(total))
        if hasattr(self, 'label_numAsist'):       self.label_numAsist.setText(str(presentes))
        if hasattr(self, 'label_numAus'):         self.label_numAus.setText(str(ausentes))
        if hasattr(self, 'label_numPend'):        self.label_numPend.setText(str(pendientes))

    def set_info_clase(self, nombre, dia, horario, sala):
        if hasattr(self, 'label_nombreclase'): self.label_nombreclase.setText(nombre)
        if hasattr(self, 'label_fecha'):       self.label_fecha.setText(dia)
        if hasattr(self, 'lblHorarioClase'):   self.lblHorarioClase.setText(horario)
        if hasattr(self, 'lblSalaClase'):      self.lblSalaClase.setText(sala)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'Correcto', msg)


# ── Vista perfil ──────────────────────────────────────────────────────────────

class VistaEntrenadorPerfil(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_entrenador(self, ctrl)

    def set_perfil_info(self, nombre, email, telefono, direccion, fecha_alta):
        if hasattr(self, 'label_Nombre'):               self.label_Nombre.setText(nombre)
        if hasattr(self, 'labelCorreoEntrenador'):      self.labelCorreoEntrenador.setText(email)
        if hasattr(self, 'labelTelefonoEntrenador'):    self.labelTelefonoEntrenador.setText(telefono)
        if hasattr(self, 'labelDireccionEntrenador'):   self.labelDireccionEntrenador.setText(direccion)
        if hasattr(self, 'labelFechaAltaEntrenadorPerfil'): self.labelFechaAltaEntrenadorPerfil.setText(fecha_alta)

    def set_stats(self, clases_semana, clases_hoy, total_clientes, pct_asistencia):
        if hasattr(self, 'label_Num_Clases_semana'):   self.label_Num_Clases_semana.setText(str(clases_semana))
        if hasattr(self, 'label_Num_Clases_Hoy'):      self.label_Num_Clases_Hoy.setText(str(clases_hoy))
        if hasattr(self, 'label_Num_Clientes_Total'):  self.label_Num_Clientes_Total.setText(str(total_clientes))
        if hasattr(self, 'label_Porcentaje_Asistencia'): self.label_Porcentaje_Asistencia.setText(pct_asistencia)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)


# ── Vista información ─────────────────────────────────────────────────────────

class VistaEntrenadorInformacion(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_entrenador(self, ctrl)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)