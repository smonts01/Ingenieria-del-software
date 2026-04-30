from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QLineEdit
from PyQt5 import uic
from datetime import date


class ControladorRecepcionista:
    """
    UC2 · Registrar nuevo usuario (clientes)
    UC8 · Registro de entradas y salidas a la instalación
    UC9 · Consultar y actualizar información de clientes
    """

    CAMPOS_OBLIGATORIOS_CLIENTE = [
        "txtDni", "txtNombre", "txtTelefono",
        "txtEmail", "txtUsername", "txtPassword",
        "txtDireccion", "dateFechaNacimiento",
    ]

    def __init__(self, modelo, usuario, controlador_principal):
        self.modelo = modelo
        self.usuario = usuario
        self.id_recepcionista = usuario["id_usuario"]
        self.ctrl_principal = controlador_principal
        self.ventana = None
        self.ventana_registro = None
        self.ventana_acceso = None

    # ------------------------------------------------------------------
    # Apertura del panel principal
    # ------------------------------------------------------------------
    def abrir(self):
        Form, Window = uic.loadUiType("./src/vista/Ui/interfaz_recepcionista.ui")

        class VentanaRecep(Window, Form):
            pass

        self.ventana = VentanaRecep()
        self._conectar_botones()
        self._cargar_lista_clientes()
        self.ventana.show()

    def _conectar_botones(self):
        v = self.ventana
        if hasattr(v, "btnRegistrarUsuario"):
            v.btnRegistrarUsuario.clicked.connect(self.abrirRegistroUsuario)
        if hasattr(v, "btnControlAcceso"):
            v.btnControlAcceso.clicked.connect(self.abrirControlAcceso)
        if hasattr(v, "btnBuscarCliente"):
            v.btnBuscarCliente.clicked.connect(self.buscarCliente)
        if hasattr(v, "btnActualizarCliente"):
            v.btnActualizarCliente.clicked.connect(self.actualizarCliente)
        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(self._cerrar_sesion)
        # Al seleccionar fila de la tabla, rellenar formulario de edición
        if hasattr(v, "tablaClientes"):
            v.tablaClientes.itemSelectionChanged.connect(self._cargar_cliente_en_formulario)

    # ------------------------------------------------------------------
    # UC9 · Cargar lista de clientes
    # ------------------------------------------------------------------
    def _cargar_lista_clientes(self):
        clientes = self.modelo.obtener_todos_los_clientes()
        v = self.ventana
        if not hasattr(v, "tablaClientes"):
            return
        cabeceras = ["ID", "Nombre", "DNI", "Teléfono", "Email", "Estado pago", "Tarifa"]
        campos    = ["id_usuario", "nombre", "dni", "telefono", "email",
                     "estado_pagado", "tarifa"]
        _rellenar_tabla(v.tablaClientes, clientes, cabeceras, campos)

    def buscarCliente(self):
        v = self.ventana
        texto = v.txtBuscarCliente.text().strip() if hasattr(v, "txtBuscarCliente") else ""
        if not texto:
            self._cargar_lista_clientes()
            return
        clientes = self.modelo.buscar_clientes(texto)
        if not clientes:
            QMessageBox.information(v, "Búsqueda", "No se encontró ningún cliente.")
            return
        cabeceras = ["ID", "Nombre", "DNI", "Teléfono", "Email", "Estado pago", "Tarifa"]
        campos    = ["id_usuario", "nombre", "dni", "telefono", "email",
                     "estado_pagado", "tarifa"]
        _rellenar_tabla(v.tablaClientes, clientes, cabeceras, campos)

    def _cargar_cliente_en_formulario(self):
        """Rellena los campos de edición con el cliente seleccionado (UC9)."""
        v = self.ventana
        if not hasattr(v, "tablaClientes"):
            return
        fila = v.tablaClientes.currentRow()
        if fila < 0:
            return
        id_usuario = v.tablaClientes.item(fila, 0)
        if id_usuario is None:
            return
        cliente = self.modelo.obtener_cliente_por_id(int(id_usuario.text()))
        if cliente is None:
            return
        # Rellenar campos si existen en el formulario
        _set_text(v, "txtEditNombre", cliente.get("nombre", ""))
        _set_text(v, "txtEditTelefono", cliente.get("telefono", ""))
        _set_text(v, "txtEditEmail", cliente.get("email", ""))
        _set_text(v, "txtEditDireccion", cliente.get("direccion", ""))

    # ------------------------------------------------------------------
    # UC9 · Actualizar información de cliente
    # ------------------------------------------------------------------
    def actualizarCliente(self):
        v = self.ventana
        if not hasattr(v, "tablaClientes"):
            return
        fila = v.tablaClientes.currentRow()
        if fila < 0:
            QMessageBox.warning(v, "Selección", "Selecciona un cliente de la lista.")
            return
        id_item = v.tablaClientes.item(fila, 0)
        if id_item is None:
            return
        id_cliente = int(id_item.text())

        nombre    = _get_text(v, "txtEditNombre")
        telefono  = _get_text(v, "txtEditTelefono")
        email     = _get_text(v, "txtEditEmail")
        direccion = _get_text(v, "txtEditDireccion")

        if not all([nombre, telefono, email, direccion]):
            QMessageBox.warning(v, "Datos incompletos",
                                "Todos los campos son obligatorios.")
            return

        datos = {"nombre": nombre, "telefono": telefono,
                 "email": email, "direccion": direccion}
        ok, mensaje = self.modelo.actualizar_cliente(id_cliente, datos)
        if ok:
            QMessageBox.information(v, "Actualización", mensaje)
            self._cargar_lista_clientes()
        else:
            QMessageBox.critical(v, "Error", mensaje)

    # ------------------------------------------------------------------
    # UC2 · Registrar nuevo usuario (cliente)
    # ------------------------------------------------------------------
    def abrirRegistroUsuario(self):
        Form, Window = uic.loadUiType(
            "./src/vista/Ui/interfaz_recepcionista_registrar_usuario.ui"
        )

        class VentanaReg(Window, Form):
            pass

        self.ventana_registro = VentanaReg()
        v = self.ventana_registro
        if hasattr(v, "btnRegistrar"):
            v.btnRegistrar.clicked.connect(self.registrarNuevoCliente)
        if hasattr(v, "btnCancelar"):
            v.btnCancelar.clicked.connect(v.close)
        if hasattr(v, "btnOjo"):
            v.btnOjo.clicked.connect(
                lambda: _toggle_password(v, "txtPassword")
            )
        v.show()

    def registrarNuevoCliente(self):
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
        }

        vacios = [k for k, val in datos.items() if not val]
        if vacios:
            QMessageBox.warning(
                v, "Campos incompletos",
                f"Faltan los siguientes campos: {', '.join(vacios)}"
            )
            return

        ok, mensaje = self.modelo.registrar_nuevo_cliente(datos)
        if ok:
            QMessageBox.information(v, "Registro exitoso", mensaje)
            v.close()
            self._cargar_lista_clientes()
        else:
            QMessageBox.critical(v, "Error en el registro", mensaje)

    # ------------------------------------------------------------------
    # UC8 · Registro de entradas y salidas
    # ------------------------------------------------------------------
    def abrirControlAcceso(self):
        Form, Window = uic.loadUiType(
            "./src/vista/Ui/interfaz_recepcionista_control_de_acceso.ui"
        )

        class VentanaAcceso(Window, Form):
            pass

        self.ventana_acceso = VentanaAcceso()
        v = self.ventana_acceso
        if hasattr(v, "btnEntrada"):
            v.btnEntrada.clicked.connect(lambda: self.registrarAcceso("entrada"))
        if hasattr(v, "btnSalida"):
            v.btnSalida.clicked.connect(lambda: self.registrarAcceso("salida"))
        if hasattr(v, "btnVolver"):
            v.btnVolver.clicked.connect(v.close)
        self._cargar_historial_acceso()
        v.show()

    def registrarAcceso(self, tipo_acceso: str):
        v = self.ventana_acceso
        id_texto = _get_text(v, "txtIdUsuario")
        if not id_texto or not id_texto.isdigit():
            QMessageBox.warning(v, "ID inválido", "Introduce un ID de usuario válido.")
            return
        id_usuario = int(id_texto)

        ok, mensaje = self.modelo.registrar_acceso(id_usuario, tipo_acceso)
        if ok:
            QMessageBox.information(v, "Acceso registrado", mensaje)
            self._cargar_historial_acceso()
            if hasattr(v, "txtIdUsuario"):
                v.txtIdUsuario.clear()
        else:
            QMessageBox.warning(v, "Error", mensaje)

    def _cargar_historial_acceso(self):
        v = self.ventana_acceso
        if not hasattr(v, "tablaAcceso"):
            return
        registros = self.modelo.obtener_historial_accesos(limite=50)
        _rellenar_tabla(
            v.tablaAcceso, registros,
            ["ID", "Nombre usuario", "Tipo", "Fecha y hora"],
            ["id_registro", "nombre", "tipo_acceso", "fecha_hora_registro"],
        )

    # ------------------------------------------------------------------
    def _cerrar_sesion(self):
        self.ventana.close()
        self.ctrl_principal.cerrar_sesion()


# ── Helpers de módulo ──────────────────────────────────────────────────

def _get_text(ventana, nombre_widget):
    widget = getattr(ventana, nombre_widget, None)
    return widget.text().strip() if widget else ""


def _get_date(ventana, nombre_widget):
    widget = getattr(ventana, nombre_widget, None)
    if widget is None:
        return ""
    return widget.date().toPyDate().isoformat()


def _set_text(ventana, nombre_widget, valor):
    widget = getattr(ventana, nombre_widget, None)
    if widget:
        widget.setText(str(valor))


def _toggle_password(ventana, nombre_widget):
    widget = getattr(ventana, nombre_widget, None)
    if widget is None:
        return
    if widget.echoMode() == QLineEdit.Password:
        widget.setEchoMode(QLineEdit.Normal)
    else:
        widget.setEchoMode(QLineEdit.Password)


def _rellenar_tabla(tabla, datos, cabeceras, campos):
    tabla.setColumnCount(len(cabeceras))
    tabla.setHorizontalHeaderLabels(cabeceras)
    tabla.setRowCount(len(datos))
    for fila_idx, fila in enumerate(datos):
        for col_idx, campo in enumerate(campos):
            tabla.setItem(fila_idx, col_idx,
                          QTableWidgetItem(str(fila.get(campo, ""))))
    tabla.resizeColumnsToContents()
