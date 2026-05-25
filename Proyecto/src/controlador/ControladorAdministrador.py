import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt


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
        self.ventana = uic.loadUi(ruta)
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
        if hasattr(v, "btnConfiguracion"):
            v.btnConfiguracion.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_configuracion.ui"))
        if hasattr(v, "btnActualizar"):
            v.btnActualizar.clicked.connect(self.cargar_datos)
        if hasattr(v, "btnNuevoTrabajador"):
            v.btnNuevoTrabajador.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_usuarios_nuevo_usuario.ui"))

        if hasattr(v, "btnRegistrarUsuario"):
            v.btnRegistrarUsuario.clicked.connect(self.registrar_usuario)
        
        if hasattr(v, "cmbRolUsuario") and v.cmbRolUsuario.count() == 0:
            v.cmbRolUsuario.addItems(["Cliente", "Entrenador", "Recepcionista", "Administrador", "Contable"])

        if hasattr(v, "txtBuscar"):
            v.txtBuscar.textChanged.connect(self.filtrar_clases)
        if hasattr(v, "btnGuardarCambios"):
            v.btnGuardarCambios.clicked.connect(self.guardar_cambios_clase)

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
        if hasattr(v, "btnGuardarCambios"):
            v.btnGuardarCambios.clicked.connect(self.modificar_usuario)
        if hasattr(v, "btnEliminarUsuario"):
            v.btnEliminarUsuario.clicked.connect(self.eliminar_usuario)

        # CRUD clases
        if hasattr(v, "btnNuevaClase"):
            v.btnNuevaClase.clicked.connect(self.registrar_clase)
        if hasattr(v, "btnModificarClase"):
            v.btnModificarClase.clicked.connect(self.modificar_clase)
        if hasattr(v, "btnEliminarClase"):
            v.btnEliminarClase.clicked.connect(self.eliminar_clase)

    def cargar_datos(self):
        v = self.ventana

        # ── PANTALLA INICIO ──────────────────────────────────────────

        if hasattr(v, "lblUsuariosNum"):
            try: v.lblUsuariosNum.setText(str(self.modelo.contar_usuarios()))
            except: v.lblUsuariosNum.setText("0")

        if hasattr(v, "lblClasesNum"):
            try: v.lblClasesNum.setText(str(self.modelo.contar_clases()))
            except: v.lblClasesNum.setText("0")

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
                self._rellenar(v.tablaInscripciones, datos)
            except Exception as e:
                print(f"Error tablaInscripciones: {e}")

        if hasattr(v, "tablaClientesPagosPendientes"):
            try:
                datos = self.modelo.pagos_pendientes()
                self._rellenar(v.tablaClientesPagosPendientes, datos)
                print(f"Pagos pendientes: {len(datos)} filas")
            except Exception as e:
                print(f"Error pagos pendientes: {e}")

        if hasattr(v, "graficoFake"):
            self._dibujar_grafico_ingresos(v.graficoFake)

        # ── PANTALLA TRABAJADORES ────────────────────────────────────

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

        if hasattr(v, "tablaTrabajadores_2"):
            try:
                datos = self.modelo.listar_trabajadores_completo()
                self._rellenar_tabla_editable(v.tablaTrabajadores_2, datos)
                if hasattr(v, "lblMostrando_2"):
                    v.lblMostrando_2.setText(f"Mostrando {len(datos)} trabajadores")
            except Exception as e:
                print(f"Error tablaTrabajadores_2: {e}")

        # ── PANTALLA CLIENTES ────────────────────────────────────────

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

        # ── OTRAS PANTALLAS ──────────────────────────────────────────

        if hasattr(v, "tablaClases"):
            try:
                datos = self.modelo.listar_clases()
                self._rellenar_tabla_editable(v.tablaClases, datos)
                if hasattr(v, "lblClasesTotales"):
                    v.lblClasesTotales.setText(str(len(datos)))
                if hasattr(v, "lblMostrando"):
                    v.lblMostrando.setText(f"Mostrando {len(datos)} clases")
            except Exception as e:
                print(f"Error tablaClases: {e}")

        if hasattr(v, "tableWidget"):
            try: self._rellenar(v.tableWidget, self.modelo.listar_pagos())
            except: pass

        if hasattr(v, "tablaRanking"):
            try: self._rellenar(v.tablaRanking, self.modelo.ranking_clientes_activos())
            except: pass

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
    # ── Gráfico ──────────────────────────────────────────────────────

    def _dibujar_grafico_ingresos(self, label):
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import io
            from PyQt5.QtGui import QPixmap

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
            pixmap = QPixmap()
            pixmap.loadFromData(buf.read())
            label.setPixmap(pixmap.scaled(label.width() or 391, label.height() or 231, 1))
        except ImportError:
            label.setText("pip install matplotlib")
        except Exception as e:
            label.setText(f"Error gráfico:\n{str(e)[:60]}")

    # ── Trabajadores ─────────────────────────────────────────────────

    def _rellenar_tabla_editable(self, tabla, datos):
        headers = ["ID","DNI","Nombre","Teléfono","Email","Usuario","Rol","Dirección","Fecha Nac."]
        tabla.setColumnCount(len(headers))
        tabla.setHorizontalHeaderLabels(headers)
        tabla.setEditTriggers(tabla.DoubleClicked | tabla.SelectedClicked)
        tabla.setSelectionBehavior(tabla.SelectRows)
        tabla.setRowCount(len(datos))
        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro):
                item = QTableWidgetItem(str(valor) if valor is not None else "")
                if col in (0, 6):
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
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
            QMessageBox.information(v, "Correcto", "Cambios guardados correctamente")
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    # ── Clientes ─────────────────────────────────────────────────────

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

    def filtrar_clientes_estado(self):
        v = self.ventana
        if not hasattr(v, "tablaClientes_2") or not hasattr(v, "cmbEstado_2"):
            return
        estado = v.cmbEstado_2.currentText()
        try:
            datos = self.modelo.listar_clientes_completo() if estado == "Todos" else self.modelo.buscar_clientes_estado(estado)
            self._rellenar(v.tablaClientes_2, datos)
        except Exception as e:
            print(f"Error filtrar_clientes_estado: {e}")

    # ── CRUD usuarios ─────────────────────────────────────────────────

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
                QMessageBox.warning(v, "Error", "Todos los campos son obligatorios")
                return
            if password != confirmar:
                QMessageBox.warning(v, "Error", "Las contraseñas no coinciden")
                return
            if len(password) < 4:
                QMessageBox.warning(v, "Error", "La contraseña debe tener al menos 4 caracteres")
                return

            # Convertir DD/MM/YYYY a YYYY-MM-DD antes de enviar a MySQL
            from datetime import datetime
            try:
                fecha = datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                QMessageBox.warning(v, "Error", "Formato de fecha incorrecto. Usa DD/MM/YYYY (ej: 25/07/2001)")
                return

            roles_map = {"Cliente":1, "Entrenador":2, "Recepcionista":3, "Administrador":4, "Contable":5}
            id_rol = roles_map.get(rol_texto, 1)

            self.modelo.registrar_usuario(dni, nombre, telefono, email,
                                          username, password, id_rol, direccion, fecha)

            datos = self.modelo.consultar(
                f"SELECT id_usuario FROM usuarios WHERE username = '{username}'"
            )
            if not datos:
                QMessageBox.warning(v, "Error", "No se pudo obtener el ID del usuario")
                return
            id_nuevo = datos[0][0]

            if id_rol == 1:
                self.modelo.ejecutar(
                    "INSERT INTO clientes (id_cliente, estado_pagado, calorias_acumuladas) VALUES (?,?,?)",
                    (id_nuevo, "pendiente", 0)
                )
            else:
                self.modelo.ejecutar(
                    "INSERT INTO empleados (id_empleado, salario) VALUES (?,?)",
                    (id_nuevo, 0.00)
                )
                if id_rol == 2:
                    self.modelo.ejecutar(
                        "INSERT INTO entrenador (id_entrenador, especialidad, id_administrador_registra) VALUES (?,?,?)",
                        (id_nuevo, "General", self.usuario["id_usuario"])
                    )
                elif id_rol == 3:
                    self.modelo.ejecutar(
                        "INSERT INTO recepcionista (id_recepcionista, turno, id_administrador_registra) VALUES (?,?,?)",
                        (id_nuevo, "mañana", self.usuario["id_usuario"])
                    )
                elif id_rol == 4:
                    self.modelo.ejecutar(
                        "INSERT INTO administrador (id_administrador) VALUES (?)",
                        (id_nuevo,)
                    )
                elif id_rol == 5:
                    self.modelo.ejecutar(
                        "INSERT INTO contable (id_contable, titulacion, id_administrador_registra) VALUES (?,?,?)",
                        (id_nuevo, "ADE", self.usuario["id_usuario"])
                    )

            QMessageBox.information(v, "Correcto",
                f"Usuario '{username}' registrado correctamente como {rol_texto}")

            for campo in ["txtDni","txtNombre","txtTelefono","txtEmail","txtDireccion",
                          "txtFechaNacimiento","txtUsuario","txtPassword","txtConfirmarPassword"]:
                if hasattr(v, campo):
                    getattr(v, campo).clear()

        except Exception as e:
            QMessageBox.warning(v, "Error", f"Error al registrar: {str(e)}")

    def modificar_usuario(self):
        v = self.ventana
        try:
            tabla = getattr(v,"tablaClientes_2",None)
            if not tabla or tabla.currentRow()<0:
                QMessageBox.warning(v,"Error","Selecciona un usuario primero")
                return
            id_usuario = int(tabla.item(tabla.currentRow(),0).text())
            telefono = v.txtTelefono.text().strip() if hasattr(v,"txtTelefono") else ""
            email    = v.txtEmail.text().strip()    if hasattr(v,"txtEmail")    else ""
            direccion= v.txtDireccion.text().strip() if hasattr(v,"txtDireccion") else ""
            self.modelo.modificar_usuario(id_usuario,telefono,email,direccion)
            QMessageBox.information(v,"Correcto","Usuario actualizado")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v,"Error",str(e))

    def eliminar_usuario(self):
        v = self.ventana
        try:
            tabla = getattr(v,"tablaClientes_2",None)
            if not tabla or tabla.currentRow()<0:
                QMessageBox.warning(v,"Error","Selecciona un usuario primero")
                return
            id_usuario = int(tabla.item(tabla.currentRow(),0).text())
            if QMessageBox.question(v,"Confirmar","¿Eliminar este usuario?",
                                    QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes:
                self.modelo.eliminar_usuario(id_usuario)
                QMessageBox.information(v,"Correcto","Usuario eliminado")
                self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v,"Error",str(e))

    # ── CRUD clases ───────────────────────────────────────────────────

    def registrar_clase(self):
        v = self.ventana
        try:
            nombre   = v.txtNombreClase.text().strip() if hasattr(v,"txtNombreClase") else ""
            dia      = v.txtDiaSemana.text().strip()   if hasattr(v,"txtDiaSemana")   else "lunes"
            hora_ini = v.txtHoraInicio.text().strip()  if hasattr(v,"txtHoraInicio")  else "09:00"
            hora_fin = v.txtHoraFin.text().strip()     if hasattr(v,"txtHoraFin")     else "10:00"
            duracion = int(v.txtDuracion.text())       if hasattr(v,"txtDuracion")    else 60
            aforo    = int(v.txtAforo.text())          if hasattr(v,"txtAforo")       else 20
            calorias = int(v.txtCalorias.text())       if hasattr(v,"txtCalorias")    else 300
            nivel    = v.cmbNivel.currentText()        if hasattr(v,"cmbNivel")       else "media"
            if not nombre:
                QMessageBox.warning(v,"Error","Introduce el nombre de la clase")
                return
            self.modelo.registrar_clase(self.usuario["id_usuario"],1,nombre,
                                        calorias,dia,hora_ini,hora_fin,duracion,aforo,nivel)
            QMessageBox.information(v,"Correcto","Clase registrada")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v,"Error",str(e))

    def modificar_clase(self):
        v = self.ventana
        try:
            tabla = getattr(v,"tablaClases",None)
            if not tabla or tabla.currentRow()<0:
                QMessageBox.warning(v,"Error","Selecciona una clase primero")
                return
            id_clase = int(tabla.item(tabla.currentRow(),0).text())
            nombre = v.txtNombreClase.text().strip() if hasattr(v,"txtNombreClase") else tabla.item(tabla.currentRow(),1).text()
            self.modelo.modificar_clase(id_clase,self.usuario["id_usuario"],1,
                                        nombre,300,"lunes","09:00","10:00",60,20,"media")
            QMessageBox.information(v,"Correcto","Clase modificada")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v,"Error",str(e))

    def eliminar_clase(self):
        v = self.ventana
        try:
            tabla = getattr(v,"tablaClases",None)
            if not tabla or tabla.currentRow()<0:
                QMessageBox.warning(v,"Error","Selecciona una clase primero")
                return
            id_clase = int(tabla.item(tabla.currentRow(),0).text())
            if QMessageBox.question(v,"Confirmar","¿Eliminar esta clase?",
                                    QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes:
                self.modelo.eliminar_clase(id_clase)
                QMessageBox.information(v,"Correcto","Clase eliminada")
                self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v,"Error",str(e))

    # ── Utilidades ────────────────────────────────────────────────────

    def _rellenar(self, tabla, datos):
        tabla.setRowCount(len(datos))
        if datos:
            tabla.setColumnCount(len(datos[0]))
        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro):
                tabla.setItem(fila, col, QTableWidgetItem(
                    str(valor) if valor is not None else ""))

    def rellenar_tabla(self, tabla, datos):
        self._rellenar(tabla, datos)

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
            self._rellenar_tabla_editable(v.tablaClases, datos)
            if hasattr(v, "lblMostrando"):
                v.lblMostrando.setText(f"Mostrando {len(datos)} clases")
        except Exception as e:
            print(f"Error filtrar_clases: {e}")

    def guardar_cambios_clase(self):
        v = self.ventana
        if not hasattr(v, "tablaClases"):
            return
        tabla = v.tablaClases
        try:
            for fila in range(tabla.rowCount()):
                id_item = tabla.item(fila, 0)
                if not id_item or not id_item.text():
                    continue
                id_clase  = int(id_item.text())
                nombre    = tabla.item(fila, 1).text() if tabla.item(fila, 1) else ""
                dia       = tabla.item(fila, 2).text() if tabla.item(fila, 2) else ""
                hora_ini  = tabla.item(fila, 3).text() if tabla.item(fila, 3) else ""
                hora_fin  = tabla.item(fila, 4).text() if tabla.item(fila, 4) else ""
                aforo     = tabla.item(fila, 5).text() if tabla.item(fila, 5) else "20"
                nivel     = tabla.item(fila, 6).text() if tabla.item(fila, 6) else "media"
                self.modelo.ejecutar("""
                    UPDATE clase SET nombre_actividad=?, dia_semana=?,
                    hora_inicio=?, hora_fin=?, aforo_maximo=?, nivel_intensidad=?
                    WHERE id_clase=?
                """, (nombre, dia, hora_ini, hora_fin, int(aforo), nivel, id_clase))
            QMessageBox.information(v, "Correcto", "Cambios guardados correctamente")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))
