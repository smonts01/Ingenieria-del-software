import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem


class ControladorCliente:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None

    def abrir(self):
        self.abrir_pantalla("interfaz_cliente_inicio.ui")

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
            v.btnInicio.clicked.connect(lambda: self.abrir_pantalla("interfaz_cliente_inicio.ui"))
        if hasattr(v, "btnClases"):
            v.btnClases.clicked.connect(lambda: self.abrir_pantalla("interfaz_cliente_clases_todas.ui"))
        if hasattr(v, "btnEstadisticas"):
            v.btnEstadisticas.clicked.connect(lambda: self.abrir_pantalla("interfaz_cliente_estadisticas.ui"))
        if hasattr(v, "btnPerfil"):
            v.btnPerfil.clicked.connect(lambda: self.abrir_pantalla("interfaz_cliente_perfil.ui"))
        if hasattr(v, "btnInformacion"):
            v.btnInformacion.clicked.connect(lambda: self.abrir_pantalla("interfaz_cliente_informacion.ui"))
        if hasattr(v, "btnReservas"):
            v.btnReservas.clicked.connect(lambda: self.abrir_pantalla("interfaz_cliente_clases_reservas.ui"))
        if hasattr(v, "btnCalorias"):
            v.btnCalorias.clicked.connect(self.mostrar_calorias)
        if hasattr(v, "btnGuardarPerfil"):
            v.btnGuardarPerfil.clicked.connect(self.guardar_perfil)
        if hasattr(v, "btnCambiarPassword"):
            v.btnCambiarPassword.clicked.connect(self.cambiar_password)

        # Botones reservar clase en pantalla de clases
        for i in range(1, 10):
            btn_name = f"btnReservar{i}"
            if hasattr(v, btn_name):
                clase_id = i
                getattr(v, btn_name).clicked.connect(
                    lambda checked, cid=clase_id: self.reservar_clase_por_fila(cid))

        # Botón reservar clase seleccionada en tabla
        if hasattr(v, "btnReservar"):
            v.btnReservar.clicked.connect(self.reservar_clase_seleccionada)

        if hasattr(v, "btnDesapuntarse"):
            v.btnDesapuntarse.clicked.connect(self.desapuntarse_clase)

    def cargar_datos(self):
        v = self.ventana
        id_u = self.usuario["id_usuario"]

        if hasattr(v, "tablaProximasClases"):
            self.rellenar_tabla(v.tablaProximasClases, self.modelo.clases_inscritas_cliente(id_u))

        if hasattr(v, "tablaTodasClases"):
            self.rellenar_tabla(v.tablaTodasClases, self.modelo.listar_clases())

        if hasattr(v, "tablaEstadisticas"):
            self.rellenar_tabla(v.tablaEstadisticas, self.modelo.estadisticas_cliente(id_u))

        if hasattr(v, "tablaHistorial"):
            self.rellenar_tabla(v.tablaHistorial, self.modelo.historial_cliente(id_u))

        if hasattr(v, "tablaPagos"):
            self.rellenar_tabla(v.tablaPagos, self.modelo.pagos_cliente(id_u))

        if hasattr(v, "lblCalorias"):
            total = self.modelo.calcular_calorias_cliente(id_u)
            v.lblCalorias.setText(f"{total} kcal")

        if hasattr(v, "txtNombre"):
            perfil = self.modelo.perfil_usuario(id_u)
            if perfil:
                v.txtNombre.setText(str(perfil[2]))
                if hasattr(v, "txtTelefono"): v.txtTelefono.setText(str(perfil[3] or ""))
                if hasattr(v, "txtEmail"):    v.txtEmail.setText(str(perfil[4] or ""))
                if hasattr(v, "txtDireccion"):v.txtDireccion.setText(str(perfil[7] or ""))
                if hasattr(v, "txtUsername"): v.txtUsername.setText(str(perfil[5] or ""))

    def reservar_clase_seleccionada(self):
        v = self.ventana
        try:
            tabla = v.tablaTodasClases if hasattr(v, "tablaTodasClases") else None
            if not tabla:
                return
            fila = tabla.currentRow()
            if fila < 0:
                QMessageBox.warning(v, "Error", "Selecciona una clase primero")
                return
            id_clase = int(tabla.item(fila, 0).text())
            self.modelo.inscribirse_clase(self.usuario["id_usuario"], id_clase)
            QMessageBox.information(v, "Correcto", "Inscripción realizada")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def reservar_clase_por_fila(self, id_clase):
        try:
            self.modelo.inscribirse_clase(self.usuario["id_usuario"], id_clase)
            QMessageBox.information(self.ventana, "Correcto", "Clase reservada")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(self.ventana, "Error", str(e))

    def desapuntarse_clase(self):
        v = self.ventana
        try:
            tabla = v.tablaProximasClases if hasattr(v, "tablaProximasClases") else None
            if not tabla:
                return
            fila = tabla.currentRow()
            if fila < 0:
                QMessageBox.warning(v, "Error", "Selecciona una clase")
                return
            id_clase = int(tabla.item(fila, 0).text())
            self.modelo.desapuntarse_clase(self.usuario["id_usuario"], id_clase)
            QMessageBox.information(v, "Correcto", "Te has desapuntado de la clase")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def mostrar_calorias(self):
        try:
            total = self.modelo.calcular_calorias_cliente(self.usuario["id_usuario"])
            QMessageBox.information(self.ventana, "Calorías quemadas",
                                    f"Has quemado un total de {total} kcal en tus clases")
        except Exception as e:
            QMessageBox.warning(self.ventana, "Error", str(e))

    def guardar_perfil(self):
        v = self.ventana
        try:
            telefono = v.txtTelefono.text().strip() if hasattr(v, "txtTelefono") else ""
            email    = v.txtEmail.text().strip()    if hasattr(v, "txtEmail")    else ""
            direccion= v.txtDireccion.text().strip() if hasattr(v, "txtDireccion") else ""
            self.modelo.modificar_usuario(self.usuario["id_usuario"], telefono, email, direccion)
            QMessageBox.information(v, "Correcto", "Perfil actualizado")
        except Exception as e:
            QMessageBox.warning(v, "Error", str(e))

    def cambiar_password(self):
        v = self.ventana
        try:
            nueva = v.txtNuevaPassword.text().strip() if hasattr(v, "txtNuevaPassword") else ""
            if not nueva:
                QMessageBox.warning(v, "Error", "Introduce la nueva contraseña")
                return
            self.modelo.cambiar_password(self.usuario["id_usuario"], nueva)
            QMessageBox.information(v, "Correcto", "Contraseña cambiada")
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
