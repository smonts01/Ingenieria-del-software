import os
from datetime import datetime
from src.vista.componentes import CargadorVista, MensajeView, TablaView


class ControladorRecepcionista:
    """Controlador de las pantallas del perfil recepcionista.

    Responsabilidad MVC: gestiona eventos de la vista y delega la lógica de
    negocio en self.modelo (capa Logica). No accede a DAO ni ejecuta SQL.
    """

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None
        self.cliente_control_actual = None

    def abrir(self):
        self.abrir_pantalla("interfaz_recepcionista.ui")

    def abrir_pantalla(self, archivo):
        if self.ventana:
            self.ventana.close()
        ruta = os.path.join(self.ruta_ui, archivo)
        self.ventana = CargadorVista.cargar(ruta)
        self.marcar_boton_activo(archivo)
        self.conectar_botones()
        self.cargar_datos()
        self.ventana.show()

    def conectar_botones(self):
        v = self.ventana

        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(self.cerrar_sesion)

        self._conectar_navegacion(v)

        # Registrar usuario / cliente
        boton_registrar = self._buscar_widget("btnInicio_20", "btnInicio_2", "btnRegistrar", "btnConfirmar")
        if boton_registrar and (self._buscar_widget("DNI", "lineEdit") is not None):
            boton_registrar.clicked.connect(self.registrar_cliente)

        # Control de acceso
        buscador_acceso = self._buscar_widget("txtDNIoID", "lineEdit")
        if buscador_acceso and self._buscar_tabla_accesos() is not None:
            buscador_acceso.textChanged.connect(self.buscar_cliente_control_acceso)

        boton_entrada = self._buscar_widget("btnEntrada", "btnInicio_3")
        if boton_entrada and self._buscar_tabla_accesos() is not None:
            boton_entrada.clicked.connect(lambda: self.registrar_acceso_control("entrada"))

        boton_salida = self._buscar_widget("btnSalida", "btnInicio_4")
        if boton_salida and self._buscar_tabla_accesos() is not None:
            boton_salida.clicked.connect(lambda: self.registrar_acceso_control("salida"))

        # Clientes recepcionista
        buscador_clientes = self._buscar_widget("lblBuscarDNI", "lineEdit")
        if buscador_clientes and self._buscar_tabla_clientes() is not None:
            buscador_clientes.textChanged.connect(self.filtrar_clientes_recepcionista)

        combo_tipo = self._buscar_widget("comboBox_adultomenor", "comboBox_2")
        if combo_tipo and self._buscar_tabla_clientes() is not None:
            if combo_tipo.count() == 0:
                combo_tipo.addItems(["Todos", "Adulto", "Menor"])
            combo_tipo.currentIndexChanged.connect(self.filtrar_clientes_recepcionista)

        combo_plan = self._buscar_widget("comboBox_plan", "comboBox_3")
        if combo_plan and self._buscar_tabla_clientes() is not None:
            if combo_plan.count() == 0:
                combo_plan.addItems(["Todos", "Basico", "Premium"])
            combo_plan.currentIndexChanged.connect(self.filtrar_clientes_recepcionista)

        boton_cambios = self._buscar_widget("btnCambios", "btnInicio_5")
        if boton_cambios and self._buscar_tabla_clientes() is not None:
            boton_cambios.clicked.connect(self.guardar_cambios_clientes_recepcionista)

        if hasattr(v, "btnActualizar"):
            v.btnActualizar.clicked.connect(self.actualizar_cliente)

    def _conectar_navegacion(self, v):
        conexiones = {
            "btnInicio": "interfaz_recepcionista.ui",
            "btnInicio_2": "interfaz_recepcionista.ui",
            "btnInicio_3": "interfaz_recepcionista.ui",
            "btnInicio_5": "interfaz_recepcionista.ui",
            "btnRegistroUsuario": "interfaz_recepcionista_registrar_usuario.ui",
            "btnControlAcceso": "interfaz_recepcionista_control_de_acceso.ui",
            "btnClientes": "interfaz_recepcionista_clientes.ui",
            "btnPerfil": "interfaz_recepcionista_perfil.ui",
        }
        # Solo conectamos los botones de menú. Los botones btnInicio_2/3/5 también
        # existen como acciones en algunas pantallas, por eso comprobamos contexto.
        if hasattr(v, "btnInicio"):
            v.btnInicio.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista.ui"))
        if hasattr(v, "btnRegistroUsuario"):
            v.btnRegistroUsuario.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_registrar_usuario.ui"))
        if hasattr(v, "btnControlAcceso"):
            v.btnControlAcceso.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_control_de_acceso.ui"))
        if hasattr(v, "btnClientes"):
            v.btnClientes.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_clientes.ui"))
        if hasattr(v, "btnPerfil"):
            v.btnPerfil.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_perfil.ui"))

        # Menú en UI antiguas donde el botón de inicio no se llama btnInicio
        if hasattr(v, "btnInicio_2") and self._buscar_tabla_clientes() is not None:
            v.btnInicio_2.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista.ui"))
        if hasattr(v, "btnInicio_3") and self._buscar_widget("lineEdit_7") is not None:
            v.btnInicio_3.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista.ui"))
        if hasattr(v, "btnInicio_5") and self._buscar_tabla_accesos() is not None:
            v.btnInicio_5.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista.ui"))

    def marcar_boton_activo(self, archivo):
        v = self.ventana
        mapa = {
            "interfaz_recepcionista.ui": "btnInicio",
            "interfaz_recepcionista_registrar_usuario.ui": "btnRegistroUsuario",
            "interfaz_recepcionista_control_de_acceso.ui": "btnControlAcceso",
            "interfaz_recepcionista_clientes.ui": "btnClientes",
            "interfaz_recepcionista_perfil.ui": "btnPerfil",
        }
        for nombre in ["btnInicio", "btnRegistroUsuario", "btnControlAcceso", "btnClientes", "btnPerfil"]:
            if hasattr(v, nombre):
                btn = getattr(v, nombre)
                btn.setCheckable(True)
                btn.setChecked(nombre == mapa.get(archivo))

    def cargar_datos(self):
        v = self.ventana

        if hasattr(v, "lblNumClientes") and hasattr(v, "tablaUltimosRegistros"):
            self.cargar_inicio_recepcionista()
            return

        if self._buscar_tabla_accesos() is not None and self._buscar_widget("txtDNIoID", "lineEdit") is not None:
            self.limpiar_cliente_control_acceso()
            datos = self.modelo.listar_ultimos_accesos_control()
            self._rellenar_tabla_accesos_control(self._buscar_tabla_accesos(), datos)
            return

        if self._buscar_tabla_clientes() is not None and self._buscar_widget("comboBox_adultomenor", "comboBox_2") is not None:
            self.cargar_clientes_recepcionista()
            return

        if hasattr(v, "label_Nombre") and hasattr(v, "label_7"):
            self.cargar_perfil_recepcionista()
            return

        if hasattr(v, "tableWidget"):
            self.rellenar_tabla(v.tableWidget, self.modelo.listar_clientes())

    # ── Helpers para compatibilidad con nombres antiguos/nuevos de .ui ─────
    def _buscar_widget(self, *nombres):
        for nombre in nombres:
            if hasattr(self.ventana, nombre):
                return getattr(self.ventana, nombre)
        return None

    def _texto(self, *nombres):
        w = self._buscar_widget(*nombres)
        return w.text().strip() if w is not None else ""

    def _buscar_tabla_clientes(self):
        return self._buscar_widget("tablaClientes", "tableWidget")

    def _buscar_tabla_accesos(self):
        return self._buscar_widget("tableAccesos", "tableWidget")

    # ── Inicio recepcionista ───────────────────────────────────────────────
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
            self._rellenar_tabla_ultimos_registros(v.tablaUltimosRegistros, self.modelo.recepcion_ultimos_registros_acceso())
        if hasattr(v, "tablaClientesRecientes"):
            self._rellenar_tabla_clientes_recientes(v.tablaClientesRecientes, self.modelo.recepcion_clientes_recientes())

    # ── Alta cliente ──────────────────────────────────────────────────────
    def registrar_cliente(self):
        v = self.ventana
        try:
            dni = self._texto("DNI", "txtDni", "lineEdit")
            nombre = self._texto("NombreCompleto", "txtNombre", "lineEdit_5")
            telefono = self._texto("Telefono", "txtTelefono", "lineEdit_2")
            direccion = self._texto("Direccion", "txtDireccion", "lineEdit_3")
            email = self._texto("Email", "txtEmail", "lineEdit_6")
            fecha = self._texto("Nacimiento", "txtFecha", "lineEdit_4")
            username = self._texto("Usuario", "txtUsuario", "lineEdit_7")
            password = self._texto("Contrasea", "txtPassword", "lineEdit_8")
            confirmar = self._texto("ConfirmarContrasea", "lineEdit_9")
            dni_tutor = self._texto("DNITutor", "lineEdit_13")
            nombre_tutor = self._texto("NombreTutor", "lineEdit_15")

            adulto = self._buscar_widget("ButtomAdulto", "radioButton")
            menor = self._buscar_widget("ButtomMenor", "radioButton_2")
            es_menor = menor.isChecked() if menor else False
            es_adulto = adulto.isChecked() if adulto else False

            if not all([dni, nombre, telefono, direccion, email, fecha, username, password, confirmar]):
                MensajeView.warning(v, "Error", "Completa todos los datos obligatorios")
                return
            if password != confirmar:
                MensajeView.warning(v, "Error", "Las contraseñas no coinciden")
                return
            if not es_adulto and not es_menor:
                MensajeView.warning(v, "Error", "Selecciona si el cliente es adulto o menor")
                return

            try:
                fecha_bd = datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                fecha_bd = datetime.strptime(fecha, "%Y-%m-%d").strftime("%Y-%m-%d")

            id_cliente = self.modelo.crear_cliente_desde_recepcion(
                dni, nombre, telefono, email, username, password, direccion,
                fecha_bd, es_menor, dni_tutor, nombre_tutor
            )
            MensajeView.information(v, "Correcto", f"Cliente registrado correctamente con ID {id_cliente}")
            for nombre_widget in ["DNI", "NombreCompleto", "Telefono", "Direccion", "Email", "Nacimiento",
                                  "Usuario", "Contrasea", "ConfirmarContrasea", "DNITutor", "NombreTutor",
                                  "lineEdit", "lineEdit_2", "lineEdit_3", "lineEdit_4", "lineEdit_5",
                                  "lineEdit_6", "lineEdit_7", "lineEdit_8", "lineEdit_9", "lineEdit_13", "lineEdit_15"]:
                w = self._buscar_widget(nombre_widget)
                if w: w.clear()
        except Exception as e:
            MensajeView.warning(v, "Error", f"Error al registrar cliente: {str(e)}")

    # ── Control de acceso ─────────────────────────────────────────────────
    def limpiar_cliente_control_acceso(self):
        self.cliente_control_actual = None
        self._set_label(("lblNombre", "lblNombreCliente_8"), "Cliente no seleccionado")
        self._set_label(("lblDNI", "lblNombreCliente_9"), "DNI: -")
        self._set_label(("lblID", "lblNombreCliente_10"), "ID: -")
        self._set_label(("lblEstado", "btnCalorias_2"), "-")

    def buscar_cliente_control_acceso(self):
        texto = self._texto("txtDNIoID", "lineEdit")
        if not texto:
            self.limpiar_cliente_control_acceso()
            return
        cliente = self.modelo.buscar_cliente_acceso_por_dni_o_id(texto)
        if not cliente:
            self.cliente_control_actual = None
            self._set_label(("lblNombre", "lblNombreCliente_8"), "Cliente no encontrado")
            self._set_label(("lblDNI", "lblNombreCliente_9"), "DNI: -")
            self._set_label(("lblID", "lblNombreCliente_10"), "ID: -")
            self._set_label(("lblEstado", "btnCalorias_2"), "-")
            return

        id_usuario, dni, nombre, estado_pago = cliente
        self.cliente_control_actual = {"id_usuario": id_usuario, "dni": dni, "nombre": nombre, "estado_pago": estado_pago}
        self._set_label(("lblNombre", "lblNombreCliente_8"), str(nombre))
        self._set_label(("lblDNI", "lblNombreCliente_9"), f"DNI: {dni}")
        self._set_label(("lblID", "lblNombreCliente_10"), f"ID: {id_usuario}")
        self._set_label(("lblEstado", "btnCalorias_2"), str(estado_pago))

    def registrar_acceso_control(self, tipo_acceso):
        v = self.ventana
        if not self.cliente_control_actual:
            MensajeView.warning(v, "Error", "Primero busca un cliente por DNI o ID")
            return
        try:
            self.modelo.registrar_acceso_cliente_control(self.cliente_control_actual["id_usuario"], tipo_acceso)
            MensajeView.information(v, "Correcto", f"{tipo_acceso.capitalize()} registrada correctamente")
            tabla = self._buscar_tabla_accesos()
            if tabla:
                self._rellenar_tabla_accesos_control(tabla, self.modelo.listar_ultimos_accesos_control())
        except Exception as e:
            MensajeView.warning(v, "Error", str(e))

    # ── Clientes recepcionista ────────────────────────────────────────────
    def cargar_clientes_recepcionista(self):
        self._set_label(("lblTotalClientes", "lblNombreCliente_14", "lblNombreCliente_24"), str(self.modelo.recepcion_total_clientes_lista()))
        self._set_label(("lblNuevosMes", "lblNombreCliente_22"), str(self.modelo.recepcion_nuevos_clientes_mes()))
        self.filtrar_clientes_recepcionista()

    def filtrar_clientes_recepcionista(self):
        tabla = self._buscar_tabla_clientes()
        if tabla is None:
            return
        dni = self._texto("lblBuscarDNI", "lineEdit")
        combo_tipo = self._buscar_widget("comboBox_adultomenor", "comboBox_2")
        combo_plan = self._buscar_widget("comboBox_plan", "comboBox_3")
        tipo = combo_tipo.currentText().strip() if combo_tipo else "Todos"
        plan = combo_plan.currentText().strip() if combo_plan else "Todos"
        datos = self.modelo.recepcion_listar_clientes_filtrados(dni, tipo, plan)
        self._rellenar_tabla_clientes_recepcionista(tabla, datos)

    def guardar_cambios_clientes_recepcionista(self):
        v = self.ventana
        tabla = self._buscar_tabla_clientes()
        if tabla is None:
            return
        try:
            for fila in range(tabla.rowCount()):
                id_item = tabla.item(fila, 0)
                if not id_item or not id_item.text().strip():
                    continue
                id_cliente = int(id_item.text().strip())
                valores = []
                for col in range(1, 8):
                    item = tabla.item(fila, col)
                    valores.append(item.text().strip() if item else "")
                dni, nombre, telefono, email, direccion, nacimiento, estado_pago = valores
                self.modelo.recepcion_guardar_cambios_cliente(
                    id_cliente, dni, nombre, telefono, email, direccion, nacimiento, estado_pago
                )
            MensajeView.information(v, "Correcto", "Cambios de clientes guardados correctamente")
            self.filtrar_clientes_recepcionista()
        except Exception as e:
            MensajeView.warning(v, "Error", f"Error al guardar cambios: {str(e)}")

    # ── Perfil recepcionista ──────────────────────────────────────────────
    def cargar_perfil_recepcionista(self):
        perfil = self.modelo.perfil_usuario(self.usuario["id_usuario"])
        if not perfil:
            return
        self._set_label(("label_Nombre",), str(perfil[2]))
        self._set_label(("label_7",), str(perfil[4]))
        self._set_label(("label_9",), str(perfil[1]))
        self._set_label(("label_16",), str(perfil[7]))

    # ── Funciones antiguas mantenidas para compatibilidad ────────────────
    def registrar_acceso(self, tipo):
        return self.registrar_acceso_control(tipo)

    def actualizar_cliente(self):
        self.guardar_cambios_clientes_recepcionista()

    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()

    # ── Relleno de tablas / labels ───────────────────────────────────────
    def _set_label(self, nombres, texto):
        for nombre in nombres:
            if hasattr(self.ventana, nombre):
                getattr(self.ventana, nombre).setText(texto)
                return

    def rellenar_tabla(self, tabla, datos):
        tabla.setRowCount(len(datos))
        if datos:
            tabla.setColumnCount(len(datos[0]))
        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro):
                tabla.setItem(fila, col, TablaView.crear_item(str(valor) if valor is not None else ""))

    def _rellenar_tabla_ultimos_registros(self, tabla, datos):
        self._rellenar_tabla_generica(tabla, ["Cliente", "DNI", "Tipo acceso", "Fecha y hora"], datos, editable=False)

    def _rellenar_tabla_clientes_recientes(self, tabla, datos):
        self._rellenar_tabla_generica(tabla, ["Cliente", "DNI", "Teléfono", "Fecha registro"], datos, editable=False)

    def _rellenar_tabla_accesos_control(self, tabla, datos):
        self._rellenar_tabla_generica(tabla, ["Cliente", "DNI", "Tipo acceso", "Fecha y hora"], datos, editable=False)

    def _rellenar_tabla_clientes_recepcionista(self, tabla, datos):
        cabeceras = ["ID", "DNI", "Nombre", "Teléfono", "Email", "Dirección", "Nacimiento", "Estado pago", "Tipo", "Plan"]
        TablaView.configurar_columnas(tabla, cabeceras)
        tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras)
        tabla.setRowCount(len(datos))
        tabla.setEditTriggers(tabla.DoubleClicked | tabla.SelectedClicked)
        tabla.setSelectionBehavior(tabla.SelectRows)
        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro[:len(cabeceras)]):
                item = TablaView.crear_item(str(valor) if valor is not None else "", editable=(col not in (0, 8, 9)))
                tabla.setItem(fila, col, item)

    def _rellenar_tabla_generica(self, tabla, cabeceras, datos, editable=False):
        TablaView.configurar_columnas(tabla, cabeceras)
        tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras)
        tabla.setRowCount(len(datos))
        tabla.setSelectionBehavior(tabla.SelectRows)
        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro[:len(cabeceras)]):
                tabla.setItem(fila, col, TablaView.crear_item(str(valor) if valor is not None else "", editable=editable))
