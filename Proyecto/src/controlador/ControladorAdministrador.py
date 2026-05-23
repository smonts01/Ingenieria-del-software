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

        if hasattr(v, "btnNuevoUsuario"):
            v.btnNuevoUsuario.clicked.connect(lambda: self.abrir_pantalla("interfaz_admin_usuarios_nuevo_usuario.ui"))

        if hasattr(v, "btnRegistrarUsuario"):
            v.btnRegistrarUsuario.clicked.connect(self.registrar_usuario)

        if hasattr(v, "btnNuevaClase"):
            v.btnNuevaClase.clicked.connect(self.registrar_clase_ejemplo)

        if hasattr(v, "btnActualizar"):
            v.btnActualizar.clicked.connect(self.cargar_datos)

    def cargar_datos(self):
        v = self.ventana

        if hasattr(v, "tablaInscripciones"):
            datos = self.modelo.ocupacion_clases()
            self.rellenar_tabla(v.tablaInscripciones, datos)

        if hasattr(v, "tablaClientesPagosPendientes"):
            datos = self.modelo.pagos_pendientes()
            self.rellenar_tabla(v.tablaClientesPagosPendientes, datos)

        if hasattr(v, "tablaClientes_2"):
            datos = self.modelo.listar_clientes()
            self.rellenar_tabla(v.tablaClientes_2, datos)

        if hasattr(v, "tablaTrabajadores_2"):
            datos = self.modelo.listar_empleados()
            self.rellenar_tabla(v.tablaTrabajadores_2, datos)

        if hasattr(v, "tablaClases"):
            datos = self.modelo.listar_clases()
            self.rellenar_tabla(v.tablaClases, datos)

        if hasattr(v, "tableWidget"):
            datos = self.modelo.listar_pagos()
            self.rellenar_tabla(v.tableWidget, datos)

        if hasattr(v, "tablaRanking"):
            datos = self.modelo.ranking_clientes_activos()
            self.rellenar_tabla(v.tablaRanking, datos)

    def registrar_usuario(self):
        v = self.ventana

        try:
            dni = v.txtDni.text()
            nombre = v.txtNombre.text()
            telefono = v.txtTelefono.text()
            email = v.txtEmail.text()
            direccion = v.txtDireccion.text()
            fecha = v.txtFechaNacimiento.text()
            username = v.txtUsuario.text()
            password = v.txtPassword.text()
            confirmar = v.txtConfirmarPassword.text()
            rol = v.cmbRolUsuario.currentIndex() + 1

            if password != confirmar:
                QMessageBox.warning(v, "Error", "Las contraseñas no coinciden")
                return

            self.modelo.registrar_usuario(
                dni, nombre, telefono, email,
                username, password, rol,
                direccion, fecha
            )

            QMessageBox.information(v, "Correcto", "Usuario registrado")

        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def registrar_clase_ejemplo(self):
        QMessageBox.information(
            self.ventana,
            "Aviso",
            "Para crear clases faltan campos editables en esta pantalla"
        )

    def rellenar_tabla(self, tabla, datos):
        tabla.setRowCount(len(datos))
        if datos:
            tabla.setColumnCount(len(datos[0]))

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                tabla.setItem(fila, columna, QTableWidgetItem(str(valor) if valor is not None else ""))

    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()