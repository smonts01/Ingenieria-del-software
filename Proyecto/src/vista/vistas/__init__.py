"""
Paquete de vistas - StayFit Gimnasio (MVC)
"""

from .vista_login import VistaLogin

# Admin — todas en vista_admin.py
from .vista_admin import (
    VistaAdminInicio,
    VistaAdminUsuariosClientes,
    VistaAdminUsuariosTrabajadores,
    VistaAdminNuevoUsuario,
    VistaAdminClases,
    VistaAdminInscripciones,
    VistaAdminPagos,
    VistaAdminEstadisticas,
)

# Cliente
from .vista_cliente_inicio import VistaClienteInicio
from .vista_cliente_clases_todas import VistaClienteClasesTodas
from .vista_cliente_reservas import VistaClienteReservas
from .vista_cliente_estadisticas import VistaClienteEstadisticas
from .vista_cliente_perfil import VistaClientePerfil
from .vista_cliente_informacion import VistaClienteInformacion

# Entrenador
from .vista_entrenador_inicio import VistaEntrenadorInicio
from .vista_entrenador_clases import VistaEntrenadorClases
from .vista_entrenador_registrar_asistencia import VistaEntrenadorRegistrarAsistencia
from .vista_entrenador_lista_clientes import VistaEntrenadorListaClientes
from .vista_entrenador_ocupacion import VistaEntrenadorOcupacion
from .vista_entrenador_perfil_info import VistaEntrenadorPerfil, VistaEntrenadorInformacion

# Contable — todas en vista_contable.py
from .vista_contable import (
    VistaContableInicio,
    VistaContableRegistrarPago,
    VistaContablePagosPendientes,
    VistaContableGestionEconomica,
    VistaContableInformes,
    VistaContablePerfil,
    VistaContableInfo,
    VistaContableInformeGestionEconomica,
    VistaContableInformeDePagos,
    VistaContableInformePagosPendientes,
    VistaContableInformeBalanceMensual,
)

# Recepcionista — todas en vista_recepcionista.py
from .vista_recepcionista import (
    VistaRecepcionistaInicio,
    VistaRecepcionistaClientes,
    VistaRecepcionistaControlAcceso,
    VistaRecepcionistaRegistrarUsuario,
    VistaRecepcionistaPerfil,
)

__all__ = [
    'VistaLogin',
    # Admin
    'VistaAdminInicio', 'VistaAdminUsuariosClientes', 'VistaAdminUsuariosTrabajadores',
    'VistaAdminNuevoUsuario', 'VistaAdminClases', 'VistaAdminInscripciones',
    'VistaAdminPagos', 'VistaAdminEstadisticas',
    # Cliente
    'VistaClienteInicio', 'VistaClienteClasesTodas', 'VistaClienteReservas',
    'VistaClienteEstadisticas', 'VistaClientePerfil', 'VistaClienteInformacion',
    # Entrenador
    'VistaEntrenadorInicio', 'VistaEntrenadorClases',
    'VistaEntrenadorRegistrarAsistencia', 'VistaEntrenadorListaClientes',
    'VistaEntrenadorOcupacion', 'VistaEntrenadorPerfil', 'VistaEntrenadorInformacion',
    # Contable
    'VistaContableInicio', 'VistaContableRegistrarPago', 'VistaContablePagosPendientes',
    'VistaContableGestionEconomica', 'VistaContableInformes', 'VistaContablePerfil',
    'VistaContableInfo', 'VistaContableInformeGestionEconomica',
    'VistaContableInformeDePagos', 'VistaContableInformePagosPendientes',
    'VistaContableInformeBalanceMensual',
    # Recepcionista
    'VistaRecepcionistaInicio', 'VistaRecepcionistaClientes',
    'VistaRecepcionistaControlAcceso', 'VistaRecepcionistaRegistrarUsuario',
    'VistaRecepcionistaPerfil',
]