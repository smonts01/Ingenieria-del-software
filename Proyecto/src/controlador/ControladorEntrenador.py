from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout
from PyQt5 import uic


class ControladorEntrenador:
    """
    UC4  · Registrar asistencia a una clase
    UC5  · Ver lista de clientes apuntados a una clase
    UC15 · Consultar ocupación de clases
    """

    def __init__(self, modelo, usuario, controlador_principal):
        self.modelo = modelo
        self.usuario = usuario
        self.id_entrenador = usuario["id_usuario"]
        self.ctrl_principal = controlador_principal
        self.ventana = None
        self.ventana_clases = None
        self.ventana_asistencia = None
        self._id_clase_seleccionada = None

    # ------------------------------------------------------------------
    # Panel principal
    # ------------------------------------------------------------------
    def abrir(self):
        Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_entrenador.ui")

        class VentanaEntrenador(Window, Form):
            pass

        self.ventana = VentanaEntrenador()
        self._conectar_botones()
        self.cargarMisClases()
        self.ventana.show()

    def _conectar_botones(self):
        v = self.ventana
        if hasattr(v, "btnVerClases"):
            v.btnVerClases.clicked.connect(self.abrirPanelClases)
        if hasattr(v, "btnOcupacion"):
            v.btnOcupacion.clicked.connect(self.consultarOcupacion)
        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(self._cerrar_sesion)

    # ------------------------------------------------------------------
    # Mis clases en el panel de inicio
    # ------------------------------------------------------------------
    def cargarMisClases(self):
        clases = self.modelo.obtener_clases_entrenador(self.id_entrenador)
        v = self.ventana
        if not hasattr(v, "tablaClases"):
            return
        _rellenar_tabla(
            v.tablaClases, clases,
            ["ID", "Actividad", "Día", "Hora inicio", "Hora fin", "Sala", "Inscritos"],
            ["id_clase", "nombre_actividad", "dia_semana", "hora_inicio",
             "hora_fin", "sala", "total_inscritos"],
        )

    # ------------------------------------------------------------------
    # UC5 · Ver lista de clientes apuntados (panel de clases)
    # ------------------------------------------------------------------
    def abrirPanelClases(self):
        Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_entrenador_clases.ui")

        class VentanaClases(Window, Form):
            pass

        self.ventana_clases = VentanaClases()
        v = self.ventana_clases
        if hasattr(v, "btnVerInscritos"):
            v.btnVerInscritos.clicked.connect(self.verListaInscritos)
        if hasattr(v, "btnRegistrarAsistencia"):
            v.btnRegistrarAsistencia.clicked.connect(self.abrirRegistroAsistencia)
        if hasattr(v, "btnVolver"):
            v.btnVolver.clicked.connect(v.close)

        self._cargar_clases_en_panel()
        v.show()

    def _cargar_clases_en_panel(self):
        clases = self.modelo.obtener_clases_entrenador(self.id_entrenador)
        v = self.ventana_clases
        if not hasattr(v, "tablaClases"):
            return
        _rellenar_tabla(
            v.tablaClases, clases,
            ["ID", "Actividad", "Día", "Hora", "Sala", "Inscritos"],
            ["id_clase", "nombre_actividad", "dia_semana", "hora_inicio", "sala",
             "total_inscritos"],
        )

    def verListaInscritos(self):
        v = self.ventana_clases
        id_clase = self._obtener_id_clase_seleccionada(v)
        if id_clase is None:
            return

        inscritos = self.modelo.obtener_inscritos_clase(id_clase)
        if not inscritos:
            QMessageBox.information(v, "Sin inscritos",
                                    "No hay clientes apuntados a esta clase.")
            return

        if hasattr(v, "tablaInscritos"):
            _rellenar_tabla(
                v.tablaInscritos, inscritos,
                ["ID", "Nombre", "DNI", "Email", "Fecha inscripción"],
                ["id_cliente", "nombre", "dni", "email", "fecha_inscripcion"],
            )
        else:
            lineas = [
                f"{r.get('nombre', '')} — {r.get('email', '')}"
                for r in inscritos
            ]
            QMessageBox.information(v, "Inscritos", "\n".join(lineas))

    # ------------------------------------------------------------------
    # UC4 · Registrar asistencia
    # ------------------------------------------------------------------
    def abrirRegistroAsistencia(self):
        v_clases = self.ventana_clases
        id_clase = self._obtener_id_clase_seleccionada(v_clases)
        if id_clase is None:
            return
        self._id_clase_seleccionada = id_clase

        inscritos = self.modelo.obtener_inscritos_clase(id_clase)
        if not inscritos:
            QMessageBox.information(v_clases, "Sin inscritos",
                                    "No hay clientes inscritos en esta clase.")
            return

        Form, Window = uic.loadUiType(
            "./src/vista/Ui/interfaz_entrenador_registrar_asistencia.ui"
        )

        class VentanaAsistencia(Window, Form):
            pass

        self.ventana_asistencia = VentanaAsistencia()
        v = self.ventana_asistencia
        self._cargar_lista_asistencia(inscritos)

        if hasattr(v, "btnConfirmar"):
            v.btnConfirmar.clicked.connect(self.confirmarAsistencia)
        if hasattr(v, "btnCancelar"):
            v.btnCancelar.clicked.connect(v.close)
        v.show()

    def _cargar_lista_asistencia(self, inscritos):
        """
        Rellena la tabla de asistencia con un checkbox por cada cliente inscrito.
        """
        v = self.ventana_asistencia
        if not hasattr(v, "tablaAsistencia"):
            return
        tabla = v.tablaAsistencia
        tabla.setColumnCount(3)
        tabla.setHorizontalHeaderLabels(["Presente", "ID", "Nombre"])
        tabla.setRowCount(len(inscritos))

        for fila_idx, cliente in enumerate(inscritos):
            # Checkbox de asistencia
            widget = QWidget()
            chk = QCheckBox()
            layout = QHBoxLayout(widget)
            layout.addWidget(chk)
            layout.setContentsMargins(4, 0, 4, 0)
            tabla.setCellWidget(fila_idx, 0, widget)
            # Guardar referencia al checkbox para leerlo después
            tabla.item_at = getattr(tabla, "item_at", {})

            tabla.setItem(fila_idx, 1,
                          QTableWidgetItem(str(cliente.get("id_cliente", ""))))
            tabla.setItem(fila_idx, 2,
                          QTableWidgetItem(str(cliente.get("nombre", ""))))

        tabla.resizeColumnsToContents()

    def confirmarAsistencia(self):
        v = self.ventana_asistencia
        if not hasattr(v, "tablaAsistencia"):
            return
        tabla = v.tablaAsistencia
        lista_asistencia = []   # [(id_cliente, presente)]

        for fila_idx in range(tabla.rowCount()):
            widget = tabla.cellWidget(fila_idx, 0)
            id_item = tabla.item(fila_idx, 1)
            if widget is None or id_item is None:
                continue
            chk = widget.findChild(QCheckBox)
            presente = "si" if (chk and chk.isChecked()) else "no"
            lista_asistencia.append((int(id_item.text()), presente))

        if not lista_asistencia:
            QMessageBox.warning(v, "Sin datos", "No hay datos de asistencia que guardar.")
            return

        ok, mensaje = self.modelo.registrar_asistencia(
            self._id_clase_seleccionada, lista_asistencia
        )
        if ok:
            QMessageBox.information(v, "Asistencia registrada", mensaje)
            v.close()
        else:
            QMessageBox.critical(v, "Error", mensaje)

    # ------------------------------------------------------------------
    # UC15 · Consultar ocupación de clases
    # ------------------------------------------------------------------
    def consultarOcupacion(self):
        clases = self.modelo.obtener_ocupacion_clases(self.id_entrenador)
        v = self.ventana
        if not clases:
            QMessageBox.information(v, "Ocupación", "No hay clases disponibles.")
            return

        if hasattr(v, "tablaOcupacion"):
            _rellenar_tabla(
                v.tablaOcupacion, clases,
                ["Actividad", "Día", "Inscritos", "Aforo", "% Ocupación"],
                ["nombre_actividad", "dia_semana", "inscritos",
                 "aforo_maximo", "porcentaje"],
            )
        else:
            lineas = [
                f"{c.get('nombre_actividad')} ({c.get('dia_semana')}) — "
                f"{c.get('inscritos')}/{c.get('aforo_maximo')} "
                f"({c.get('porcentaje', 0):.0f}%)"
                for c in clases
            ]
            QMessageBox.information(v, "Ocupación de clases", "\n".join(lineas))

    # ------------------------------------------------------------------
    def _obtener_id_clase_seleccionada(self, ventana):
        tabla = getattr(ventana, "tablaClases", None)
        if tabla is None:
            QMessageBox.warning(ventana, "Error", "Tabla de clases no disponible.")
            return None
        fila = tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(ventana, "Selección", "Selecciona una clase de la lista.")
            return None
        item = tabla.item(fila, 0)
        if item is None:
            return None
        return int(item.text())

    def _cerrar_sesion(self):
        self.ventana.close()
        self.ctrl_principal.cerrar_sesion()


# ── Helpers ────────────────────────────────────────────────────────────

def _rellenar_tabla(tabla, datos, cabeceras, campos):
    tabla.setColumnCount(len(cabeceras))
    tabla.setHorizontalHeaderLabels(cabeceras)
    tabla.setRowCount(len(datos))
    for fila_idx, fila in enumerate(datos):
        for col_idx, campo in enumerate(campos):
            tabla.setItem(fila_idx, col_idx,
                          QTableWidgetItem(str(fila.get(campo, ""))))
    tabla.resizeColumnsToContents()
