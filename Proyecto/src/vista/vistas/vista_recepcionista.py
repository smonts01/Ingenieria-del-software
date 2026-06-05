"""
Vistas del rol Recepcionista
  - VistaRecepcionistaInicio           (interfaz_recepcionista.ui)
  - VistaRecepcionistaClientes         (interfaz_recepcionista_clientes.ui)
  - VistaRecepcionistaControlAcceso    (interfaz_recepcionista_control_de_acceso.ui)
  - VistaRecepcionistaRegistrarUsuario (interfaz_recepcionista_registrar_usuario.ui)
  - VistaRecepcionistaPerfil           (interfaz_recepcionista_perfil.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMessageBox


def _conectar_menu_recepcionista(vista, ctrl):
    vista.btnInicio.clicked.connect(ctrl.ir_inicio)
    vista.btnClases.clicked.connect(ctrl.ir_clases)
    vista.btnInscripciones.clicked.connect(ctrl.ir_registrar_usuario)
    vista.btnOcupacion.clicked.connect(ctrl.ir_control_acceso)
    vista.btnPagos.clicked.connect(ctrl.ir_clientes)
    vista.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)


# ---------------------------------------------------------------------------
class VistaRecepcionistaInicio(QMainWindow):
    """Dashboard principal del recepcionista."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_recepcionista.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    def set_bienvenida(self, nombre: str):
        self.lblBienvenida.setText(f"¡Hola, {nombre}!")

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaCliente.setText(fecha)

    def set_num_clases(self, valor: str, idx: int = 1):
        lbl = getattr(self, f"lblNumClases{'_' + str(idx) if idx > 1 else ''}", None)
        if lbl:
            lbl.setText(valor)

    def cargar_tabla(self, datos: list[list], cabeceras: list[str]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(datos))
        self._tabla.setColumnCount(len(cabeceras))
        self._tabla.setHorizontalHeaderLabels(cabeceras)
        for fi, fila in enumerate(datos):
            for ci, val in enumerate(fila):
                self._tabla.setItem(fi, ci, QTableWidgetItem(str(val)))

    def conectar_senales(self, ctrl):
        _conectar_menu_recepcionista(self, ctrl)


# ---------------------------------------------------------------------------
class VistaRecepcionistaClientes(QMainWindow):
    """Vista del listado de clientes para el recepcionista."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_recepcionista_clientes.ui", self)

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    # --- Filtros ---
    def get_filtro_estado(self) -> str:
        return self.comboBox_2.currentText()

    def get_filtro_tipo(self) -> str:
        return self.comboBox_3.currentText()

    def poblar_combo_estado(self, opciones: list[str]):
        self.comboBox_2.clear()
        self.comboBox_2.addItems(["Todos"] + opciones)

    def poblar_combo_tipo(self, opciones: list[str]):
        self.comboBox_3.clear()
        self.comboBox_3.addItems(["Todos"] + opciones)

    # --- Cards de clientes (hasta 11 visibles en el diseño) ---
    def set_cliente_card(self, nombre_widget: str, texto: str):
        """Actualiza el texto de un QLabel de card por su objectName."""
        
        lbl = self.findChild(QLabel, nombre_widget)
        if lbl:
            lbl.setText(texto)

    # --- Feedback ---
    def mostrar_error(self, msg: str):
        
        QMessageBox.critical(self, "Error", msg)

    def conectar_senales(self, ctrl):
        self.comboBox_2.currentIndexChanged.connect(ctrl.aplicar_filtros)
        self.comboBox_3.currentIndexChanged.connect(ctrl.aplicar_filtros)
        self.btnInicio_4.clicked.connect(ctrl.ir_registrar_usuario)
        self.btnInicio_5.clicked.connect(ctrl.ir_control_acceso)
        _conectar_menu_recepcionista(self, ctrl)


# ---------------------------------------------------------------------------
class VistaRecepcionistaControlAcceso(QMainWindow):
    """Vista de control de acceso al gimnasio."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_recepcionista_control_de_acceso.ui", self)

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    # --- Cards de acceso activo (hasta 6) ---
    def set_acceso_card(self, idx: int, nombre: str, extra: str = ""):
        """
        Actualiza los datos de una card de acceso.
        :param idx: Índice de la card (numérico en el objectName).
        :param nombre: Nombre del socio.
        :param extra: Información adicional (tarifa, hora entrada, etc.).
        """
        lbl_nombre = getattr(self, f"lblNombreCliente_{idx}", None) \
            or self.findChild(type(self.lblNombreCliente),
                              f"lblNombreCliente_{idx}")
        if lbl_nombre:
            lbl_nombre.setText(nombre)

    def set_num_accesos_hoy(self, valor: str):

        lbl = self.findChild(QLabel, "lblNumAccesosHoy")
        if lbl:
            lbl.setText(valor)

    # --- Botones de acción rápida ---
    def conectar_senales(self, ctrl):
        self.btnCalorias_2.clicked.connect(ctrl.registrar_entrada)
        self.btnInicio_2.clicked.connect(ctrl.registrar_salida)
        self.btnInicio_3.clicked.connect(ctrl.buscar_socio)
        self.btnInicio_4.clicked.connect(ctrl.ir_registrar_usuario)
        _conectar_menu_recepcionista(self, ctrl)

    # --- Feedback ---
    def mostrar_mensaje(self, titulo: str, msg: str):

        QMessageBox.information(self, titulo, msg)

    def mostrar_error(self, msg: str):

        QMessageBox.critical(self, "Error", msg)


# ---------------------------------------------------------------------------
class VistaRecepcionistaRegistrarUsuario(QMainWindow):
    """Vista para registrar un nuevo usuario desde recepción."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_recepcionista_registrar_usuario.ui", self)

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def get_datos_formulario(self) -> dict:
        datos = {}
        for w in self.findChildren(QLineEdit):
            datos[w.objectName()] = w.text().strip()
        return datos

    def limpiar_formulario(self):
        for w in self.findChildren(QLineEdit):
            w.clear()

    def mostrar_error(self, msg: str):

        QMessageBox.critical(self, "Error de validación", msg)

    def mostrar_exito(self, msg: str):

        QMessageBox.information(self, "Usuario registrado", msg)

    def conectar_senales(self, ctrl):
        self.btnInicio_2.clicked.connect(ctrl.registrar_usuario)
        _conectar_menu_recepcionista(self, ctrl)


# ---------------------------------------------------------------------------
class VistaRecepcionistaPerfil(QMainWindow):
    """Vista del perfil del recepcionista."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_recepcionista_perfil.ui", self)

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)
        lbl_nombre = getattr(self, "label_Nombre", None)
        if lbl_nombre:
            lbl_nombre.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaCliente.setText(fecha)

    def get_campo(self, nombre: str) -> str:
        w = self.findChild(QLineEdit, nombre)
        return w.text().strip() if w else ""

    def set_campo(self, nombre: str, valor: str):
        w = self.findChild(QLineEdit, nombre)
        if w:
            w.setText(valor)

    def mostrar_aviso_perfil(self, visible: bool):
        self.frameAvisoPerfil.setVisible(visible)

    def mostrar_error(self, msg: str):

        QMessageBox.critical(self, "Error", msg)

    def mostrar_exito(self, msg: str):

        QMessageBox.information(self, "Guardado", msg)

    def conectar_senales(self, ctrl):
        _conectar_menu_recepcionista(self, ctrl)
