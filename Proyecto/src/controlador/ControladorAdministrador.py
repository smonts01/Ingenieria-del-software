from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QLineEdit
from PyQt5 import uic


class ControladorAdministrador:
    """
    UC2  · Registrar nuevo usuario (trabajadores)
    UC10 · Gestionar clases (crear / modificar)
    UC13 · Generar ranking de clientes más activos
    UC15 · Consultar ocupación de clases
    """

    def __init__(self, modelo, usuario, controlador_principal):
        self.modelo = modelo
        self.usuario = usuario
        self.id_administrador = usuario["id_usuario"]
        self.ctrl_principal = controlador_principal
        self.ventana = None

    # ------------------------------------------------------------------
    # Panel principal
    # ------------------------------------------------------------------
    def abrir(self):
        Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_comun.ui")

        class VentanaAdmin(Window, Form):
            pass

        self.ventana = VentanaAdmin()
        self._conectar_botones()
        self.ventana.show()

    def _conectar_botones(self):
        v = self.ventana
        if hasattr(v, "btnRegistrarTrabajador"):
            v.btnRegistrarTrabajador.clicked.connect(self.abrirRegistroTrabajador)
        if hasattr(v, "btnGestionarClases"):
            v.btnGestionarClases.clicked.connect(self.abrirGestionClases)
        if hasattr(v, "btnRanking"):
            v.btnRanking.clicked.connect(self.generarRankingClientesActivos)
        if hasattr(v, "btnOcupacion"):
            v.btnOcupacion.clicked.connect(self.consultarOcupacionClases)
        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(self._cerrar_sesion)

    # ------------------------------------------------------------------
    # UC2 · Registrar trabajador
    # ------------------------------------------------------------------
    def abrirRegistroTrabajador(self):
        Form, Window = uic.loadUiType(
            "./src/vista/Ui/interfaz_recepcionista_registrar_usuario.ui"
        )

        class VentanaReg(Window, Form):
            pass

        self.ventana_registro = VentanaReg()
        v = self.ventana_registro
        # El administrador también elige el rol del nuevo trabajador
        if hasattr(v, "btnRegistrar"):
            v.btnRegistrar.clicked.connect(self.registrarTrabajador)
        if hasattr(v, "btnCancelar"):
            v.btnCancelar.clicked.connect(v.close)
        if hasattr(v, "btnOjo"):
            v.btnOjo.clicked.connect(lambda: _toggle_password(v, "txtPassword"))
        v.show()

    def registrarTrabajador(self):
        v = self.ventana_registro
        datos = {
            "dni":              _get_text(v, "txtDni"),
            "nombre":           _get_text(v, "txtNombre"),
            "telefono":         _get_text(v, "txtTelefono"),
            "email":            _get_text(v, "txtEmail"),
            "username":         _get_text(v, "txtUsername"),
            "password":         _get_text(v, "txtPassword"),
            "direccion":        _get_text(v, "txtDireccion"),
            "fecha_nacimiento": _get_date(v, "dateFechaNacimiento"),
            "rol":              _get_combo(v, "cmbRol") or "recepcionista",
            "salario":          _get_text(v, "txtSalario"),
            # Campos específicos de rol
            "especialidad":     _get_text(v, "txtEspecialidad"),
            "turno":            _get_text(v, "txtTurno"),
            "titulacion":       _get_text(v, "txtTitulacion"),
        }

        campos_base = ["dni", "nombre", "telefono", "email", "username",
                       "password", "direccion", "fecha_nacimiento", "salario"]
        vacios = [c for c in campos_base if not datos.get(c)]
        if vacios:
            QMessageBox.warning(v, "Campos incompletos",
                                f"Faltan: {', '.join(vacios)}")
            return

        ok, mensaje = self.modelo.registrar_nuevo_trabajador(
            datos, self.id_administrador
        )
        if ok:
            QMessageBox.information(v, "Registro exitoso", mensaje)
            v.close()
        else:
            QMessageBox.critical(v, "Error en el registro", mensaje)

    # ------------------------------------------------------------------
    # UC10 · Gestionar clases
    # ------------------------------------------------------------------
    def abrirGestionClases(self):
        Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_comun.ui")

        class VentanaGClases(Window, Form):
            pass

        self.ventana_clases = VentanaGClases()
        v = self.ventana_clases
        if hasattr(v, "btnNuevaClase"):
            v.btnNuevaClase.clicked.connect(lambda: self._abrir_formulario_clase(None))
        if hasattr(v, "btnModificarClase"):
            v.btnModificarClase.clicked.connect(self._modificar_clase_seleccionada)
        if hasattr(v, "btnVolver"):
            v.btnVolver.clicked.connect(v.close)
        self._cargar_tabla_clases()
        v.show()

    def _cargar_tabla_clases(self):
        clases = self.modelo.obtener_todas_las_clases()
        v = self.ventana_clases
        if not hasattr(v, "tablaClases"):
            return
        _rellenar_tabla(
            v.tablaClases, clases,
            ["ID", "Actividad", "Día", "Hora inicio", "Hora fin",
             "Entrenador", "Sala", "Aforo", "Intensidad"],
            ["id_clase", "nombre_actividad", "dia_semana", "hora_inicio",
             "hora_fin", "entrenador", "sala", "aforo_maximo", "nivel_intensidad"],
        )

    def _modificar_clase_seleccionada(self):
        v = self.ventana_clases
        tabla = getattr(v, "tablaClases", None)
        if tabla is None:
            return
        fila = tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(v, "Selección", "Selecciona una clase.")
            return
        id_item = tabla.item(fila, 0)
        if id_item is None:
            return
        id_clase = int(id_item.text())
        clase = self.modelo.obtener_clase_por_id(id_clase)
        self._abrir_formulario_clase(clase)

    def _abrir_formulario_clase(self, clase_actual):
        """Formulario reutilizable para crear o editar una clase."""
        Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_comun.ui")

        class VentanaFormClase(Window, Form):
            pass

        self.ventana_form_clase = VentanaFormClase()
        v = self.ventana_form_clase

        # Pre-rellenar si es edición
        if clase_actual:
            _set_text(v, "txtNombreActividad", clase_actual.get("nombre_actividad", ""))
            _set_text(v, "txtDia", clase_actual.get("dia_semana", ""))
            _set_text(v, "txtHoraInicio", str(clase_actual.get("hora_inicio", "")))
            _set_text(v, "txtHoraFin", str(clase_actual.get("hora_fin", "")))
            _set_text(v, "txtAforo", str(clase_actual.get("aforo_maximo", "")))
            _set_text(v, "txtCalorias", str(clase_actual.get("calorias_estimadas", "")))
            _set_text(v, "txtDuracion", str(clase_actual.get("duracion", "")))

        if hasattr(v, "btnGuardar"):
            v.btnGuardar.clicked.connect(
                lambda: self._guardar_clase(
                    clase_actual["id_clase"] if clase_actual else None
                )
            )
        if hasattr(v, "btnCancelar"):
            v.btnCancelar.clicked.connect(v.close)
        v.show()

    def _guardar_clase(self, id_clase=None):
        v = self.ventana_form_clase
        datos = {
            "nombre_actividad":   _get_text(v, "txtNombreActividad"),
            "dia_semana":         _get_text(v, "txtDia"),
            "hora_inicio":        _get_text(v, "txtHoraInicio"),
            "hora_fin":           _get_text(v, "txtHoraFin"),
            "aforo_maximo":       _get_text(v, "txtAforo"),
            "calorias_estimadas": _get_text(v, "txtCalorias"),
            "duracion":           _get_text(v, "txtDuracion"),
            "nivel_intensidad":   _get_combo(v, "cmbIntensidad") or "media",
            "id_entrenador":      _get_text(v, "txtIdEntrenador"),
            "id_sala":            _get_text(v, "txtIdSala"),
        }

        campos_req = ["nombre_actividad", "dia_semana", "hora_inicio",
                      "hora_fin", "aforo_maximo", "duracion"]
        vacios = [c for c in campos_req if not datos.get(c)]
        if vacios:
            QMessageBox.warning(v, "Campos incompletos",
                                f"Faltan: {', '.join(vacios)}")
            return

        if id_clase:
            ok, msg = self.modelo.modificar_clase(id_clase, datos)
        else:
            ok, msg = self.modelo.crear_clase(datos)

        if ok:
            QMessageBox.information(v, "Guardado", msg)
            v.close()
            self._cargar_tabla_clases()
        else:
            QMessageBox.critical(v, "Error", msg)

    # ------------------------------------------------------------------
    # UC13 · Ranking de clientes más activos
    # ------------------------------------------------------------------
    def generarRankingClientesActivos(self):
        ranking = self.modelo.obtener_ranking_clientes()
        v = self.ventana
        if not ranking:
            QMessageBox.information(v, "Ranking",
                                    "No hay datos de asistencia disponibles.")
            return

        if hasattr(v, "tablaRanking"):
            _rellenar_tabla(
                v.tablaRanking, ranking,
                ["Posición", "Nombre", "DNI", "Clases asistidas"],
                ["posicion", "nombre", "dni", "total_asistencias"],
            )
        else:
            lineas = [
                f"{i+1}. {r.get('nombre')} — {r.get('total_asistencias')} clases"
                for i, r in enumerate(ranking)
            ]
            QMessageBox.information(v, "Ranking de clientes más activos",
                                    "\n".join(lineas))

    # ------------------------------------------------------------------
    # UC15 · Ocupación de clases (vista global)
    # ------------------------------------------------------------------
    def consultarOcupacionClases(self):
        clases = self.modelo.obtener_ocupacion_clases()     # sin filtro de entrenador
        v = self.ventana
        if not clases:
            QMessageBox.information(v, "Ocupación", "No hay clases registradas.")
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
                f"{c.get('nombre_actividad')} — "
                f"{c.get('inscritos')}/{c.get('aforo_maximo')} "
                f"({c.get('porcentaje', 0):.0f}%)"
                for c in clases
            ]
            QMessageBox.information(v, "Ocupación de clases", "\n".join(lineas))

    # ------------------------------------------------------------------
    def _cerrar_sesion(self):
        self.ventana.close()
        self.ctrl_principal.cerrar_sesion()


# ── Helpers ────────────────────────────────────────────────────────────

def _get_text(v, nombre):
    w = getattr(v, nombre, None)
    return w.text().strip() if w else ""

def _get_date(v, nombre):
    w = getattr(v, nombre, None)
    return w.date().toPyDate().isoformat() if w else ""

def _get_combo(v, nombre):
    w = getattr(v, nombre, None)
    return w.currentText().strip() if w else ""

def _set_text(v, nombre, valor):
    w = getattr(v, nombre, None)
    if w:
        w.setText(str(valor))

def _toggle_password(v, nombre):
    w = getattr(v, nombre, None)
    if w:
        mode = QLineEdit.Normal if w.echoMode() == QLineEdit.Password else QLineEdit.Password
        w.setEchoMode(mode)

def _rellenar_tabla(tabla, datos, cabeceras, campos):
    tabla.setColumnCount(len(cabeceras))
    tabla.setHorizontalHeaderLabels(cabeceras)
    tabla.setRowCount(len(datos))
    for fi, fila in enumerate(datos):
        for ci, campo in enumerate(campos):
            tabla.setItem(fi, ci, QTableWidgetItem(str(fila.get(campo, ""))))
    tabla.resizeColumnsToContents()
