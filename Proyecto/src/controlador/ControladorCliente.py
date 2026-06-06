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
        self._vo = self.modelo.datos_inicio_cliente(id_cliente)

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
        # Las cards de clases vienen diseñadas en el .ui.
        # El controlador solo mantiene el nombre del cliente en cabecera y conecta reservas.
        pass

    def _cargar_reservas(self):
        # Pantalla visual de reservas. Los datos dinámicos principales se cargan en Inicio.
        pass

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
        if hasattr(v, "btnMini"):
            v.btnMini.setText(f"Total semanal: {vo.calorias_semana} kcal")
        if hasattr(v, "lblNumRacha"):
            v.lblNumRacha.setText(str(vo.racha_dias))
        if hasattr(v, "lblTextoRacha"):
            v.lblTextoRacha.setText(f"Llevas {vo.racha_dias} días consecutivos entrenando.")

        self._rellenar_leyendas_distribucion(vo.distribucion_tipos)

    def _cargar_perfil(self):
        v = self.ventana
        vo = self._vo

        if hasattr(v, "lblNombrePerfil"):
            v.lblNombrePerfil.setText(str(vo.nombre))
        if hasattr(v, "lblEmailPerfil"):
            v.lblEmailPerfil.setText(str(vo.email))
        if hasattr(v, "txtNombre"):
            v.txtNombre.setText(str(vo.nombre))
        if hasattr(v, "txtTelefono"):
            v.txtTelefono.setText(str(vo.telefono))
        if hasattr(v, "txtEmail"):
            v.txtEmail.setText(str(vo.email))
        if hasattr(v, "txtFecha"):
            v.txtFecha.setText(str(vo.fecha_nacimiento))
        if hasattr(v, "txtDireccion"):
            v.txtDireccion.setText(str(vo.direccion))
        if hasattr(v, "lblAsistenciasValor"):
            v.lblAsistenciasValor.setText(f"{vo.asistencias_mes} / {vo.inscripciones_mes} clases")

    def reservar_clase_card(self, numero_card):
        v = self.ventana
        label = getattr(v, f"lblClase{numero_card}", None)
        if label is None:
            MensajeView.warning(v, "Error", "No se ha encontrado la clase seleccionada")
            return

        nombre_clase = label.text().strip()
        if not nombre_clase:
            MensajeView.warning(v, "Error", "No se ha seleccionado ninguna clase")
            return

        try:
            self.modelo.inscribirse_clase_por_nombre(self.usuario["id_usuario"], nombre_clase)
            MensajeView.information(v, "Reserva confirmada", f"Te has inscrito en {nombre_clase}.")
            self._cargar_vo_cliente()
            self.cargar_datos()
        except Exception as e:
            MensajeView.warning(v, "Error al reservar", str(e))

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

        if not hasattr(v, "txtBuscarClases"):
            return

        texto = v.txtBuscarClases.text().strip().lower()

        # Cambia este nombre si tu tabla se llama de otra forma
        if hasattr(v, "tablaClases"):
            tabla = v.tablaClases
        elif hasattr(v, "tablaTodasClases"):
            tabla = v.tablaTodasClases
        elif hasattr(v, "tablaClasesTodas"):
            tabla = v.tablaClasesTodas
        else:
            return

        for fila in range(tabla.rowCount()):
            coincide = False

            for col in range(tabla.columnCount()):
                item = tabla.item(fila, col)
                if item and texto in item.text().lower():
                    coincide = True
                    break

            tabla.setRowHidden(fila, not coincide)

    def cerrar_sesion(self):
        if self.ventana:
            self.ventana.close()
        self.vista_login.show()
