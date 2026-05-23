import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem


class ControladorRecepcionista:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None

    def abrir(self):
        self.abrir_pantalla("interfaz_recepcionista.ui")

    def abrir_pantalla(self, archivo):
        if self.ventana:
            self.ventana.close()
        ruta = os.path.join(self.ruta_ui, archivo)
        self.ventana = uic.loadUi(ruta)
        self.conectar_botones()
        self.cargar_datos()
        self.ventana.show()

    def conectar_botones(self):
        v = self.ventana

        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(self.cerrar_sesion)
        if hasattr(v, "btnInicio"):
            v.btnInicio.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista.ui"))
        if hasattr(v, "btnClases"):
            v.btnClases.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_clientes.ui"))
        if hasattr(v, "btnInscripciones"):
            v.btnInscripciones.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_registrar_usuario.ui"))
        if hasattr(v, "btnPagos"):
            v.btnPagos.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_control_de_acceso.ui"))
        if hasattr(v, "btnOcupacion"):
            v.btnOcupacion.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_perfil.ui"))
        if hasattr(v, "btnInicio_4"):
            v.btnInicio_4.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_registrar_usuario.ui"))
        if hasattr(v, "btnInicio_5"):
            v.btnInicio_5.clicked.connect(self.cargar_datos)
        # Control de acceso
        if hasattr(v, "btnInicio_2"):
            v.btnInicio_2.clicked.connect(lambda: self.registrar_acceso("entrada"))
        if hasattr(v, "btnInicio_3"):
            v.btnInicio_3.clicked.connect(lambda: self.registrar_acceso("salida"))
        # Registrar cliente
        if hasattr(v, "btnRegistrar") or hasattr(v, "btnConfirmar"):
            btn = getattr(v, "btnRegistrar", None) or getattr(v, "btnConfirmar", None)
            btn.clicked.connect(self.registrar_cliente)
        # Actualizar cliente
        if hasattr(v, "btnActualizar"):
            v.btnActualizar.clicked.connect(self.actualizar_cliente)

    def cargar_datos(self):
        v = self.ventana

        if hasattr(v, "tablaProximasClases"):
            self.rellenar_tabla(v.tablaProximasClases, self.modelo.listar_clases())
        if hasattr(v, "tablaProximasClases_2"):
            self.rellenar_tabla(v.tablaProximasClases_2, self.modelo.pagos_pendientes())
        if hasattr(v, "tableWidget"):
            titulo = v.windowTitle().lower() if v.windowTitle() else ""
            if "control" in titulo or "acceso" in titulo:
                datos = self.modelo.listar_accesos()
            else:
                datos = self.modelo.listar_clientes()
            self.rellenar_tabla(v.tableWidget, datos)

    def registrar_acceso(self, tipo):
        v = self.ventana
        try:
            campo = None
            for nombre in ("lineEdit", "txtId", "txtUsuario"):
                if hasattr(v, nombre):
                    campo = getattr(v, nombre)
                    break
            if not campo or not campo.text().strip():
                QMessageBox.warning(v, "Error", "Introduce el ID del usuario")
                return
            id_usuario = int(campo.text().strip())
            self.modelo.registrar_acceso(id_usuario, tipo)
            QMessageBox.information(v, "Correcto", f"{'Entrada' if tipo == 'entrada' else 'Salida'} registrada")
            self.cargar_datos()
        except ValueError:
            QMessageBox.warning(v, "Error", "El ID debe ser un número")
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def registrar_cliente(self):
        v = self.ventana
        try:
            campos = {}
            for nombre in ("lineEdit", "lineEdit_2", "lineEdit_3", "lineEdit_4",
                           "lineEdit_5", "lineEdit_6", "lineEdit_7", "lineEdit_8"):
                if hasattr(v, nombre):
                    campos[nombre] = getattr(v, nombre).text().strip()

            # Try named fields first
            dni      = getattr(v, "txtDni",      None)
            nombre   = getattr(v, "txtNombre",    None)
            telefono = getattr(v, "txtTelefono",  None)
            email    = getattr(v, "txtEmail",     None)
            direccion= getattr(v, "txtDireccion", None)
            fecha    = getattr(v, "txtFecha",     None)
            username = getattr(v, "txtUsuario",   None)
            password = getattr(v, "txtPassword",  None)

            vals = [x.text().strip() if x else "" for x in
                    [dni, nombre, telefono, email, direccion, fecha, username, password]]

            if not all(vals):
                # fallback to lineEdits
                vals_list = list(campos.values())
                while len(vals_list) < 8:
                    vals_list.append("")
                vals = vals_list

            if not vals[0] or not vals[6] or not vals[7]:
                QMessageBox.warning(v, "Error", "DNI, usuario y contraseña son obligatorios")
                return

            self.modelo.registrar_usuario(
                vals[0], vals[1], vals[2], vals[3],
                vals[6], vals[7], 1, vals[4], vals[5]
            )
            QMessageBox.information(v, "Correcto", "Cliente registrado correctamente")
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def actualizar_cliente(self):
        v = self.ventana
        try:
            tabla = v.tableWidget if hasattr(v, "tableWidget") else None
            if not tabla:
                return
            fila = tabla.currentRow()
            if fila < 0:
                QMessageBox.warning(v, "Error", "Selecciona un cliente")
                return
            id_cliente = int(tabla.item(fila, 0).text())
            telefono = v.txtTelefono.text().strip() if hasattr(v, "txtTelefono") else ""
            email    = v.txtEmail.text().strip()    if hasattr(v, "txtEmail")    else ""
            direccion= v.txtDireccion.text().strip() if hasattr(v, "txtDireccion") else ""
            self.modelo.modificar_usuario(id_cliente, telefono, email, direccion)
            QMessageBox.information(v, "Correcto", "Cliente actualizado")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def rellenar_tabla(self, tabla, datos):
        tabla.setRowCount(len(datos))
        if datos:
            tabla.setColumnCount(len(datos[0]))
        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro):
                tabla.setItem(fila, col, QTableWidgetItem(str(valor) if valor is not None else ""))

    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()
