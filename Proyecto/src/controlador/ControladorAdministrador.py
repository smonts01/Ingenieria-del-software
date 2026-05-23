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
        self.aplicar_imagenes()
        self.conectar_botones()
        self.cargar_datos()
        self.ventana.show()

    def aplicar_imagenes(self):
        img = "./src/vista/imagenes"
        v = self.ventana
        # Apply stylesheet images to labels by name
        estilos = {
            "lblLogo": f"image: url({img}/logo_stayfit.png);",
            "lblOla":  f"image: url({img}/ola.png);",
        }
        for nombre, estilo in estilos.items():
            if hasattr(v, nombre):
                getattr(v, nombre).setStyleSheet(estilo)

    def conectar_botones(self):
        v = self.ventana

        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(self.cerrar_sesion)
        if hasattr(v, "btnInicio"):
            v.btnInicio.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_inicio.ui"))
        if hasattr(v, "btnUsuarios"):
            v.btnUsuarios.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_usuarios_clientes.ui"))
        if hasattr(v, "btnTrabajadores"):
            v.btnTrabajadores.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_usuarios_trabajadores.ui"))
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
        if hasattr(v, "btnNuevoUsuario"):
            v.btnNuevoUsuario.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_usuarios_nuevo_usuario.ui"))
        if hasattr(v, "btnRegistrarUsuario"):
            v.btnRegistrarUsuario.clicked.connect(self.registrar_usuario)
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

        if hasattr(v, "tablaInscripciones"):
            self.rellenar_tabla(v.tablaInscripciones, self.modelo.ocupacion_clases())
        if hasattr(v, "tablaClientesPagosPendientes"):
            self.rellenar_tabla(v.tablaClientesPagosPendientes, self.modelo.pagos_pendientes())
        if hasattr(v, "tablaClientes_2"):
            self.rellenar_tabla(v.tablaClientes_2, self.modelo.listar_clientes())
        if hasattr(v, "tablaTrabajadores_2"):
            self.rellenar_tabla(v.tablaTrabajadores_2, self.modelo.listar_empleados())
        if hasattr(v, "tablaClases"):
            self.rellenar_tabla(v.tablaClases, self.modelo.listar_clases())
        if hasattr(v, "tableWidget"):
            self.rellenar_tabla(v.tableWidget, self.modelo.listar_pagos())
        if hasattr(v, "tablaRanking"):
            self.rellenar_tabla(v.tablaRanking, self.modelo.ranking_clientes_activos())

    def registrar_usuario(self):
        v = self.ventana
        try:
            dni      = v.txtDni.text().strip()
            nombre   = v.txtNombre.text().strip()
            telefono = v.txtTelefono.text().strip()
            email    = v.txtEmail.text().strip()
            direccion= v.txtDireccion.text().strip()
            fecha    = v.txtFechaNacimiento.text().strip()
            username = v.txtUsuario.text().strip()
            password = v.txtPassword.text().strip()
            confirmar= v.txtConfirmarPassword.text().strip()
            rol      = v.cmbRolUsuario.currentIndex() + 1

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
            tabla = v.tablaClientes_2 if hasattr(v, "tablaClientes_2") else None
            if not tabla:
                return
            fila = tabla.currentRow()
            if fila < 0:
                QMessageBox.warning(v, "Error", "Selecciona un usuario primero")
                return
            id_usuario = int(tabla.item(fila, 0).text())
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
            tabla = v.tablaClientes_2 if hasattr(v, "tablaClientes_2") else None
            if not tabla:
                return
            fila = tabla.currentRow()
            if fila < 0:
                QMessageBox.warning(v, "Error", "Selecciona un usuario primero")
                return
            id_usuario = int(tabla.item(fila, 0).text())
            resp = QMessageBox.question(v, "Confirmar", "¿Eliminar este usuario?",
                                        QMessageBox.Yes | QMessageBox.No)
            if resp == QMessageBox.Yes:
                self.modelo.eliminar_usuario(id_usuario)
                QMessageBox.information(v, "Correcto", "Usuario eliminado")
                self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def registrar_clase(self):
        v = self.ventana
        try:
            nombre     = v.txtNombreClase.text().strip()   if hasattr(v, "txtNombreClase")     else ""
            dia        = v.txtDiaSemana.text().strip()     if hasattr(v, "txtDiaSemana")       else "lunes"
            hora_ini   = v.txtHoraInicio.text().strip()    if hasattr(v, "txtHoraInicio")      else "09:00"
            hora_fin   = v.txtHoraFin.text().strip()       if hasattr(v, "txtHoraFin")         else "10:00"
            duracion   = int(v.txtDuracion.text())         if hasattr(v, "txtDuracion")        else 60
            aforo      = int(v.txtAforo.text())            if hasattr(v, "txtAforo")           else 20
            calorias   = int(v.txtCalorias.text())         if hasattr(v, "txtCalorias")        else 300
            nivel      = v.cmbNivel.currentText()          if hasattr(v, "cmbNivel")           else "media"
            id_sala    = 1
            id_entren  = self.usuario["id_usuario"]

            if not nombre:
                QMessageBox.warning(v, "Error", "Introduce el nombre de la clase")
                return

            self.modelo.registrar_clase(id_entren, id_sala, nombre, calorias,
                                        dia, hora_ini, hora_fin, duracion, aforo, nivel)
            QMessageBox.information(v, "Correcto", "Clase registrada correctamente")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def modificar_clase(self):
        v = self.ventana
        try:
            tabla = v.tablaClases if hasattr(v, "tablaClases") else None
            if not tabla:
                return
            fila = tabla.currentRow()
            if fila < 0:
                QMessageBox.warning(v, "Error", "Selecciona una clase primero")
                return
            id_clase = int(tabla.item(fila, 0).text())
            nombre   = v.txtNombreClase.text().strip() if hasattr(v, "txtNombreClase") else tabla.item(fila, 1).text()
            self.modelo.modificar_clase(id_clase, self.usuario["id_usuario"], 1,
                                        nombre, 300, "lunes", "09:00", "10:00", 60, 20, "media")
            QMessageBox.information(v, "Correcto", "Clase modificada")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def eliminar_clase(self):
        v = self.ventana
        try:
            tabla = v.tablaClases if hasattr(v, "tablaClases") else None
            if not tabla:
                return
            fila = tabla.currentRow()
            if fila < 0:
                QMessageBox.warning(v, "Error", "Selecciona una clase primero")
                return
            id_clase = int(tabla.item(fila, 0).text())
            resp = QMessageBox.question(v, "Confirmar", "¿Eliminar esta clase?",
                                        QMessageBox.Yes | QMessageBox.No)
            if resp == QMessageBox.Yes:
                self.modelo.eliminar_clase(id_clase)
                QMessageBox.information(v, "Correcto", "Clase eliminada")
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
