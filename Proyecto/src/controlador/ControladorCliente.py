from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5 import uic


class ControladorCliente:
    """
    UC3  · Inscribirse a una clase
    UC7  · Consultar información (pagos, inscripciones, horarios, calorías)
    UC16 · Calcular calorías quemadas
    """

    def __init__(self, modelo, usuario, controlador_principal):
        self.modelo = modelo
        self.usuario = usuario                        # dict del usuario autenticado
        self.id_cliente = usuario["id_usuario"]
        self.ctrl_principal = controlador_principal

        # Ventanas (se cargan al abrir)
        self.ventana_inicio = None
        self.ventana_clases = None
        self.ventana_inscripciones = None

    # ------------------------------------------------------------------
    # Apertura de la interfaz principal del cliente
    # ------------------------------------------------------------------
    def abrir(self):
        Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_cliente_inicio.ui")

        class VentanaInicio(Window, Form):
            pass

        self.ventana_inicio = VentanaInicio()
        self._conectar_botones_inicio()
        self._cargar_datos_inicio()
        self.ventana_inicio.show()

    def _conectar_botones_inicio(self):
        v = self.ventana_inicio
        # Botones de navegación lateral
        if hasattr(v, "btnClases"):
            v.btnClases.clicked.connect(self.abrirClases)
        if hasattr(v, "btnInscripciones"):
            v.btnInscripciones.clicked.connect(self.abrirInscripciones)
        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(self._cerrar_sesion)
        # Consultas de información (UC7)
        if hasattr(v, "btnHistorialPagos"):
            v.btnHistorialPagos.clicked.connect(self.consultarHistorialPagos)
        if hasattr(v, "btnPagosPendientes"):
            v.btnPagosPendientes.clicked.connect(self.consultarPagosPendientes)
        if hasattr(v, "btnCalorias"):
            v.btnCalorias.clicked.connect(self.consultarCaloriasQuemadas)

    # ------------------------------------------------------------------
    # UC7 · Consultar información — carga inicial del panel
    # ------------------------------------------------------------------
    def _cargar_datos_inicio(self):
        v = self.ventana_inicio
        nombre = self.usuario.get("nombre", "Cliente")
        if hasattr(v, "lblBienvenida"):
            v.lblBienvenida.setText(f"Bienvenido/a, {nombre}")

        # Mostrar estado de pago en el panel de inicio si existe el label
        estado = self.modelo.obtener_estado_pago(self.id_cliente)
        if hasattr(v, "lblEstadoPago"):
            v.lblEstadoPago.setText(f"Estado de pago: {estado or 'Sin datos'}")

    # ------------------------------------------------------------------
    # UC7 · Historial de pagos
    # ------------------------------------------------------------------
    def consultarHistorialPagos(self):
        pagos = self.modelo.obtener_historial_pagos(self.id_cliente)
        v = self.ventana_inicio
        if not hasattr(v, "tablaPagos"):
            QMessageBox.information(v, "Historial de pagos",
                                    self._formatear_lista(pagos,
                                                          ["fecha_pago", "importe", "estado", "tipo_cuota"]))
            return
        self._rellenar_tabla(v.tablaPagos,
                             pagos,
                             ["Fecha", "Importe (€)", "Estado", "Tipo cuota"],
                             ["fecha_pago", "importe", "estado", "tipo_cuota"])

    # ------------------------------------------------------------------
    # UC7 · Pagos pendientes
    # ------------------------------------------------------------------
    def consultarPagosPendientes(self):
        pagos = self.modelo.obtener_pagos_pendientes_cliente(self.id_cliente)
        if not pagos:
            QMessageBox.information(
                self.ventana_inicio, "Pagos pendientes",
                "No tienes ningún pago pendiente. ¡Todo al día!"
            )
            return
        v = self.ventana_inicio
        if hasattr(v, "tablaPagosPendientes"):
            self._rellenar_tabla(v.tablaPagosPendientes,
                                 pagos,
                                 ["Tarifa", "Importe (€)", "Fecha"],
                                 ["nombre", "importe", "fecha_pago"])
        else:
            QMessageBox.warning(v, "Pagos pendientes",
                                self._formatear_lista(pagos, ["nombre", "importe", "fecha_pago"]))

    # ------------------------------------------------------------------
    # UC16 · Calcular calorías quemadas
    # ------------------------------------------------------------------
    def consultarCaloriasQuemadas(self):
        total = self.modelo.obtener_calorias_quemadas(self.id_cliente)
        if total is None or total == 0:
            QMessageBox.information(
                self.ventana_inicio, "Calorías quemadas",
                "Todavía no tienes clases registradas con asistencia confirmada."
            )
            return
        v = self.ventana_inicio
        if hasattr(v, "lblCalorias"):
            v.lblCalorias.setText(f"{total} kcal quemadas en total")
        else:
            QMessageBox.information(v, "Calorías quemadas",
                                    f"Total de calorías quemadas: {total} kcal")

    # ------------------------------------------------------------------
    # UC3 · Inscribirse a una clase — abrir panel de clases
    # ------------------------------------------------------------------
    def abrirClases(self):
        Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_cliente_clases.ui")

        class VentanaClases(Window, Form):
            pass

        self.ventana_clases = VentanaClases()
        self._conectar_botones_clases()
        self.cargarClasesDisponibles()
        self.ventana_clases.show()

    def _conectar_botones_clases(self):
        v = self.ventana_clases
        if hasattr(v, "btnInscribirse"):
            v.btnInscribirse.clicked.connect(self.inscribirseClase)
        if hasattr(v, "btnVolver"):
            v.btnVolver.clicked.connect(self.ventana_clases.close)

    def cargarClasesDisponibles(self):
        clases = self.modelo.obtener_clases_disponibles(self.id_cliente)
        v = self.ventana_clases
        if not hasattr(v, "tablaClases"):
            return
        self._rellenar_tabla(
            v.tablaClases,
            clases,
            ["Actividad", "Día", "Hora inicio", "Hora fin", "Entrenador",
             "Sala", "Plazas libres", "Intensidad"],
            ["nombre_actividad", "dia_semana", "hora_inicio", "hora_fin",
             "entrenador", "sala", "plazas_libres", "nivel_intensidad"],
        )

    def inscribirseClase(self):
        v = self.ventana_clases
        if not hasattr(v, "tablaClases"):
            return
        fila = v.tablaClases.currentRow()
        if fila < 0:
            QMessageBox.warning(v, "Selección", "Selecciona una clase de la lista.")
            return

        # Recuperar id_clase guardado en la celda oculta (columna 0 con id)
        item_id = v.tablaClases.item(fila, 0)
        if item_id is None:
            return
        id_clase = int(item_id.data(32))   # Qt.UserRole = 32

        ok, mensaje = self.modelo.inscribir_cliente_clase(self.id_cliente, id_clase)
        if ok:
            QMessageBox.information(v, "Inscripción", mensaje)
            self.cargarClasesDisponibles()        # refrescar lista
        else:
            QMessageBox.warning(v, "Error en inscripción", mensaje)

    # ------------------------------------------------------------------
    # Panel de inscripciones actuales del cliente
    # ------------------------------------------------------------------
    def abrirInscripciones(self):
        Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_cliente_inscripciones.ui")

        class VentanaInscripciones(Window, Form):
            pass

        self.ventana_inscripciones = VentanaInscripciones()
        self.cargarMisInscripciones()
        if hasattr(self.ventana_inscripciones, "btnVolver"):
            self.ventana_inscripciones.btnVolver.clicked.connect(
                self.ventana_inscripciones.close
            )
        self.ventana_inscripciones.show()

    def cargarMisInscripciones(self):
        inscripciones = self.modelo.obtener_inscripciones_cliente(self.id_cliente)
        v = self.ventana_inscripciones
        if not hasattr(v, "tablaInscripciones"):
            return
        self._rellenar_tabla(
            v.tablaInscripciones,
            inscripciones,
            ["Actividad", "Día", "Hora", "Sala", "Estado", "Fecha inscripción"],
            ["nombre_actividad", "dia_semana", "hora_inicio", "sala",
             "estado", "fecha_inscripcion"],
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _cerrar_sesion(self):
        self.ventana_inicio.close()
        self.ctrl_principal.cerrar_sesion()

    @staticmethod
    def _rellenar_tabla(tabla, datos, cabeceras, campos):
        tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras)
        tabla.setRowCount(len(datos))
        for fila_idx, fila in enumerate(datos):
            for col_idx, campo in enumerate(campos):
                valor = str(fila.get(campo, ""))
                item = QTableWidgetItem(valor)
                # Guardar id en la primera celda como dato de usuario
                if col_idx == 0 and "id_clase" in fila:
                    item.setData(32, fila["id_clase"])
                tabla.setItem(fila_idx, col_idx, item)
        tabla.resizeColumnsToContents()

    @staticmethod
    def _formatear_lista(datos, campos):
        if not datos:
            return "No hay datos disponibles."
        lineas = []
        for fila in datos:
            lineas.append(" | ".join(str(fila.get(c, "")) for c in campos))
        return "\n".join(lineas)
