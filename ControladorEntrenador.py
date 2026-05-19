import os
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

    def cargar_datos(self):
        v = self.ventana

        if hasattr(v, "tablaProximasClasesEntrenador"):
            datos = self.modelo.clases_de_entrenador(self.usuario["id_usuario"])
            self.rellenar_tabla(v.tablaProximasClasesEntrenador, datos)

        if hasattr(v, "tablaMisClases"):
            datos = self.modelo.clases_de_entrenador(self.usuario["id_usuario"])
            self.rellenar_tabla(v.tablaMisClases, datos)

        if hasattr(v, "tablaOcupacionClases"):
            datos = self.modelo.ocupacion_clases()
            self.rellenar_tabla(v.tablaOcupacionClases, datos)

        if hasattr(v, "tablaInscritos"):
            clases = self.modelo.clases_de_entrenador(self.usuario["id_usuario"])
            if clases:
                datos = self.modelo.clientes_inscritos_clase(clases[0][0])
                self.rellenar_tabla(v.tablaInscritos, datos)

        if hasattr(v, "comboSeleccionarClase"):
            clases = self.modelo.clases_de_entrenador(self.usuario["id_usuario"])
            v.comboSeleccionarClase.clear()
            for clase in clases:
                v.comboSeleccionarClase.addItem(str(clase[1]), clase[0])
            v.comboSeleccionarClase.currentIndexChanged.connect(self.cargar_inscritos_asistencia)
            self.cargar_inscritos_asistencia()

    def cargar_inscritos_asistencia(self):
        v = self.ventana

        if not hasattr(v, "comboSeleccionarClase"):
            return

        id_clase = v.comboSeleccionarClase.currentData()
        if not id_clase:
            return

        datos = self.modelo.clientes_inscritos_clase(id_clase)

        tabla = v.tablaInscritosAsistencia
        tabla.setRowCount(len(datos))
        tabla.setColumnCount(5)

        for fila, cliente in enumerate(datos):
            tabla.setItem(fila, 0, QTableWidgetItem(str(cliente[0])))
            tabla.setItem(fila, 1, QTableWidgetItem(str(cliente[1])))
            tabla.setItem(fila, 2, QTableWidgetItem(str(cliente[2])))
            tabla.setItem(fila, 3, QTableWidgetItem(str(cliente[3])))
            tabla.setItem(fila, 4, QTableWidgetItem("si"))

    def guardar_asistencia(self):
        v = self.ventana
        id_clase = v.comboSeleccionarClase.currentData()
        fecha = "2026-05-19"
        presentes = []

        for fila in range(v.tablaInscritosAsistencia.rowCount()):
            id_cliente = v.tablaInscritosAsistencia.item(fila, 0)
            presente = v.tablaInscritosAsistencia.item(fila, 4)

            if id_cliente and presente and presente.text().lower() == "si":
                presentes.append(int(id_cliente.text()))

        self.modelo.registrar_asistencia_lista(id_clase, fecha, presentes)
        QMessageBox.information(v, "Correcto", "Asistencia guardada")

    def rellenar_tabla(self, tabla, datos):
        tabla.setRowCount(len(datos))
        if datos:
            tabla.setColumnCount(len(datos[0]))

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))

    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()