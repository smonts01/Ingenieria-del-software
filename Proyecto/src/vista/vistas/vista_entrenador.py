from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
# QMainWindow: clase base de las ventanas.
# QTableWidgetItem: permite insertar texto en celdas de tablas.
# QMessageBox: muestra ventanas emergentes de error o éxito.

from PyQt5.uic import loadUi

#Carga el .ui en __init_
#Conecta sus botones en set_controlador()
#Expone métodos set_() y get_() para el controlador




# Conecta los botones comunes del menú lateral con los métodos del controlador.
# Se usa en todas las pantallas del entrenador 
# v = vista actual
# ctrl = controlador del entrenador
def _menu_entrenador(v, ctrl):
    v.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
    
    if hasattr(v, 'btnInicio'):    
        v.btnInicio.clicked.connect(ctrl.ir_inicio)
    if hasattr(v, 'btnInicio_2'):  
        v.btnInicio_2.clicked.connect(ctrl.ir_inicio)

    if hasattr(v, 'btnClases'):    
        v.btnClases.clicked.connect(ctrl.ir_clases)
    if hasattr(v, 'btnClases_2'):  
        v.btnClases_2.clicked.connect(ctrl.ir_clases)

    if hasattr(v, 'btnInscritos'):         
        v.btnInscritos.clicked.connect(ctrl.ir_inscritos)
    if hasattr(v, 'btnOcupacion'):         
        v.btnOcupacion.clicked.connect(ctrl.ir_ocupacion)
    if hasattr(v, 'btnRegistroAsistencia'):
        v.btnRegistroAsistencia.clicked.connect(ctrl.ir_asistencia)
    if hasattr(v, 'btnPerfil'):            
        v.btnPerfil.clicked.connect(ctrl.ir_perfil)
    if hasattr(v, 'btnInformacion'):
        v.btnInformacion.clicked.connect(ctrl.ir_informacion)


#Convierte un VO o una tupla/lista en una lista de valores.
def _vo_a_lista(vo, n):

    if isinstance(vo, (list, tuple)):
        return list(vo)[:n]
    props = [v for k, v in type(vo).__dict__.items() if isinstance(v, property) and not k.startswith('_')]
    
    return [str(getattr(vo, p.fget.__name__, '')) for p in props[:n]]




# Rellena una tabla de PyQt con cabeceras y datos.
# tabla = QTableWidget que se va a rellenar
# cabeceras = nombres de las columnas
# datos = filas recibidas desde el controlador

def _rellenar(tabla, cabeceras, datos):
    tabla.clear()
    tabla.setColumnCount(len(cabeceras))
    tabla.setHorizontalHeaderLabels(cabeceras)
    tabla.setRowCount(len(datos))
    for fi, fila in enumerate(datos):
        vals = _vo_a_lista(fila, len(cabeceras))
        for ci, val in enumerate(vals):
            tabla.setItem(fi, ci, QTableWidgetItem(str(val) if val is not None else ''))


# VISTA INICIO
class VistaEntrenadorInicio(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()        # Inicializa la ventana
        loadUi(ruta_ui, self)     # Carga el ui 
        self.controlador = None   # Se rellena después en set_controlador()

    def set_controlador(self, ctrl):
        self.controlador = ctrl # Guarda el controlador para poder llamarlo
        _menu_entrenador(self, ctrl) # Conectar botones del menú lateral

    
    # Rellena la tabla de próximas clases con los datos que le pasa el controlador.
    def cargar_tabla_proximas(self, datos):
        _rellenar(self.tablaProximasClasesEntrenador, ['Clase', 'Sala', 'Horario', 'Día', 'Capacidad'], datos)
        self.tablaProximasClasesEntrenador.verticalHeader().setVisible(False)

    # Métodos set_xxx para actualizar textos de la pantalla en los labels
    def set_num_clases_hoy(self, v):
        if hasattr(self, 'labelNumClases'): 
            self.labelNumClases.setText(v)

    def set_num_asistencias(self, v):
        if hasattr(self, 'labelNumAsistencias'): 
            self.labelNumAsistencias.setText(v)

    def set_ocupacion_media(self, v):
        if hasattr(self, 'lblPorcentajeOcupacion'): 
            self.lblPorcentajeOcupacion.setText(v)

    def set_proxima_clase(self, nombre, hora, sala):
        if hasattr(self, 'labelClase'): 
            self.labelClase.setText(nombre)
        
        if hasattr(self, 'labelHora'):  
            self.labelHora.setText(hora)
        
        if hasattr(self, 'labelSala'):  
            self.labelSala.setText(sala)

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)


# VISTA MIS CLASES
class VistaEntrenadorClases(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_entrenador(self, ctrl)

    def cargar_tabla(self, datos):
        # Rellena la tabla principal con las clases asignadas al entrenador.
        _rellenar(self.tablaMisClases, ['Clase', 'Sala', 'Horario', 'Día', 'Capacidad'], datos)
        self.tablaMisClases.verticalHeader().setVisible(False)

    def set_total_clases(self, v):
        if hasattr(self, 'labelTotalClasesAsignadas'): 
            self.labelTotalClasesAsignadas.setText(v)

    def set_clases_hoy(self, v):
        if hasattr(self, 'labelClasesHoy'): 
            self.labelClasesHoy.setText(v)

    def set_ocupacion_media(self, v):
        if hasattr(self, 'lblPorcentajeOcupacionClase'): 
            self.lblPorcentajeOcupacionClase.setText(v)

    def set_proxima_clase(self, nombre, dia_hora):
        if hasattr(self, 'labelProximaClase'): 
            self.labelProximaClase.setText(nombre)
        if hasattr(self, 'lblHoraProxClase'):  
            self.lblHoraProxClase.setText(dia_hora)

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)



# Vista de alumnos inscritos
# Permite seleccionar una clase y ver los clientes inscritos en ella

class VistaEntrenadorListaClientes(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_entrenador(self, ctrl)

        # Cuando cambia la clase seleccionada en el combo,
        # se avisa al controlador para cargar los clientes inscritos.
        self.comboClasesInscritos.currentIndexChanged.connect(ctrl.cargar_clientes_inscritos)

    def poblar_combo_clases(self, clases):
        self.comboClasesInscritos.blockSignals(True)

        self.comboClasesInscritos.clear()# Limpia opciones anteriores

        for clase in clases:
            self.comboClasesInscritos.addItem(str(clase.nombre_actividad), clase.id_clase)
        self.comboClasesInscritos.blockSignals(False)

    def get_id_clase_seleccionada(self):
        # Devuelve el id_clase guardado como dato oculto en el combo
        return self.comboClasesInscritos.currentData()

    def cargar_tabla_inscritos(self, datos):
        # Rellena la tabla con los clientes inscritos en la clase seleccionada
        cabeceras = ['Cliente', 'Teléfono', 'Email']
        tabla = self.tablaInscritos


        tabla.clear()
        tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras)
        tabla.setRowCount(len(datos))

        for fi, vo in enumerate(datos):
            # Cada vo representa un cliente inscrito.
            for ci, val in enumerate([vo.nombre, vo.telefono, vo.email]):
                tabla.setItem(fi, ci, QTableWidgetItem(str(val) if val is not None else ''))

    def set_num_inscritos(self, v):
        if hasattr(self, 'label_numInscritos_ins'): 
            self.label_numInscritos_ins.setText(v)
        if hasattr(self, 'label_total_inscritos'):  
            self.label_total_inscritos.setText(v)

    def set_info_clase(self, nombre, sala, dia, horario):
        if hasattr(self, 'label_nombreclase_ins'): 
            self.label_nombreclase_ins.setText(nombre)
        if hasattr(self, 'lblSalaClase_ins'):       
            self.lblSalaClase_ins.setText(sala)
        if hasattr(self, 'label_fecha_ins'):        
            self.label_fecha_ins.setText(dia)
        if hasattr(self, 'lblHorarioClase_ins'):    
            self.lblHorarioClase_ins.setText(horario)

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)


#  VISTA OCUPACIÓN

class VistaEntrenadorOcupacion(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_entrenador(self, ctrl)

    def cargar_tabla(self, datos):
        # Rellena la tabla con los datos de ocupación de cada clase
        _rellenar(self.tablaOcupacionClases, ['ID', 'Clase', 'Inscritos', 'Aforo', 'Ocupación %'], datos)

    def set_resumen(self, clases_llenas, ocupacion_media, nombre_mas_llena, inscritos_aforo, plazas_libres):
        
        if hasattr(self, 'label_Num_Clases'):           
            self.label_Num_Clases.setText(str(clases_llenas))
        if hasattr(self, 'label_Porcentaje_Ocupacion'):  
            self.label_Porcentaje_Ocupacion.setText(ocupacion_media)
        if hasattr(self, 'label_Porcentaje_Ocupacion_2'):
            self.label_Porcentaje_Ocupacion_2.setText(ocupacion_media)
        if hasattr(self, 'label_Clase_masLlena'):        
            self.label_Clase_masLlena.setText(nombre_mas_llena)
        if hasattr(self, 'label_inscritos'):             
            self.label_inscritos.setText(inscritos_aforo)
        if hasattr(self, 'label_plazasLibres'):          
            self.label_plazasLibres.setText(str(plazas_libres))

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)


# VISTA REGISTRAR ASISTENCIA
# Vista para registrar asistencia.
# Permite elegir una clase, ver sus alumnos y escribir si asistieron o no

class VistaEntrenadorRegistrarAsistencia(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_entrenador(self, ctrl)

        # Si cambia la clase seleccionada, el controlador recarga la tabla de asistencia
        self.comboSeleccionarClase.currentIndexChanged.connect(ctrl.cargar_inscritos_asistencia)

        # Al pulsar guardar, el controlador lee la tabla y guarda la asistencia.
        self.pushButton_GuardarAsist.clicked.connect(ctrl.guardar_asistencia)

    
    
    def poblar_combo_clases(self, clases):
        self.comboSeleccionarClase.blockSignals(True)

        self.comboSeleccionarClase.clear()

        for clase in clases:
            self.comboSeleccionarClase.addItem(f"{clase.nombre_actividad} - {clase.dia_semana} {clase.hora_inicio} - {clase.hora_fin}", clase.id_clase)


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
            id_c, nombre = cliente.id_cliente, cliente.nombre

            # Busca si ese cliente ya tiene asistencia registrada.
            # Si no aparece, se marca como pendiente.
            estado = mapa_asistencia.get(id_c, 'pendiente')

            # Convierte el estado a texto visible en la tabla
            estado_str = 'si' if estado == 'si' else ('no' if estado == 'no' else 'Pendiente')

            # Columna 0: ID y nombre del cliente.
            tabla.setItem(fi, 0, QTableWidgetItem(f'{id_c} - {nombre}'))

            # Columna 1: estado editable por el usuario.
            tabla.setItem(fi, 1, QTableWidgetItem(estado_str))

            # Columna 2: indicación para el usuario.
            tabla.setItem(fi, 2, QTableWidgetItem('Escribe si o no'))

    def get_datos_asistencia(self):
        # Lee la tabla de asistencia y devuelve una lista de tuplas
        tabla = self.tablaInscritosAsistencia
        filas = []
        for fi in range(tabla.rowCount()):
            item_c = tabla.item(fi, 0) # Cliente
            item_e = tabla.item(fi, 1) # Estado escrito

            if item_c and item_e:
                filas.append((item_c.text(), item_e.text().strip().lower()))

        return filas

    def set_resumen_asistencia(self, total, presentes, ausentes, pendientes):
        
        if hasattr(self, 'label_TotalInscritos'): 
            self.label_TotalInscritos.setText(str(total))
        if hasattr(self, 'label_numInscritos'):   
            self.label_numInscritos.setText(str(total))
        if hasattr(self, 'label_numAsist'):       
            self.label_numAsist.setText(str(presentes))
        if hasattr(self, 'label_numAus'):         
            self.label_numAus.setText(str(ausentes))
        if hasattr(self, 'label_numPend'):        
            self.label_numPend.setText(str(pendientes))

    def set_info_clase(self, nombre, dia, horario, sala):
        if hasattr(self, 'label_nombreclase'): self.label_nombreclase.setText(nombre)
        if hasattr(self, 'label_fecha'):       self.label_fecha.setText(dia)
        if hasattr(self, 'lblHorarioClase'):   self.lblHorarioClase.setText(horario)
        if hasattr(self, 'lblSalaClase'):      self.lblSalaClase.setText(sala)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'Correcto', msg)


# VISTA DEL PERFIL del entrenador

class VistaEntrenadorPerfil(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_entrenador(self, ctrl)

    def set_perfil_info(self, nombre, email, telefono, direccion, fecha_alta):
        # Actualiza los labels con los datos personales del entrenador
        if hasattr(self, 'label_Nombre'):               
            self.label_Nombre.setText(nombre)
        
        if hasattr(self, 'labelCorreoEntrenador'):      
            self.labelCorreoEntrenador.setText(email)
        
        if hasattr(self, 'labelTelefonoEntrenador'):    
            self.labelTelefonoEntrenador.setText(telefono)
        
        if hasattr(self, 'labelDireccionEntrenador'):   
            self.labelDireccionEntrenador.setText(direccion)
        
        if hasattr(self, 'labelFechaAltaEntrenadorPerfil'): 
            self.labelFechaAltaEntrenadorPerfil.setText(fecha_alta)

    def set_stats(self, clases_semana, clases_hoy, total_clientes, pct_asistencia):

        if hasattr(self, 'label_Num_Clases_semana'):   
            self.label_Num_Clases_semana.setText(str(clases_semana))
        
        if hasattr(self, 'label_Num_Clases_Hoy'):      
            self.label_Num_Clases_Hoy.setText(str(clases_hoy))
        
        if hasattr(self, 'label_Num_Clientes_Total'):  
            self.label_Num_Clientes_Total.setText(str(total_clientes))
        
        if hasattr(self, 'label_Porcentaje_Asistencia'): 
            self.label_Porcentaje_Asistencia.setText(pct_asistencia)

    def mostrar_error(self, msg): 
        QMessageBox.warning(self, 'Error', msg)


# VISTA DE INFORMACIÓN 

class VistaEntrenadorInformacion(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_entrenador(self, ctrl)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)