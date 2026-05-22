"""
Vista de lista de clientes inscritos en una clase (interfaz_entrenador_verListaClientes.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi


class VistaEntrenadorListaClientes(QMainWindow):
    """Vista con el listado de clientes inscritos en una clase."""

    CABECERAS = ["ID", "Nombre", "Email", "Teléfono", "Estado"]

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_entrenador_verListaClientes.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    # --- Cabecera ---
    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaEntrenador.setText(fecha)

    # --- Info de la clase seleccionada ---
    def set_nombre_clase(self, nombre: str):
        self.label_nombreclase_ins.setText(nombre)

    def set_fecha_clase(self, fecha: str):
        self.label_fecha_ins.setText(fecha)

    def set_horario_clase(self, horario: str):
        self.lblHorarioClase_ins.setText(horario)

    def set_sala_clase(self, sala: str):
        self.lblSalaClase_ins.setText(sala)

    def set_num_inscritos(self, valor: str):
        self.label_numInscritos_ins.setText(valor)

    def set_total_inscritos(self, valor: str):
        self.label_total_inscritos.setText(valor)

    # --- Tabla ---
    def cargar_tabla(self, clientes: list[list]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(clientes))
        self._tabla.setColumnCount(len(self.CABECERAS))
        self._tabla.setHorizontalHeaderLabels(self.CABECERAS)
        for fila_idx, fila in enumerate(clientes):
            for col_idx, valor in enumerate(fila):
                self._tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.btnInicio_2.clicked.connect(ctrl.ir_inicio)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnOcupacion.clicked.connect(ctrl.ir_ocupacion)
        self.btnRegistroAsistencia.clicked.connect(ctrl.ir_registro_asistencia)
        self.btnInformacion.clicked.connect(ctrl.ir_informacion)
        self.btnPerfil.clicked.connect(ctrl.ir_perfil)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
