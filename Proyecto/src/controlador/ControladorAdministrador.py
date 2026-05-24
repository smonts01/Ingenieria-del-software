import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem


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
        if hasattr(v, "btnRegistrarUsuario"):
            v.btnRegistrarUsuario.clicked.connect(self.registrar_usuario)

        # Pantalla trabajadores
        if hasattr(v, "lblTabClientes"):
            v.lblTabClientes.mousePressEvent = lambda e: self.abrir_pantalla("interfaz_admin_usuarios_clientes.ui")
        if hasattr(v, "lblTabTrabajadores"):
            v.lblTabTrabajadores.mousePressEvent = lambda e: self.abrir_pantalla("interfaz_admin_usuarios_trabajadores.ui")
        if hasattr(v, "txtBuscarTrabajador"):
            v.txtBuscarTrabajador.textChanged.connect(self.filtrar_trabajadores)
        if hasattr(v, "cmbRoles"):
            v.cmbRoles.currentIndexChanged.connect(self.filtrar_por_rol)
            if v.cmbRoles.count() == 0:
                v.cmbRoles.addItems(["Todos", "entrenador", "recepcionista", "contable", "administrador"])
        if hasattr(v, "btnGuardarCambios_2"):
            v.btnGuardarCambios_2.clicked.connect(self.guardar_cambios_trabajador)

        # Pantalla clientes
        if hasattr(v, "txtBuscarCliente"):
            v.txtBuscarCliente.textChanged.connect(self.filtrar_clientes)
        if hasattr(v, "cmbEstado_2"):
            v.cmbEstado_2.currentIndexChanged.connect(self.filtrar_clientes_estado)
            if v.cmbEstado_2.count() == 0:
                v.cmbEstado_2.addItems(["Todos", "abonado", "pendiente"])
        if hasattr(v, "btnNuevaClase"):
            v.btnNuevaClase.clicked.connect(self.registrar_clase)
        if hasattr(v, "btnModificarClase"):
            v.btnModificarClase.clicked.connect(self.modificar_clase)
        if hasattr(v, "btnEliminarClase"):
            v.btnEliminarClase.clicked.connect(self.eliminar_clase)
        if hasattr(v, "btnEliminarUsuario"):
            v.btnEliminarUsuario.clicked.connect(self.eliminar_usuario)
        if hasattr(v, "btnActualizar"):
            v.btnActualizar.clicked.connect(self.cargar_datos)
        if hasattr(v, "btnGuardarCambios"):
            v.btnGuardarCambios.clicked.connect(self.modificar_usuario)

    def cargar_datos(self):
        v = self.ventana

        # 1. Total clientes
        if hasattr(v, "lblUsuariosNum"):
            try:
                v.lblUsuariosNum.setText(str(self.modelo.contar_usuarios()))
            except Exception:
                v.lblUsuariosNum.setText("0")

        # 2. Total clases
        if hasattr(v, "lblClasesNum"):
            try:
                v.lblClasesNum.setText(str(self.modelo.contar_clases()))
            except Exception:
                v.lblClasesNum.setText("0")

        # 3. Inscripciones por clase
        clases_labels = [
            ("lblClasesNum_2", "spinning"),
            ("lblClasesNum_3", "zumba"),
            ("lblClasesNum_4", "yoga"),
            ("lblClasesNum_5", "pilates"),
            ("lblClasesNum_6", "crossfit"),
        ]
        for lbl_name, clase in clases_labels:
            if hasattr(v, lbl_name):
                try:
                    n = self.modelo.contar_inscripciones_clase(clase)
                    getattr(v, lbl_name).setText(str(n))
                except Exception:
                    getattr(v, lbl_name).setText("0")

        # 4. Clientes por plan
        if hasattr(v, "clientesbasico"):
            try:
                v.clientesbasico.setText(str(self.modelo.contar_clientes_tarifa("basico")))
            except Exception:
                v.clientesbasico.setText("0")

        if hasattr(v, "ClientesPremium"):
            try:
                v.ClientesPremium.setText(str(self.modelo.contar_clientes_tarifa("premium")))
            except Exception:
                v.ClientesPremium.setText("0")

        # 5. Tabla inscripciones recientes
        if hasattr(v, "tablaInscripciones"):
            try:
                self.rellenar_tabla(v.tablaInscripciones,
                                    self.modelo.listar_inscripciones_resumen())
            except Exception:
                pass

        # 6. Tabla pagos pendientes
        if hasattr(v, "tablaClientesPagosPendientes"):
            try:
                self.rellenar_tabla(v.tablaClientesPagosPendientes,
                                    self.modelo.pagos_pendientes())
            except Exception:
                pass

        # 7. Gráfico ingresos por mes
        if hasattr(v, "graficoFake"):
            self._dibujar_grafico_ingresos(v.graficoFake)

        # 8. Pantalla trabajadores
        if hasattr(v, "lblNumTrabajadores"):
            try:
                v.lblNumTrabajadores.setText(str(self.modelo.contar_trabajadores()))
            except Exception:
                v.lblNumTrabajadores.setText("0")
        if hasattr(v, "Entrenadores"):
            try:
                v.Entrenadores.setText(str(self.modelo.contar_por_rol("entrenador")))
            except Exception:
                v.Entrenadores.setText("0")
        if hasattr(v, "Recepcionista"):
            try:
                v.Recepcionista.setText(str(self.modelo.contar_por_rol("recepcionista")))
            except Exception:
                v.Recepcionista.setText("0")
        if hasattr(v, "Contables"):
            try:
                v.Contables.setText(str(self.modelo.contar_por_rol("contable")))
            except Exception:
                v.Contables.setText("0")
        if hasattr(v, "tablaTrabajadores_2"):
            try:
                datos = self.modelo.listar_trabajadores_completo()
                self._rellenar_tabla_editable(v.tablaTrabajadores_2, datos)
                if hasattr(v, "lblMostrando_2"):
                    v.lblMostrando_2.setText(f"Mostrando {len(datos)} trabajadores")
            except Exception:
                pass

        # 9. Pantalla clientes
        if hasattr(v, "lblNumUsuarios"):
            try:
                v.lblNumUsuarios.setText(str(self.modelo.contar_usuarios()))
            except Exception:
                v.lblNumUsuarios.setText("0")
        if hasattr(v, "tablaClientes_2"):
            try:
                datos = self.modelo.listar_clientes_completo()
                self.rellenar_tabla(v.tablaClientes_2, datos)
                if hasattr(v, "lblMostrando_2"):
                    v.lblMostrando_2.setText(f"Mostrando {len(datos)} clientes")
            except Exception:
                pass
        if hasattr(v, "tablaClases"):
            try:
                self.rellenar_tabla(v.tablaClases, self.modelo.listar_clases())
            except Exception:
                pass
        if hasattr(v, "tableWidget"):
            try:
                self.rellenar_tabla(v.tableWidget, self.modelo.listar_pagos())
            except Exception:
                pass
        if hasattr(v, "tablaRanking"):
            try:
                self.rellenar_tabla(v.tablaRanking, self.modelo.ranking_clientes_activos())
            except Exception:
                pass

    def _dibujar_grafico_ingresos(self, label):
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import io
            from PyQt5.QtGui import QPixmap

            datos = self.modelo.ingresos_por_mes()
            if not datos:
                label.setText("Sin datos de ingresos aún")
                return

            # datos: (anio, mes, total) - ya vienen en orden DESC, invertir para mostrar cronológico
            meses_nombres = ["", "Ene", "Feb", "Mar", "Abr", "May", "Jun",
                             "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
            etiquetas = [f"{meses_nombres[int(r[1])]}\n{str(r[0])[-2:]}" for r in datos][::-1]
            valores   = [float(r[2]) for r in datos][::-1]

            fig, ax = plt.subplots(figsize=(4.0, 2.3), dpi=92)
            fig.patch.set_facecolor("#F8F9FA")
            ax.set_facecolor("#F8F9FA")

            colores = ["#00BFA5" if v == max(valores) else "#80CBC4" for v in valores]
            bars = ax.bar(etiquetas, valores, color=colores, width=0.55, edgecolor="white", linewidth=0.5)

            ax.set_ylabel("€", fontsize=8)
            ax.set_title("Ingresos por mes", fontsize=9, fontweight="bold", color="#333333", pad=6)
            ax.tick_params(axis="x", labelsize=7)
            ax.tick_params(axis="y", labelsize=7)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_alpha(0.3)
            ax.spines["bottom"].set_alpha(0.3)

            max_val = max(valores) if valores else 1
            for bar, val in zip(bars, valores):
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + max_val * 0.03,
                        f"{val:.0f}€",
                        ha="center", va="bottom", fontsize=6.5, color="#333")

            plt.tight_layout(pad=0.5)
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight", dpi=92)
            plt.close(fig)
            buf.seek(0)

            pixmap = QPixmap()
            pixmap.loadFromData(buf.read())
            w = label.width()  or 391
            h = label.height() or 231
            label.setPixmap(pixmap.scaled(w, h, 1))  # 1 = KeepAspectRatio

        except ImportError:
            label.setText("Instala matplotlib:\npip install matplotlib")
        except Exception as e:
            label.setText(f"Error gráfico:\n{str(e)[:60]}")

    # ── CRUD usuarios ──────────────────────────────────────────────

    def registrar_usuario(self):
        v = self.ventana
        try:
            dni      = v.txtDni.text().strip()      if hasattr(v, "txtDni")      else ""
            nombre   = v.txtNombre.text().strip()    if hasattr(v, "txtNombre")   else ""
            telefono = v.txtTelefono.text().strip()  if hasattr(v, "txtTelefono") else ""
            email    = v.txtEmail.text().strip()     if hasattr(v, "txtEmail")    else ""
            direccion= v.txtDireccion.text().strip() if hasattr(v, "txtDireccion")else ""
            fecha    = v.txtFechaNacimiento.text().strip() if hasattr(v, "txtFechaNacimiento") else "2000-01-01"
            username = v.txtUsuario.text().strip()   if hasattr(v, "txtUsuario")  else ""
            password = v.txtPassword.text().strip()  if hasattr(v, "txtPassword") else ""
            confirmar= v.txtConfirmarPassword.text().strip() if hasattr(v, "txtConfirmarPassword") else password
            rol      = v.cmbRolUsuario.currentIndex() + 1   if hasattr(v, "cmbRolUsuario")        else 1

            if not all([dni, nombre, telefono, email, username, password]):
                QMessageBox.warning(v, "Error", "Completa todos los campos obligatorios")
                return
            if password != confirmar:
                QMessageBox.warning(v, "Error", "Las contraseñas no coinciden")
                return

            self.modelo.registrar_usuario(dni, nombre, telefono, email,
                                          username, password, rol, direccion, fecha)
            QMessageBox.information(v, "Correcto", "Usuario registrado correctamente")
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def modificar_usuario(self):
        v = self.ventana
        try:
            tabla = getattr(v, "tablaClientes_2", None)
            if not tabla or tabla.currentRow() < 0:
                QMessageBox.warning(v, "Error", "Selecciona un usuario primero")
                return
            id_usuario = int(tabla.item(tabla.currentRow(), 0).text())
            telefono = v.txtTelefono.text().strip() if hasattr(v, "txtTelefono") else ""
            email    = v.txtEmail.text().strip()    if hasattr(v, "txtEmail")    else ""
            direccion= v.txtDireccion.text().strip() if hasattr(v, "txtDireccion") else ""
            self.modelo.modificar_usuario(id_usuario, telefono, email, direccion)
            QMessageBox.information(v, "Correcto", "Usuario actualizado")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def eliminar_usuario(self):
        v = self.ventana
        try:
            tabla = getattr(v, "tablaClientes_2", None)
            if not tabla or tabla.currentRow() < 0:
                QMessageBox.warning(v, "Error", "Selecciona un usuario primero")
                return
            id_usuario = int(tabla.item(tabla.currentRow(), 0).text())
            if QMessageBox.question(v, "Confirmar", "¿Eliminar este usuario?",
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self.modelo.eliminar_usuario(id_usuario)
                QMessageBox.information(v, "Correcto", "Usuario eliminado")
                self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    # ── CRUD clases ────────────────────────────────────────────────

    def registrar_clase(self):
        v = self.ventana
        try:
            nombre   = v.txtNombreClase.text().strip() if hasattr(v, "txtNombreClase") else ""
            dia      = v.txtDiaSemana.text().strip()   if hasattr(v, "txtDiaSemana")   else "lunes"
            hora_ini = v.txtHoraInicio.text().strip()  if hasattr(v, "txtHoraInicio")  else "09:00"
            hora_fin = v.txtHoraFin.text().strip()     if hasattr(v, "txtHoraFin")     else "10:00"
            duracion = int(v.txtDuracion.text())       if hasattr(v, "txtDuracion")    else 60
            aforo    = int(v.txtAforo.text())          if hasattr(v, "txtAforo")       else 20
            calorias = int(v.txtCalorias.text())       if hasattr(v, "txtCalorias")    else 300
            nivel    = v.cmbNivel.currentText()        if hasattr(v, "cmbNivel")       else "media"
            if not nombre:
                QMessageBox.warning(v, "Error", "Introduce el nombre de la clase")
                return
            self.modelo.registrar_clase(self.usuario["id_usuario"], 1, nombre,
                                        calorias, dia, hora_ini, hora_fin, duracion, aforo, nivel)
            QMessageBox.information(v, "Correcto", "Clase registrada correctamente")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def modificar_clase(self):
        v = self.ventana
        try:
            tabla = getattr(v, "tablaClases", None)
            if not tabla or tabla.currentRow() < 0:
                QMessageBox.warning(v, "Error", "Selecciona una clase primero")
                return
            id_clase = int(tabla.item(tabla.currentRow(), 0).text())
            nombre   = v.txtNombreClase.text().strip() if hasattr(v, "txtNombreClase") else tabla.item(tabla.currentRow(), 1).text()
            self.modelo.modificar_clase(id_clase, self.usuario["id_usuario"], 1,
                                        nombre, 300, "lunes", "09:00", "10:00", 60, 20, "media")
            QMessageBox.information(v, "Correcto", "Clase modificada")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def eliminar_clase(self):
        v = self.ventana
        try:
            tabla = getattr(v, "tablaClases", None)
            if not tabla or tabla.currentRow() < 0:
                QMessageBox.warning(v, "Error", "Selecciona una clase primero")
                return
            id_clase = int(tabla.item(tabla.currentRow(), 0).text())
            if QMessageBox.question(v, "Confirmar", "¿Eliminar esta clase?",
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self.modelo.eliminar_clase(id_clase)
                QMessageBox.information(v, "Correcto", "Clase eliminada")
                self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    # ── Utilidades ─────────────────────────────────────────────────


    def _rellenar_tabla_editable(self, tabla, datos):
        from PyQt5.QtWidgets import QTableWidgetItem
        from PyQt5.QtCore import Qt
        headers = ["ID", "DNI", "Nombre", "Teléfono", "Email", "Usuario", "Rol", "Dirección", "Fecha Nac."]
        tabla.setColumnCount(len(headers))
        tabla.setHorizontalHeaderLabels(headers)
        tabla.setRowCount(len(datos))
        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro):
                item = QTableWidgetItem(str(valor) if valor is not None else "")
                # ID y Rol no editables
                if col in (0, 6):
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                tabla.setItem(fila, col, item)

    def filtrar_trabajadores(self):
        v = self.ventana
        if not hasattr(v, "txtBuscarTrabajador") or not hasattr(v, "tablaTrabajadores_2"):
            return
        texto = v.txtBuscarTrabajador.text().strip()
        try:
            if texto:
                datos = self.modelo.buscar_trabajadores(texto)
            else:
                datos = self.modelo.listar_trabajadores_completo()
            self._rellenar_tabla_editable(v.tablaTrabajadores_2, datos)
            if hasattr(v, "lblMostrando_2"):
                v.lblMostrando_2.setText(f"Mostrando {len(datos)} trabajadores")
        except Exception as e:
            pass

    def filtrar_por_rol(self):
        v = self.ventana
        if not hasattr(v, "cmbRoles") or not hasattr(v, "tablaTrabajadores_2"):
            return
        rol = v.cmbRoles.currentText()
        try:
            if rol == "Todos":
                datos = self.modelo.listar_trabajadores_completo()
            else:
                datos = self.modelo.buscar_trabajadores_rol(rol)
            self._rellenar_tabla_editable(v.tablaTrabajadores_2, datos)
            if hasattr(v, "lblMostrando_2"):
                v.lblMostrando_2.setText(f"Mostrando {len(datos)} trabajadores")
        except Exception:
            pass

    def guardar_cambios_trabajador(self):
        v = self.ventana
        if not hasattr(v, "tablaTrabajadores_2"):
            return
        tabla = v.tablaTrabajadores_2
        try:
            guardados = 0
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
                guardados += 1
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(v, "Correcto", f"Cambios guardados para {guardados} trabajadores")
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(v, "Error", str(e))

    def filtrar_clientes(self):
        v = self.ventana
        if not hasattr(v, "txtBuscarCliente") or not hasattr(v, "tablaClientes_2"):
            return
        texto = v.txtBuscarCliente.text().strip()
        try:
            datos = self.modelo.buscar_clientes(texto) if texto else self.modelo.listar_clientes_completo()
            self.rellenar_tabla(v.tablaClientes_2, datos)
            if hasattr(v, "lblMostrando_2"):
                v.lblMostrando_2.setText(f"Mostrando {len(datos)} clientes")
        except Exception:
            pass

    def filtrar_clientes_estado(self):
        v = self.ventana
        if not hasattr(v, "cmbEstado_2") or not hasattr(v, "tablaClientes_2"):
            return
        estado = v.cmbEstado_2.currentText()
        try:
            datos = self.modelo.listar_clientes_completo() if estado == "Todos" else self.modelo.buscar_clientes_estado(estado)
            self.rellenar_tabla(v.tablaClientes_2, datos)
        except Exception:
            pass

    def rellenar_tabla(self, tabla, datos):
        tabla.setRowCount(len(datos))
        if datos:
            tabla.setColumnCount(len(datos[0]))
        for fila, registro in enumerate(datos):
            for col, valor in enumerate(registro):
                tabla.setItem(fila, col, QTableWidgetItem(
                    str(valor) if valor is not None else ""))

    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()
