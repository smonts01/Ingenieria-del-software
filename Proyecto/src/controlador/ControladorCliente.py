"""
Controlador del rol Cliente — Patrón MVC según ejemplo de la profesora.

Responsabilidad:
- Instanciar la Vista y asignarle set_controlador(self)
- Responder a los eventos que la Vista delega
- Llamar al Modelo para obtener/guardar datos
- Llamar a métodos de la Vista para actualizar la UI
- NO conecta botones, NO toca widgets directamente
"""
import os
from datetime import date, timedelta

from src.vista.componentes import MensajeView, BotonesView
from src.vista.vistas.vista_cliente import (
    VistaClienteInicio,
    VistaClienteClasesTodas,
    VistaClienteReservas,
    VistaClienteEstadisticas,
    VistaClientePerfil,
    VistaClienteInformacion,
)

_VISTAS = {
    'interfaz_cliente_inicio.ui':        VistaClienteInicio,
    'interfaz_cliente_clases_todas.ui':  VistaClienteClasesTodas,
    'interfaz_cliente_clases_reservas.ui': VistaClienteReservas,
    'interfaz_cliente_estadisticas.ui':  VistaClienteEstadisticas,
    'interfaz_cliente_perfil.ui':        VistaClientePerfil,
    'interfaz_cliente_informacion.ui':   VistaClienteInformacion,
}


class ControladorCliente:

    def __init__(self, modelo, usuario, ruta_ui, vista_login):
        self.modelo = modelo
        self.usuario = usuario
        self.ruta_ui = ruta_ui
        self.vista_login = vista_login
        self.ventana = None
        self._vo = None

    def abrir(self):
        self.ir_inicio()

    def abrir_pantalla(self, archivo):
        if self.ventana:
            self.ventana.close()
        ruta = os.path.join(self.ruta_ui, archivo)
        ClaseVista = _VISTAS[archivo]
        self._cargar_vo_cliente()
        self.ventana = ClaseVista(ruta)
        self.ventana.set_controlador(self)
        self._añadir_boton_ayuda()
        self.cargar_datos()
        self.ventana.show()

    # ── Navegación ────────────────────────────────────────────────────────
    def ir_inicio(self):       self.abrir_pantalla('interfaz_cliente_inicio.ui')
    def ir_clases(self):       self.abrir_pantalla('interfaz_cliente_clases_todas.ui')
    def ir_reservas(self):     self.abrir_pantalla('interfaz_cliente_clases_reservas.ui')
    def ir_estadisticas(self): self.abrir_pantalla('interfaz_cliente_estadisticas.ui')
    def ir_perfil(self):       self.abrir_pantalla('interfaz_cliente_perfil.ui')
    def ir_informacion(self):  self.abrir_pantalla('interfaz_cliente_informacion.ui')

    # ── VO ────────────────────────────────────────────────────────────────
    def _cargar_vo_cliente(self):
        try:
            self._vo = self.modelo.datos_inicio_cliente(self.usuario['id_usuario'])
        except Exception as e:
            print('ERROR AL CARGAR VO CLIENTE:', repr(e))
            self._vo = None

    # ── Carga de datos ────────────────────────────────────────────────────
    def cargar_datos(self):
        if self._vo is None:
            MensajeView.warning(self.ventana, 'Error', 'No se pudieron cargar los datos del cliente')
            return
        self._rellenar_cabecera()
        v = self.ventana
        if isinstance(v, VistaClienteInicio):       self._cargar_inicio()
        elif isinstance(v, VistaClienteClasesTodas):self._cargar_clases_todas()
        elif isinstance(v, VistaClienteReservas):   self._cargar_reservas()
        elif isinstance(v, VistaClienteEstadisticas):self._cargar_estadisticas()
        elif isinstance(v, VistaClientePerfil):     self._cargar_perfil()

    def _rellenar_cabecera(self):
        vo = self._vo
        v  = self.ventana
        v.set_nombre_cliente(str(vo.nombre))
        v.set_fecha_alta(f'Cliente desde {vo.fecha_registro}')

    def _cargar_inicio(self):
        v, vo = self.ventana, self._vo
        v.set_bienvenida(f'Bienvenida, {vo.nombre}')
        v.set_num_clases(str(len(vo.proximas_clases)))
        v.set_estado_pago(str(vo.estado_pagado).capitalize())
        v.set_sub_pago('Sin pagos pendientes' if str(vo.estado_pagado).lower() == 'abonado' else 'Tienes pagos pendientes')
        v.set_calorias_semana(f'{vo.calorias_semana} kcal')
        v.set_asistencias(vo.get_asistencias_str())
        v.set_cuota(str(vo.nombre_tarifa))
        v.set_cantidad_pago(vo.get_precio_str())
        v.set_mes_pago(str(vo.ultimo_pago_fecha))
        v.set_pendiente_pago(str(vo.ultimo_pago_estado).capitalize())
        v.cargar_tabla_proximas(vo.proximas_clases)

    def _cargar_clases_todas(self):
        v = self.ventana
        id_c = self.usuario['id_usuario']
        try:
            clases   = self.modelo.clases_ocupacion_cliente()
            inscritas = self.modelo.clases_inscritas_cliente(id_c)
            asistidas = self.modelo.clases_asistidas_cliente(id_c)
            ids_ins   = [ins.id_clase for ins in inscritas]

            # Poblar combos
            nombres  = sorted(set(str(c[1]).strip() for c in clases if c[1]))
            horarios = sorted(set(f"{str(c[3])[:5]} - {str(c[4])[:5]}" for c in clases if c[3] and c[4]))
            v.poblar_combo_tipo(nombres)
            v.poblar_combo_horario(horarios)

            # Periodo
            hoy    = date.today()
            lunes  = hoy - timedelta(days=hoy.weekday())
            domingo = lunes + timedelta(days=6)
            v.set_periodo(f"{lunes.day} - {domingo.day} {domingo.strftime('%B %Y').lower()}")

            # Cards
            v.cargar_cards(clases, ids_ins, asistidas)

            # Próxima clase
            proxima = next((c for c in clases if c[0] not in asistidas), None)
            if proxima:
                v.set_prox_datos(f"{proxima[1]}\n{proxima[2]} · {str(proxima[3])[:5]} - {str(proxima[4])[:5]}\n{proxima[5]}")
            else:
                v.set_prox_datos('No tienes próximas clases')
        except Exception as e:
            print('Error cargar clases todas:', e)

    def _cargar_reservas(self):
        v = self.ventana
        try:
            reservas = self._vo.proximas_clases
            clases_ocupacion = self.modelo.clases_ocupacion_cliente()
            # mapa nombre_lower -> (inscritos, aforo)
            ocup = {str(c[1]).lower(): (c[6], c[7]) for c in clases_ocupacion}
            v.cargar_cards(reservas, ocup)
        except Exception as e:
            print('Error cargar reservas:', e)

    def _cargar_estadisticas(self):
        v, vo = self.ventana, self._vo
        v.set_entrenos(str(vo.entrenos_semana), vo.get_delta_entrenos_str())
        v.set_tiempo(vo.get_tiempo_semana_str(), vo.get_delta_tiempo_str())
        v.set_calorias(f'{vo.calorias_semana} kcal')
        try:
            objetivo = self.modelo.calcular_objetivo_semanal(vo.calorias_semana)
            v.set_objetivo(objetivo['texto_porcentaje'], objetivo['texto_objetivo'])
        except Exception as e:
            print('Error objetivo:', e)
        v.set_mini(f'Total semanal: {vo.calorias_semana} kcal')
        try:
            calorias_dias = self.modelo.calorias_semana_por_dia(self.usuario['id_usuario'])
            v.actualizar_barras(calorias_dias)
            v.set_total_calorias(f'Total semanal: {sum(calorias_dias.values())} kcal')
        except Exception as e:
            print('Error barras:', e)
        v.set_dias_label('Lun          Mar          Mié          Jue          Vie          Sáb')
        v.set_racha(vo.racha_dias)
        v.set_leyendas_distribucion(vo.distribucion_tipos)

    def _cargar_perfil(self):
        v, vo = self.ventana, self._vo
        v.set_perfil(
            str(vo.nombre), str(vo.email),
            str(vo.telefono), str(vo.fecha_nacimiento),
            str(vo.direccion),
            f'{vo.asistencias_mes} / {vo.inscripciones_mes} clases'
        )
        try:
            objetivo = self.modelo.calcular_objetivo_semanal(vo.calorias_semana)
            v.set_objetivo(objetivo['texto_porcentaje'])
            v.set_barra_progreso(objetivo['porcentaje'])
        except Exception as e:
            print('Error objetivo perfil:', e)

    # ── Acciones ──────────────────────────────────────────────────────────
    def reservar_clase_card(self, numero_card):
        v = self.ventana
        nombre_clase = v.get_nombre_clase_card(numero_card)
        if not nombre_clase:
            MensajeView.warning(v, 'Error', 'No se ha encontrado la clase seleccionada')
            return
        accion = v.get_accion_boton_card(numero_card)
        try:
            if accion == 'cancelar':
                self.modelo.desapuntarse_clase_por_nombre(self.usuario['id_usuario'], nombre_clase)
                MensajeView.information(v, 'Reserva cancelada', f'Te has desapuntado de {nombre_clase}.')
            else:
                self.modelo.inscribirse_clase_por_nombre(self.usuario['id_usuario'], nombre_clase)
                MensajeView.information(v, 'Reserva confirmada', f'Te has inscrito en {nombre_clase}.')
            self._cargar_vo_cliente()
            self.cargar_datos()
        except Exception as e:
            MensajeView.warning(v, 'Error al gestionar la reserva', str(e))

    def filtrar_clases(self):
        v = self.ventana
        if not isinstance(v, VistaClienteClasesTodas):
            return
        v.aplicar_filtro_cards(
            v.get_texto_buscar(),
            v.get_filtro_tipo(),
            v.get_filtro_horario()
        )

    def guardar_perfil(self):
        v = self.ventana
        telefono  = v.get_telefono()
        email     = v.get_email()
        direccion = v.get_direccion()
        if not email:
            v.mostrar_error('El email no puede estar vacío')
            return
        try:
            self.modelo.modificar_usuario(self.usuario['id_usuario'], telefono, email, direccion)
            v.mostrar_exito('Los cambios se han guardado correctamente')
            self._cargar_vo_cliente()
            self.cargar_datos()
        except Exception as e:
            v.mostrar_error(str(e))

    # ── Cerrar sesión ─────────────────────────────────────────────────────
    def cerrar_sesion(self):
        if self.ventana:
            self.ventana.close()
        self.vista_login.show()

    # ── Ayuda ─────────────────────────────────────────────────────────────
    def _añadir_boton_ayuda(self):
        BotonesView.crear_boton_ayuda(self.ventana, 1015, 20, self._mostrar_ayuda)

    def _mostrar_ayuda(self):
        v = self.ventana
        if isinstance(v, VistaClienteInicio):
            MensajeView.information(v, 'Ayuda — Inicio',
                'Esta es tu pantalla de inicio.\n\n'
                '• Aquí ves un resumen de tus próximas clases.\n'
                '• Consulta el estado de tu último pago.\n'
                '• Las calorías muestran tu actividad semanal.')
        elif isinstance(v, VistaClienteClasesTodas):
            MensajeView.information(v, 'Ayuda — Clases disponibles',
                'Aquí puedes ver y reservar clases del gimnasio.\n\n'
                '• Usa el buscador para filtrar por nombre.\n'
                '• El desplegable Categoría filtra por tipo.\n'
                '• Pulsa Reservar para inscribirte.\n'
                '• Pulsa Cancelar si quieres darte de baja.')
        elif isinstance(v, VistaClienteReservas):
            MensajeView.information(v, 'Ayuda — Mis reservas',
                'Aquí aparecen las clases en las que estás inscrito.\n\n'
                '• Solo se muestran tus próximas reservas activas.\n'
                '• Para cancelar ve a Clases disponibles.')
        elif isinstance(v, VistaClienteEstadisticas):
            MensajeView.information(v, 'Ayuda — Estadísticas',
                'Resumen de tu actividad semanal.\n\n'
                '• El gráfico muestra calorías quemadas por día.\n'
                '• La racha indica días consecutivos entrenando.')
        elif isinstance(v, VistaClientePerfil):
            MensajeView.information(v, 'Ayuda — Mi perfil',
                'Visualiza tus datos personales.\n\n'
                '• Puedes modificar teléfono, email y dirección.\n'
                '• Pulsa Guardar cambios para confirmar.')
        else:
            MensajeView.information(v, 'Ayuda — Información',
                'Información general del gimnasio.\n\n'
                '• Usa el menú lateral para navegar.')