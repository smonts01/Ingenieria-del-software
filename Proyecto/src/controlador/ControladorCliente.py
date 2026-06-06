import os
from src.vista.componentes import CargadorVista, MensajeView, TablaView
from datetime import date, timedelta


class ControladorCliente:
    """
    Controlador del perfil Cliente.

    Responsabilidad MVC:
    - Carga vistas .ui y conecta botones.
    - Lee/escribe widgets de la interfaz.
    - Llama siempre a la capa Logica mediante self.modelo.
    - No accede directamente a DAO ni ejecuta SQL.
    """

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None
        self._vo = None

    def abrir(self):
        self.abrir_pantalla("interfaz_cliente_inicio.ui")

    def abrir_pantalla(self, archivo):
        if self.ventana:
            self.ventana.close()

        ruta = os.path.join(self.ruta_ui, archivo)
        self.ventana = CargadorVista.cargar(ruta)
        self._cargar_vo_cliente()
        self.conectar_botones()
        self.cargar_datos()
        self.ventana.show()

    def _cargar_vo_cliente(self):
        id_cliente = self.usuario["id_usuario"]

        try:
            self._vo = self.modelo.datos_inicio_cliente(id_cliente)
            print("VO CLIENTE:", self._vo)
        except Exception as e:
            print("ERROR AL CARGAR VO CLIENTE:", repr(e))
            self._vo = None

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

        if hasattr(v, "lblTabRes"):
            v.lblTabRes.mousePressEvent = lambda event: self.abrir_pantalla("interfaz_cliente_clases_reservas.ui")

        if hasattr(v, "lblTabTodas"):
            v.lblTabTodas.mousePressEvent = lambda event: self.abrir_pantalla("interfaz_cliente_clases_todas.ui")
        
        
        # Pantalla de clases: botones de reserva
        for i in range(1, 6):
            boton = getattr(v, f"btnReservar{i}", None)
            if boton:
                boton.clicked.connect(lambda checked=False, n=i: self.reservar_clase_card(n))
        
                # Buscador de clases
        if hasattr(v, "txtBuscarClases"):
            v.txtBuscarClases.textChanged.connect(self.filtrar_clases)

        # Combo de tipo/categoría
        if hasattr(v, "cmbTipo"):
            v.cmbTipo.blockSignals(True)
            v.cmbTipo.clear()
            try:
                clases = self.modelo.listar_clases()
                nombres = sorted(set(str(c[1]).strip() for c in clases if c[1]))
            except Exception:
                nombres = []
            v.cmbTipo.addItems(["Todas las categorías"] + nombres)
            v.cmbTipo.blockSignals(False)
            v.cmbTipo.currentIndexChanged.connect(self.filtrar_clases)

        # Combo de horario
        if hasattr(v, "cmbHorario"):
            v.cmbHorario.blockSignals(True)
            v.cmbHorario.clear()
            try:
                clases = self.modelo.listar_clases()
                horarios = sorted(set(
                    f"{str(c[3])[:5]} - {str(c[4])[:5]}"
                    for c in clases if c[3] and c[4]
                ))
            except Exception:
                horarios = []
            v.cmbHorario.addItems(["Todos los horarios"] + horarios)
            v.cmbHorario.blockSignals(False)
            v.cmbHorario.currentIndexChanged.connect(self.filtrar_clases)
        
        if hasattr(v, "btnPeriodo"):
            hoy = date.today()
            lunes = hoy - timedelta(days=hoy.weekday())
            domingo = lunes + timedelta(days=6)
            rango = f"{lunes.day} - {domingo.day} {domingo.strftime('%B %Y').lower()}"
            v.btnPeriodo.setText(rango)

        # Pantalla perfil: guardar cambios
        if hasattr(v, "btnGuardarCambios"):
            v.btnGuardarCambios.clicked.connect(self.guardar_perfil)

    def cargar_datos(self):
        if self._vo is None:
            MensajeView.warning(self.ventana, "Error", "No se pudieron cargar los datos del cliente")
            return

        self._rellenar_cabecera()

        v = self.ventana
        if hasattr(v, "lblBienvenida"):
            self._cargar_inicio()
        elif hasattr(v, "lblTituloClases"):
            self._cargar_clases_todas()
        elif hasattr(v, "lblTituloReservas"):
            self._cargar_reservas()
        elif hasattr(v, "lblTituloEstadisticas"):
            self._cargar_estadisticas()
        elif hasattr(v, "lblTituloPerfil"):
            self._cargar_perfil()

    def _rellenar_cabecera(self):
        v = self.ventana
        vo = self._vo

        if hasattr(v, "lblNombreCliente"):
            v.lblNombreCliente.setText(str(vo.nombre))

        if hasattr(v, "lblFechaAltaCliente"):
            v.lblFechaAltaCliente.setText(f"Cliente desde {vo.fecha_registro}")

    def _cargar_inicio(self):
        v = self.ventana
        vo = self._vo

        if hasattr(v, "lblBienvenida"):
            v.lblBienvenida.setText(f"Bienvenida, {vo.nombre}")
        if hasattr(v, "lblNumClases"):
            v.lblNumClases.setText(str(len(vo.proximas_clases)))
        if hasattr(v, "lblEstadoPago"):
            v.lblEstadoPago.setText(str(vo.estado_pagado).capitalize())
        if hasattr(v, "lblSubPago"):
            if str(vo.estado_pagado).lower() == "abonado":
                v.lblSubPago.setText("Sin pagos pendientes")
            else:
                v.lblSubPago.setText("Tienes pagos pendientes")
        if hasattr(v, "lblCaloriasSemana"):
            v.lblCaloriasSemana.setText(f"{vo.calorias_semana} kcal")
        if hasattr(v, "lblAsistencias"):
            v.lblAsistencias.setText(vo.get_asistencias_str())
        if hasattr(v, "lblCuota"):
            v.lblCuota.setText(str(vo.nombre_tarifa))
        if hasattr(v, "lblCantidadPago"):
            v.lblCantidadPago.setText(vo.get_precio_str())
        if hasattr(v, "lblMesPago"):
            v.lblMesPago.setText(str(vo.ultimo_pago_fecha))
        if hasattr(v, "lblPendientePago"):
            v.lblPendientePago.setText(str(vo.ultimo_pago_estado).capitalize())
        if hasattr(v, "tablaProximasClases"):
            self._rellenar_tabla_proximas(v.tablaProximasClases, vo.proximas_clases)

    def _cargar_clases_todas(self):
        v = self.ventana
        id_cliente = self.usuario["id_usuario"]

        clases = self.modelo.clases_ocupacion_cliente()
        inscritas = self.modelo.clases_inscritas_cliente(id_cliente)

        asistidas = self.modelo.clases_asistidas_cliente(id_cliente)

    

        ids_inscritas = []

        descripciones = {
            "yoga": "Flexibilidad y relajación.",
            "pilates": "Core y postura.",
            "spinning": "Cardio de alta intensidad.",
            "zumba": "Baile y cardio.",
            "crossfit": "Fuerza y resistencia.",
        }

        for ins in inscritas:
            ids_inscritas.append(ins.id_clase)


        self._cards_clases = []



        for i, clase in enumerate(clases[:5], start=1):
            
            id_clase = clase[0]
            nombre = clase[1]
            dia = clase[2]
            hora_inicio = str(clase[3])[:5]
            hora_fin = str(clase[4])[:5]
            sala = clase[5]
            inscritos = clase[6]
            aforo = clase[7]
            
            horario = f"{hora_inicio} - {hora_fin}"

            lbl_clase = getattr(v, f"lblClase{i}", None)
            
            labels_desc = {
                1: "lblDesc1",
                2: "lblDesc2",
                3: "lblDesc3",
                4: "lblDesc4",
                5: "lblDesc4_2",
            }

            lbl_desc = getattr(v, labels_desc.get(i), None)

            if lbl_desc:
                descripcion = descripciones.get(
                    str(nombre).strip().lower(),
                    "Clase disponible para reservar."
                )
                lbl_desc.setText(descripcion)
            
            labels_fecha = {
                1: "lblFecha1",
                2: "lblFecha2",
                3: "lblFecha3",
                4: "lblFecha4",
                5: "lblFecha4_2",
            }

            lbl_fecha = getattr(v, labels_fecha.get(i), None)


            labels_plazas = {
                1: "lblPlazas1",
                2: "lblPlazas2",
                3: "lblPlazas3",
                4: "lblPlazas4",
                5: "lblPlazas4_2",
            }

            lbl_ocupacion = getattr(v, labels_plazas.get(i), None)
            btn = getattr(v, f"btnReservar{i}", None)

            if lbl_clase:
                lbl_clase.setText(str(nombre))

           

            if lbl_fecha:
                lbl_fecha.setText(f"{dia}\n{hora_inicio} - {hora_fin}\n{sala}")

            if lbl_ocupacion:
                lbl_ocupacion.setText(f"{inscritos} / {aforo}")

            if btn:
                if id_clase in asistidas:
                    btn.setText("Realizada")
                    btn.setEnabled(False)
                elif id_clase in ids_inscritas:
                    btn.setText("Cancelar")
                    btn.setEnabled(True)
                else:
                    btn.setText("Reservar")
                    btn.setEnabled(True)

            nombres_cards = {
                1: "cardClase1",
                2: "cardClase2",
                3: "cardClase3",
                4: "cardClase4",
                5: "cardClase4_2",
            }

            card = getattr(v, nombres_cards.get(i), None)

            self._cards_clases.append({
                "card": card,
                "nombre": str(nombre).lower(),
                "horario": horario,
            })
            
        
        if hasattr(v, "lblProxDatos"):
            proxima = None

            for clase in clases:
                id_clase = clase[0]

                if id_clase not in asistidas:
                    proxima = clase
                    break

            if proxima:
                nombre = proxima[1]
                dia = proxima[2]
                hora_inicio = str(proxima[3])[:5]
                hora_fin = str(proxima[4])[:5]
                sala = proxima[5]

                v.lblProxDatos.setText(f"{nombre}\n{dia} · {hora_inicio} - {hora_fin}\n{sala}")
            else:
                v.lblProxDatos.setText("No tienes próximas clases")

    def _cargar_reservas(self):
        v = self.ventana
        id_cliente = self.usuario["id_usuario"]

        
        reservas = self._vo.proximas_clases

        clases_ocupacion = self.modelo.clases_ocupacion_cliente()

        ocupacion_por_id = {}
        for clase in clases_ocupacion:
            id_clase = clase[0]
            ocupacion_por_id[id_clase] = {
                "inscritos": clase[6],
                "aforo": clase[7],
            }

        descripciones = {
            "yoga": "Flexibilidad y relajación.",
            "pilates": "Core y postura.",
            "spinning": "Cardio de alta intensidad.",
            "zumba": "Baile y cardio.",
            "crossfit": "Fuerza y resistencia.",
        }

        cards = {
            1: "cardReserva1",
            2: "cardReserva2",
            3: "cardReserva3",
            4: "cardReserva4",
        }

        labels_clase = {
            1: "lblReservaClase1",
            2: "lblReservaClase2",
            3: "lblReservaClase3",
            4: "lblReservaClase4",
        }

        labels_desc = {
            1: "lblReservaDesc1",
            2: "lblReservaDesc2",
            3: "lblReservaDesc3",
            4: "lblReservaDesc4",
        }

        labels_fecha = {
            1: "lblReservaFecha1",
            2: "lblReservaFecha2",
            3: "lblReservaFecha3",
            4: "lblReservaFecha4",
        }

        labels_plazas = {
            1: "lblPlazasReserva1",
            2: "lblPlazasReserva2",
            3: "lblPlazasReserva3",
            4: "lblPlazasReserva4",
        }

        labels_estado = {
            1: "lblEstadoReserva1",
            2: "lblEstadoReserva2",
            3: "lblEstadoReserva3",
            4: "lblEstadoReserva4",
        }

        for i in range(1, 5):
            card = getattr(v, cards.get(i), None)
            if card:
                card.setVisible(False)

        for i, reserva in enumerate(reservas[:4], start=1):
            nombre = reserva.get("nombre_actividad", "")
            dia = reserva.get("fecha", "")
            hora_inicio = str(reserva.get("hora_inicio", ""))[:5]
            hora_fin = ""
            sala = reserva.get("nombre_sala", "")

            
            inscritos = 0
            aforo = 0

            for clase in clases_ocupacion:
                if str(clase[1]).lower() == str(nombre).lower():
                    inscritos = clase[6]
                    aforo = clase[7]
                    break
            

            card = getattr(v, cards.get(i), None)
            lbl_clase = getattr(v, labels_clase.get(i), None)
            lbl_desc = getattr(v, labels_desc.get(i), None)
            lbl_fecha = getattr(v, labels_fecha.get(i), None)
            lbl_plazas = getattr(v, labels_plazas.get(i), None)
            lbl_estado = getattr(v, labels_estado.get(i), None)

            if card:
                card.setVisible(True)

            if lbl_clase:
                lbl_clase.setText(str(nombre))

            if lbl_desc:
                clave = str(nombre).strip().lower()
                lbl_desc.setText(descripciones.get(clave, "Clase reservada."))

            if lbl_fecha:
                lbl_fecha.setText(f"{dia}\n{hora_inicio}\n{sala}")

            if lbl_plazas:
                lbl_plazas.setText(f"Plazas: {inscritos} / {aforo}")

            if lbl_estado:
                lbl_estado.setText("Reserva confirmada")

    def _cargar_estadisticas(self):
        v = self.ventana
        vo = self._vo

        if hasattr(v, "lblNumEntrenos"):
            v.lblNumEntrenos.setText(str(vo.entrenos_semana))
        if hasattr(v, "lblSubEntrenos"):
            v.lblSubEntrenos.setText(vo.get_delta_entrenos_str())
        if hasattr(v, "lblNumTiempo"):
            v.lblNumTiempo.setText(vo.get_tiempo_semana_str())
        if hasattr(v, "lblSubTiempo"):
            v.lblSubTiempo.setText(vo.get_delta_tiempo_str())
        if hasattr(v, "lblNumCalorias"):
            v.lblNumCalorias.setText(f"{vo.calorias_semana} kcal")

        objetivo = self.modelo.calcular_objetivo_semanal(vo.calorias_semana)

        if hasattr(v, "lblNumObjetivo"):
            v.lblNumObjetivo.setText(objetivo["texto_porcentaje"])

        if hasattr(v, "lblTextoObjetivo"):
            v.lblTextoObjetivo.setText(objetivo["texto_objetivo"])



        if hasattr(v, "btnMini"):
            v.btnMini.setText(f"Total semanal: {vo.calorias_semana} kcal")

        
        calorias_dias = self.modelo.calorias_semana_por_dia(self.usuario["id_usuario"])

        barras = {
            "lunes": getattr(v, "barLun", None),
            "martes": getattr(v, "barMar", None),
            "miercoles": getattr(v, "barMie", None),
            "jueves": getattr(v, "barJue", None),
            "viernes": getattr(v, "barVie", None),
            "sabado": getattr(v, "barSab", None),
        }

        max_kcal = max(calorias_dias.values()) if calorias_dias else 0

        if max_kcal == 0:
            max_kcal = 1

        altura_maxima = 80

        for dia, barra in barras.items():
            if barra:
                kcal = calorias_dias.get(dia, 0)
                altura = int((kcal / max_kcal) * altura_maxima)

                if kcal == 0:
                    altura = 0
                elif altura < 8:
                    altura = 8

                geo = barra.geometry()
                bottom = geo.y() + geo.height()

                barra.setGeometry(
                    geo.x(),
                    bottom - altura,
                    geo.width(),
                    altura
                )

        if hasattr(v, "dias"):
            v.dias.setText("Lun          Mar          Mié          Jue          Vie          Sáb")

        if hasattr(v, "lblTotalCalorias"):
            v.lblTotalCalorias.setText(f"Total semanal: {sum(calorias_dias.values())} kcal")
                        

        if hasattr(v, "lblNumEntrenos_2"):
            v.lblNumEntrenos_2.setText(str(vo.racha_dias))
        if hasattr(v, "lblSigueRacha"):
            v.lblSigueRacha.setText(f"Llevas {vo.racha_dias} días consecutivos entrenando.")

        self._rellenar_leyendas_distribucion(vo.distribucion_tipos)

    def _cargar_perfil(self):
        v = self.ventana
        vo = self._vo

        if hasattr(v, "lblNombreCompleto"):
            v.lblNombreCompleto.setText(str(vo.nombre))
        if hasattr(v, "lblEmailPerfil"):
            v.lblEmailPerfil.setText(str(vo.email))
        if hasattr(v, "txtNombre"):
            v.txtNombre.setText(str(vo.nombre))
        if hasattr(v, "lblNumTelefono"):
            v.lblNumTelefono.setText(str(vo.telefono))
        if hasattr(v, "lblCorreoElectronico"):
            v.lblCorreoElectronico.setText(str(vo.email))
        if hasattr(v, "lblFechaNacimiento"):
            v.lblFechaNacimiento.setText(str(vo.fecha_nacimiento))
        if hasattr(v, "lblDireccion"):
            v.lblDireccion.setText(str(vo.direccion))
        if hasattr(v, "lblAsistenciasValor"):
            v.lblAsistenciasValor.setText(f"{vo.asistencias_mes} / {vo.inscripciones_mes} clases")

        objetivo = self.modelo.calcular_objetivo_semanal(vo.calorias_semana)

        if hasattr(v, "lblPorcentaje"):
            v.lblPorcentaje.setText(objetivo["texto_porcentaje"])

        if hasattr(v, "barraProgresoValor") and hasattr(v, "barraProgresoFondo"):
            porcentaje = objetivo["porcentaje"]

            ancho_fondo = v.barraProgresoFondo.width()
            ancho_valor = int(ancho_fondo * porcentaje / 100)

            v.barraProgresoValor.setFixedWidth(ancho_valor)

    def reservar_clase_card(self, numero_card):
        v = self.ventana

        labels_clase = {
            1: "lblClase1",
            2: "lblClase2",
            3: "lblClase3",
            4: "lblClase4",
            5: "lblClase4_2",
        }

        label = getattr(v, labels_clase.get(numero_card), None)

        if label is None:
            MensajeView.warning(v, "Error", "No se ha encontrado la clase seleccionada")
            return

        nombre_clase = label.text().strip()

        if not nombre_clase:
            MensajeView.warning(v, "Error", "No se ha seleccionado ninguna clase")
            return

        boton = getattr(v, f"btnReservar{numero_card}", None)
        accion = boton.text().strip().lower() if boton else "reservar"

        try:
            if accion == "cancelar":
                self.modelo.desapuntarse_clase_por_nombre(
                    self.usuario["id_usuario"],
                    nombre_clase
                )
                MensajeView.information(
                    v,
                    "Reserva cancelada",
                    f"Te has desapuntado de {nombre_clase}."
                )
            else:
                self.modelo.inscribirse_clase_por_nombre(
                    self.usuario["id_usuario"],
                    nombre_clase
                )
                MensajeView.information(
                    v,
                    "Reserva confirmada",
                    f"Te has inscrito en {nombre_clase}."
                )

            self._cargar_vo_cliente()
            self.cargar_datos()

        except Exception as e:
            MensajeView.warning(v, "Error al gestionar la reserva", str(e))

    def guardar_perfil(self):
        v = self.ventana

        telefono = v.txtTelefono.text().strip() if hasattr(v, "txtTelefono") else ""
        email = v.txtEmail.text().strip() if hasattr(v, "txtEmail") else ""
        direccion = v.txtDireccion.text().strip() if hasattr(v, "txtDireccion") else ""

        if not email:
            MensajeView.warning(v, "Error", "El email no puede estar vacío")
            return

        try:
            self.modelo.modificar_usuario(self.usuario["id_usuario"], telefono, email, direccion)
            MensajeView.information(v, "Perfil actualizado", "Los cambios se han guardado correctamente")
            self._cargar_vo_cliente()
            self.cargar_datos()
        except Exception as e:
            MensajeView.warning(v, "Error al guardar", str(e))

    def _rellenar_tabla_proximas(self, tabla, datos):
        cabeceras = ["Clase", "Fecha", "Hora", "Sala"]
        TablaView.configurar_columnas(tabla, cabeceras)
        tabla.setColumnCount(len(cabeceras))
        tabla.setHorizontalHeaderLabels(cabeceras)
        tabla.setRowCount(len(datos))

        for fila, registro in enumerate(datos):
            valores = [
                registro.get("nombre_actividad", ""),
                registro.get("fecha", ""),
                registro.get("hora_inicio", ""),
                registro.get("nombre_sala", ""),
            ]
            for col, valor in enumerate(valores):
                tabla.setItem(fila, col, TablaView.crear_item(str(valor), editable=False))

    def _rellenar_leyendas_distribucion(self, distribucion):
        v = self.ventana
        labels = [
            getattr(v, "lblLeyenda1", None),
            getattr(v, "lblLeyenda2", None),
            getattr(v, "lblLeyenda3", None),
            getattr(v, "lblLeyenda4", None),
        ]
        items = list(distribucion.items()) if isinstance(distribucion, dict) else []

        for i, label in enumerate(labels):
            if label is None:
                continue
            if i < len(items):
                tipo, porcentaje = items[i]
                label.setText(f"● {tipo} {porcentaje}%")
            else:
                label.setText("")

    def filtrar_clases(self):
        v = self.ventana

        if not hasattr(self, "_cards_clases"):
            return

        texto = ""
        if hasattr(v, "txtBuscarClases"):
            texto = v.txtBuscarClases.text().strip().lower()

        tipo = "todas las categorías"
        if hasattr(v, "cmbTipo"):
            tipo = v.cmbTipo.currentText().strip().lower()

        horario = "todos los horarios"
        if hasattr(v, "cmbHorario"):
            horario = v.cmbHorario.currentText().strip().lower()

        for item in self._cards_clases:
            card = item["card"]

            if card is None:
                continue

            coincide_texto = texto == "" or texto in item["nombre"]
            coincide_tipo = tipo == "todas las categorías" or tipo == item["nombre"]
            coincide_horario = horario == "todos los horarios" or horario == item["horario"].lower()

            card.setVisible(coincide_texto and coincide_tipo and coincide_horario)

    def cerrar_sesion(self):
        if self.ventana:
            self.ventana.close()
        self.vista_login.show()
