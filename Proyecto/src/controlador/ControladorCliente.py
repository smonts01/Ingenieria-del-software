import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

from src.modelo.dao.ClienteDaoJDBC import ClienteDaoJDBC


# Índice de cada página en el QStackedWidget
PAGE_INICIO       = 0
PAGE_CLASES       = 1
PAGE_ESTADISTICAS = 2
PAGE_PERFIL       = 3
PAGE_INFORMACION  = 4

# Colores fijos para las leyendas de distribución (hasta 4 tipos)
_COLORES_LEYENDA = [
    "color:#1F2937;",   # oscuro (primero/mayor)
    "color:#FF9F2E;",   # naranja
    "color:#8E6CFF;",   # morado
    "color:#9CA3AF;",   # gris (resto)
]


class ControladorCliente:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo     = modelo
        self.usuario    = usuario       # dict con al menos 'id_usuario'
        self.ruta_ui    = ruta_ui
        self.vista_login = vista_login
        self.ventana    = None
        self._vo        = None          # ClienteInicioVO cargado al abrir

    # Apertura 

    def abrir(self):
        """
        Carga el VO desde el DAO, instancia la ventana única y la inicializa.
        """
        id_cliente = self.usuario["id_usuario"]

        dao = ClienteDaoJDBC()
        self._vo = dao.selectInicioCliente(id_cliente)

        if self._vo is None:
            QMessageBox.critical(
                None, "Error",
                f"No se pudieron cargar los datos del cliente (id={id_cliente})."
            )
            self.vista_login.show()
            return

        ruta = os.path.join(self.ruta_ui, "interfaz_cliente_unificada.ui")
        self.ventana = uic.loadUi(ruta)

        self._conectar_botones()
        self._inicializar_interfaz()
        self._cambiar_pagina(PAGE_INICIO)
        self.ventana.show()

    # Navegación 

    def _cambiar_pagina(self, indice: int):
        self.ventana.stackedWidget.setCurrentIndex(indice)
        self._actualizar_estilo_menu(indice)

    def _actualizar_estilo_menu(self, indice_activo: int):
        nav = [
            (self.ventana.btnInicio,       PAGE_INICIO),
            (self.ventana.btnClases,       PAGE_CLASES),
            (self.ventana.btnEstadisticas, PAGE_ESTADISTICAS),
            (self.ventana.btnPerfil,       PAGE_PERFIL),
            (self.ventana.btnInformacion,  PAGE_INFORMACION),
        ]
        for btn, idx in nav:
            btn.setProperty("activo", idx == indice_activo)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    # Conexión de botones 

    def _conectar_botones(self):
        v = self.ventana

        # Menú lateral
        v.btnInicio.clicked.connect(       lambda: self._cambiar_pagina(PAGE_INICIO))
        v.btnClases.clicked.connect(       lambda: self._cambiar_pagina(PAGE_CLASES))
        v.btnEstadisticas.clicked.connect( lambda: self._cambiar_pagina(PAGE_ESTADISTICAS))
        v.btnPerfil.clicked.connect(       lambda: self._cambiar_pagina(PAGE_PERFIL))
        v.btnInformacion.clicked.connect(  lambda: self._cambiar_pagina(PAGE_INFORMACION))
        v.btnCerrarSesion.clicked.connect( self._cerrar_sesion)

        # Página Clases — botones de reserva fijos (cards 1-4)
        for i in range(1, 5):
            btn = getattr(v, f"btnReservar{i}", None)
            if btn:
                btn.clicked.connect(
                    lambda checked, n=i: self._reservar_clase_card(n)
                )

        # Página Perfil
        v.btnGuardarCambios.clicked.connect(self._guardar_perfil)

    # Inicialización completa de la interfaz con el VO 
    def _inicializar_interfaz(self):
        vo = self._vo
        v  = self.ventana

        # Header 
        v.lblNombreCliente.setText(f"Hola, {vo.nombre}")
        v.lblFechaAltaCliente.setText(f"Cliente desde {vo.fecha_registro}")

        # Inicio título de bienvenida
        v.lblBienvenida.setText(f"Bienvenida, {vo.nombre}")

        # Inicio card1: Próximas clases (inscritas esta semana)
        v.lblNumClases.setText(str(vo.clases_semana))

        # Inicio — card2: Estado de pago 
        v.lblEstadoPago.setText(vo.estado_pagado.capitalize())

        # Inicio — card3: Calorías esta semana 
        v.lblCaloriasSemana.setText(f"{vo.calorias_semana:,} kcal".replace(",", "."))

        # Inicio — card4: Asistencias este mes 
        v.lblAsistencias.setText(vo.get_asistencias_str())

        # Inicio — cardPago: Último pago 
        v.lblCuota.setText(vo.nombre_tarifa)
        v.lblCantidadPago.setText(vo.get_precio_str())
        v.lblMesPago.setText(vo.ultimo_pago_fecha)
        v.lblPendientePago.setText(vo.ultimo_pago_estado.capitalize())

        # Inicio — tabla: Próximas clases inscritas 
        self._rellenar_tabla_proximas(vo.proximas_clases)

        # Estadísticas — cards 
        v.lblNumEntrenos.setText(str(vo.entrenos_semana))
        v.lblSubEntrenos.setText(vo.get_delta_entrenos_str())

        v.lblNumTiempo.setText(vo.get_tiempo_semana_str())
        v.lblSubTiempo.setText(vo.get_delta_tiempo_str())

        v.lblNumCalorias.setText(f"{vo.calorias_semana:,} kcal".replace(",", "."))

        # Objetivo semanal: porcentaje de entrenos realizados vs objetivo=5
        objetivo = 5
        pct = min(100, round(vo.entrenos_semana * 100 / objetivo)) if objetivo else 0
        v.lblNumObjetivo.setText(f"{pct}%")

        # Estadísticas — cardGrafico: texto resumen total
        v.btnMini.setText(f"Total semanal: {vo.calorias_semana:,} kcal".replace(",", "."))

        # Estadísticas — cardDistribucion: leyendas
        self._rellenar_leyendas_distribucion(vo.distribucion_tipos)

        # Estadísticas — cardRacha
        v.lblNumRacha.setText(str(vo.racha_dias))
        v.lblTextoRacha.setText(f"Llevas {vo.racha_dias} días consecutivos entrenando.")

        # Perfil — card izquierdo
        v.lblNombrePerfil.setText(vo.nombre)
        v.lblEmailPerfil.setText(vo.email)

        # Perfil — cardInfoPersonal: campos editables
        v.txtNombre.setText(vo.nombre)
        v.txtTelefono.setText(vo.telefono)
        v.txtEmail.setText(vo.email)
        v.txtFecha.setText(vo.fecha_nacimiento)
        v.txtDireccion.setText(vo.direccion)

        # Perfil — cardObjetivos: barra de progreso y asistencias
        self._actualizar_barra_progreso(vo.asistencias_mes, vo.inscripciones_mes)
        v.lblAsistenciasValor.setText(
            f"{vo.asistencias_mes} / {vo.inscripciones_mes} clases"
        )

    # Helpers de relleno

    def _rellenar_tabla_proximas(self, proximas: list):
        """Rellena tablaProximasClases con los datos del VO."""
        tabla = self.ventana.tablaProximasClases
        tabla.setRowCount(0)
        for fila in proximas:
            row = tabla.rowCount()
            tabla.insertRow(row)
            tabla.setItem(row, 0, QTableWidgetItem(fila["nombre_actividad"]))
            tabla.setItem(row, 1, QTableWidgetItem(fila["fecha"]))
            tabla.setItem(row, 2, QTableWidgetItem(fila["hora_inicio"]))
            tabla.setItem(row, 3, QTableWidgetItem(fila["nombre_sala"]))

    def _rellenar_leyendas_distribucion(self, distribucion: dict):
        """
        Actualiza los 4 QLabel de leyenda de la card de distribución.
        Si hay menos de 4 tipos, los labels sobrantes se vacían.
        """
        v      = self.ventana
        labels = [v.lblLeyenda1, v.lblLeyenda2, v.lblLeyenda3, v.lblLeyenda4]
        items  = list(distribucion.items())  # [(tipo, pct), ...]

        for i, lbl in enumerate(labels):
            if i < len(items):
                tipo, pct = items[i]
                lbl.setText(f"● {tipo:<12} {pct}%")
                lbl.setStyleSheet(_COLORES_LEYENDA[i] + ' font:8pt "Segoe UI";')
            else:
                lbl.setText("")

    def _actualizar_barra_progreso(self, asistencias: int, inscripciones: int):
        """
        Redimensiona barraProgresoValor proporcionalmente al ratio
        asistencias/inscripciones, sin salir del ancho de barraProgresoFondo.
        """
        v    = self.ventana
        base = v.barraProgresoFondo
        fill = v.barraProgresoValor

        ancho_max = base.width()
        if inscripciones > 0:
            ancho = min(ancho_max, round(asistencias * ancho_max / inscripciones))
        else:
            ancho = 0

        fill.setFixedWidth(max(0, ancho))
        pct = round(asistencias * 100 / inscripciones) if inscripciones else 0
        v.lblPorcentaje.setText(f"{pct}%")

    # Acciones de la página Clases

    def _reservar_clase_card(self, numero_card: int):
        """
        Intenta reservar la clase estática mostrada en la card N.
        Las cards son contenido de muestra del .ui; en una versión
        final se debería obtener el id_clase dinámicamente del modelo.
        """
        v = self.ventana
        lbl_clase = getattr(v, f"lblClase{numero_card}", None)
        nombre = lbl_clase.text() if lbl_clase else f"clase {numero_card}"
        try:
            # En el modelo real: self.modelo.inscribirse_clase(id_usuario, id_clase)
            # Aquí usamos el nombre como referencia orientativa:
            self.modelo.inscribirse_clase_por_nombre(
                self.usuario["id_usuario"], nombre
            )
            QMessageBox.information(v, "Reserva confirmada",
                                    f"Te has inscrito en {nombre}.")
            self._refrescar_datos()
        except Exception as e:
            QMessageBox.warning(v, "Error al reservar", str(e))

    # Acciones de la página Perfil 

    def _guardar_perfil(self):
        v = self.ventana
        try:
            telefono  = v.txtTelefono.text().strip()
            email     = v.txtEmail.text().strip()
            direccion = v.txtDireccion.text().strip()

            if not email:
                QMessageBox.warning(v, "Error", "El email no puede estar vacío.")
                return

            self.modelo.modificar_usuario(
                self.usuario["id_usuario"], telefono, email, direccion
            )
            QMessageBox.information(v, "Perfil actualizado",
                                    "Los cambios se han guardado correctamente.")

            # Refrescar el VO y la interfaz para que el header refleje cambios
            self._refrescar_datos()

        except Exception as e:
            QMessageBox.warning(v, "Error al guardar", str(e))

    # Refresco de datos

    def _refrescar_datos(self):
        """
        Recarga el VO desde el DAO y actualiza todos los widgets,
        manteniendo la página activa que el usuario estaba viendo.
        """
        dao = ClienteDaoJDBC()
        vo_nuevo = dao.selectInicioCliente(self.usuario["id_usuario"])
        if vo_nuevo:
            self._vo = vo_nuevo
            pagina_actual = self.ventana.stackedWidget.currentIndex()
            self._inicializar_interfaz()
            self._cambiar_pagina(pagina_actual)

    # Cerrar sesión

    def _cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()