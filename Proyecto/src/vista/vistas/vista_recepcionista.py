"""
Vistas del rol Recepcionista — Patrón MVC según ejemplo de la profesora.

Responsabilidad de la Vista:
- Cargar el .ui en __init__
- Conectar sus propios botones en __init__
- Crear VOs con los datos del formulario y pasarlos al controlador
- Exponer métodos set_xxx() para que el controlador actualice la UI
- Nunca contiene lógica de negocio
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QLineEdit, QMessageBox
from PyQt5.uic import loadUi
from src.modelo.VO.RegistroAccesoResumenVO import RegistroAccesoResumenVO


def _rellenar_tabla_accesos(tabla, cabeceras, datos):
    """Rellena tabla con lista de RegistroAccesoResumenVO."""
    tabla.setColumnCount(len(cabeceras))
    tabla.setHorizontalHeaderLabels(cabeceras)
    tabla.setRowCount(len(datos))
    for fi, vo in enumerate(datos):
        valores = [
            str(getattr(vo, 'nombre', '')),
            str(getattr(vo, 'dni', '')),
            str(getattr(vo, 'tipo_acceso', '')),
            str(getattr(vo, 'fecha_hora_registro', '')),
        ]
        for ci, val in enumerate(valores[:len(cabeceras)]):
            tabla.setItem(fi, ci, QTableWidgetItem(val))


def _rellenar_tabla_tuplas(tabla, cabeceras, datos):
    """Rellena tabla con lista de tuplas."""
    tabla.setColumnCount(len(cabeceras))
    tabla.setHorizontalHeaderLabels(cabeceras)
    tabla.setRowCount(len(datos))
    for fi, fila in enumerate(datos):
        valores = list(fila) if isinstance(fila, (list, tuple)) else [str(fila)]
        for ci, val in enumerate(valores[:len(cabeceras)]):
            tabla.setItem(fi, ci, QTableWidgetItem(str(val) if val is not None else ''))


# ──────────────────────────────────────────────────────────────────────────────
class VistaRecepcionistaInicio(QMainWindow):
    """Vista del dashboard del recepcionista (interfaz_recepcionista.ui)."""

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None
        # La vista conecta sus propios botones
        self.btnCerrarSesion.clicked.connect(self._on_cerrar_sesion)
        self.btnInicio.clicked.connect(self._on_inicio)
        self.btnRegistroUsuario.clicked.connect(self._on_registrar_usuario)
        self.btnControlAcceso.clicked.connect(self._on_control_acceso)
        self.btnClientes.clicked.connect(self._on_clientes)
        self.btnPerfil.clicked.connect(self._on_perfil)

    # — Delegación al controlador —
    def _on_cerrar_sesion(self):    self.controlador.cerrar_sesion()
    def _on_inicio(self):           self.controlador.ir_inicio()
    def _on_registrar_usuario(self):self.controlador.ir_registrar_usuario()
    def _on_control_acceso(self):   self.controlador.ir_control_acceso()
    def _on_clientes(self):         self.controlador.ir_clientes()
    def _on_perfil(self):           self.controlador.ir_perfil()

    def set_controlador(self, ctrl):
        self.controlador = ctrl

    # — Métodos que el controlador llama para actualizar la UI —
    def set_num_clientes(self, valor: str):
        self.lblNumClientes.setText(valor)

    def set_num_entradas(self, valor: str):
        self.lblNumEntradas.setText(valor)

    def set_num_clases_hoy(self, valor: str):
        self.lblNumClasesHoy.setText(valor)

    def cargar_tabla_registros(self, cabeceras: list, datos: list):
        _rellenar_tabla_accesos(self.tablaUltimosRegistros, cabeceras, datos)

    def cargar_tabla_clientes_recientes(self, cabeceras: list, datos: list):
        _rellenar_tabla_tuplas(self.tablaClientesRecientes, cabeceras, datos)


# ──────────────────────────────────────────────────────────────────────────────
class VistaRecepcionistaRegistrarUsuario(QMainWindow):
    """Vista para registrar un nuevo cliente (interfaz_recepcionista_registrar_usuario.ui)."""

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None
        # Menú lateral
        self.btnCerrarSesion.clicked.connect(self._on_cerrar_sesion)
        self.btnInicio.clicked.connect(self._on_inicio)
        self.btnRegistroUsuario.clicked.connect(self._on_registrar_usuario)
        self.btnControlAcceso.clicked.connect(self._on_control_acceso)
        self.btnClientes.clicked.connect(self._on_clientes)
        self.btnPerfil.clicked.connect(self._on_perfil)
        # Botón registrar
        self.btnInicio_20.clicked.connect(self._on_confirmar_registro)

    # — Delegación al controlador —
    def _on_cerrar_sesion(self):        self.controlador.cerrar_sesion()
    def _on_inicio(self):               self.controlador.ir_inicio()
    def _on_registrar_usuario(self):    self.controlador.ir_registrar_usuario()
    def _on_control_acceso(self):       self.controlador.ir_control_acceso()
    def _on_clientes(self):             self.controlador.ir_clientes()
    def _on_perfil(self):               self.controlador.ir_perfil()
    def _on_confirmar_registro(self):   self.controlador.registrar_cliente()

    def set_controlador(self, ctrl):
        self.controlador = ctrl

    # — Getters del formulario (el controlador lee los datos a través de estos) —
    def get_dni(self):          return self.DNI.text().strip()
    def get_nombre(self):       return self.NombreCompleto.text().strip()
    def get_telefono(self):     return self.Telefono.text().strip()
    def get_direccion(self):    return self.Direccion.text().strip()
    def get_email(self):        return self.Email.text().strip()
    def get_fecha(self):        return self.Nacimiento.text().strip()
    def get_username(self):     return self.Usuario.text().strip()
    def get_password(self):     return self.Contrasea.text().strip()
    def get_confirmar(self):    return self.ConfirmarContrasea.text().strip()
    def get_dni_tutor(self):    return self.DNITutor.text().strip() if hasattr(self, 'DNITutor') else ''
    def get_nombre_tutor(self): return self.NombreTutor.text().strip() if hasattr(self, 'NombreTutor') else ''
    def get_plan(self):         return self.PlanComboBox.currentText().strip() if hasattr(self, 'PlanComboBox') else 'Basico'
    def es_menor(self):         return self.ButtomMenor.isChecked() if hasattr(self, 'ButtomMenor') else False
    def es_adulto(self):        return self.ButtomAdulto.isChecked() if hasattr(self, 'ButtomAdulto') else True

    # — Métodos que el controlador llama para actualizar la UI —
    def limpiar_formulario(self):
        for w in self.findChildren(QLineEdit):
            w.clear()

    def mostrar_error(self, msg: str):
        QMessageBox.warning(self, 'Error', msg)

    def mostrar_exito(self, msg: str):
        QMessageBox.information(self, 'Correcto', msg)


# ──────────────────────────────────────────────────────────────────────────────
class VistaRecepcionistaControlAcceso(QMainWindow):
    """Vista de control de acceso (interfaz_recepcionista_control_de_acceso.ui)."""

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None
        # Menú lateral
        self.btnCerrarSesion.clicked.connect(self._on_cerrar_sesion)
        self.btnInicio.clicked.connect(self._on_inicio)
        self.btnRegistroUsuario.clicked.connect(self._on_registrar_usuario)
        self.btnControlAcceso.clicked.connect(self._on_control_acceso)
        self.btnClientes.clicked.connect(self._on_clientes)
        self.btnPerfil.clicked.connect(self._on_perfil)
        # Buscador y botones de acción
        self.txtDNIoID.textChanged.connect(self._on_buscar)
        self.btnEntrada.clicked.connect(self._on_entrada)
        self.btnSalida.clicked.connect(self._on_salida)

    # — Delegación al controlador —
    def _on_cerrar_sesion(self):        self.controlador.cerrar_sesion()
    def _on_inicio(self):               self.controlador.ir_inicio()
    def _on_registrar_usuario(self):    self.controlador.ir_registrar_usuario()
    def _on_control_acceso(self):       self.controlador.ir_control_acceso()
    def _on_clientes(self):             self.controlador.ir_clientes()
    def _on_perfil(self):               self.controlador.ir_perfil()
    def _on_buscar(self):               self.controlador.buscar_cliente_control_acceso()
    def _on_entrada(self):              self.controlador.registrar_acceso_control('entrada')
    def _on_salida(self):               self.controlador.registrar_acceso_control('salida')

    def set_controlador(self, ctrl):
        self.controlador = ctrl

    # — Getter —
    def get_dni_id(self):
        return self.txtDNIoID.text().strip()

    # — Métodos que el controlador llama para actualizar la UI —
    def set_cliente_encontrado(self, nombre, dni, id_usuario, estado_pago):
        self.lblNombre.setText(str(nombre))
        self.lblDNI.setText(f'DNI: {dni}')
        self.lblID.setText(f'ID: {id_usuario}')
        self.lblEstado.setText(str(estado_pago))

    def set_cliente_no_encontrado(self):
        self.lblNombre.setText('Cliente no encontrado')
        self.lblDNI.setText('DNI: -')
        self.lblID.setText('ID: -')
        self.lblEstado.setText('-')

    def limpiar_cliente(self):
        self.lblNombre.setText('Cliente no seleccionado')
        self.lblDNI.setText('DNI: -')
        self.lblID.setText('ID: -')
        self.lblEstado.setText('-')

    def cargar_tabla_accesos(self, cabeceras: list, datos: list):
        _rellenar_tabla_accesos(self.tableAccesos, cabeceras, datos)

    def mostrar_error(self, msg: str):
        QMessageBox.warning(self, 'Error', msg)

    def mostrar_exito(self, msg: str):
        QMessageBox.information(self, 'Correcto', msg)


# ──────────────────────────────────────────────────────────────────────────────
class VistaRecepcionistaClientes(QMainWindow):
    """Vista del listado de clientes (interfaz_recepcionista_clientes.ui)."""

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None
        # Menú lateral
        self.btnCerrarSesion.clicked.connect(self._on_cerrar_sesion)
        self.btnInicio.clicked.connect(self._on_inicio)
        self.btnRegistroUsuario.clicked.connect(self._on_registrar_usuario)
        self.btnControlAcceso.clicked.connect(self._on_control_acceso)
        self.btnClientes.clicked.connect(self._on_clientes)
        self.btnPerfil.clicked.connect(self._on_perfil)
        # Filtros y guardar
        self.lblBuscarDNI.textChanged.connect(self._on_filtrar)
        self.comboBox_adultomenor.currentIndexChanged.connect(self._on_filtrar)
        self.comboBox_plan.currentIndexChanged.connect(self._on_filtrar)
        self.btnCambios.clicked.connect(self._on_guardar)

    # — Delegación al controlador —
    def _on_cerrar_sesion(self):        self.controlador.cerrar_sesion()
    def _on_inicio(self):               self.controlador.ir_inicio()
    def _on_registrar_usuario(self):    self.controlador.ir_registrar_usuario()
    def _on_control_acceso(self):       self.controlador.ir_control_acceso()
    def _on_clientes(self):             self.controlador.ir_clientes()
    def _on_perfil(self):               self.controlador.ir_perfil()
    def _on_filtrar(self):              self.controlador.filtrar_clientes_recepcionista()
    def _on_guardar(self):              self.controlador.guardar_cambios_clientes_recepcionista()

    def set_controlador(self, ctrl):
        self.controlador = ctrl

    # — Getters de filtros —
    def get_filtro_dni(self):   return self.lblBuscarDNI.text().strip()
    def get_filtro_tipo(self):  return self.comboBox_adultomenor.currentText()
    def get_filtro_plan(self):  return self.comboBox_plan.currentText()

    # — Métodos que el controlador llama para actualizar la UI —
    def set_total_clientes(self, valor: str):
        self.lblTotalClientes.setText(valor)

    def set_nuevos_mes(self, valor: str):
        self.lblNuevosMes.setText(valor)

    def cargar_tabla_clientes(self, cabeceras: list, datos: list):
        _rellenar_tabla_tuplas(self.tablaClientes, cabeceras, datos)
        self.tablaClientes.setEditTriggers(
            self.tablaClientes.DoubleClicked | self.tablaClientes.SelectedClicked
        )
        self.tablaClientes.setSelectionBehavior(self.tablaClientes.SelectRows)

    def num_filas(self) -> int:
        return self.tablaClientes.rowCount()

    def get_fila_tabla(self, fila: int, num_cols: int) -> list:
        return [
            self.tablaClientes.item(fila, col).text().strip()
            if self.tablaClientes.item(fila, col) else ''
            for col in range(num_cols)
        ]

    def mostrar_error(self, msg: str):
        QMessageBox.warning(self, 'Error', msg)

    def mostrar_exito(self, msg: str):
        QMessageBox.information(self, 'Correcto', msg)


# ──────────────────────────────────────────────────────────────────────────────
class VistaRecepcionistaPerfil(QMainWindow):
    """Vista del perfil del recepcionista (interfaz_recepcionista_perfil.ui)."""

    def __init__(self, ruta_ui):
        super().__init__()
        loadUi(ruta_ui, self)
        self.controlador = None
        # Menú lateral
        self.btnCerrarSesion.clicked.connect(self._on_cerrar_sesion)
        self.btnInicio.clicked.connect(self._on_inicio)
        self.btnRegistroUsuario.clicked.connect(self._on_registrar_usuario)
        self.btnControlAcceso.clicked.connect(self._on_control_acceso)
        self.btnClientes.clicked.connect(self._on_clientes)
        self.btnPerfil.clicked.connect(self._on_perfil)

    # — Delegación al controlador —
    def _on_cerrar_sesion(self):        self.controlador.cerrar_sesion()
    def _on_inicio(self):               self.controlador.ir_inicio()
    def _on_registrar_usuario(self):    self.controlador.ir_registrar_usuario()
    def _on_control_acceso(self):       self.controlador.ir_control_acceso()
    def _on_clientes(self):             self.controlador.ir_clientes()
    def _on_perfil(self):               self.controlador.ir_perfil()

    def set_controlador(self, ctrl):
        self.controlador = ctrl

    # — Métodos que el controlador llama para actualizar la UI —
    def set_nombre(self, valor: str):   self.label_Nombre.setText(valor)
    def set_email(self, valor: str):    self.label_7.setText(valor)
    def set_username(self, valor: str): self.label_9.setText(valor)
    def set_direccion(self, valor: str):self.label_16.setText(valor)