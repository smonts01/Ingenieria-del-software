"""
Controlador del rol Contable — Patrón MVC según ejemplo de la profesora.
"""
import os
import ctypes.wintypes
from datetime import datetime

from src.vista.componentes import MensajeView, BotonesView, ArchivoView
from src.modelo.VO.RegistroPagoVO import RegistroPagoVO
from src.vista.vistas.vista_contable import (
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

_VISTAS = {
    'interfaz_contable.ui':                             VistaContableInicio,
    'interfaz_contable_registrar_pago.ui':              VistaContableRegistrarPago,
    'interfaz_contable_pagos_pendientes.ui':            VistaContablePagosPendientes,
    'interfaz_contable_gestion_economica.ui':           VistaContableGestionEconomica,
    'interfaz_contable_informes.ui':                    VistaContableInformes,
    'interfaz_contable_perfil.ui':                      VistaContablePerfil,
    'interfaz_contable_info.ui':                        VistaContableInfo,
    'interfaz_contable_informes_gestion_economica.ui':  VistaContableInformeGestionEconomica,
    'interfaz_contable_informes_de_pagos.ui':           VistaContableInformeDePagos,
    'interfaz_contable_informes_pagos_pendientes.ui':   VistaContableInformePagosPendientes,
    'interfaz_contable_informes_balance_mensual.ui':    VistaContableInformeBalanceMensual,
}


class ControladorContable:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None
        self._tipo_informe_actual = 'informe'
        self.id_pago_seleccionado = None
        self.id_cliente_seleccionado = None

    def abrir(self):
        self.ir_inicio()

    def abrir_pantalla(self, archivo):
        if self.ventana:
            self.ventana.close()
        ruta = os.path.join(self.ruta_ui, archivo)
        ClaseVista = _VISTAS[archivo]
        self.ventana = ClaseVista(ruta)
        self.ventana.set_controlador(self)
        self._añadir_boton_ayuda()
        self.cargar_datos()
        self.ventana.show()

    # ── Navegación ────────────────────────────────────────────────────────
    def ir_inicio(self):              self.abrir_pantalla('interfaz_contable.ui')
    def ir_registrar_pago(self):      self.abrir_pantalla('interfaz_contable_registrar_pago.ui')
    def ir_pagos_pendientes(self):    self.abrir_pantalla('interfaz_contable_pagos_pendientes.ui')
    def ir_gestion_economica(self):   self.abrir_pantalla('interfaz_contable_gestion_economica.ui')
    def ir_informes(self):            self.abrir_pantalla('interfaz_contable_informes.ui')
    def ir_perfil(self):              self.abrir_pantalla('interfaz_contable_perfil.ui')
    def ir_informacion(self):         self.abrir_pantalla('interfaz_contable_info.ui')

    def generar_y_abrir_informe(self, tipo, archivo):
        self._tipo_informe_actual = tipo
        self.abrir_pantalla(archivo)

    # ── Carga de datos ────────────────────────────────────────────────────
    def cargar_datos(self):
        v = self.ventana
        if isinstance(v, VistaContableInicio):              self._cargar_inicio()
        elif isinstance(v, VistaContableRegistrarPago):     self._cargar_registrar_pago()
        elif isinstance(v, VistaContablePagosPendientes):   self._cargar_pagos_pendientes()
        elif isinstance(v, VistaContableGestionEconomica):  self._cargar_gestion_economica()
        elif isinstance(v, VistaContableInformes):          self._cargar_informes()
        elif isinstance(v, VistaContablePerfil):            self._cargar_perfil()
        elif isinstance(v, VistaContableInformeGestionEconomica):
            try: v.cargar_tabla(self.modelo.informe_gestion_economica_contable())
            except Exception as e: print('Error informe gestion eco:', e)
        elif isinstance(v, VistaContableInformeDePagos):
            try: v.cargar_tabla(self.modelo.informe_pagos_realizados())
            except Exception as e: print('Error informe pagos:', e)
        elif isinstance(v, VistaContableInformePagosPendientes):
            try: v.cargar_tabla(self.modelo.pagos_pendientes())
            except Exception as e: print('Error informe pendientes:', e)
        elif isinstance(v, VistaContableInformeBalanceMensual):
            try: v.cargar_tabla(self.modelo.informe_balance_mensual_contable())
            except Exception as e: print('Error informe balance:', e)

    def _cargar_inicio(self):
        v = self.ventana
        try: v.set_num_pagos_pendientes(str(self.modelo.num_pagos_pendientes_contable()))
        except: v.set_num_pagos_pendientes('0')
        try: v.set_ingresos_mes(f'{float(self.modelo.ingresos_mes_contable()):.2f} €')
        except: v.set_ingresos_mes('0.00 €')
        try: v.set_num_tarifas(str(self.modelo.num_tarifas_activas_contable()))
        except: v.set_num_tarifas('0')
        try: v.set_num_informes(str(self.modelo.num_informes_mes_contable()))
        except: pass
        try: v.cargar_tabla_ultimos_pagos(self.modelo.ultimos_pagos_inicio_contable())
        except Exception as e: print('Error tabla ultimos pagos:', e)
        try: v.cargar_tabla_pagos_pendientes(self.modelo.pagos_pendientes_inicio_contable())
        except Exception as e: print('Error tabla pagos pendientes inicio:', e)

    def _cargar_registrar_pago(self):
        v = self.ventana
        try: v.set_num_pendientes(str(self.modelo.num_pagos_pendientes_contable()))
        except: pass
        try: v.set_cobros_hoy(str(self.modelo.cobros_hoy_contable()))
        except: pass
        try: v.set_num_informes(str(self.modelo.num_informes_mes_contable()))
        except: pass
        try:
            pago = self.modelo.primer_pago_pendiente()
            if pago:
                self._mostrar_pago_en_vista(pago)
            else:
                v.set_sin_pago()
        except Exception as e: print('Error primer pago:', e)

    def _cargar_pagos_pendientes(self):
        """Carga la pantalla de pagos pendientes completa."""
        v = self.ventana
        try:
            v.set_resumen(
                self.modelo.contable_clientes_con_deuda(),
                self.modelo.contable_importe_pendiente(),
                self.modelo.contable_pagos_vencidos(),
                self.modelo.contable_pagos_vencen_semana(),
                self.modelo.num_pagos_pendientes_contable()
            )
        except Exception as e: print('Error resumen pagos pend:', e)
        self.cargar_pagos_pendientes_filtrados()

   

    def cargar_pagos_pendientes_filtrados(self, *args):
        v = self.ventana

        try:
            filtro = v.get_filtro()
            datos = self.modelo.pagos_pendientes()

            if filtro == 'vencido':
                datos_filtrados = []

                for fila in datos:
                    fecha_pago = fila.fecha if hasattr(fila, "fecha") else fila[4]

                    if self.modelo.es_pago_vencido(fecha_pago):
                        datos_filtrados.append(fila)

            else:
                datos_filtrados = datos

            v.cargar_tabla(datos_filtrados)

        except Exception as e:
            print('Error filtrar pagos pendientes:', e)




    def _cargar_gestion_economica(self):
        v = self.ventana
        try:
            tarifas = self.modelo.contable_tarifas_economica()
            for t in tarifas:
                v.set_tarifa(str(t[0]).lower(), str(t[1]), str(t[2]))
        except Exception as e: print('Error tarifas:', e)
        try: v.cargar_tabla_salarios(self.modelo.contable_salarios_personal())
        except Exception as e: print('Error salarios:', e)
        try: v.set_num_tarifas(str(self.modelo.num_tarifas_activas_contable()))
        except: pass
        try: v.set_nominas(f'{float(self.modelo.contable_total_nominas()):.2f} €')
        except: pass
        try: v.set_pagos_pendientes(f'{float(self.modelo.contable_importe_pendiente()):.2f} €')
        except: pass
        try:
            ingresos, gastos, balance = self.modelo.contable_balance_economico()
            v.set_balance(f'{float(ingresos):.2f} €',
                          f'{float(gastos):.2f} €',
                          f'{float(balance):.2f} €')
        except Exception as e: print('Error balance eco:', e)

    def _cargar_informes(self):
        v = self.ventana
        try: v.set_num_informes(str(self.modelo.num_informes_mes_contable()))
        except: pass
        try: v.set_ingresos_mes(f'{float(self.modelo.ingresos_mes_contable()):.2f} €')
        except: pass
        try: v.set_gastos_mes(f'{float(self.modelo.contable_gastos_mes()):.2f} €')
        except: pass
        try: v.set_balance_mes(f'{float(self.modelo.contable_balance_mes()):.2f} €')
        except: pass
        try: v.cargar_tabla_historial(self.modelo.historial_informes_contable())
        except Exception as e: print('Error historial informes:', e)

    def _cargar_perfil(self):
        v = self.ventana
        try:
            perfil = self.modelo.perfil_usuario(self.usuario['id_usuario'])
            if perfil:
                fecha_alta = f'Miembro desde: {perfil[8]}' if perfil[8] else 'Miembro desde: -'
                v.set_perfil(str(perfil[2]), str(perfil[6]).capitalize(),
                             str(perfil[4]), str(perfil[3]),
                             str(perfil[7]), fecha_alta)
            v.set_stats(
                self.modelo.contable_pagos_registrados(self.usuario['id_usuario']),
                self.modelo.contable_pendientes_revisados(),
                self.modelo.contable_informes_generados_usuario(self.usuario['id_usuario']),
                self.modelo.contable_importe_gestionado(self.usuario['id_usuario'])
            )
        except Exception as e: print('Error perfil:', e)

    # ── Acciones ──────────────────────────────────────────────────────────
    def buscar_cliente_registrar_pago(self):
        v = self.ventana
        dni = v.get_dni()
        if not dni:
            return
        try:
            pago = self.modelo.buscar_pago_pendiente_por_dni(dni)
            if pago:
                self._mostrar_pago_en_vista(pago)
            else:
                v.set_sin_pago(dni)
        except Exception as e:
            v.mostrar_error(str(e))

    def _mostrar_pago_en_vista(self, pago):
        id_pago, id_cliente, nombre, dni_real, id_tarifa, tarifa, importe, fecha_pago = pago[:8]
        self.id_pago_seleccionado = id_pago
        self.id_cliente_seleccionado = id_cliente
        self.ventana.set_cliente(nombre, dni_real, id_cliente, 'pendiente',
                                 tarifa, importe, fecha_pago)

    def registrar_pago(self):
        v = self.ventana
        try:
            dni = v.get_dni()
            if not dni:
                v.mostrar_error('Introduce el DNI del cliente.')
                return
            metodo_pago = v.get_metodo_pago()
            try:
                metodo_pago = self.modelo.normalizar_metodo_pago(metodo_pago)
            except ValueError as e:
                v.mostrar_error(str(e))
                return
            fecha_texto = v.get_fecha_texto()
            fecha_pago = (fecha_texto + ' 00:00:00') if fecha_texto else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            pago_vo = RegistroPagoVO(dni, self.usuario['id_usuario'], metodo_pago, fecha_pago)
            correcto, mensaje = self.modelo.registrar_pago_contable(
                pago_vo.dni_cliente, pago_vo.id_contable,
                pago_vo.metodo_pago, pago_vo.fecha_pago
            )
            if correcto:
                v.mostrar_exito(mensaje)
                v.limpiar_dni()
                v.set_estado_abonado()
                self.cargar_datos()
            else:
                v.mostrar_error(mensaje)
        except Exception as e:
            v.mostrar_error(str(e))

    def marcar_abonado(self):
        v = self.ventana
        try:
            id_pago = v.get_id_pago_seleccionado()
            if id_pago is None:
                v.mostrar_error('Selecciona un pago primero')
                return
            self.modelo.marcar_pago_abonado(id_pago)
            v.mostrar_exito('Pago marcado como abonado')
            self.cargar_datos()
        except Exception as e:
            v.mostrar_error(str(e))

    def generar_informe(self):
        v = self.ventana

        try:
            self.modelo.generar_informe(self.usuario['id_usuario'], 'general')
            v.mostrar_exito('Informe generado correctamente')

            if isinstance(v, VistaContableInformes):
                self._cargar_informes()
            else:
                self.cargar_datos()

        except Exception as e:
            v.mostrar_error(str(e))

    def exportar_pdf(self):
        v = self.ventana

        try:
            tipo = self._tipo_informe_actual

            cabeceras, filas = v.obtener_datos_tabla_informe()

            ruta = self.modelo.exportar_pdf_informe(
                self.usuario['id_usuario'],
                tipo,
                cabeceras,
                filas
            )

            self.cargar_datos()

            v.mostrar_exito(f'Guardado en:\n{ruta}')

        except Exception as e:
            v.mostrar_error(str(e))

    # ── Cerrar sesión ─────────────────────────────────────────────────────
    def cerrar_sesion(self):
        if self.ventana:
            self.ventana.close()
        self.vista_login.show()

    # ── Ayuda ─────────────────────────────────────────────────────────────
    def _añadir_boton_ayuda(self):
        BotonesView.crear_boton_ayuda(self.ventana, 1015, 30, self._mostrar_ayuda)

    def _mostrar_ayuda(self):
        v = self.ventana
        if isinstance(v, VistaContableInicio):
            MensajeView.information(v, 'Ayuda — Inicio',
                'Panel de control del contable.\n\n'
                '• Resumen económico: ingresos, pagos pendientes e informes.\n'
                '• Las tablas muestran últimos pagos y pendientes.')
        elif isinstance(v, VistaContableRegistrarPago):
            MensajeView.information(v, 'Ayuda — Registrar pago',
                'Registra el pago de un cliente.\n\n'
                '• Busca al cliente por DNI y pulsa Enter.\n'
                '• Selecciona el método de pago.\n'
                '• Pulsa Confirmar para registrar el pago.')
        elif isinstance(v, VistaContablePagosPendientes):
            MensajeView.information(v, 'Ayuda — Pagos pendientes',
                'Clientes con pagos pendientes.\n\n'
                '• Filtra por estado con el desplegable.\n')
        elif isinstance(v, VistaContableGestionEconomica):
            MensajeView.information(v, 'Ayuda — Gestión económica',
                'Situación económica del gimnasio.\n\n'
                '• Tarifas activas, nóminas y balance del mes.')
        elif isinstance(v, VistaContableInformes):
            MensajeView.information(v, 'Ayuda — Informes',
                'Generación de informes económicos.\n\n'
                '• Selecciona el tipo de informe y pulsa el botón.\n'
                '• Usa Exportar infome a PDF para guardar el informe.')
        elif isinstance(v, VistaContablePerfil):
            MensajeView.information(v, 'Ayuda — Mi perfil',
                'Información de tu cuenta de contable.')
        else:
            MensajeView.information(v, 'Ayuda',
                'Usa el menú lateral para navegar entre secciones.')