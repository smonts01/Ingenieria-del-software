import os
from src.vista.componentes import CargadorVista, MensajeView, TablaView, ImagenView


class ControladorAdministrador:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None

    def abrir(self):
        self.abrir_pantalla("interfaz_admin_inicio.ui")

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

        # Menú lateral
        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(self.cerrar_sesion)
        if hasattr(v, "btnInicio"):
            v.btnInicio.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_inicio.ui"))
        if hasattr(v, "btnUsuarios"):
            v.btnUsuarios.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_usuarios_clientes.ui"))
        if hasattr(v, "btnClases"):
            v.btnClases.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_clases.ui"))
        if hasattr(v, "btnInscripciones"):
            v.btnInscripciones.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_inscripciones.ui"))
        if hasattr(v, "btnPagos"):
            v.btnPagos.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_pagos.ui"))
        if hasattr(v, "btnEstadisticas"):
            v.btnEstadisticas.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_estadisticas.ui"))
        if hasattr(v, "btnActualizar"):
            v.btnActualizar.clicked.connect(self.cargar_datos)
        if hasattr(v, "btnNuevoTrabajador"):
            v.btnNuevoTrabajador.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_usuarios_nuevo_usuario.ui"))
        if hasattr(v, "txtBuscarClientePendiente"):
            v.txtBuscarClientePendiente.textChanged.connect(self.filtrar_pagos_pendientes)
        if hasattr(v, "txtBuscarDNI"):
            v.txtBuscarDNI.textChanged.connect(self.filtrar_pagos_pendientes)
        if hasattr(v, "cmbRolUsuario") and v.cmbRolUsuario.count() == 0:
            v.cmbRolUsuario.addItems(["Cliente", "Entrenador", "Recepcionista", "Administrador", "Contable"])

        if hasattr(v, "txtBuscar") and hasattr(v, "tablaClases"):
            v.txtBuscar.textChanged.connect(self.filtrar_clases)

        if hasattr(v, "txtBuscarInscripciones"):
            v.txtBuscarInscripciones.textChanged.connect(self.filtrar_inscripciones)

        # Tabs clientes/trabajadores
        if hasattr(v, "lblTabClientes"):
            v.lblTabClientes.mousePressEvent = lambda e: self.abrir_pantalla("interfaz_admin_usuarios_clientes.ui")
        if hasattr(v, "lblTabTrabajadores"):
            v.lblTabTrabajadores.mousePressEvent = lambda e: self.abrir_pantalla("interfaz_admin_usuarios_trabajadores.ui")

        # Pantalla clientes
        if hasattr(v, "txtBuscarCliente"):
            v.txtBuscarCliente.textChanged.connect(self.filtrar_clientes)

        # Pantalla trabajadores
        if hasattr(v, "txtBuscarTrabajador"):
            v.txtBuscarTrabajador.textChanged.connect(self.filtrar_trabajadores)

        if hasattr(v, "cmbRoles"):
            v.cmbRoles.currentIndexChanged.connect(self.filtrar_por_rol)
            if v.cmbRoles.count() == 0:
                v.cmbRoles.addItems(["Todos", "entrenador", "recepcionista", "contable", "administrador"])
        if hasattr(v, "btnGuardarCambios_2"):
            v.btnGuardarCambios_2.clicked.connect(self.guardar_cambios_trabajador)

        # CRUD usuarios
        if hasattr(v, "btnRegistrarUsuario"):
            v.btnRegistrarUsuario.clicked.connect(self.registrar_usuario)
        if hasattr(v, "btnGuardarCambios") and hasattr(v, "tablaClases"):
            v.btnGuardarCambios.clicked.connect(self.guardar_cambios_clase)

        # CRUD clases
        if hasattr(v, "btnNuevaClase") and hasattr(v, "tablaClases"):
            v.btnNuevaClase.clicked.connect(self.anadir_fila_clase)

    def cargar_datos(self):
        v = self.ventana

        if hasattr(v, "lblUsuariosNum"):
            try: v.lblUsuariosNum.setText(str(self.modelo.contar_usuarios()))
            except: v.lblUsuariosNum.setText("0")

        self._actualizar_resumen_clases()

        if hasattr(v, "lblTotalClases"):
            try: v.lblTotalClases.setText(str(self.modelo.contar_clases()))
            except: v.lblTotalClases.setText("0")

        for lbl, clase in [("lblClasesNum_2","spinning"),("lblClasesNum_3","zumba"),
                            ("lblClasesNum_4","yoga"),("lblClasesNum_5","pilates"),
                            ("lblClasesNum_6","crossfit")]:
            if hasattr(v, lbl):
                try: getattr(v, lbl).setText(str(self.modelo.contar_inscripciones_clase(clase)))
                except: getattr(v, lbl).setText("0")

        
        if hasattr(v, "clientesbasico"):
            try: v.clientesbasico.setText(str(self.modelo.contar_clientes_tarifa("basico")))
            except: v.clientesbasico.setText("0")

        if hasattr(v, "ClientesPremium"):
            try: v.ClientesPremium.setText(str(self.modelo.contar_clientes_tarifa("premium")))
            except: v.ClientesPremium.setText("0")

        if hasattr(v, "tablaInscripciones"):
            try:
                datos = self.modelo.listar_inscripciones_resumen()
                self._rellenar_tabla_inscripciones(v.tablaInscripciones, datos)
                self._actualizar_resumen_inscripciones(datos)
            except Exception as e:
                print(f"Error tablaInscripciones: {e}")

        if hasattr(v, "tablaClientesPagosPendientes"):
            try:
                datos = self.modelo.clientes_pendientes_admin()
                cabeceras = ["ID cliente", "Nombre", "Tarifa", "Estado pago"]
                self._rellenar_con_cabeceras(
                    v.tablaClientesPagosPendientes,
                    datos,
                    cabeceras
                )
            except Exception as e:
                print(f"Error clientes pendientes administrador: {e}")

        if hasattr(v, "graficoFake"):
            self._dibujar_grafico_ingresos(v.graficoFake)


        if hasattr(v, "tablaPagoAdmin") or hasattr(v, "tableWidget"):
            try:
                datos = self.modelo.listar_pagos_pendientes_admin()
                tabla = v.tablaPagoAdmin if hasattr(v, "tablaPagoAdmin") else v.tableWidget
                self._rellenar_tabla_pagos_admin(tabla, datos)
                self._actualizar_resumen_pagos_admin()
            except Exception as e:
                print(f"Error pagos admin: {e}")

        if hasattr(v, "lblNumTrabajadores"):
            try: v.lblNumTrabajadores.setText(str(self.modelo.contar_trabajadores()))
            except: v.lblNumTrabajadores.setText("0")

        if hasattr(v, "Entrenadores"):
            try: v.Entrenadores.setText(str(self.modelo.contar_por_rol("entrenador")))
            except: v.Entrenadores.setText("0")

        if hasattr(v, "Recepcionista"):
            try: v.Recepcionista.setText(str(self.modelo.contar_por_rol("recepcionista")))
            except: v.Recepcionista.setText("0")

        if hasattr(v, "Contables"):
            try: v.Contables.setText(str(self.modelo.contar_por_rol("contable")))
            except: v.Contables.setText("0")

        if hasattr(v, "Administradores"):
            try: v.Administradores.setText(str(self.modelo.contar_por_rol("administrador")))
            except: v.Administradores.setText("0")

        if hasattr(v, "tablaTrabajadores_2"):
            try:
                datos = self.modelo.listar_trabajadores_completo()
                self._rellenar_tabla_editable(v.tablaTrabajadores_2, datos)

                # Actualiza el texto de abajo
                if hasattr(v, "lblMostrando_2"):
                    v.lblMostrando_2.setText(f"Mostrando {len(datos)} trabajadores")

                # Actualiza el resumen de la derecha
                self._actualizar_resumen_trabajadores(datos)

            except Exception as e:
                print(f"Error tablaTrabajadores_2: {e}")

        if hasattr(v, "lblNumUsuarios"):
            try: v.lblNumUsuarios.setText(str(self.modelo.contar_usuarios()))
            except: v.lblNumUsuarios.setText("0")

        if hasattr(v, "tablaClientes_2"):
            try:
                datos = self.modelo.listar_clientes_completo()
                self._rellenar(v.tablaClientes_2, datos)
                if hasattr(v, "lblMostrando_2"):
                    v.lblMostrando_2.setText(f"Mostrando {len(datos)} clientes")
            except Exception as e:
                print(f"Error tablaClientes_2: {e}")

        if hasattr(v, "lblNumR1") and hasattr(v, "tablaRanking"):
            try:
                self.cargar_estadisticas_admin()
            except Exception as e:
                print(f"Error estadísticas admin: {e}")
                
        if hasattr(v, "tablaClases"):
            try:
                datos = self.modelo.listar_clases()
                self._rellenar_tabla_clases(v.tablaClases, datos)
                self._actualizar_resumen_clases(datos)
            except Exception as e:
                print(f"Error tablaClases: {e}")

        if hasattr(v, "tablaInscripciones") and hasattr(v, "lblTotal"):
            try:
                self._rellenar(v.tablaInscripciones, self.modelo.listar_inscripciones_resumen())
                stats = self.modelo.estadisticas_inscripciones()
                v.lblTotal.setText(str(stats["total"]))
                if hasattr(v, "label_4"):
                    v.label_4.setText(str(stats["clase_mas"]))
                if hasattr(v, "label_5"):
                    v.label_5.setText(str(stats["num_mas"]))
                if hasattr(v, "label_8"):
                    v.label_8.setText(str(stats["clase_menos"]))
                if hasattr(v, "label_9"):
                    v.label_9.setText(str(stats["num_menos"]))
                if hasattr(v, "label_15"):
                    v.label_15.setText(f"{stats['ocupacion']}%")
            except Exception as e:
                print(f"Error inscripciones stats: {e}")


    def _dibujar_grafico_ingresos(self, label):
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import io

            datos = self.modelo.ingresos_por_mes()
            if not datos:
                label.setText("Sin datos de ingresos")
                return

            meses_nombres = ["","Ene","Feb","Mar","Abr","May","Jun",
                             "Jul","Ago","Sep","Oct","Nov","Dic"]
            etiquetas = [f"{meses_nombres[int(r[1])]}\n{str(r[0])[-2:]}" for r in datos][::-1]
            valores   = [float(r[2]) for r in datos][::-1]

            fig, ax = plt.subplots(figsize=(4.0, 2.3), dpi=92)
            fig.patch.set_facecolor("#F8F9FA")
            ax.set_facecolor("#F8F9FA")
            colores = ["#00BFA5" if v == max(valores) else "#80CBC4" for v in valores]
            bars = ax.bar(etiquetas, valores, color=colores, width=0.55, edgecolor="white")
            ax.set_ylabel("€", fontsize=8)
            ax.set_title("Ingresos por mes", fontsize=9, fontweight="bold", color="#333")
            ax.tick_params(axis="x", labelsize=7)
            ax.tick_params(axis="y", labelsize=7)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            max_val = max(valores) if valores else 1
            for bar, val in zip(bars, valores):
                ax.text(bar.get_x() + bar.get_width()/2,
                        bar.get_height() + max_val*0.03,
                        f"{val:.0f}€", ha="center", va="bottom", fontsize=6.5)
            plt.tight_layout(pad=0.5)
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight", dpi=92)
            plt.close(fig)
            buf.seek(0)
            pixmap = ImagenView.desde_bytes(buf.read())
            label.setPixmap(pixmap.scaled(label.width() or 391, label.height() or 231, 1))
        except ImportError:
            label.setText("pip install matplotlib")
        except Exception as e:
            label.setText(f"Error gráfico:\n{str(e)[:60]}")


    def _rellenar_tabla_editable(self, tabla, datos):
        headers = ["ID","DNI","Nombre","Teléfono","Email","Usuario","Rol","Dirección","Fecha Nac."]
        tabla.setColumnCount(len(headers))
        tabla.setHorizontalHeaderLabels(headers)
        tabla.setEditTriggers(tabla.DoubleClicked | tabla.SelectedClicked)
        tabla.setSelectionBehavior(tabla.SelectRows)
        tabla.setRowCount(len(datos))
        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro):
                item = TablaView.crear_item(str(valor) if valor is not None else "")
                if col in (0, 6):
                    item = TablaView.crear_item(valor, editable=False)
                tabla.setItem(fila, col, item)

    def filtrar_trabajadores(self):
        v = self.ventana
        if not hasattr(v, "tablaTrabajadores_2"):
            return
        texto = v.txtBuscarTrabajador.text().strip() if hasattr(v, "txtBuscarTrabajador") else ""
        try:
            datos = self.modelo.buscar_trabajadores(texto) if texto else self.modelo.listar_trabajadores_completo()
            self._rellenar_tabla_editable(v.tablaTrabajadores_2, datos)
            if hasattr(v, "lblMostrando_2"):
                v.lblMostrando_2.setText(f"Mostrando {len(datos)} trabajadores")
        except Exception as e:
            print(f"Error filtrar_trabajadores: {e}")

    def filtrar_por_rol(self):
        v = self.ventana
        if not hasattr(v, "tablaTrabajadores_2") or not hasattr(v, "cmbRoles"):
            return
        rol = v.cmbRoles.currentText()
        try:
            datos = self.modelo.listar_trabajadores_completo() if rol == "Todos" else self.modelo.buscar_trabajadores_rol(rol)
            self._rellenar_tabla_editable(v.tablaTrabajadores_2, datos)
            if hasattr(v, "lblMostrando_2"):
                v.lblMostrando_2.setText(f"Mostrando {len(datos)} trabajadores")
        except Exception as e:
            print(f"Error filtrar_por_rol: {e}")

    def guardar_cambios_trabajador(self):
        v = self.ventana
        if not hasattr(v, "tablaTrabajadores_2"):
            return
        tabla = v.tablaTrabajadores_2
        try:
            for fila in range(tabla.rowCount()):
                id_item = tabla.item(fila, 0)
                if not id_item or not id_item.text():
                    continue
                id_usuario = int(id_item.text())
                nombre    = tabla.item(fila, 2).text() if tabla.item(fila, 2) else ""
                telefono  = tabla.item(fila, 3).text() if tabla.item(fila, 3) else ""
                email     = tabla.item(fila, 4).text() if tabla.item(fila, 4) else ""
                direccion = tabla.item(fila, 7).text() if tabla.item(fila, 7) else ""
                self.modelo.guardar_cambios_trabajador(id_usuario, nombre, telefono, email, direccion)
            MensajeView.information(v, "Correcto", "Cambios guardados correctamente")
        except Exception as e:
            MensajeView.warning(v, "Error", str(e))


    def filtrar_clientes(self):
        v = self.ventana
        if not hasattr(v, "tablaClientes_2"):
            return
        texto = v.txtBuscarCliente.text().strip() if hasattr(v, "txtBuscarCliente") else ""
        try:
            datos = self.modelo.buscar_clientes(texto) if texto else self.modelo.listar_clientes_completo()
            self._rellenar(v.tablaClientes_2, datos)
            if hasattr(v, "lblMostrando_2"):
                v.lblMostrando_2.setText(f"Mostrando {len(datos)} clientes")
        except Exception as e:
            print(f"Error filtrar_clientes: {e}")


    def registrar_usuario(self):
        v = self.ventana
        try:
            dni       = v.txtDni.text().strip()              if hasattr(v,"txtDni")             else ""
            nombre    = v.txtNombre.text().strip()            if hasattr(v,"txtNombre")          else ""
            telefono  = v.txtTelefono.text().strip()          if hasattr(v,"txtTelefono")        else ""
            email     = v.txtEmail.text().strip()             if hasattr(v,"txtEmail")           else ""
            direccion = v.txtDireccion.text().strip()         if hasattr(v,"txtDireccion")       else ""
            fecha     = v.txtFechaNacimiento.text().strip()   if hasattr(v,"txtFechaNacimiento") else "01/01/2000"
            username  = v.txtUsuario.text().strip()           if hasattr(v,"txtUsuario")         else ""
            password  = v.txtPassword.text().strip()          if hasattr(v,"txtPassword")        else ""
            confirmar = v.txtConfirmarPassword.text().strip() if hasattr(v,"txtConfirmarPassword") else ""
            rol_texto = v.cmbRolUsuario.currentText()         if hasattr(v,"cmbRolUsuario")      else "cliente"

            if not all([dni, nombre, telefono, email, username, password]):
                MensajeView.warning(v, "Error", "Todos los campos son obligatorios")
                return
            if password != confirmar:
                MensajeView.warning(v, "Error", "Las contraseñas no coinciden")
                return
            if len(password) < 4:
                MensajeView.warning(v, "Error", "La contraseña debe tener al menos 4 caracteres")
                return

        
            from datetime import datetime
            try:
                fecha = datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                MensajeView.warning(v, "Error", "Formato de fecha incorrecto. Usa DD/MM/YYYY (ej: 25/07/2001)")
                return

            roles_map = {"Cliente":1, "Entrenador":2, "Recepcionista":3, "Administrador":4, "Contable":5}
            id_rol = roles_map.get(rol_texto, 1)

            self.modelo.crear_usuario_completo(
                dni, nombre, telefono, email, username, password,
                id_rol, direccion, fecha, self.usuario["id_usuario"]
            )

            MensajeView.information(v, "Correcto",
                f"Usuario '{username}' registrado correctamente como {rol_texto}")

            for campo in ["txtDni","txtNombre","txtTelefono","txtEmail","txtDireccion",
                          "txtFechaNacimiento","txtUsuario","txtPassword","txtConfirmarPassword"]:
                if hasattr(v, campo):
                    getattr(v, campo).clear()

        except Exception as e:
            MensajeView.warning(v, "Error", f"Error al registrar: {str(e)}")





 

    def _rellenar(self, tabla, datos):
        tabla.setRowCount(len(datos))
        if datos:
            tabla.setColumnCount(len(datos[0]))
        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro):
                tabla.setItem(fila, col, TablaView.crear_item(
                    str(valor) if valor is not None else ""))


    def _rellenar_con_cabeceras(self, tabla, datos, cabeceras):
        TablaView.configurar_columnas(tabla, cabeceras)
        tabla.setRowCount(len(datos))
        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro[:len(cabeceras)]):
                TablaView.poner_item(tabla, fila, col, valor)


    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()

    def filtrar_clases(self):
        v = self.ventana

        if not hasattr(v, "tablaClases"):
            return

        texto = v.txtBuscar.text().strip() if hasattr(v, "txtBuscar") else ""

        try:
            if texto:
                datos = self.modelo.buscar_clases(texto)
            else:
                datos = self.modelo.listar_clases()

            self._rellenar_tabla_clases(v.tablaClases, datos)
            self._actualizar_resumen_clases(datos)

        except Exception as e:
            print(f"Error filtrar_clases: {e}")

    def filtrar_inscripciones(self):
        v = self.ventana

        if not hasattr(v, "tablaInscripciones"):
            return

        texto = v.txtBuscarInscripciones.text().strip() if hasattr(v, "txtBuscarInscripciones") else ""

        try:
            if texto:
                datos = self.modelo.buscar_inscripciones(texto)
            else:
                datos = self.modelo.listar_inscripciones_resumen()

            self._rellenar_tabla_inscripciones(v.tablaInscripciones, datos)
            self._actualizar_resumen_inscripciones(datos)

        except Exception as e:
            print(f"Error filtrar_inscripciones: {e}")
            
    def guardar_cambios_clase(self):
        v = self.ventana

        if not hasattr(v, "tablaClases"):
            return

        tabla = v.tablaClases

        try:
            for fila in range(tabla.rowCount()):
                id_item = tabla.item(fila, 0)

                id_texto = id_item.text().strip() if id_item and id_item.text() else ""
                nombre = tabla.item(fila, 1).text().strip() if tabla.item(fila, 1) else ""
                dia = tabla.item(fila, 2).text().strip() if tabla.item(fila, 2) else ""
                hora_ini = tabla.item(fila, 3).text().strip() if tabla.item(fila, 3) else ""
                hora_fin = tabla.item(fila, 4).text().strip() if tabla.item(fila, 4) else ""
                aforo = tabla.item(fila, 5).text().strip() if tabla.item(fila, 5) else ""
                nivel = tabla.item(fila, 6).text().strip() if tabla.item(fila, 6) else ""

                if not nombre:
                    continue

                if not dia:
                    dia = "lunes"
                if not hora_ini:
                    hora_ini = "09:00"
                if not hora_fin:
                    hora_fin = "10:00"
                if not aforo:
                    aforo = "20"
                if not nivel:
                    nivel = "media"

                try:
                    aforo = int(aforo)
                except ValueError:
                    MensajeView.warning(v, "Error", f"El aforo de la fila {fila + 1} debe ser un número")
                    return

                if id_texto:
                    self.modelo.guardar_cambios_clase_tabla(
                        int(id_texto), nombre, dia, hora_ini, hora_fin, aforo, nivel
                    )
                else:
                    self.modelo.registrar_clase(
                        2,
                        1,
                        nombre,
                        300,
                        dia,
                        hora_ini,
                        hora_fin,
                        60,
                        aforo,
                        nivel
                    )

            MensajeView.information(v, "Correcto", "Clases guardadas correctamente")

            datos_actualizados = self.modelo.listar_clases()
            self._rellenar_tabla_clases(v.tablaClases, datos_actualizados)
            self._actualizar_resumen_clases(datos_actualizados)

        except Exception as e:
            MensajeView.warning(v, "Error", str(e))

    def _actualizar_resumen_trabajadores(self, trabajadores):
        total = len(trabajadores)

        entrenadores = 0
        recepcion = 0
        contables = 0
        administradores = 0

        for trabajador in trabajadores:
            rol = str(trabajador[6]).lower().strip() if len(trabajador) > 6 else ""

            if "entrenador" in rol:
                entrenadores += 1
            elif "recepcionista" in rol or "recepción" in rol or "recepcion" in rol:
                recepcion += 1
            elif "contable" in rol:
                contables += 1
            elif "administrador" in rol or "admin" in rol:
                administradores += 1

        v = self.ventana

        if hasattr(v, "lblNumTrabajadores"):
            v.lblNumTrabajadores.setText(str(total))

        if hasattr(v, "Entrenadores"):
            v.Entrenadores.setText(str(entrenadores))

        if hasattr(v, "Recepcionista"):
            v.Recepcionista.setText(str(recepcion))

        if hasattr(v, "Contables"):
            v.Contables.setText(str(contables))

        if hasattr(v, "Administradores"):
            v.Administradores.setText(str(administradores))


    def _rellenar_tabla_clases(self, tabla, datos):
        cabeceras = ["ID", "Nombre", "Día", "Hora inicio", "Hora fin", "Aforo", "Nivel"]

        TablaView.configurar_columnas(tabla, cabeceras)
        tabla.setRowCount(len(datos))
        tabla.setEditTriggers(tabla.DoubleClicked | tabla.SelectedClicked)
        tabla.setSelectionBehavior(tabla.SelectRows)

        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro[:len(cabeceras)]):
                editable = col != 0
                item = TablaView.crear_item(str(valor) if valor is not None else "", editable=editable)
                tabla.setItem(fila, col, item)

    def _rellenar_tabla_inscripciones(self, tabla, datos):
        cabeceras = ["Usuario", "Clase", "Fecha", "Estado"]

        TablaView.configurar_columnas(tabla, cabeceras)
        tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras)
        tabla.setRowCount(len(datos))
        tabla.setEditTriggers(tabla.DoubleClicked | tabla.SelectedClicked)
        tabla.setSelectionBehavior(tabla.SelectRows)

        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro[:len(cabeceras)]):
                item = TablaView.crear_item(
                    str(valor) if valor is not None else "",
                    editable=True
                )
                tabla.setItem(fila, col, item)


    def _actualizar_resumen_inscripciones(self, datos):
        v = self.ventana
        total = len(datos)

        if hasattr(v, "lblTotalInscripciones"):
            v.lblTotalInscripciones.setText(str(total))

        if hasattr(v, "lblMostrando"):
            v.lblMostrando.setText(f"Mostrando {total} inscripciones")


    def anadir_fila_clase(self):
        v = self.ventana

        if not hasattr(v, "tablaClases"):
            return

        tabla = v.tablaClases
        fila = tabla.rowCount()
        tabla.insertRow(fila)

        valores = ["", "Nueva clase", "lunes", "09:00", "10:00", "20", "media"]

        for col, valor in enumerate(valores):
            editable = col != 0
            item = TablaView.crear_item(valor, editable=editable)
            tabla.setItem(fila, col, item)

        tabla.selectRow(fila)

        total = tabla.rowCount()

        if hasattr(v, "lblTotalClases"):
            v.lblTotalClases.setText(str(total))

        if hasattr(v, "lblMostrando"):
            v.lblMostrando.setText(f"Mostrando {total} clases")

    def _actualizar_resumen_clases(self, datos=None):
        v = self.ventana

        if datos is None:
            try:
                total = self.modelo.contar_clases()
            except:
                total = 0
        else:
            total = len(datos)

        # Tarjeta de Inicio: "Clases activas"
        if hasattr(v, "lblClasesNum"):
            v.lblClasesNum.setText(str(total))

        # Pantalla de Clases: "Resumen de clases"
        if hasattr(v, "lblTotalClases"):
            v.lblTotalClases.setText(str(total))

        # Texto inferior de la tabla
        if hasattr(v, "lblMostrando"):
            v.lblMostrando.setText(f"Mostrando {total} clases")

    def _rellenar_tabla_pagos_admin(self, tabla, datos):
        cabeceras = ["Cliente", "DNI", "Tarifa", "Importe pendiente", "Fecha límite", "Estado"]

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


    def _actualizar_resumen_pagos_admin(self):
        v = self.ventana

        try:
            ingresos_mes = float(self.modelo.ingresos_mes_actual())
        except:
            ingresos_mes = 0

        try:
            ingresos_anio = float(self.modelo.ingresos_anio_actual())
        except:
            ingresos_anio = 0

        try:
            clientes_pendientes = int(self.modelo.numero_clientes_pendientes_pago())
        except:
            clientes_pendientes = 0

        try:
            importe_pendiente = float(self.modelo.importe_pendiente_cobrar())
        except:
            importe_pendiente = 0

        if hasattr(v, "label_4"):
            v.label_4.setText(f"{ingresos_mes:.2f}€")

        if hasattr(v, "label_8"):
            v.label_8.setText(f"{ingresos_anio:.2f}€")

        if hasattr(v, "label_13"):
            v.label_13.setText(str(clientes_pendientes))

        if hasattr(v, "label_5"):
            v.label_5.setText(f"{importe_pendiente:.2f}€")


    def filtrar_pagos_pendientes(self):
            v = self.ventana

            if hasattr(v, "txtBuscarDNI"):
                texto = v.txtBuscarDNI.text().strip()
            elif hasattr(v, "txtBuscarClientePendiente"):
                texto = v.txtBuscarClientePendiente.text().strip()
            else:
                texto = ""

            try:
                if texto:
                    datos = self.modelo.buscar_pago_pendiente_por_dni(texto)
                else:
                    datos = self.modelo.listar_pagos_pendientes_admin()

                if hasattr(v, "tablaPagoAdmin"):
                    tabla = v.tablaPagoAdmin
                elif hasattr(v, "tableWidget"):
                    tabla = v.tableWidget
                else:
                    return

                self._rellenar_tabla_pagos_admin(tabla, datos)
                self._actualizar_resumen_pagos_admin()

            except Exception as e:
                print(f"Error filtrar_pagos_pendientes: {e}")

    def cargar_estadisticas_admin(self):
        v = self.ventana

        stats = self.modelo.estadisticas_admin()

        if hasattr(v, "lblNumR1"):
            v.lblNumR1.setText(str(stats["clientes_activos"]))

        if hasattr(v, "lblNumR2"):
            v.lblNumR2.setText(str(stats["reservas"]))

        if hasattr(v, "lblNumR3"):
            v.lblNumR3.setText(f'{stats["ocupacion"]}%')

        if hasattr(v, "lblNumR4"):
            v.lblNumR4.setText(str(stats["asistencias"]))

        if hasattr(v, "lblNumClasesActivas"):
            v.lblNumClasesActivas.setText(str(stats["clases_activas"]))

        if hasattr(v, "lblNumEntrenadores"):
            v.lblNumEntrenadores.setText(str(stats["entrenadores"]))

        if hasattr(v, "lblNumSalas"):
            v.lblNumSalas.setText(str(stats["salas"]))

        if hasattr(v, "tablaRanking"):
            datos_ranking = self.modelo.ranking_usuarios_activos_estadisticas()
            self._rellenar_tabla_ranking_estadisticas(v.tablaRanking, datos_ranking)

        datos_ocupacion = self.modelo.ocupacion_por_clase_estadisticas()
        self._actualizar_ocupacion_por_clase(datos_ocupacion)


    def _rellenar_tabla_ranking_estadisticas(self, tabla, datos):
        cabeceras = ["#", "Cliente", "Asistencias", "Última clase", "Estado"]

        TablaView.configurar_columnas(tabla, cabeceras)
        tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras)
        tabla.setRowCount(len(datos))
        tabla.setSelectionBehavior(tabla.SelectRows)

        for fila, registro in enumerate(datos):
            numero = fila + 1
            nombre = registro[0]
            asistencias = registro[1]
            ultima_clase = registro[2]
            estado = registro[3]

            valores = [numero, nombre, asistencias, ultima_clase, estado]

            for col, valor in enumerate(valores):
                item = TablaView.crear_item(
                    str(valor) if valor is not None else "",
                    editable=False
                )
                tabla.setItem(fila, col, item)


    def _actualizar_ocupacion_por_clase(self, datos):
        v = self.ventana

        for i in range(4):
            label_nombre = f"lblOcc{i}"
            barra_nombre = f"progOcc{i}"

            if i < len(datos):
                nombre_clase = str(datos[i][0])
                porcentaje = int(datos[i][1]) if datos[i][1] is not None else 0
            else:
                nombre_clase = "-"
                porcentaje = 0

            if hasattr(v, label_nombre):
                getattr(v, label_nombre).setText(nombre_clase)

            if hasattr(v, barra_nombre):
                barra = getattr(v, barra_nombre)
                barra.setValue(porcentaje)
                barra.setFormat(f"{porcentaje}%")