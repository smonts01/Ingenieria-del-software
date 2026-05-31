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
            v.btnClientes.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_clientes.ui"))

        if hasattr(v, "btnRegistroUsuario"):
            v.btnRegistroUsuario.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_registrar_usuario.ui"))

        if hasattr(v, "btnControlAcceso"):
            v.btnControlAcceso.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_control_de_acceso.ui"))

        if hasattr(v, "btnPerfil"):
            v.btnPerfil.clicked.connect(lambda: self.abrir_pantalla("interfaz_recepcionista_perfil.ui"))

        # Control de acceso
        if hasattr(v, "txtDNIoID"):
            v.txtDNIoID.textChanged.connect(self.buscar_cliente_control_acceso)

        if hasattr(v, "btnEntrada"):
            v.btnEntrada.clicked.connect(lambda: self.registrar_acceso_control("entrada"))

        if hasattr(v, "btnSalida"):
            v.btnSalida.clicked.connect(lambda: self.registrar_acceso_control("salida"))

        if hasattr(v, "btnInicio_20"):
            v.btnInicio_20.clicked.connect(self.registrar_cliente)

        # Actualizar cliente
        if hasattr(v, "btnActualizar"):
            v.btnActualizar.clicked.connect(self.actualizar_cliente)

    def cargar_datos(self):
        v = self.ventana

        # Inicio recepcionista
        if hasattr(v, "lblNumClientes") and hasattr(v, "tablaUltimosRegistros"):
            try:
                self.cargar_inicio_recepcionista()
                return
            except Exception as e:
                print(f"Error inicio recepcionista: {e}")


        # Pantalla control de acceso
        if hasattr(v, "txtDNIoID") and hasattr(v, "tableAccesos"):
            try:
                self.limpiar_cliente_control_acceso()
                datos = self.modelo.listar_ultimos_accesos_control()
                self._rellenar_tabla_accesos_control(v.tableAccesos, datos)
                return
            except Exception as e:
                print(f"Error control acceso recepcionista: {e}")

        # Otras pantallas
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
            dni = v.DNI.text().strip() if hasattr(v, "DNI") else ""
            nombre = v.NombreCompleto.text().strip() if hasattr(v, "NombreCompleto") else ""
            telefono = v.Telefono.text().strip() if hasattr(v, "Telefono") else ""
            direccion = v.Direccion.text().strip() if hasattr(v, "Direccion") else ""
            email = v.Email.text().strip() if hasattr(v, "Email") else ""
            fecha = v.Nacimiento.text().strip() if hasattr(v, "Nacimiento") else ""

            username = v.Usuario.text().strip() if hasattr(v, "Usuario") else ""
            password = v.Contrasea.text().strip() if hasattr(v, "Contrasea") else ""
            confirmar = v.ConfirmarContrasea.text().strip() if hasattr(v, "ConfirmarContrasea") else ""

            es_adulto = v.ButtomAdulto.isChecked() if hasattr(v, "ButtomAdulto") else False
            es_menor = v.ButtomMenor.isChecked() if hasattr(v, "ButtomMenor") else False

            dni_tutor = v.DNITutor.text().strip() if hasattr(v, "DNITutor") else ""
            nombre_tutor = v.NombreTutor.text().strip() if hasattr(v, "NombreTutor") else ""

            if not all([dni, nombre, telefono, direccion, email, fecha, username, password, confirmar]):
                MensajeView.warning(v, "Error", "Completa todos los datos obligatorios")
                return

            if password != confirmar:
                MensajeView.warning(v, "Error", "Las contraseñas no coinciden")
                return

            if len(password) < 4:
                MensajeView.warning(v, "Error", "La contraseña debe tener al menos 4 caracteres")
                return

            if not es_adulto and not es_menor:
                MensajeView.warning(v, "Error", "Selecciona si el cliente es adulto o menor")
                return

            if es_menor and not all([dni_tutor, nombre_tutor]):
                MensajeView.warning(v, "Error", "Para registrar un menor debes indicar DNI tutor y nombre tutor")
                return

            from datetime import datetime

            try:
                fecha_bd = datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                try:
                    fecha_bd = datetime.strptime(fecha, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    MensajeView.warning(v, "Error", "Formato de fecha incorrecto. Usa DD/MM/YYYY")
                    return

            id_cliente = self.modelo.crear_cliente_desde_recepcion(
                dni=dni,
                nombre=nombre,
                telefono=telefono,
                email=email,
                username=username,
                password=password,
                direccion=direccion,
                fecha_nacimiento=fecha_bd,
                es_menor=es_menor,
                dni_tutor=dni_tutor,
                nombre_tutor=nombre_tutor
            )

            MensajeView.information(v, "Correcto", f"Cliente registrado correctamente con ID {id_cliente}")

            for campo in [
                "DNI", "NombreCompleto", "Telefono", "Direccion", "Email", "Nacimiento",
                "Usuario", "Contrasea", "ConfirmarContrasea", "DNITutor", "NombreTutor"
            ]:
                if hasattr(v, campo):
                    getattr(v, campo).clear()

            if hasattr(v, "ButtomAdulto"):
                v.ButtomAdulto.setChecked(False)

            if hasattr(v, "ButtomMenor"):
                v.ButtomMenor.setChecked(False)

            self.cargar_datos()

        except Exception as e:
            MensajeView.warning(v, "Error", f"Error al registrar cliente: {str(e)}")

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


    def limpiar_cliente_control_acceso(self):
        v = self.ventana

        if hasattr(v, "lblNombre"):
            v.lblNombre.setText("Cliente no seleccionado")

        if hasattr(v, "lblDNI"):
            v.lblDNI.setText("DNI: -")

        if hasattr(v, "lblID"):
            v.lblID.setText("ID: -")

        if hasattr(v, "lblEstado"):
            v.lblEstado.setText("Estado pago: -")

        self.cliente_control_actual = None


    def buscar_cliente_control_acceso(self):
        v = self.ventana

        if not hasattr(v, "txtDNIoID"):
            return

        texto = v.txtDNIoID.text().strip()

        if not texto:
            self.limpiar_cliente_control_acceso()
            return

        try:
            cliente = self.modelo.buscar_cliente_acceso_por_dni_o_id(texto)

            if not cliente:
                self.cliente_control_actual = None

                if hasattr(v, "lblNombre"):
                    v.lblNombre.setText("Cliente no encontrado")
                if hasattr(v, "lblDNI"):
                    v.lblDNI.setText("DNI: -")
                if hasattr(v, "lblID"):
                    v.lblID.setText("ID: -")
                if hasattr(v, "lblEstado"):
                    v.lblEstado.setText("")

                return

            id_usuario = cliente[0]
            dni = cliente[1]
            nombre = cliente[2]
            estado_pago = cliente[3]

            self.cliente_control_actual = {
                "id_usuario": id_usuario,
                "dni": dni,
                "nombre": nombre,
                "estado_pago": estado_pago
            }

            if hasattr(v, "lblNombre"):
                v.lblNombre.setText(str(nombre))

            if hasattr(v, "lblDNI"):
                v.lblDNI.setText(f"DNI: {dni}")

            if hasattr(v, "lblID"):
                v.lblID.setText(f"ID: {id_usuario}")

            if hasattr(v, "lblEstado"):
                v.lblEstado.setText(str(estado_pago))

        except Exception as e:
            print(f"Error buscar cliente control acceso: {e}")


    def registrar_acceso_control(self, tipo_acceso):
        v = self.ventana

        if not hasattr(self, "cliente_control_actual") or not self.cliente_control_actual:
            MensajeView.warning(v, "Error", "Primero busca un cliente por DNI o ID")
            return

        try:
            id_usuario = self.cliente_control_actual["id_usuario"]

            self.modelo.registrar_acceso_cliente_control(id_usuario, tipo_acceso)

            MensajeView.information(
                v,
                "Correcto",
                f"{'Entrada' if tipo_acceso == 'entrada' else 'Salida'} registrada correctamente"
            )

            datos = self.modelo.listar_ultimos_accesos_control()

            if hasattr(v, "tableAccesos"):
                self._rellenar_tabla_accesos_control(v.tableAccesos, datos)

        except Exception as e:
            MensajeView.warning(v, "Error", str(e))


    def _rellenar_tabla_accesos_control(self, tabla, datos):
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