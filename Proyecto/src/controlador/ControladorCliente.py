import os
from PyQt5.QtWidgets import QMessageBox

from src.modelo.dao.ClienteDaoJDBC import ClienteDaoJDBC
from src.vista.logica_cliente import VentanaCliente


class ControladorCliente:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.vista = None
        
    # Abrir vista inicio

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

    # Conectar bonotes
    def conectar_botones(self):
        v = self.ventana
    
    # Menu lateral
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
        
        # Pantalla clases todas
        if hasattr(v, "lblTabRes"):
            v.lblTabRes.mousePressEvent = lambda e: self.abrir_pantalla("interfaz_cliente_clases_reservas.ui")
        if hasattr(v, "btnReservar1"):
            v.btnReservar1.clicked.connect(lambda: self.reservar_clase(1))
        if hasattr(v, "btnReservar2"):
            v.btnReservar2.clicked.connect(lambda: self.reservar_clase(2))
        if hasattr(v, "btnReservar3"):
            v.btnReservar3.clicked.connect(lambda: self.reservar_clase(3))
        if hasattr(v, "btnReservar4"):
            v.btnReservar4.clicked.connect(lambda: self.reservar_clase(4))
        if hasattr(v, "btnReservar5"):
            v.btnReservar5.clicked.connect(lambda: self.reservar_clase(5))
        if hasattr(v, "txtBuscarClases"):
            v.txtBuscar.textChanged.connect(self.filtrar_clases)
        if hasattr(v, "cmbTipo") and v.cmbTipo.count() == 0:
            v.cmbTipo.addItems(["Yoga", "Pilates", "Spinning", "Zumba", "Crossfit"])
        if hasattr(v, "cmbHorario") and v.cmbHorario.count() == 0:
            v.cmbHorario.addItems(["09:00-10:00", "10:00-11:00"])
        
        # Pantalla clases reservas
        if hasattr(v, "lblTabTodas"):
            v.lblTabTodas.mousePressEvent = lambda e: self.abrir_pantalla("interfaz_cliente_clases_todas.ui")
        
    # Cargar datos
    def cargar_datos(self):
        v = self.ventana
        
        # Pantalla inicio
        if hasattr(v, "lblNombreCliente"):
            pass
        if hasattr(v, "lblFechaAltaCliente"):
            pass
        if hasattr(v, "lblNumClases"):
            pass
        if hasattr(v, "lblCaloriasSemana"):
            pass
        if hasattr(v, "lblAsistencias"):
            pass
        if hasattr(v, "lblCantidadPago"):
            pass
        if hasattr(v, "lblPendientePago"):
            pass
        if hasattr(v, "lblMesPago"):
            pass
        if hasattr(v, "tablaProximasClases"):
            pass
        
        #Pantalla clases todas
        
        
        #Pantralla clases reservas
        if hasattr(v, "lblReservaClase1"):
            pass
        if hasattr(v, "lblReservaDesc1"):
            pass
        if hasattr(v, "lblReservaFecha1"):
            pass
        if hasattr(v, "lblPlazasReseva1"):
            pass
        
        if hasattr(v, "lblReservaClase2"):
            pass
        if hasattr(v, "lblReservaDesc2"):
            pass
        if hasattr(v, "lblReservaFecha2"):
            pass
        if hasattr(v, "lblPlazasReseva2"):
            pass
        
        if hasattr(v, "lblReservaClase3"):
            pass
        if hasattr(v, "lblReservaDesc3"):
            pass
        if hasattr(v, "lblReservaFecha3"):
            pass
        if hasattr(v, "lblPlazasReseva3"):
            pass
        
        if hasattr(v, "lblReservaClase4"):
            pass
        if hasattr(v, "lblReservaDesc4"):
            pass
        if hasattr(v, "lblReservaFecha4"):
            pass
        if hasattr(v, "lblPlazasReseva4"):
            pass
        
        if hasattr(v, "lblReservaClase5"):
            pass
        if hasattr(v, "lblReservaDesc5"):
            pass
        if hasattr(v, "lblReservaFecha5"):
            pass
        if hasattr(v, "lblPlazasReseva5"):
            pass
        
        #Pantalla estadisticas
        if hasattr(v, "lblNumEntrenos"):
            pass
        if hasattr(v, "lblNumTiempo"):
            pass
        if hasattr(v, "lblNumCalorias"):
            pass
        if hasattr(v, "lblNumObjetivo"):
            pass
        if hasattr(v, "lblNumEntrenos2"):
            pass
        
        if hasattr(v, "barLun"):
            pass
        if hasattr(v, "barMar"):
            pass
        if hasattr(v, "barMie"):
            pass
        if hasattr(v, "barJue"):
            pass
        if hasattr(v, "barVie"):
            pass
        if hasattr(v, "barSab"):
            pass
        if hasattr(v, "lblTotalCalorias"):
            pass
        
        #Pantalla perfil
        if hasattr(v, "lblNombrePerfil"):
            pass
        if hasattr(v, "lblEmailPerfil"):
            pass
        if hasattr(v, "lblPocentaje"):
            pass
        if hasattr(v, "lblAsistenciasValor"):
            pass
        if hasattr(v, "lblNombrePerfil"):
            pass
        
        if hasattr(v, "lblNombreCompleto"):
            pass
        if hasattr(v, "lblNumTelefono"):
            pass
        if hasattr(v, "lblCorreoElectronico"):
            pass
        if hasattr(v, "lblFechaNacimiento"):
            pass
        if hasattr(v, "lblGenero"):
            pass
        if hasattr(v, "lblDireccion"):
            pass
        if hasattr(v, "lblPeso"):
            pass
        if hasattr(v, "lblAltura"):
            pass
        
        
        #Pantalla informacion
        
        
        
        
        
    # Reservar clases 
        def reservar_clase(self, numero_card: int):
            v = self.ventana
            try:
                nombre = self.get_nombre_clase_card(numero_card)

                if not nombre:
                    QMessageBox.warning(v, "Error", "No se ha podido obtener el nombre de la clase")
                    return
                self.modelo.inscribirse_clase_por_nombre(
                    self.usuario["id_usuario"], nombre
                )
                QMessageBox.information(
                    v,
                    "Reserva confirmada",
                    f"Te has inscrito en {nombre}."
                )
                self.cargar_datos()
            except Exception as e:
                QMessageBox.warning(v, "Error al reservar", str(e))


    # Cerrar sesión
    def cerrar_sesion(self):
        self.ventana.close()
        self.vista_login.show()