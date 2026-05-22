"""
Vista de información del gimnasio para el cliente (interfaz_cliente_informacion.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class VistaClienteInformacion(QMainWindow):
    """Vista con la información general del gimnasio."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_cliente_informacion.ui", self)

    # --- Cabecera ---
    def set_nombre_cliente(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaCliente.setText(fecha)

    # --- Sección "Sobre el gimnasio" ---
    def set_texto_sobre(self, texto: str):
        self.lblSobreTexto.setText(texto)

    # --- Horarios ---
    def set_horario(self, texto: str):
        self.lblHorarioTexto.setText(texto)

    # --- Contacto ---
    def set_telefono(self, telefono: str):
        self.lblTelefono.setText(telefono)

    def set_email(self, email: str):
        self.lblEmail.setText(email)

    def set_whatsapp(self, whatsapp: str):
        self.lblWhatsapp.setText(whatsapp)

    # --- Dirección ---
    def set_direccion(self, direccion: str):
        self.lblDireccion.setText(direccion)

    # --- Normas (hasta 5) ---
    def set_norma(self, idx: int, texto: str):
        """Actualiza una norma del gimnasio (idx 1-5)."""
        lbl = getattr(self, f"lblNorma{idx}", None)
        if lbl:
            lbl.setText(texto)

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.btnInicio.clicked.connect(ctrl.ir_inicio)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
        self.btnPerfil.clicked.connect(ctrl.ir_perfil)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
