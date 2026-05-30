import os
from src.vista.componentes import CargadorVista, MensajeView, TablaView, ImagenView


class ControladorCliente:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None

    #Abrir interfaz inicio
    def abrir(self):
        self.abrir_pantalla("interfaz_cliente_inicio.ui")

    def abrir_pantalla(self, archivo):
        if self.ventana:
            self.ventana.close()
        ruta = os.path.join(self.ruta_ui, archivo)
        self.ventana = CargadorVista.cargar(ruta)
        self.conectar_botones()
        self.cargar_datos()
        self.ventana.show()

    #Conexion de los botones
    def conectar_botones(self):
        v = self.ventana

        # Menu lateral
        if hasattr(v, "btnCerrarSesion"):
            v.btnCerrarSesion.clicked.connect(self.cerrar_sesion)
        if hasattr(v, "btnInicio"):
            v.btnInicio.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_cliente_inicio.ui"))
        if hasattr(v, "btnClases"):
            v.btnClases.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_cliente_clases_todas.ui"))
        if hasattr(v, "btnEstadisticas"):
            v.btnEstadisticas.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_cliente_estadisticas.ui"))
        if hasattr(v, "btnPerfil"):
            v.btnPerfil.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_cliente_perfil.ui"))
        if hasattr(v, "btnInformacion"):
            v.btnInformacion.clicked.connect(
                lambda: self.abrir_pantalla("interfaz_cliente_informacion.ui"))

        # Pantalla clases todas
        if hasattr(v, "lblTabRes"):
            v.lblTabRes.mousePressEvent = lambda e: self.abrir_pantalla(
                "interfaz_cliente_clases_reservas.ui")
        for i in range(1, 5):
            btn = f"btnReservar{i}"
            if hasattr(v, btn):
                getattr(v, btn).clicked.connect(
                    lambda checked, n=i: self.reservar_clase(n))
        if hasattr(v, "btnReservar5"):
            v.btnReservar5.clicked.connect(lambda: self.reservar_clase(5))
        if hasattr(v, "txtBuscarClases"):
            v.txtBuscarClases.textChanged.connect(self.filtrar_clases)
        if hasattr(v, "cmbTipo") and v.cmbTipo.count() == 0:
            v.cmbTipo.addItems(
                ["Todos", "Yoga", "Pilates", "Spinning", "Zumba", "Crossfit"])
        if hasattr(v, "cmbTipo"):
            v.cmbTipo.currentIndexChanged.connect(self.filtrar_clases)
        if hasattr(v, "cmbHorario") and v.cmbHorario.count() == 0:
            v.cmbHorario.addItems(
                ["Todos", "09:00-10:00", "10:00-11:00",
                 "11:00-12:00", "17:00-18:00", "18:00-19:00"])
        if hasattr(v, "cmbHorario"):
            v.cmbHorario.currentIndexChanged.connect(self.filtrar_clases)

        # Pantalla clases reservas
        if hasattr(v, "lblTabTodas"):
            v.lblTabTodas.mousePressEvent = lambda e: self.abrir_pantalla(
                "interfaz_cliente_clases_todas.ui")

    # Cargar datos
    def cargar_datos(self):
        v = self.ventana
        uid = self.usuario["id_usuario"]
        
        try:
            datos = self.modelo.datos_inicio_cliente(uid)
        except Exception as e:
            print(f"Error datos_inicio_cliente: {e}")
            datos = None

        # Cabecera común
        nombre = datos.nombre if datos else self.usuario.get("nombre", "")
        fecha_registro = datos.fecha_registro if datos else "-"

        if hasattr(v, "lblNombreCliente"):
            v.lblNombreCliente.setText(nombre)
        if hasattr(v, "lblFechaAltaCliente"):
            v.lblFechaAltaCliente.setText(str(fecha_registro))
        if hasattr(v, "lblBienvenida"):
            v.lblBienvenida.setText(f"¡Hola, {nombre}!")

        # PANTALLA INICIO
        if hasattr(v, "lblNumClases"):
            try:
                v.lblNumClases.setText(
                    str(datos.clases_semana) if datos else "0")
            except:
                v.lblNumClases.setText("0")

        if hasattr(v, "lblAsistencias"):
            try:
                v.lblAsistencias.setText(
                    str(datos.asistencias_mes) if datos else "0")
            except:
                v.lblAsistencias.setText("0")

        if hasattr(v, "lblCaloriasSemana"):
            try:
                v.lblCaloriasSemana.setText(
                    str(datos.calorias_semana) if datos else "0")
            except:
                v.lblCaloriasSemana.setText("0")

        # Tarjeta de pago
        if hasattr(v, "lblCantidadPago"):
            try:
                v.lblCantidadPago.setText(
                    f"{float(datos.precio_tarifa):.2f}€" if datos else "0.00€")
            except:
                v.lblCantidadPago.setText("0.00€")

        if hasattr(v, "lblCuota"):
            try:
                v.lblCuota.setText(datos.nombre_tarifa if datos else "-")
            except:
                v.lblCuota.setText("-")

        if hasattr(v, "lblEstadoPago"):
            try:
                v.lblEstadoPago.setText(
                    datos.ultimo_pago_estado if datos else "-")
            except:
                v.lblEstadoPago.setText("-")

        if hasattr(v, "lblPendientePago"):
            try:
                pendiente = (datos.ultimo_pago_estado == "pendiente") if datos else False
                v.lblPendientePago.setVisible(pendiente)
            except:
                v.lblPendientePago.setVisible(False)

        if hasattr(v, "lblMesPago"):
            try:
                v.lblMesPago.setText(datos.ultimo_pago_fecha if datos else "-")
            except:
                v.lblMesPago.setText("-")

        # Tabla próximas clases
        if hasattr(v, "tablaProximasClases"):
            try:
                filas = []
                if datos and datos.proximas_clases:
                    for c in datos.proximas_clases:
                        filas.append([
                            c.get("nombre_actividad", ""),
                            c.get("fecha", ""),
                            c.get("hora_inicio", ""),
                            c.get("nombre_sala", ""),
                        ])
                cabeceras = ["Clase", "Día", "Hora", "Sala"]
                self._rellenar_con_cabeceras(v.tablaProximasClases, filas, cabeceras)
            except Exception as e:
                print(f"Error tablaProximasClases: {e}")

        # PANTALLA CLASES TODAS 
        self._cargar_cards_clases()

        # PANTALLA RESERVAS
        self._cargar_cards_reservas()

        # PANTALLA ESTADÍSTICAS
        if hasattr(v, "lblNumEntrenos"):
            try:
                v.lblNumEntrenos.setText(
                    str(datos.entrenos_semana) if datos else "0")
            except:
                v.lblNumEntrenos.setText("0")

        if hasattr(v, "lblNumEntrenos_2"):
            try:
                v.lblNumEntrenos_2.setText(
                    str(datos.asistencias_mes) if datos else "0")
            except:
                v.lblNumEntrenos_2.setText("0")

        if hasattr(v, "lblNumTiempo"):
            try:
                v.lblNumTiempo.setText(
                    f"{datos.tiempo_semana_min} min" if datos else "0 min")
            except:
                v.lblNumTiempo.setText("0 min")

        if hasattr(v, "lblNumCalorias"):
            try:
                v.lblNumCalorias.setText(
                    str(datos.calorias_semana) if datos else "0")
            except:
                v.lblNumCalorias.setText("0")

        if hasattr(v, "lblNumObjetivo"):
            try:
                v.lblNumObjetivo.setText(
                    str(datos.racha_dias) if datos else "0")
            except:
                v.lblNumObjetivo.setText("0")

        if hasattr(v, "lblTotalCalorias"):
            try:
                v.lblTotalCalorias.setText(
                    str(datos.calorias_acumuladas) if datos else "0")
            except:
                v.lblTotalCalorias.setText("0")

        # Racha
        if hasattr(v, "lblSigueRacha"):
            try:
                v.lblSigueRacha.setText(
                    f"{datos.racha_dias} día(s)" if datos else "0 días")
            except:
                v.lblSigueRacha.setText("0 días")
                
        # Daigrama de barras 
        barras = ["barLun", "barMar", "barMie", "barJue", "barVie", "barSab"]
        if any(hasattr(v, b) for b in barras):
            MAX_HEIGHT = 120
            
            try:
                dist = datos.distribucion_tipos if datos else {}
                valores = list(dist.values())[:6]
                while len(valores) < 6:
                    valores.append(0)
            except:
                valores = [0] * 6

            for nombre_barra, pct in zip(barras, valores):
                barra = getattr(v, nombre_barra, None)
                if barra:
                    try:
                        barra.setFixedHeight(
                            max(4, int(int(pct) * MAX_HEIGHT / 100)))
                    except:
                        barra.setFixedHeight(4)

        # PANTALLA PERFIL 
        if hasattr(v, "lblNombrePerfil"):
            v.lblNombrePerfil.setText(nombre)

        if hasattr(v, "lblEmailPerfil"):
            try:
                v.lblEmailPerfil.setText(datos.email if datos else "")
            except:
                v.lblEmailPerfil.setText("")

        # Barra de progreso de objetivo
        if hasattr(v, "lblPorcentaje"):
            try:
                pct = datos.asistencias_mes if datos else 0
                OBJETIVO = 20
                pct_real = min(int(int(pct) * 100 / OBJETIVO), 100)
                v.lblPorcentaje.setText(f"{pct_real}%")
                if hasattr(v, "barraProgresoFondo") and hasattr(v, "barraProgresoValor"):
                    ancho_total = v.barraProgresoFondo.width() or 200
                    v.barraProgresoValor.setFixedWidth(
                        int(ancho_total * pct_real / 100))
            except:
                v.lblPorcentaje.setText("0%")

        if hasattr(v, "lblAsistenciasValor"):
            try:
                v.lblAsistenciasValor.setText(
                    str(datos.asistencias_mes) if datos else "0")
            except:
                v.lblAsistenciasValor.setText("0")

        if hasattr(v, "lblObjetivoSemanal"):
            try:
                v.lblObjetivoSemanal.setText(
                    f"Racha: {datos.racha_dias} día(s)" if datos else "-")
            except:
                v.lblObjetivoSemanal.setText("-")

        # Datos personales
        mapa_perfil = {
            "lblNombreCompleto":    "nombre",
            "lblNumTelefono":       "telefono",
            "lblCorreoElectronico": "email",
            "lblFechaNacimiento":   "fecha_nacimiento",
            "lblDIreccion":         "direccion",
        }
        for lbl, campo in mapa_perfil.items():
            if hasattr(v, lbl):
                try:
                    valor = getattr(datos, campo) if datos else "-"
                    getattr(v, lbl).setText(str(valor) if valor else "-")
                except:
                    getattr(v, lbl).setText("-")

        for lbl in ["lblPeso", "lblAltura", "lblGenero"]:
            if hasattr(v, lbl):
                getattr(v, lbl).setText("-")

        # PANTALLA INFORMACIÓN
        INFO_GIMNASIO = {
            "horario":    "Lun-Vie: 07:00 - 22:00  |  Sáb: 09:00 - 14:00",
            "direccion":  "Calle Principal 1, Ciudad",
            "email":      "info@stayfit.com",
            "telefono":   "+34 600 000 000",
            "sobre":      "Tu gimnasio de confianza. Instalaciones de primer nivel para alcanzar tus objetivos.",
            "normas": [
                "Respeta el material y las instalaciones.",
                "Reserva tu clase con antelación.",
                "Trae tu toalla y botella de agua.",
                "Mantén el orden en los vestuarios.",
                "Consulta con un entrenador ante cualquier duda.",
            ],
        }

        if hasattr(v, "lblHorarioTexto"):
            v.lblHorarioTexto.setText(INFO_GIMNASIO["horario"])
        if hasattr(v, "lblDireccionGimnasio"):
            v.lblDireccionGimnasio.setText(INFO_GIMNASIO["direccion"])
        if hasattr(v, "lblEmailGimnasio"):
            v.lblEmailGimnasio.setText(INFO_GIMNASIO["email"])
        if hasattr(v, "lblTelefonoGimnasio"):
            v.lblTelefonoGimnasio.setText(INFO_GIMNASIO["telefono"])
        if hasattr(v, "lblSobreTexto"):
            v.lblSobreTexto.setText(INFO_GIMNASIO["sobre"])
        for i, norma in enumerate(INFO_GIMNASIO["normas"], start=1):
            lbl = f"lblNorma{i}"
            if hasattr(v, lbl):
                getattr(v, lbl).setText(norma)

    # Clases disponibles
    _SLOTS_CLASES = {
        1: ("lblClase1",   "lblDesc1",   "lblFecha1",   "lblPlazas1",   "btnReservar1"),
        2: ("lblClase2",   "lblDesc2",   "lblFecha2",   "lblPlazas2",   "btnReservar2"),
        3: ("lblClase3",   "lblDesc3",   "lblFecha3",   "lblPlazas3",   "btnReservar3"),
        4: ("lblClase4",   "lblDesc4",   "lblFecha4",   "lblPlazas4",   "btnReservar4"),
        5: ("lblClase4_2", "lblDesc4_2", "lblFecha4_2", "lblPlazas4_2", "btnReservar5"),
    }

    def _cargar_cards_clases(self):
        """Rellena las 5 cards de clases disponibles."""
        v = self.ventana
        if not hasattr(v, "lblClase1"):
            return

        try:
            clases = self.modelo.listar_clases()
        except Exception as e:
            print(f"Error _cargar_cards_clases: {e}")
            clases = []

        for idx, (lbl_nombre, lbl_desc, lbl_fecha, lbl_plazas, btn) in \
                self._SLOTS_CLASES.items():
            clase = clases[idx - 1] if idx - 1 < len(clases) else None

            if hasattr(v, lbl_nombre):
                getattr(v, lbl_nombre).setText(
                    str(clase[1]) if clase else "-")          

            if hasattr(v, lbl_desc):
                nivel = str(clase[6]).capitalize() if clase else "-" 
                getattr(v, lbl_desc).setText(f"Nivel: {nivel}")

            if hasattr(v, lbl_fecha):
                if clase:
                    dia = str(clase[2]).capitalize()           
                    hora = str(clase[3])[:5]                 
                    getattr(v, lbl_fecha).setText(f"{dia}  {hora}")
                else:
                    getattr(v, lbl_fecha).setText("-")

            if hasattr(v, lbl_plazas):
                getattr(v, lbl_plazas).setText(
                    str(clase[5]) if clase else "-")          

            if hasattr(v, btn):
                getattr(v, btn).setEnabled(clase is not None)

        if hasattr(v, "lblProxDatos"):
            v.lblProxDatos.setText(f"{len(clases)} clase(s) disponibles")

    # Clases ya reservadas
    _SLOTS_RESERVAS = {
        1: ("lblReservaClase1", "lblReservaDesc1", "lblReservaFecha1",
            "lblPlazasReserva1", "lblBadge1",   "cardReserva1"),
        2: ("lblReservaClase2", "lblReservaDesc2", "lblReservaFecha2",
            "lblPlazasReserva2", "lblBadge1_2", "cardReserva2"),
        3: ("lblReservaClase3", "lblReservaDesc3", "lblReservaFecha3",
            "lblPlazasReserva3", "lblBadge1_3", "cardReserva3"),
        4: ("lblReservaClase4", "lblReservaDesc4", "lblReservaFecha4",
            "lblPlazasReserva4", "lblBadge1_4", "cardReserva4"),
    }

    def _cargar_cards_reservas(self):
        """Rellena las 4 cards de reservas activas del cliente."""
        v = self.ventana
        if not hasattr(v, "lblReservaClase1"):
            return

        uid = self.usuario["id_usuario"]
        try:
            reservas = self.modelo.clases_inscritas_cliente(uid)
        except Exception as e:
            print(f"Error _cargar_cards_reservas: {e}")
            reservas = []
            
        for slot in self._SLOTS_RESERVAS.values():
            card = getattr(v, slot[5], None)
            if card:
                card.setVisible(False)

        for idx, (lbl_clase, lbl_desc, lbl_fecha, lbl_plazas, lbl_badge, card_name) \
                in self._SLOTS_RESERVAS.items():
            reserva = reservas[idx - 1] if idx - 1 < len(reservas) else None

            card = getattr(v, card_name, None)
            if card:
                card.setVisible(reserva is not None)

            if reserva is None:
                continue

            if hasattr(v, lbl_clase):
                getattr(v, lbl_clase).setText(str(reserva[1]))   
            if hasattr(v, lbl_desc):
                nivel = str(reserva[5]).capitalize()              
                getattr(v, lbl_desc).setText(f"Nivel: {nivel}")
            if hasattr(v, lbl_fecha):
                dia = str(reserva[2]).capitalize()                
                hora = str(reserva[3])[:5]                        
                getattr(v, lbl_fecha).setText(f"{dia}  {hora}")
            if hasattr(v, lbl_plazas):
                hora_fin = str(reserva[4])[:5]                    
                getattr(v, lbl_plazas).setText(f"Fin: {hora_fin}")
            if hasattr(v, lbl_badge):
                getattr(v, lbl_badge).setText("Confirmada")

        if hasattr(v, "lblInfoReservas"):
            v.lblInfoReservas.setText(
                f"Tienes {len(reservas)} reserva(s) activa(s)")

    # Reservar clase
    def reservar_clase(self, numero_card: int):
        v = self.ventana
        try:
            lbl_nombre = self._SLOTS_CLASES[numero_card][0]
            nombre = getattr(v, lbl_nombre).text() \
                if hasattr(v, lbl_nombre) else ""

            if not nombre or nombre == "-":
                MensajeView.warning(
                    v, "Error", "No se ha podido obtener el nombre de la clase.")
                return

            clases = self.modelo.listar_clases()
            id_clase = None
            for c in clases:
                if str(c[1]).lower() == nombre.lower(): 
                    id_clase = c[0]                     
                    break

            if id_clase is None:
                MensajeView.warning(v, "Error", f"Clase '{nombre}' no encontrada.")
                return

            from PyQt5.QtWidgets import QMessageBox
            resp = QMessageBox.question(
                v, "Confirmar reserva",
                f"¿Deseas reservar la clase '{nombre}'?")
            if resp != QMessageBox.Yes:
                return

            self.modelo.inscribirse_clase(self.usuario["id_usuario"], id_clase)
            MensajeView.information(
                v, "Reserva confirmada", f"Te has inscrito en {nombre}.")
            self.cargar_datos()

        except Exception as e:
            MensajeView.warning(v, "Error al reservar", str(e))

    #Filtrar clases
    def filtrar_clases(self):
        v = self.ventana
        if not hasattr(v, "lblClase1"):
            return

        texto  = v.txtBuscarClases.text().strip() if hasattr(v, "txtBuscarClases") else ""
        tipo   = v.cmbTipo.currentText()           if hasattr(v, "cmbTipo")         else "Todos"
        horario = v.cmbHorario.currentText()       if hasattr(v, "cmbHorario")      else "Todos"

        try:
            if texto:
                clases = self.modelo.buscar_clases(texto)
            else:
                clases = self.modelo.listar_clases()
        except:
            clases = []

        if tipo and tipo != "Todos":
            clases = [c for c in clases
                      if tipo.lower() in str(c[1]).lower()]

        if horario and horario != "Todos":
            hora_ini = horario.split("-")[0].strip()
            clases = [c for c in clases
                      if str(c[3]).startswith(hora_ini)]

        for idx, (lbl_nombre, lbl_desc, lbl_fecha, lbl_plazas, btn) \
                in self._SLOTS_CLASES.items():
            clase = clases[idx - 1] if idx - 1 < len(clases) else None

            if hasattr(v, lbl_nombre):
                getattr(v, lbl_nombre).setText(str(clase[1]) if clase else "-")
            if hasattr(v, lbl_desc):
                nivel = str(clase[6]).capitalize() if clase else "-"
                getattr(v, lbl_desc).setText(f"Nivel: {nivel}")
            if hasattr(v, lbl_fecha):
                if clase:
                    getattr(v, lbl_fecha).setText(
                        f"{str(clase[2]).capitalize()}  {str(clase[3])[:5]}")
                else:
                    getattr(v, lbl_fecha).setText("-")
            if hasattr(v, lbl_plazas):
                getattr(v, lbl_plazas).setText(str(clase[5]) if clase else "-")
            if hasattr(v, btn):
                getattr(v, btn).setEnabled(clase is not None)

        if hasattr(v, "lblProxDatos"):
            v.lblProxDatos.setText(f"{len(clases)} clase(s) encontrada(s)")

    # Extra
    def _rellenar_con_cabeceras(self, tabla, datos, cabeceras):
        TablaView.configurar_columnas(tabla, cabeceras)
        tabla.setRowCount(len(datos))
        for fila_idx, fila in enumerate(datos):
            for col_idx, valor in enumerate(fila[:len(cabeceras)]):
                TablaView.poner_item(tabla, fila_idx, col_idx, valor)

    #Cerrar sesion
    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()