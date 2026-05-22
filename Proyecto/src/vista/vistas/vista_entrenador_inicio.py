"""
Vista del panel de inicio del entrenador (interfaz_entrenador.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi


class VistaEntrenadorInicio(QMainWindow):
    """Vista del dashboard principal del entrenador."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_entrenador.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    # --- Cabecera ---
    def set_bienvenida(self, nombre: str):
        self.lblBienvenida.setText(f"¡Hola, {nombre}!")

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaEntrenador.setText(fecha)

    # --- Próxima clase ---
    def set_proxima_clase(self, nombre: str):
        self.labelClase.setText(nombre)

    def set_hora_proxima(self, hora: str):
        self.labelHora.setText(hora)

    def set_sala_proxima(self, sala: str):
        self.labelSala.setText(sala)

    # --- KPIs ---
    def set_num_asistencias(self, valor: str):
        self.labelNumAsistencias.setText(valor)

    def set_num_clases(self, valor: str):
        self.labelNumClases.setText(valor)

    # --- Consejo del día ---
    def set_consejo(self, texto: str):
        self.lblConsejo.setText(texto)

    # --- Tabla de agenda ---
    def cargar_tabla(self, datos: list[list], cabeceras: list[str]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(datos))
        self._tabla.setColumnCount(len(cabeceras))
        self._tabla.setHorizontalHeaderLabels(cabeceras)
        for fila_idx, fila in enumerate(datos):
            for col_idx, valor in enumerate(fila):
                self._tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.btnClases_2.clicked.connect(ctrl.ir_clases)
        self.btnInscritos.clicked.connect(ctrl.ir_inscritos)
        self.btnOcupacion.clicked.connect(ctrl.ir_ocupacion)
        self.btnRegistroAsistencia.clicked.connect(ctrl.ir_registro_asistencia)
        self.btnInformacion.clicked.connect(ctrl.ir_informacion)
        self.btnPerfil.clicked.connect(ctrl.ir_perfil)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
