import os
from src.vista.componentes import CargadorVista, MensajeView, TablaView


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
        self.ventana = CargadorVista.cargar(ruta)
        self.conectar_botones()
        self.cargar_datos()
        self.ventana.show()

    def conectar_botones(self):
        v = self.ventana

        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(self.cerrar_sesion)
        if hasattr(v, "btnInicio"):
            v.btnInicio.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista.ui"))
        if hasattr(v, "btnClientes"):
            v.btnClases.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_clientes.ui"))
        if hasattr(v, "btnRegistroUsuario"):
            v.btnInscripciones.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_registrar_usuario.ui"))
        if hasattr(v, "btnControlAcceso"):
            v.btnPagos.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_control_de_acceso.ui"))
        if hasattr(v, "btnPerfil"):
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
        if hasattr(v, "lblNumClientes") and hasattr(v, "tablaUltimosRegistros"):
            try:
                self.cargar_inicio_recepcionista()
                return
            except Exception as e:
                print(f"Error inicio recepcionista: {e}")

    def registrar_acceso(self, tipo):
        v = self.ventana
        try:
            campo = None
            for nombre in ("lineEdit", "txtId", "txtUsuario"):
                if hasattr(v, nombre):
                    campo = getattr(v, nombre)
                    break
            if not campo or not campo.text().strip():
                MensajeView.warning(v, "Error", "Introduce el ID del usuario")
                return
            id_usuario = int(campo.text().strip())
            self.modelo.registrar_acceso(id_usuario, tipo)
            MensajeView.information(v, "Correcto", f"{'Entrada' if tipo == 'entrada' else 'Salida'} registrada")
            self.cargar_datos()
        except ValueError:
            MensajeView.warning(v, "Error", "El ID debe ser un número")
        except Exception as e:
            MensajeView.warning(v, "Error", str(e))

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
                MensajeView.warning(v, "Error", "DNI, usuario y contraseña son obligatorios")
                return

            self.modelo.registrar_usuario(
                vals[0], vals[1], vals[2], vals[3],
                vals[6], vals[7], 1, vals[4], vals[5]
            )
            MensajeView.information(v, "Correcto", "Cliente registrado correctamente")
        except Exception as e:
            MensajeView.warning(v, "Error", str(e))

    def actualizar_cliente(self):
        v = self.ventana
        try:
            tabla = v.tableWidget if hasattr(v, "tableWidget") else None
            if not tabla:
                return
            fila = tabla.currentRow()
            if fila < 0:
                MensajeView.warning(v, "Error", "Selecciona un cliente")
                return
            id_cliente = int(tabla.item(fila, 0).text())
            telefono = v.txtTelefono.text().strip() if hasattr(v, "txtTelefono") else ""
            email    = v.txtEmail.text().strip()    if hasattr(v, "txtEmail")    else ""
            direccion= v.txtDireccion.text().strip() if hasattr(v, "txtDireccion") else ""
            self.modelo.modificar_usuario(id_cliente, telefono, email, direccion)
            MensajeView.information(v, "Correcto", "Cliente actualizado")
            self.cargar_datos()
        except Exception as e:
            MensajeView.warning(v, "Error", str(e))

    def rellenar_tabla(self, tabla, datos):
        tabla.setRowCount(len(datos))
        if datos:
            tabla.setColumnCount(len(datos[0]))
        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro):
                tabla.setItem(fila, col, TablaView.crear_item(str(valor) if valor is not None else ""))

    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()

    def cargar_inicio_recepcionista(self):
        v = self.ventana

        if hasattr(v, "lblNumClientes"):
            v.lblNumClientes.setText(str(self.modelo.recepcion_total_clientes()))

        if hasattr(v, "lblNumEntradas"):
            v.lblNumEntradas.setText(str(self.modelo.recepcion_entradas_hoy()))

        if hasattr(v, "lblNuevosUsuarios"):
            v.lblNuevosUsuarios.setText(str(self.modelo.recepcion_nuevos_usuarios_hoy()))

        if hasattr(v, "lblNumClasesHoy"):
            v.lblNumClasesHoy.setText(str(self.modelo.recepcion_clases_hoy()))

        if hasattr(v, "tablaUltimosRegistros"):
            datos = self.modelo.recepcion_ultimos_registros_acceso()
            self._rellenar_tabla_ultimos_registros(v.tablaUltimosRegistros, datos)

        if hasattr(v, "tablaClientesRecientes"):
            datos = self.modelo.recepcion_clientes_recientes()
            self._rellenar_tabla_clientes_recientes(v.tablaClientesRecientes, datos)


    def _rellenar_tabla_ultimos_registros(self, tabla, datos):
        cabeceras = ["Cliente", "DNI", "Tipo acceso", "Fecha y hora"]

        TablaView.configurar_columnas(tabla, cabeceras)
        tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras)
        tabla.setRowCount(len(datos))
        tabla.setSelectionBehavior(tabla.SelectRows)

        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro[:len(cabeceras)]):
                item = TablaView.crear_item(
                    str(valor) if valor is not None else "",
                    editable=False
                )
                tabla.setItem(fila, col, item)


    def _rellenar_tabla_clientes_recientes(self, tabla, datos):
        cabeceras = ["Cliente", "DNI", "Teléfono", "Fecha registro"]

        TablaView.configurar_columnas(tabla, cabeceras)
        tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras)
        tabla.setRowCount(len(datos))
        tabla.setSelectionBehavior(tabla.SelectRows)

        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro[:len(cabeceras)]):
                item = TablaView.crear_item(
                    str(valor) if valor is not None else "",
                    editable=False
                )
                tabla.setItem(fila, col, item)
