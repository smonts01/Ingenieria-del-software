"""
Vista del panel de inicio del administrador (interfaz_admin_inicio.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QTableWidget


class VistaAdminInicio(QMainWindow):
    """Vista del dashboard principal del administrador."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_admin_inicio.ui", self)

    # --- Actualización de tarjetas de resumen ---
    def set_num_usuarios(self, valor: str):
        """Total de usuarios activos."""
        self.lblClasesNum.setText(valor)

    def set_num_clases(self, valor: str):
        """Total de clases activas."""
        self.lblClasesNum_2.setText(valor)

    def set_num_inscripciones(self, valor: str):
        """Total de inscripciones del mes."""
        self.lblClasesNum_3.setText(valor)

    def set_ingresos_mes(self, valor: str):
        """Ingresos totales del mes (€)."""
        self.lblClasesNum_4.setText(valor)

    def set_nombre_admin(self, nombre: str):
        """Actualiza el saludo con el nombre del administrador."""
        self.lblNombreAdmin.setText(f"Hola, {nombre}")

    # --- Tabla de actividad reciente ---
    def cargar_tabla_actividad(self, datos: list[list[str]], cabeceras: list[str]):
        """
        Rellena la tabla de actividad reciente.
        :param datos: Lista de filas, cada fila es una lista de strings.
        :param cabeceras: Nombres de columnas.
        """
        tabla = self.cardTabla.findChild(type(self.cardTabla), "tableWidget") \
            if hasattr(self, "tableWidget") else None
        # Búsqueda genérica del QTableWidget dentro del card
        
        tabla = self.findChild(QTableWidget)
        if tabla is None:
            return
        tabla.setRowCount(len(datos))
        tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras)
        for fila_idx, fila in enumerate(datos):
            for col_idx, valor in enumerate(fila):
                tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    # --- Navegación (señales conectadas por el controlador) ---
    def conectar_navegacion(self, ctrl):
        """El controlador conecta los botones del menú lateral."""
        self.btnUsuarios.clicked.connect(ctrl.ir_usuarios)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnInscripciones.clicked.connect(ctrl.ir_inscripciones)
        self.btnPagos.clicked.connect(ctrl.ir_pagos)
        self.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
        self.btnConfiguracion.clicked.connect(ctrl.ir_configuracion)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
