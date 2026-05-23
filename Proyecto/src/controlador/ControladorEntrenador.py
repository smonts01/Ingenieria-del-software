import os
from datetime import date
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem


class ControladorEntrenador:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None

    def abrir(self):
        self.abrir_pantalla("interfaz_entrenador.ui")

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
        for boton in ["btnInicio", "btnInicio_2"]:
            if hasattr(v, boton):
                getattr(v, boton).clicked.connect(lambda: self.abrir_pantalla("interfaz_entrenador.ui"))
        if hasattr(v, "btnClases"):
            v.btnClases.clicked.connect(lambda: self.abrir_pantalla("interfaz_entrenador_clases.ui"))
        if hasattr(v, "btnClases_2"):
            v.btnClases_2.clicked.connect(lambda: self.abrir_pantalla("interfaz_entrenador_clases.ui"))
        if hasattr(v, "btnInscritos"):
            v.btnInscritos.clicked.connect(lambda: self.abrir_pantalla("interfaz_entrenador_verListaClientes.ui"))
        if hasattr(v, "btnOcupacion"):
            v.btnOcupacion.clicked.connect(lambda: self.abrir_pantalla("interfaz_entrenador_ocupacionClases.ui"))
        if hasattr(v, "btnPerfil"):
            v.btnPerfil.clicked.connect(lambda: self.abrir_pantalla("interfaz_entrenador_perfil.ui"))
        if hasattr(v, "btnInformacion"):
            v.btnInformacion.clicked.connect(lambda: self.abrir_pantalla("interfaz_entrenador_informacion.ui"))
        if hasattr(v, "btnRegistroAsistencia"):
            v.btnRegistroAsistencia.clicked.connect(lambda: self.abrir_pantalla("interfaz_entrenador_registrar_asistencia.ui"))
        if hasattr(v, "pushButton_GuardarAsist"):
            v.pushButton_GuardarAsist.clicked.connect(self.guardar_asistencia)
        if hasattr(v, "btnGuardarAsistencia"):
            v.btnGuardarAsistencia.clicked.connect(self.guardar_asistencia)

    def cargar_datos(self):
        v = self.ventana
        id_u = self.usuario["id_usuario"]

        if hasattr(v, "tablaProximasClasesEntrenador"):
            self.rellenar_tabla(v.tablaProximasClasesEntrenador, self.modelo.clases_de_entrenador(id_u))
        if hasattr(v, "tablaMisClases"):
            self.rellenar_tabla(v.tablaMisClases, self.modelo.clases_de_entrenador(id_u))
        if hasattr(v, "tablaOcupacionClases"):
            self.rellenar_tabla(v.tablaOcupacionClases, self.modelo.ocupacion_clases_entrenador(id_u))
        
        if hasattr(v, "comboClasesInscritos"):
            clases = self.modelo.clases_de_entrenador(id_u)
            v.comboClasesInscritos.clear()

            for clase in clases:
                v.comboClasesInscritos.addItem(str(clase[1]), clase[0])

            try:
                v.comboClasesInscritos.currentIndexChanged.disconnect()
            except Exception:
                pass

            v.comboClasesInscritos.currentIndexChanged.connect(self.cargar_clientes_inscritos)
            self.cargar_clientes_inscritos()

        if hasattr(v, "txtNombre"):
            perfil = self.modelo.perfil_usuario(id_u)
            if perfil:
                v.txtNombre.setText(str(perfil[2]))
                if hasattr(v, "txtTelefono"): v.txtTelefono.setText(str(perfil[3] or ""))
                if hasattr(v, "txtEmail"):    v.txtEmail.setText(str(perfil[4] or ""))

        if hasattr(v, "comboSeleccionarClase"):
            clases = self.modelo.clases_de_entrenador(id_u)
            v.comboSeleccionarClase.clear()
            for clase in clases:
                v.comboSeleccionarClase.addItem(str(clase[1]), clase[0])
            try:
                v.comboSeleccionarClase.currentIndexChanged.disconnect()
            except Exception:
                pass
            v.comboSeleccionarClase.currentIndexChanged.connect(self.cargar_inscritos_asistencia)
            self.cargar_inscritos_asistencia()


    def cargar_clientes_inscritos(self):
        v = self.ventana

        if not hasattr(v, "comboClasesInscritos"):
            return

        id_clase = v.comboClasesInscritos.currentData()

        if not id_clase:
            return

        datos = self.modelo.clientes_inscritos_clase(id_clase)

        if hasattr(v, "tablaInscritos"):
            self.rellenar_tabla(v.tablaInscritos, datos)

        if hasattr(v, "label_numInscritos_ins"):
            v.label_numInscritos_ins.setText(str(len(datos)))

        if hasattr(v, "label_total_inscritos"):
            v.label_total_inscritos.setText(str(len(datos)))

            

    def cargar_inscritos_asistencia(self):
        v = self.ventana
        if not hasattr(v, "comboSeleccionarClase"):
            return
        id_clase = v.comboSeleccionarClase.currentData()
        if not id_clase:
            return
        datos = self.modelo.clientes_inscritos_clase(id_clase)
        if not hasattr(v, "tablaInscritosAsistencia"):
            return
        tabla = v.tablaInscritosAsistencia
        tabla.setRowCount(len(datos))
        tabla.setColumnCount(5)
        for fila, cliente in enumerate(datos):
            for col in range(min(4, len(cliente))):
                tabla.setItem(fila, col, QTableWidgetItem(str(cliente[col]) if cliente[col] is not None else ""))
            tabla.setItem(fila, 4, QTableWidgetItem("si"))

    def guardar_asistencia(self):
        v = self.ventana
        try:
            if not hasattr(v, "comboSeleccionarClase"):
                QMessageBox.warning(v, "Error", "No hay clase seleccionada")
                return
            id_clase = v.comboSeleccionarClase.currentData()
            if not id_clase:
                QMessageBox.warning(v, "Error", "Selecciona una clase")
                return
            fecha = date.today().isoformat()
            presentes = []
            if hasattr(v, "tablaInscritosAsistencia"):
                for fila in range(v.tablaInscritosAsistencia.rowCount()):
                    item_id      = v.tablaInscritosAsistencia.item(fila, 0)
                    item_presente= v.tablaInscritosAsistencia.item(fila, 4)
                    if item_id and item_presente and item_presente.text().lower() == "si":
                        presentes.append(int(item_id.text()))
            self.modelo.registrar_asistencia_lista(id_clase, fecha, presentes)
            QMessageBox.information(v, "Correcto", f"Asistencia guardada ({len(presentes)} presentes)")
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
