"""
Paquete de vistas - StayFit Gimnasio (MVC)
"""

from .vista_login import VistaLogin

# Admin
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
from .vista_cliente import (
    VistaClienteInicio,
    VistaClienteClasesTodas,
    VistaClienteReservas,
    VistaClienteEstadisticas,
    VistaClientePerfil,
    VistaClienteInformacion,
)

# Entrenador
from .vista_entrenador import (
    VistaEntrenadorInicio,
    VistaEntrenadorClases,
    VistaEntrenadorListaClientes,
    VistaEntrenadorOcupacion,
    VistaEntrenadorRegistrarAsistencia,
    VistaEntrenadorPerfil,
    VistaEntrenadorInformacion,
)

# Contable
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

# Recepcionista
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
    'VistaEntrenadorInicio', 'VistaEntrenadorClases', 'VistaEntrenadorListaClientes',
    'VistaEntrenadorOcupacion', 'VistaEntrenadorRegistrarAsistencia',
    'VistaEntrenadorPerfil', 'VistaEntrenadorInformacion',
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