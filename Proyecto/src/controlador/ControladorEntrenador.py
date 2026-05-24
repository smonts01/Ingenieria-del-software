import os
from datetime import date
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


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
            self.rellenar_tabla(v.tablaProximasClasesEntrenador, self.modelo.clases_entrenador_tabla(id_u))

        if hasattr(v, "labelNumClases"):
            clases = self.modelo.clases_de_entrenador(id_u)
            v.labelNumClases.setText(str(len(clases)))

        if hasattr(v, "labelClase") or hasattr(v, "labelHora"):
            clases = self.modelo.clases_de_entrenador(id_u)

            if clases:
                primera_clase = clases[0]

                nombre = primera_clase[1]
                hora_inicio = primera_clase[3]
                hora_fin = primera_clase[4]

                if hasattr(v, "labelClase"):
                    v.labelClase.setText(str(nombre))

                if hasattr(v, "labelHora"):
                    v.labelHora.setText(f"{hora_inicio} - {hora_fin}")

        if hasattr(v, "labelNumAsistencias"):
            clases = self.modelo.clases_de_entrenador(id_u)
            total_pendientes = 0

            for clase in clases:
                inscritos = self.modelo.clientes_inscritos_clase(clase[0])
                total_pendientes += len(inscritos)

            v.labelNumAsistencias.setText(str(total_pendientes))

        if hasattr(v, "lblPorcentajeOcupacion"):
            ocupaciones = self.modelo.ocupacion_clases_entrenador(id_u)

            if ocupaciones:
                suma = 0

                for ocupacion in ocupaciones:
                    suma += float(ocupacion[4])

                media = round(suma / len(ocupaciones), 2)
                v.lblPorcentajeOcupacion.setText(f"{media}%")



        if hasattr(v, "tablaMisClases"):
            self.rellenar_tabla(v.tablaMisClases, self.modelo.clases_entrenador_tabla(id_u))
        if hasattr(v, "tablaOcupacionClases"):
            datos_ocupacion = self.modelo.ocupacion_clases_entrenador(id_u)

            tabla = v.tablaOcupacionClases
            tabla.clear()
            tabla.setRowCount(len(datos_ocupacion))
            tabla.setColumnCount(5)
            tabla.setHorizontalHeaderLabels(["ID", "Clase", "Inscritos", "Aforo", "Ocupación %"])

            for fila, dato in enumerate(datos_ocupacion):
                for col, valor in enumerate(dato):
                    tabla.setItem(fila, col, QTableWidgetItem(str(valor)))

            if datos_ocupacion:
                total_ocupacion = 0
                clases_llenas = 0
                clase_mas_llena = datos_ocupacion[0]

                for dato in datos_ocupacion:
                    inscritos = int(dato[2])
                    aforo = int(dato[3])
                    ocupacion = float(dato[4])

                    total_ocupacion += ocupacion

                    if inscritos >= aforo:
                        clases_llenas += 1

                ocupacion_media = round(total_ocupacion / len(datos_ocupacion), 2)

                nombre_clase_mas_llena = clase_mas_llena[1]
                inscritos_mas_llena = clase_mas_llena[2]
                aforo_mas_llena = clase_mas_llena[3]
                plazas_libres = int(aforo_mas_llena) - int(inscritos_mas_llena)

                if hasattr(v, "label_Porcentaje_Ocupacion"):
                    v.label_Porcentaje_Ocupacion.setText(f"{ocupacion_media}%")

                if hasattr(v, "label_Clase_masLlena"):
                    v.label_Clase_masLlena.setText(str(nombre_clase_mas_llena))

                if hasattr(v, "label_inscritos"):
                    v.label_inscritos.setText(f"{inscritos_mas_llena}/{aforo_mas_llena} inscritos")

                if hasattr(v, "label_plazasLibres"):
                    v.label_plazasLibres.setText(str(plazas_libres))

                if hasattr(v, "label_Num_Clases"):
                    v.label_Num_Clases.setText(str(clases_llenas))

                if hasattr(v, "label_Porcentaje_Ocupacion_2"):
                    v.label_Porcentaje_Ocupacion_2.setText(f"{ocupacion_media}%")



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

        if hasattr(v, "label_Nombre"):
            perfil = self.modelo.perfil_usuario(id_u)
            if perfil:
                v.label_Nombre.setText(str(perfil[2]))

                if hasattr(v, "labelCorreoEntrenador"):
                    v.labelCorreoEntrenador.setText(str(perfil[4] or ""))

                if hasattr(v, "labelTelefonoEntrenador"):
                    v.labelTelefonoEntrenador.setText(str(perfil[3] or ""))

                if hasattr(v, "labelDireccionEntrenador"):
                    v.labelDireccionEntrenador.setText(str(perfil[7] or ""))

                if hasattr(v, "labelFechaAltaEntrenadorPerfil"):
                    v.labelFechaAltaEntrenadorPerfil.setText(str(perfil[8] or ""))

        if hasattr(v, "label_Num_Clases_semana"):
            clases = self.modelo.clases_de_entrenador(id_u)
            v.label_Num_Clases_semana.setText(str(len(clases)))

        if hasattr(v, "label_Num_Clases_Hoy"):
            clases = self.modelo.clases_de_entrenador(id_u)
            v.label_Num_Clases_Hoy.setText(str(len(clases)))

        if hasattr(v, "label_Num_Clientes_Total"):
            clases = self.modelo.clases_de_entrenador(id_u)
            total_clientes = 0

            for clase in clases:
                inscritos = self.modelo.clientes_inscritos_clase(clase[0])
                total_clientes += len(inscritos)

            v.label_Num_Clientes_Total.setText(str(total_clientes))

        if hasattr(v, "label_Porcentaje_Asistencia"):
            clases = self.modelo.clases_de_entrenador(id_u)
            total_registros = 0
            total_presentes = 0

            for clase in clases:
                asistencias = self.modelo.consultar_asistencia_clase(clase[0])

                for asistencia in asistencias:
                    total_registros += 1
                    if asistencia[2] == "si":
                        total_presentes += 1

            if total_registros > 0:
                porcentaje = round((total_presentes * 100) / total_registros, 2)
            else:
                porcentaje = 0

            v.label_Porcentaje_Asistencia.setText(f"{porcentaje}%")

        if hasattr(v, "comboSeleccionarClase"):
            clases = self.modelo.clases_de_entrenador(id_u)

            try:
                v.comboSeleccionarClase.currentIndexChanged.disconnect()
            except Exception:
                pass

            v.comboSeleccionarClase.clear()

            for clase in clases:
                id_clase = clase[0]
                nombre = clase[1]
                dia = clase[2]
                hora_inicio = clase[3]
                hora_fin = clase[4]

                v.comboSeleccionarClase.addItem(
                    f"{nombre} - {dia} {hora_inicio} - {hora_fin}",
                    id_clase
                )

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
            tabla = v.tablaInscritos
            tabla.clear()
            tabla.setRowCount(len(datos))
            tabla.setColumnCount(3)
            tabla.setHorizontalHeaderLabels(["Cliente", "Teléfono", "Email"])

            for fila, cliente in enumerate(datos):
                nombre = cliente[1]
                telefono = cliente[2]
                email = cliente[3]

                tabla.setItem(fila, 0, QTableWidgetItem(str(nombre)))
                tabla.setItem(fila, 1, QTableWidgetItem(str(telefono)))
                tabla.setItem(fila, 2, QTableWidgetItem(str(email)))

        if hasattr(v, "label_numInscritos_ins"):
            v.label_numInscritos_ins.setText(str(len(datos)))

        if hasattr(v, "label_total_inscritos"):
            v.label_total_inscritos.setText(str(len(datos)))

        info = self.modelo.informacion_clase_con_sala(id_clase)

        if info:
            nombre_clase = info[0]
            sala = info[1]
            dia = info[2]
            hora_inicio = info[3]
            hora_fin = info[4]

            if hasattr(v, "label_nombreclase_ins"):
                v.label_nombreclase_ins.setText(str(nombre_clase))

            if hasattr(v, "lblSalaClase_ins"):
                v.lblSalaClase_ins.setText(str(sala))

            if hasattr(v, "label_fecha_ins"):
                v.label_fecha_ins.setText(str(dia))

            if hasattr(v, "lblHorarioClase_ins"):
                v.lblHorarioClase_ins.setText(f"{hora_inicio} - {hora_fin}")

            

    def cargar_inscritos_asistencia(self):
        v = self.ventana

        if not hasattr(v, "comboSeleccionarClase"):
            return

        id_clase = v.comboSeleccionarClase.currentData()

        if id_clase is None:
            return

        datos = self.modelo.clientes_inscritos_clase(id_clase)

        if not hasattr(v, "tablaInscritosAsistencia"):
            return

        tabla = v.tablaInscritosAsistencia
        tabla.clear()
        tabla.setRowCount(len(datos))
        tabla.setColumnCount(3)
        tabla.setHorizontalHeaderLabels(["Cliente", "Estado", "Acción"])

        for fila, cliente in enumerate(datos):
            id_cliente = cliente[0]
            nombre = cliente[1]

            tabla.setItem(fila, 0, QTableWidgetItem(f"{id_cliente} - {nombre}"))
            tabla.setItem(fila, 1, QTableWidgetItem("Pendiente"))
            tabla.setItem(fila, 2, QTableWidgetItem("Escribe si o no"))

        if hasattr(v, "label_TotalInscritos"):
            v.label_TotalInscritos.setText(str(len(datos)))

        if hasattr(v, "label_numInscritos"):
            v.label_numInscritos.setText(str(len(datos)))

        if hasattr(v, "label_numAsist"):
            v.label_numAsist.setText("0")

        if hasattr(v, "label_numPend"):
            v.label_numPend.setText(str(len(datos)))

        if hasattr(v, "label_numAus"):
            v.label_numAus.setText("0")

        clase = self.modelo.buscar_clase(id_clase)

        if clase:
            nombre = clase[3]
            dia = clase[5]
            hora_inicio = clase[6]
            hora_fin = clase[7]

            if hasattr(v, "label_nombreclase"):
                v.label_nombreclase.setText(str(nombre))

            if hasattr(v, "label_fecha"):
                v.label_fecha.setText(str(dia))

            if hasattr(v, "lblHorarioClase"):
                v.lblHorarioClase.setText(f"{hora_inicio} - {hora_fin}")

    def actualizar_resumen_asistencia(self):
        v = self.ventana

        if not hasattr(v, "tablaInscritosAsistencia"):
            return

        tabla = v.tablaInscritosAsistencia
        total = tabla.rowCount()
        asistieron = 0

        for fila in range(total):
            check = tabla.cellWidget(fila, 4)
            if check and check.isChecked():
                asistieron += 1

        ausencias = total - asistieron

        if hasattr(v, "label_numAsist"):
            v.label_numAsist.setText(str(asistieron))

        if hasattr(v, "label_numAus"):
            v.label_numAus.setText(str(ausencias))

        if hasattr(v, "label_numPend"):
            v.label_numPend.setText("0")

        if hasattr(v, "label_TotalInscritos"):
            v.label_TotalInscritos.setText(str(total))

        if hasattr(v, "label_numInscritos"):
            v.label_numInscritos.setText(str(total))

    def guardar_asistencia(self):
        v = self.ventana

        try:
            if not hasattr(v, "comboSeleccionarClase"):
                QMessageBox.warning(v, "Error", "No hay selector de clase")
                return

            id_clase = v.comboSeleccionarClase.currentData()

            if id_clase is None:
                QMessageBox.warning(v, "Error", "Selecciona una clase")
                return

            fecha = date.today().isoformat()
            presentes = []
            total = 0
            ausencias = 0
            pendientes = 0

            if hasattr(v, "tablaInscritosAsistencia"):
                tabla = v.tablaInscritosAsistencia

                for fila in range(tabla.rowCount()):
                    item_cliente = tabla.item(fila, 0)
                    item_estado = tabla.item(fila, 1)

                    if not item_cliente:
                        continue

                    total += 1

                    id_cliente = int(item_cliente.text().split(" - ")[0])
                    estado = item_estado.text().strip().lower() if item_estado else ""

                    if estado in ["si", "sí", "asistio", "asistió"]:
                        presentes.append(id_cliente)
                    elif estado in ["no", "ausencia", "ausente"]:
                        ausencias += 1
                    else:
                        pendientes += 1

            self.modelo.registrar_asistencia_lista(id_clase, fecha, presentes)

            if hasattr(v, "label_numAsist"):
                v.label_numAsist.setText(str(len(presentes)))

            if hasattr(v, "label_numPend"):
                v.label_numPend.setText(str(pendientes))

            if hasattr(v, "label_numAus"):
                v.label_numAus.setText(str(ausencias))

            if hasattr(v, "label_TotalInscritos"):
                v.label_TotalInscritos.setText(str(total))

            QMessageBox.information(
                v,
                "Correcto",
                f"Asistencia guardada correctamente.\nAsistieron: {len(presentes)}"
            )

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
