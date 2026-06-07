"""
Vistas del rol Administrador — Patrón MVC según ejemplo de la profesora.

Responsabilidad de la Vista:
- Cargar el .ui en __init__
- Conectar sus propios botones en set_controlador() una vez tiene la referencia
- Exponer métodos set_xxx() / get_xxx() para que el controlador
  actualice la UI o lea datos sin tocar widgets directamente
- Nunca contiene lógica de negocio
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QLineEdit, QMessageBox
from PyQt5.uic import loadUi
from src.vista.componentes import TablaView
import io
import matplotlib
import matplotlib.pyplot as plt
from src.vista.componentes import ImagenView

# ── Helpers internos ──────────────────────────────────────────────────────────

def _menu_admin(v, ctrl):
    """Conecta el menú lateral común a todas las vistas admin."""
    v.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
    v.btnInicio.clicked.connect(ctrl.ir_inicio)
    v.btnUsuarios.clicked.connect(ctrl.ir_usuarios_clientes)
    v.btnClases.clicked.connect(ctrl.ir_clases)
    v.btnInscripciones.clicked.connect(ctrl.ir_inscripciones)
    v.btnPagos.clicked.connect(ctrl.ir_pagos)
    v.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)


def _rellenar_tabla(tabla, cabeceras, datos, extractor=None, editables=None):
    TablaView.configurar_columnas(tabla, cabeceras)
    tabla.setRowCount(len(datos))
    tabla.setEditTriggers(tabla.DoubleClicked | tabla.SelectedClicked)
    tabla.setSelectionBehavior(tabla.SelectRows)
    no_edit = editables or set()
    for fi, fila in enumerate(datos):
        valores = extractor(fila) if extractor else (
            list(fila) if isinstance(fila, (list, tuple)) else [str(fila)]
        )
        for ci, val in enumerate(valores[:len(cabeceras)]):
            item = TablaView.crear_item(
                str(val) if val is not None else '',
                editable=(ci not in no_edit)
            )
            tabla.setItem(fi, ci, item)


def _ext_cliente(c):
    return [c.id_usuario, c.dni, c.nombre, c.telefono,
            c.email, c.username, c.estado_pagado,
            c.direccion, c.fecha_nacimiento]


def _ext_trabajador(t):
    return [t.id_usuario, t.dni, t.nombre, t.telefono,
            t.email, t.username, t.nombre_rol,
            t.direccion, t.fecha_nacimiento]


def _ext_clase(c):
    if hasattr(c, 'id_clase'):
        return [c.id_clase, c.nombre_actividad, c.dia_semana,
                c.hora_inicio, c.hora_fin, c.aforo_maximo, c.nivel_intensidad]
    return list(c)


def _ext_inscripcion(r):
    return [r.nombre_cliente, r.nombre_actividad,
            r.fecha_inscripcion, r.estado]


# ── Vista inicio ──────────────────────────────────────────────────────────────

class VistaAdminInicio(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_admin(self, ctrl)
        self.btnCrearBackup.clicked.connect(ctrl.crear_copia_seguridad)
        self.btnRestaurarBackup.clicked.connect(ctrl.restaurar_copia_seguridad)

    def set_num_usuarios(self, v):
        if hasattr(self, 'lblUsuariosNum'): self.lblUsuariosNum.setText(v)

    def set_num_clases(self, v):
        if hasattr(self, 'lblClasesNum'): self.lblClasesNum.setText(v)

    def set_clases_por_tipo(self, tipo, v):
        mapa = {'spinning': 'lblClasesNum_2', 'zumba': 'lblClasesNum_3',
                'yoga': 'lblClasesNum_4', 'pilates': 'lblClasesNum_5',
                'crossfit': 'lblClasesNum_6'}
        lbl = mapa.get(tipo)
        if lbl and hasattr(self, lbl): getattr(self, lbl).setText(v)

    def set_clientes_basico(self, v):
        if hasattr(self, 'clientesbasico'): self.clientesbasico.setText(v)

    def set_clientes_premium(self, v):
        if hasattr(self, 'ClientesPremium'): self.ClientesPremium.setText(v)

    def cargar_tabla_inscripciones(self, datos):
        _rellenar_tabla(self.tablaInscripciones,
                        ['Usuario', 'Clase', 'Fecha', 'Estado'],
                        datos, _ext_inscripcion)

    def cargar_tabla_pagos_pendientes(self, cabeceras, datos):
        _rellenar_tabla(self.tablaClientesPagosPendientes,
                        cabeceras, datos, editables={0, 1, 2, 3})

    def set_grafico(self, pixmap, w, h):
        if hasattr(self, 'graficoFake'):
            self.graficoFake.setPixmap(pixmap.scaled(w or 391, h or 231, 1))

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'Correcto', msg)
    def dibujar_grafico_ingresos(self, etiquetas, valores):
        try:
            matplotlib.use('Agg')

            fig, ax = plt.subplots(figsize=(4.0, 2.3), dpi=92)
            fig.patch.set_facecolor('#F8F9FA')
            ax.set_facecolor('#F8F9FA')
            colores = ['#00BFA5' if v == max(valores) else '#80CBC4' for v in valores]
            bars = ax.bar(etiquetas, valores, color=colores, width=0.55, edgecolor='white')
            ax.set_ylabel('€', fontsize=8)
            ax.set_title('Ingresos por mes', fontsize=9, fontweight='bold', color='#333')
            ax.tick_params(axis='x', labelsize=7)
            ax.tick_params(axis='y', labelsize=7)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            max_val = max(valores) if valores else 1
            for bar, val in zip(bars, valores):
                ax.text(bar.get_x() + bar.get_width()/2,
                        bar.get_height() + max_val*0.03,
                        f'{val:.0f}€', ha='center', va='bottom', fontsize=6.5)
            plt.tight_layout(pad=0.5)
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=92)
            plt.close(fig)
            buf.seek(0)
            pixmap = ImagenView.desde_bytes(buf.read())
            w = self.graficoFake.width() if hasattr(self, 'graficoFake') else 391
            h = self.graficoFake.height() if hasattr(self, 'graficoFake') else 231
            self.set_grafico(pixmap, w, h)
        except Exception as e:
            print('Error grafico vista:', e)


# ── Vista usuarios clientes ───────────────────────────────────────────────────

class VistaAdminUsuariosClientes(QMainWindow):

    CABECERAS = ['ID', 'DNI', 'Nombre', 'Teléfono', 'Email',
                 'Usuario', 'Estado pago', 'Dirección', 'Fecha nacimiento']

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_admin(self, ctrl)
        self.txtBuscarCliente.textChanged.connect(ctrl.filtrar_clientes)
        if hasattr(self, 'lblTabClientes'):
            self.lblTabClientes.mousePressEvent = lambda e: ctrl.ir_usuarios_clientes()
        if hasattr(self, 'lblTabTrabajadores'):
            self.lblTabTrabajadores.mousePressEvent = lambda e: ctrl.ir_usuarios_trabajadores()

    def get_texto_buscar(self): return self.txtBuscarCliente.text().strip()

    def set_num_usuarios(self, v):
        if hasattr(self, 'lblNumUsuarios'): self.lblNumUsuarios.setText(v)

    def cargar_tabla(self, datos):
        _rellenar_tabla(self.tablaClientes_2, self.CABECERAS, datos, _ext_cliente)

    def set_texto_mostrando(self, texto):
        if hasattr(self, 'lblMostrando_2'): self.lblMostrando_2.setText(texto)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'Correcto', msg)


# ── Vista usuarios trabajadores ───────────────────────────────────────────────

class VistaAdminUsuariosTrabajadores(QMainWindow):

    CABECERAS = ['ID', 'DNI', 'Nombre', 'Teléfono', 'Email',
                 'Usuario', 'Rol', 'Dirección', 'Fecha nacimiento']

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_admin(self, ctrl)
        self.txtBuscarTrabajador.textChanged.connect(ctrl.filtrar_trabajadores)
        self.cmbRoles.currentIndexChanged.connect(ctrl.filtrar_por_rol)
        self.btnNuevoTrabajador.clicked.connect(ctrl.ir_nuevo_usuario)
        if hasattr(self, 'btnGuardarCambios_2'):
            self.btnGuardarCambios_2.clicked.connect(ctrl.guardar_cambios_trabajador)
        if hasattr(self, 'lblTabClientes'):
            self.lblTabClientes.mousePressEvent = lambda e: ctrl.ir_usuarios_clientes()
        if hasattr(self, 'lblTabTrabajadores'):
            self.lblTabTrabajadores.mousePressEvent = lambda e: ctrl.ir_usuarios_trabajadores()
        if self.cmbRoles.count() == 0:
            self.cmbRoles.addItems(['Todos los roles', 'entrenador',
                                    'recepcionista', 'contable', 'administrador'])

    def get_texto_buscar(self): return self.txtBuscarTrabajador.text().strip()
    def get_rol_filtro(self):   return self.cmbRoles.currentText()

    def set_resumen(self, total, entrenadores, recepcionistas, contables, administradores):
        if hasattr(self, 'lblNumTrabajadores'): self.lblNumTrabajadores.setText(str(total))
        if hasattr(self, 'Entrenadores'):       self.Entrenadores.setText(str(entrenadores))
        if hasattr(self, 'Recepcionista'):      self.Recepcionista.setText(str(recepcionistas))
        if hasattr(self, 'Contables'):          self.Contables.setText(str(contables))
        if hasattr(self, 'Administradores'):    self.Administradores.setText(str(administradores))

    def cargar_tabla(self, datos):
        _rellenar_tabla(self.tablaTrabajadores_2, self.CABECERAS,
                        datos, _ext_trabajador, editables={0, 6})

    def get_datos_tabla(self):
        tabla = self.tablaTrabajadores_2
        return [
            [tabla.item(fi, ci).text() if tabla.item(fi, ci) else ''
             for ci in range(tabla.columnCount())]
            for fi in range(tabla.rowCount())
        ]

    def set_texto_mostrando(self, texto):
        if hasattr(self, 'lblMostrando_2'): self.lblMostrando_2.setText(texto)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'Correcto', msg)


# ── Vista nuevo usuario ───────────────────────────────────────────────────────

class VistaAdminNuevoUsuario(QMainWindow):

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None
        if self.cmbRolUsuario.count() == 0:
            self.cmbRolUsuario.addItems(
                ['Cliente', 'Entrenador', 'Recepcionista', 'Administrador', 'Contable']
            )

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_admin(self, ctrl)
        self.btnRegistrarUsuario.clicked.connect(ctrl.registrar_usuario)

    def get_dni(self):       return self.txtDni.text().strip()
    def get_nombre(self):    return self.txtNombre.text().strip()
    def get_telefono(self):  return self.txtTelefono.text().strip()
    def get_email(self):     return self.txtEmail.text().strip()
    def get_direccion(self): return self.txtDireccion.text().strip()
    def get_fecha(self):     return self.txtFechaNacimiento.text().strip()
    def get_username(self):  return self.txtUsuario.text().strip()
    def get_password(self):  return self.txtPassword.text().strip()
    def get_confirmar(self): return self.txtConfirmarPassword.text().strip()
    def get_rol(self):       return self.cmbRolUsuario.currentText()

    def limpiar(self):
        for w in self.findChildren(QLineEdit):
            w.clear()

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'Correcto', msg)


# ── Vista clases ──────────────────────────────────────────────────────────────

class VistaAdminClases(QMainWindow):

    CABECERAS = ['ID', 'Nombre', 'Día', 'Hora inicio', 'Hora fin', 'Aforo', 'Nivel']

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_admin(self, ctrl)
        self.txtBuscar.textChanged.connect(ctrl.filtrar_clases)
        self.btnNuevaClase.clicked.connect(ctrl.anadir_fila_clase)
        self.btnGuardarCambios.clicked.connect(ctrl.guardar_cambios_clase)

    def get_texto_buscar(self): return self.txtBuscar.text().strip()

    def cargar_tabla(self, datos):
        _rellenar_tabla(self.tablaClases, self.CABECERAS,
                        datos, _ext_clase, editables={0})

    def get_datos_tabla(self):
        tabla = self.tablaClases
        return [
            [tabla.item(fi, ci).text() if tabla.item(fi, ci) else ''
             for ci in range(tabla.columnCount())]
            for fi in range(tabla.rowCount())
        ]

    def insertar_fila_vacia(self):

        tabla = self.tablaClases
        fi = tabla.rowCount()
        tabla.insertRow(fi)
        for ci, val in enumerate(['', 'Nueva clase', 'lunes', '09:00', '10:00', '20', 'media']):
            tabla.setItem(fi, ci, TablaView.crear_item(val, editable=(ci != 0)))
        tabla.selectRow(fi)
        return fi

    def set_total_clases(self, v):
        if hasattr(self, 'lblTotalClases'): self.lblTotalClases.setText(v)
        if hasattr(self, 'lblMostrando'):   self.lblMostrando.setText(f'Mostrando {v} clases')

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)
    def mostrar_exito(self, msg): QMessageBox.information(self, 'Correcto', msg)


# ── Vista inscripciones ───────────────────────────────────────────────────────

class VistaAdminInscripciones(QMainWindow):

    CABECERAS = ['Usuario', 'Clase', 'Fecha', 'Estado']

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_admin(self, ctrl)
        self.txtBuscarInscripciones.textChanged.connect(ctrl.filtrar_inscripciones)

    def get_texto_buscar(self): return self.txtBuscarInscripciones.text().strip()

    def cargar_tabla(self, datos):
        _rellenar_tabla(self.tablaInscripciones, self.CABECERAS,
                        datos, _ext_inscripcion)

    def set_stats(self, stats: dict):
        if hasattr(self, 'lblTotal'):  self.lblTotal.setText(str(stats.get('total', '')))
        if hasattr(self, 'label_4'):   self.label_4.setText(str(stats.get('clase_mas', '')))
        if hasattr(self, 'label_5'):   self.label_5.setText(str(stats.get('num_mas', '')))
        if hasattr(self, 'label_8'):   self.label_8.setText(str(stats.get('clase_menos', '')))
        if hasattr(self, 'label_9'):   self.label_9.setText(str(stats.get('num_menos', '')))
        if hasattr(self, 'label_15'):  self.label_15.setText(f"{stats.get('ocupacion', 0)}%")

    def set_texto_mostrando(self, texto):
        if hasattr(self, 'lblMostrando'): self.lblMostrando.setText(texto)

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)


# ── Vista pagos ───────────────────────────────────────────────────────────────

class VistaAdminPagos(QMainWindow):

    CABECERAS_PAGOS = ['Cliente', 'DNI', 'Tarifa', 'Importe pendiente', 'Fecha límite']

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_admin(self, ctrl)
        self.txtBuscarDNI.textChanged.connect(ctrl.filtrar_pagos_pendientes)

    def get_texto_buscar(self): return self.txtBuscarDNI.text().strip()

    def cargar_tabla_pagos(self, datos):
        _rellenar_tabla(self.tablaPagoAdmin, self.CABECERAS_PAGOS,
                        datos, editables={0, 1, 2, 3, 4})

    def set_resumen_pagos(self, ingresos_mes, ingresos_anio,
                          clientes_pendientes, importe_pendiente):
        if hasattr(self, 'label_4'):  self.label_4.setText(f'{ingresos_mes:.2f}€')
        if hasattr(self, 'label_8'):  self.label_8.setText(f'{ingresos_anio:.2f}€')
        if hasattr(self, 'label_13'): self.label_13.setText(str(clientes_pendientes))
        if hasattr(self, 'label_5'):  self.label_5.setText(f'{importe_pendiente:.2f}€')

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)


# ── Vista estadísticas ────────────────────────────────────────────────────────

class VistaAdminEstadisticas(QMainWindow):

    CABECERAS_RANKING = ['#', 'Cliente', 'Asistencias', 'Última clase', 'Estado']

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None

    def set_controlador(self, ctrl):
        self.controlador = ctrl
        _menu_admin(self, ctrl)

    def set_stats(self, stats: dict):
        if hasattr(self, 'lblNumR1'): self.lblNumR1.setText(str(stats.get('clientes_activos', '')))
        if hasattr(self, 'lblNumR2'): self.lblNumR2.setText(str(stats.get('reservas', '')))
        if hasattr(self, 'lblNumR3'): self.lblNumR3.setText(f"{stats.get('ocupacion', 0)}%")
        if hasattr(self, 'lblNumR4'): self.lblNumR4.setText(str(stats.get('asistencias', '')))
        if hasattr(self, 'lblNumClasesActivas'): self.lblNumClasesActivas.setText(str(stats.get('clases_activas', '')))
        if hasattr(self, 'lblNumEntrenadores'):  self.lblNumEntrenadores.setText(str(stats.get('entrenadores', '')))
        if hasattr(self, 'lblNumSalas'):         self.lblNumSalas.setText(str(stats.get('salas', '')))

    def cargar_tabla_ranking(self, datos):
        tabla = self.tablaRanking
        TablaView.configurar_columnas(tabla, self.CABECERAS_RANKING)
        tabla.setRowCount(len(datos))
        tabla.setSelectionBehavior(tabla.SelectRows)
        for fi, reg in enumerate(datos):
            vals = [fi + 1, reg.nombre, reg.asistencias, reg.ultima_clase, reg.estado]
            for ci, val in enumerate(vals):
                tabla.setItem(fi, ci, TablaView.crear_item(
                    str(val) if val is not None else '', editable=False))

    def set_ocupacion_clase(self, idx, nombre, porcentaje):
        lbl = f'lblOcc{idx}'
        bar = f'progOcc{idx}'
        if hasattr(self, lbl): getattr(self, lbl).setText(nombre)
        if hasattr(self, bar):
            b = getattr(self, bar)
            b.setValue(porcentaje)
            b.setFormat(f'{porcentaje}%')

    def mostrar_error(self, msg): QMessageBox.warning(self, 'Error', msg)