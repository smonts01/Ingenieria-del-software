
from .vista_login import VistaLogin

from .vista_admin_inicio import VistaAdminInicio
from .vista_admin_clases import VistaAdminClases
from .vista_admin_usuarios_clientes import VistaAdminUsuariosClientes
from .vista_admin_usuarios_trabajadores import VistaAdminUsuariosTrabajadores
from .vista_admin_nuevo_usuario import VistaAdminNuevoUsuario
from .vista_admin_inscripciones import VistaAdminInscripciones
from .vista_admin_pagos import VistaAdminPagos
from .vista_admin_estadisticas import VistaAdminEstadisticas

from .vista_cliente_inicio import VistaClienteInicio
from .vista_cliente_clases_todas import VistaClienteClasesTodas
from .vista_cliente_reservas import VistaClienteReservas
from .vista_cliente_estadisticas import VistaClienteEstadisticas
from .vista_cliente_perfil import VistaClientePerfil
from .vista_cliente_informacion import VistaClienteInformacion

from .vista_entrenador_inicio import VistaEntrenadorInicio
from .vista_entrenador_clases import VistaEntrenadorClases
from .vista_entrenador_registrar_asistencia import VistaEntrenadorRegistrarAsistencia
from .vista_entrenador_lista_clientes import VistaEntrenadorListaClientes
from .vista_entrenador_ocupacion import VistaEntrenadorOcupacion
from .vista_entrenador_perfil_info import VistaEntrenadorPerfil, VistaEntrenadorInformacion

from .vista_contable import (
    VistaContableInicio,
    VistaContableGestionEconomica,
    VistaContablePagosPendientes,
    VistaContableRegistrarPago,
)
from .vista_contable_informes import (
    VistaContableInformes,
    VistaContableInformeBalanceMensual,
    VistaContableInformeDePagos,
    VistaContableInformeGestionEconomica,
    VistaContableInformePagosPendientes,
)
from .vista_contable_perfil_info import VistaContablePerfil, VistaContableInfo

from .vista_recepcionista import (
    VistaRecepcionistaInicio,
    VistaRecepcionistaClientes,
    VistaRecepcionistaControlAcceso,
    VistaRecepcionistaRegistrarUsuario,
    VistaRecepcionistaPerfil,
)


"""
Paquete de vistas - StayFit Gimnasio (MVC)

Estructura por roles:
  LOGIN
    VistaLogin

  ADMINISTRADOR
    VistaAdminInicio
    VistaAdminClases
    VistaAdminUsuariosClientes
    VistaAdminUsuariosTrabajadores
    VistaAdminNuevoUsuario
  CLIENTE
    VistaClienteInicio
    VistaClienteClasesTodas
    VistaClienteReservas
    VistaClienteEstadisticas
    VistaClientePerfil
    VistaClienteInformacion

  ENTRENADOR
    VistaEntrenadorInicio
    VistaEntrenadorClases
    VistaEntrenadorRegistrarAsistencia
    VistaEntrenadorListaClientes
    VistaEntrenadorOcupacion
    VistaEntrenadorPerfil
    VistaEntrenadorInformacion

  CONTABLE
    VistaContableInicio
    VistaContableGestionEconomica
    VistaContablePagosPendientes
    VistaContableRegistrarPago
    VistaContableInformes
    VistaContableInformeBalanceMensual
    VistaContableInformeDePagos
    VistaContableInformeGestionEconomica
    VistaContableInformePagosPendientes
    VistaContablePerfil
    VistaContableInfo

  RECEPCIONISTA
    VistaRecepcionistaInicio
    VistaRecepcionistaClientes
    VistaRecepcionistaControlAcceso
    VistaRecepcionistaRegistrarUsuario
    VistaRecepcionistaPerfil
"""

__all__ = [
    "VistaLogin",
    # Admin
    "VistaAdminInicio", "VistaAdminClases", "VistaAdminUsuariosClientes",
    "VistaAdminUsuariosTrabajadores", "VistaAdminNuevoUsuario",
    "VistaAdminInscripciones", "VistaAdminPagos", "VistaAdminEstadisticas",
    # Cliente
    "VistaClienteInicio", "VistaClienteClasesTodas", "VistaClienteReservas",
    "VistaClienteEstadisticas", "VistaClientePerfil", "VistaClienteInformacion",
    # Entrenador
    "VistaEntrenadorInicio", "VistaEntrenadorClases",
    "VistaEntrenadorRegistrarAsistencia", "VistaEntrenadorListaClientes",
    "VistaEntrenadorOcupacion", "VistaEntrenadorPerfil", "VistaEntrenadorInformacion",
    # Contable
    "VistaContableInicio", "VistaContableGestionEconomica",
    "VistaContablePagosPendientes", "VistaContableRegistrarPago",
    "VistaContableInformes", "VistaContableInformeBalanceMensual",
    "VistaContableInformeDePagos", "VistaContableInformeGestionEconomica",
    "VistaContableInformePagosPendientes", "VistaContablePerfil", "VistaContableInfo",
    # Recepcionista
    "VistaRecepcionistaInicio", "VistaRecepcionistaClientes",
    "VistaRecepcionistaControlAcceso", "VistaRecepcionistaRegistrarUsuario",
    "VistaRecepcionistaPerfil",
]
